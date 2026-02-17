# =============================================================================
# AI Integration — Encryption, API calls, and handlers
# =============================================================================

# --- Encryption helpers using openssl ---

#' Get or create the encryption key from environment
#'
#' Uses AI_ENCRYPTION_KEY env var (hex-encoded 32-byte key).
#' Falls back to a deterministic key derived from DB_PASSWORD for simplicity.
#' @return Raw 32-byte key
get_encryption_key <- function() {
  hex_key <- Sys.getenv("AI_ENCRYPTION_KEY", "")
  if (nchar(hex_key) >= 64) {
    return(openssl::hex_to_raw(substr(hex_key, 1, 64)))
  }
  # Fallback: derive from DB_PASSWORD using SHA-256
  db_pass <- Sys.getenv("DB_PASSWORD", "changeme_in_production")
  openssl::sha256(charToRaw(db_pass))
}

#' Encrypt an API key
#'
#' @param plaintext Character, the API key
#' @return Character, base64-encoded ciphertext (iv:ciphertext)
encrypt_api_key <- function(plaintext) {
  key <- get_encryption_key()
  iv <- openssl::rand_bytes(16)
  ciphertext <- openssl::aes_cbc_encrypt(charToRaw(plaintext), key, iv = iv)
  paste0(
    openssl::base64_encode(iv), ":",
    openssl::base64_encode(ciphertext)
  )
}

#' Decrypt an API key
#'
#' @param encrypted Character, base64-encoded "iv:ciphertext"
#' @return Character, the decrypted API key
decrypt_api_key <- function(encrypted) {
  parts <- strsplit(encrypted, ":", fixed = TRUE)[[1]]
  if (length(parts) != 2) stop("Invalid encrypted key format")
  iv <- openssl::base64_decode(parts[1])
  ciphertext <- openssl::base64_decode(parts[2])
  key <- get_encryption_key()
  rawToChar(openssl::aes_cbc_decrypt(ciphertext, key, iv = iv))
}

# --- AI API call functions ---

#' Call the Anthropic Claude API
#'
#' @param api_key Character
#' @param prompt Character
#' @param model Character, default "claude-sonnet-4-5-20250929"
#' @return Character, the response text
call_anthropic <- function(api_key, prompt, model = "claude-sonnet-4-5-20250929") {
  body <- jsonlite::toJSON(list(
    model = model,
    max_tokens = 1024L,
    messages = list(list(role = "user", content = prompt))
  ), auto_unbox = TRUE)

  response <- httr::POST(
    url = "https://api.anthropic.com/v1/messages",
    httr::add_headers(
      "x-api-key" = api_key,
      "anthropic-version" = "2023-06-01",
      "content-type" = "application/json"
    ),
    body = body,
    encode = "raw",
    httr::timeout(30)
  )

  if (httr::status_code(response) != 200) {
    msg <- tryCatch({
      parsed <- httr::content(response, as = "parsed", simplifyVector = TRUE)
      parsed$error$message %||% paste("API error:", httr::status_code(response))
    }, error = function(e) paste("API error:", httr::status_code(response)))
    stop(msg)
  }

  parsed <- httr::content(response, as = "parsed", simplifyVector = TRUE)
  parsed$content[[1]]$text
}

#' Call an OpenAI-compatible chat completions API
#'
#' @param api_key Character
#' @param prompt Character
#' @param model Character, default "gpt-4o-mini"
#' @param base_url Character, API base URL
#' @return Character, the response text
call_openai_compatible <- function(api_key, prompt, model = "gpt-4o-mini",
                                   base_url = "https://api.openai.com/v1") {
  body <- jsonlite::toJSON(list(
    model = model,
    max_tokens = 1024L,
    messages = list(list(role = "user", content = prompt))
  ), auto_unbox = TRUE)

  response <- httr::POST(
    url = paste0(base_url, "/chat/completions"),
    httr::add_headers(
      "Authorization" = paste("Bearer", api_key),
      "Content-Type" = "application/json"
    ),
    body = body,
    encode = "raw",
    httr::timeout(30)
  )

  if (httr::status_code(response) != 200) {
    msg <- tryCatch({
      parsed <- httr::content(response, as = "parsed", simplifyVector = TRUE)
      parsed$error$message %||% paste("API error:", httr::status_code(response))
    }, error = function(e) paste("API error:", httr::status_code(response)))
    stop(msg)
  }

  parsed <- httr::content(response, as = "parsed", simplifyVector = TRUE)
  parsed$choices[[1]]$message$content
}

#' Call the OpenAI API
#'
#' @param api_key Character
#' @param prompt Character
#' @param model Character, default "gpt-4o-mini"
#' @return Character, the response text
call_openai <- function(api_key, prompt, model = "gpt-4o-mini") {
  call_openai_compatible(api_key, prompt, model = model)
}

#' Call the Google Gemini API
#'
#' @param api_key Character
#' @param prompt Character
#' @param model Character, default "gemini-2.0-flash"
#' @return Character, the response text
call_gemini <- function(api_key, prompt, model = "gemini-2.0-flash") {
  body <- jsonlite::toJSON(list(
    contents = list(list(
      parts = list(list(text = prompt))
    ))
  ), auto_unbox = TRUE)

  url <- paste0(
    "https://generativelanguage.googleapis.com/v1beta/models/",
    model, ":generateContent?key=", api_key
  )

  response <- httr::POST(
    url = url,
    httr::add_headers("Content-Type" = "application/json"),
    body = body,
    encode = "raw",
    httr::timeout(30)
  )

  if (httr::status_code(response) != 200) {
    msg <- tryCatch({
      parsed <- httr::content(response, as = "parsed", simplifyVector = TRUE)
      parsed$error$message %||% paste("API error:", httr::status_code(response))
    }, error = function(e) paste("API error:", httr::status_code(response)))
    stop(msg)
  }

  parsed <- httr::content(response, as = "parsed", simplifyVector = TRUE)
  parsed$candidates[[1]]$content$parts[[1]]$text
}

#' Call the DeepSeek API (OpenAI-compatible)
#'
#' @param api_key Character
#' @param prompt Character
#' @param model Character, default "deepseek-chat"
#' @return Character, the response text
call_deepseek <- function(api_key, prompt, model = "deepseek-chat") {
  call_openai_compatible(api_key, prompt, model = model,
                         base_url = "https://api.deepseek.com/v1")
}

#' Test an AI provider connection with a lightweight request
#'
#' @param provider Character, "anthropic" or "openai"
#' @param api_key Character, the decrypted API key
#' @return TRUE if successful, stops with error otherwise
test_ai_connection <- function(provider, api_key) {
  if (provider == "anthropic") {
    call_anthropic(api_key, "Say 'ok'.", model = "claude-haiku-4-5-20251001")
  } else if (provider == "openai") {
    call_openai(api_key, "Say 'ok'.", model = "gpt-4o-mini")
  } else if (provider == "gemini") {
    call_gemini(api_key, "Say 'ok'.", model = "gemini-2.0-flash")
  } else if (provider == "deepseek") {
    call_deepseek(api_key, "Say 'ok'.", model = "deepseek-chat")
  } else {
    stop("Unsupported provider: ", provider)
  }
  TRUE
}

#' Build the AI explanation prompt
#'
#' @param topic_id Character
#' @param statement Character, the problem statement
#' @param student_answer Character
#' @param correct_answer Character
#' @return Character, the prompt
build_explain_prompt <- function(topic_id, statement, student_answer, correct_answer) {
  topic_label <- gsub("_", " ", topic_id)
  paste0(
    "You are a patient math tutor helping a statistics student with ", topic_label, ".\n\n",
    "The student was given this problem:\n", statement, "\n\n",
    "The student answered: ", student_answer, "\n",
    "The correct answer is: ", correct_answer, "\n\n",
    "Please provide a clear, step-by-step explanation of how to solve this problem correctly. ",
    "Format your response as numbered steps (Step 1:, Step 2:, etc.). ",
    "If the student's answer shows a common misconception, briefly explain what went wrong. ",
    "Use plain text for math notation (e.g., 3/4 instead of LaTeX). ",
    "Keep the explanation concise and focused."
  )
}

# --- HTTP Handlers ---

#' Save AI configuration
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_save_ai_config <- function(req, res, pool) {
  body <- req$body
  student_id <- req$args$student_id
  if (is.null(student_id)) student_id <- body$student_id

  if (is.null(student_id) || is.null(body$provider) || is.null(body$api_key)) {
    return(bad_request(res, "student_id, provider, and api_key are required"))
  }

  if (!(body$provider %in% c("anthropic", "openai", "gemini", "deepseek"))) {
    return(bad_request(res, "provider must be 'anthropic', 'openai', 'gemini', or 'deepseek'"))
  }

  encrypted <- encrypt_api_key(body$api_key)
  fisherapp::save_ai_config(pool, student_id, body$provider, encrypted)

  list(
    student_id = student_id,
    provider   = body$provider,
    configured = TRUE
  )
}

#' Get AI configuration (without the key)
#'
#' @param student_id Character UUID (from path)
#' @param res Plumber response
#' @param pool Database pool
handle_get_ai_config <- function(student_id, res, pool) {
  config <- fisherapp::get_ai_config(pool, student_id)

  if (is.null(config)) {
    return(list(
      student_id = student_id,
      provider   = NULL,
      configured = FALSE
    ))
  }

  # Mask the key — only show last 4 characters
  decrypted <- tryCatch(
    decrypt_api_key(config$encrypted_key),
    error = function(e) ""
  )
  masked <- if (nchar(decrypted) > 4) {
    paste0(strrep("*", nchar(decrypted) - 4), substr(decrypted, nchar(decrypted) - 3, nchar(decrypted)))
  } else {
    "****"
  }

  list(
    student_id = student_id,
    provider   = config$provider,
    configured = TRUE,
    key_hint   = masked
  )
}

#' Delete AI configuration
#'
#' @param student_id Character UUID (from path)
#' @param res Plumber response
#' @param pool Database pool
handle_delete_ai_config <- function(student_id, res, pool) {
  fisherapp::delete_ai_config(pool, student_id)
  list(student_id = student_id, configured = FALSE)
}

#' Test AI connection
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_test_ai_connection <- function(req, res, pool) {
  body <- req$body
  student_id <- req$args$student_id
  if (is.null(student_id)) student_id <- body$student_id

  if (is.null(student_id)) {
    return(bad_request(res, "student_id is required"))
  }

  config <- fisherapp::get_ai_config(pool, student_id)
  if (is.null(config)) {
    return(bad_request(res, "No AI configuration found. Save a key first."))
  }

  api_key <- tryCatch(
    decrypt_api_key(config$encrypted_key),
    error = function(e) {
      return(bad_request(res, "Failed to decrypt API key"))
    }
  )

  tryCatch({
    test_ai_connection(config$provider, api_key)
    list(student_id = student_id, provider = config$provider, success = TRUE)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = paste("Connection failed:", conditionMessage(e)))
  })
}

#' Get AI explanation for a problem
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_ai_explain <- function(req, res, pool) {
  body <- req$body
  required <- c("student_id", "topic_id", "statement", "student_answer", "correct_answer")
  missing <- setdiff(required, names(body))
  if (length(missing) > 0) {
    return(bad_request(res, paste("Missing fields:", paste(missing, collapse = ", "))))
  }

  config <- fisherapp::get_ai_config(pool, body$student_id)
  if (is.null(config)) {
    return(bad_request(res, "No AI configuration found. Add an API key in Settings."))
  }

  api_key <- tryCatch(
    decrypt_api_key(config$encrypted_key),
    error = function(e) NULL
  )
  if (is.null(api_key)) {
    return(bad_request(res, "Failed to decrypt API key"))
  }

  prompt <- build_explain_prompt(
    body$topic_id, body$statement,
    body$student_answer, body$correct_answer
  )

  tryCatch({
    response_text <- if (config$provider == "anthropic") {
      call_anthropic(api_key, prompt)
    } else if (config$provider == "gemini") {
      call_gemini(api_key, prompt)
    } else if (config$provider == "deepseek") {
      call_deepseek(api_key, prompt)
    } else {
      call_openai(api_key, prompt)
    }

    list(
      explanation = response_text,
      provider    = config$provider
    )
  }, error = function(e) {
    res$status <- 502
    list(status = "error", message = paste("AI provider error:", conditionMessage(e)))
  })
}
