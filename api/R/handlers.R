# =============================================================================
# API Request Handlers
# =============================================================================

# --- Student handlers ---

#' Register a new student
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_register_student <- function(req, res, pool) {
  body <- req$body
  if (is.null(body$email) || is.null(body$password)) {
    return(bad_request(res, "email and password are required"))
  }

  # Hash password
  password_hash <- sodium::password_store(body$password)

  # Check for duplicate email
  existing <- fisherapp::lookup_student_by_email(pool, body$email)
  if (!is.null(existing)) {
    return(bad_request(res, "Email already registered"))
  }

  student <- fisherapp::create_student_in_db(
    con            = pool,
    email          = body$email,
    password_hash  = password_hash,
    display_name   = body$name,
    institution_id = body$institution_id,
    course_id      = body$course_id
  )

  list(
    student_id      = student$student_id,
    email           = body$email,
    name            = body$name,
    needs_placement = TRUE
  )
}

#' Login a student
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_login_student <- function(req, res, pool) {
  body <- req$body
  if (is.null(body$email) || is.null(body$password)) {
    return(bad_request(res, "email and password are required"))
  }

  row <- fisherapp::lookup_student_by_email(pool, body$email)
  if (is.null(row)) {
    res$status <- 401
    return(list(status = "error", message = "Invalid email or password"))
  }

  if (!sodium::password_verify(row$password_hash[1], body$password)) {
    res$status <- 401
    return(list(status = "error", message = "Invalid email or password"))
  }

  # Check placement status
  student <- fisherapp::load_student_model(pool, row$student_id[1])
  needs_placement <- is.null(student$placement_completed_at)

  list(
    student_id      = row$student_id[1],
    needs_placement = needs_placement
  )
}

#' Get student progress
#'
#' @param student_id Character UUID
#' @param res Plumber response
#' @param pool Database pool
handle_get_progress <- function(student_id, res, pool) {
  student <- fisherapp::load_student_model(pool, student_id)
  if (is.null(student)) {
    return(not_found(res, "Student not found"))
  }

  progress <- fisherapp::student_progress(student)
  list(
    student_id      = student_id,
    total_attempts  = student$total_attempts,
    total_correct   = student$total_correct,
    overall_accuracy = if (student$total_attempts > 0) {
      round(student$total_correct / student$total_attempts, 3)
    } else NA,
    topics = progress
  )
}

# --- Session handlers ---

#' Start a new session
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_start_session <- function(req, res, pool) {
  body <- req$body
  if (is.null(body$student_id)) {
    return(bad_request(res, "student_id is required"))
  }

  student <- fisherapp::load_student_model(pool, body$student_id)
  if (is.null(student)) {
    return(not_found(res, "Student not found"))
  }

  # End any existing active session first
  if (!is.null(student$current_session)) {
    student <- fisherapp::end_session(student)
    old_sess <- student$session_history[[length(student$session_history)]]
    fisherapp::save_session_end(pool, student, old_sess$session_id)
  }

  student <- fisherapp::start_session(student)
  fisherapp::save_session_start(pool, student)

  list(
    session_id = student$current_session$session_id,
    student_id = body$student_id,
    started_at = format(student$current_session$started_at,
                        "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
  )
}

#' End a session
#'
#' @param session_id Character UUID (from path)
#' @param res Plumber response
#' @param pool Database pool
handle_end_session <- function(session_id, res, pool) {
  # Find which student owns this session
  row <- DBI::dbGetQuery(pool,
    "SELECT student_id FROM sessions WHERE session_id = $1",
    params = list(session_id)
  )
  if (nrow(row) == 0) {
    return(not_found(res, "Session not found"))
  }

  student <- fisherapp::load_student_model(pool, row$student_id[1])
  if (is.null(student) || is.null(student$current_session) ||
      student$current_session$session_id != session_id) {
    return(bad_request(res, "Session is not active"))
  }

  student <- fisherapp::end_session(student)
  fisherapp::save_session_end(pool, student, session_id)
  fisherapp::save_student_model(pool, student)

  sess <- student$session_history[[length(student$session_history)]]
  list(
    session_id       = session_id,
    ended_at         = format(sess$ended_at, "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
    problems_served  = sess$problems_served,
    problems_correct = sess$problems_correct
  )
}

# --- Problem handlers ---

#' Get next problem
#'
#' @param student_id Character UUID (from query)
#' @param res Plumber response
#' @param pool Database pool
handle_get_next_problem <- function(student_id, res, pool, topics = NULL) {
  if (is.null(student_id) || student_id == "") {
    return(bad_request(res, "student_id query parameter is required"))
  }

  student <- fisherapp::load_student_model(pool, student_id)
  if (is.null(student)) {
    return(not_found(res, "Student not found"))
  }
  if (is.null(student$current_session)) {
    return(bad_request(res, "No active session. Start a session first."))
  }

  # Parse comma-separated topic filter
  allowed_topics <- NULL
  if (!is.null(topics) && nchar(topics) > 0) {
    allowed_topics <- trimws(strsplit(topics, ",")[[1]])
    allowed_topics <- allowed_topics[nchar(allowed_topics) > 0]
    if (length(allowed_topics) == 0) allowed_topics <- NULL
  }

  result <- fisherapp::get_next_problem(student, allowed_topics = allowed_topics)

  if (is.null(result$problem)) {
    return(list(
      problem      = NULL,
      intervention = result$intervention,
      session_id   = student$current_session$session_id
    ))
  }

  # Cache the problem server-side (client never sees answer)
  cache_problem(result$problem)

  # Save any student state changes from stuck-loop interventions
  fisherapp::save_student_model(pool, result$student)

  # Return problem without answer or solution steps
  list(
    problem_id   = result$problem$problem_id,
    topic_id     = result$problem$topic_id,
    difficulty   = result$problem$difficulty,
    statement    = result$problem$statement,
    session_id   = student$current_session$session_id,
    intervention = result$intervention
  )
}

#' Check answer (submit)
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_check_answer <- function(req, res, pool) {
  body <- req$body
  required <- c("student_id", "session_id", "problem_id", "answer")
  missing <- setdiff(required, names(body))
  if (length(missing) > 0) {
    return(bad_request(res, paste("Missing fields:", paste(missing, collapse = ", "))))
  }

  # Retrieve cached problem
  problem <- get_cached_problem(body$problem_id)
  if (is.null(problem)) {
    return(bad_request(res, "Problem not found or expired. Request a new problem."))
  }

  # Load student
  student <- fisherapp::load_student_model(pool, body$student_id)
  if (is.null(student)) {
    return(not_found(res, "Student not found"))
  }
  if (is.null(student$current_session) ||
      student$current_session$session_id != body$session_id) {
    return(bad_request(res, "Session mismatch or no active session"))
  }

  # Submit answer through the R package pipeline
  submit_result <- fisherapp::submit_answer(student, problem, body$answer)
  student <- submit_result$student

  # Persist all changes
  attempt_num <- student$current_session$problems_served
  fisherapp::save_attempt(
    pool, body$session_id, body$student_id,
    problem, body$answer, submit_result$result, attempt_num
  )
  fisherapp::save_student_model(pool, student)

  # Remove from cache (used)
  remove_cached_problem(body$problem_id)

  # Return full result (now including answer and solution)
  list(
    correct         = submit_result$result$correct,
    correct_answer  = submit_result$result$correct_answer,
    solution_steps  = submit_result$result$solution_steps,
    mastery_changed = submit_result$mastery_changed,
    new_mastery     = submit_result$new_mastery,
    topic_id        = problem$topic_id,
    difficulty      = problem$difficulty
  )
}

# --- Placement handlers ---

#' Start a placement test
#'
#' Initializes placement state machine. Returns first problem.
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_placement_start <- function(req, res, pool) {
  body <- req$body
  if (is.null(body$student_id)) {
    return(bad_request(res, "student_id is required"))
  }

  student <- fisherapp::load_student_model(pool, body$student_id)
  if (is.null(student)) {
    return(not_found(res, "Student not found"))
  }

  graph <- fisherapp::load_knowledge_graph()
  topo_order <- fisherapp::get_topic_order(graph)
  questions_per_topic <- 3L
  max_possible <- length(topo_order) * questions_per_topic
  max_questions <- min(as.integer(body$max_questions %||% 25L), max_possible)

  # Initialize placement state
  state <- list(
    student_id       = body$student_id,
    topo_order       = topo_order,
    current_topic_idx = 1L,
    topic_low        = 1L,
    topic_high       = 5L,
    topic_current    = 3L,
    topic_correct    = 0L,
    topic_asked      = 0L,
    total_asked      = 0L,
    max_questions    = max_questions,
    questions_per_topic = 3L,
    topic_placements = list(),
    attempt_log      = list(),
    completed        = FALSE
  )

  # Generate first problem
  result <- placement_generate_next(state, student)
  if (result$completed) {
    # All topics done immediately (unlikely but handle)
    remove_placement_state(body$student_id)
    return(finalize_placement(result$state, student, pool))
  }

  cache_placement_state(body$student_id, result$state)
  if (!is.null(result$problem)) {
    cache_problem(result$problem)
  }

  list(
    placement_active = TRUE,
    question_number  = result$state$total_asked + 1L,
    problem_id       = if (!is.null(result$problem)) result$problem$problem_id else NULL,
    topic_id         = if (!is.null(result$problem)) result$problem$topic_id else NULL,
    difficulty       = if (!is.null(result$problem)) result$problem$difficulty else NULL,
    statement        = if (!is.null(result$problem)) result$problem$statement else NULL,
    total_questions  = result$state$max_questions
  )
}

#' Submit a placement answer
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_placement_answer <- function(req, res, pool) {
  body <- req$body
  if (is.null(body$student_id) || is.null(body$problem_id) || is.null(body$answer)) {
    return(bad_request(res, "student_id, problem_id, and answer are required"))
  }

  state <- get_placement_state(body$student_id)
  if (is.null(state)) {
    return(bad_request(res, "No active placement test. Start one first."))
  }

  problem <- get_cached_problem(body$problem_id)
  if (is.null(problem)) {
    return(bad_request(res, "Problem not found or expired."))
  }

  # Check answer
  result <- fisherapp::check_answer(problem, body$answer)
  remove_cached_problem(body$problem_id)

  # Update state
  state$total_asked <- state$total_asked + 1L
  state$topic_asked <- state$topic_asked + 1L
  state$attempt_log[[state$total_asked]] <- list(
    question_num = state$total_asked,
    topic_id     = problem$topic_id,
    difficulty   = state$topic_current,
    correct      = result$correct
  )

  if (result$correct) {
    state$topic_correct <- state$topic_correct + 1L
    state$topic_low <- state$topic_current
    state$topic_current <- min(5L, state$topic_current + 1L)
  } else {
    state$topic_high <- state$topic_current
    state$topic_current <- max(1L, state$topic_current - 1L)
  }

  # Check if this topic is done
  topic_done <- (state$topic_high - state$topic_low <= 1L) ||
                (state$topic_asked >= state$questions_per_topic)

  if (topic_done) {
    # Record placement for this topic
    tid <- state$topo_order[state$current_topic_idx]
    accuracy <- if (state$topic_asked > 0) state$topic_correct / state$topic_asked else 0
    if (accuracy >= 0.85 && state$topic_low >= 4L) {
      tp_status <- "skip"
      start_diff <- 5L
    } else {
      tp_status <- "placed"
      start_diff <- max(1L, state$topic_low)
    }
    state$topic_placements[[tid]] <- list(
      status             = tp_status,
      start_difficulty   = start_diff,
      estimated_accuracy = accuracy,
      questions_asked    = state$topic_asked
    )

    # Move to next topic
    state$current_topic_idx <- state$current_topic_idx + 1L
    state$topic_low <- 1L
    state$topic_high <- 5L
    state$topic_current <- 3L
    state$topic_correct <- 0L
    state$topic_asked <- 0L
  }

  # Check if placement is complete
  if (state$current_topic_idx > length(state$topo_order) ||
      state$total_asked >= state$max_questions) {
    # Place any remaining topics (only if there are topics left)
    if (state$current_topic_idx <= length(state$topo_order)) {
      for (i in seq(state$current_topic_idx, length(state$topo_order))) {
        tid <- state$topo_order[i]
        if (is.null(state$topic_placements[[tid]])) {
          state$topic_placements[[tid]] <- list(
            status = "placed", start_difficulty = 1L,
            estimated_accuracy = 0, questions_asked = 0L
          )
        }
      }
    }

    student <- fisherapp::load_student_model(pool, body$student_id)
    remove_placement_state(body$student_id)
    return(finalize_placement(state, student, pool))
  }

  # Generate next problem
  student <- fisherapp::load_student_model(pool, body$student_id)
  next_result <- placement_generate_next(state, student)
  cache_placement_state(body$student_id, next_result$state)

  if (next_result$completed || is.null(next_result$problem)) {
    student <- fisherapp::load_student_model(pool, body$student_id)
    remove_placement_state(body$student_id)
    return(finalize_placement(next_result$state, student, pool))
  }

  cache_problem(next_result$problem)

  list(
    placement_active = TRUE,
    question_number  = next_result$state$total_asked + 1L,
    problem_id       = next_result$problem$problem_id,
    topic_id         = next_result$problem$topic_id,
    difficulty       = next_result$problem$difficulty,
    statement        = next_result$problem$statement,
    previous_correct = result$correct,
    total_questions  = state$max_questions
  )
}

#' Generate next placement problem
#' @keywords internal
placement_generate_next <- function(state, student) {
  while (state$current_topic_idx <= length(state$topo_order) &&
         state$total_asked < state$max_questions) {
    tid <- state$topo_order[state$current_topic_idx]
    problem <- tryCatch(
      fisherapp::generate_problem(tid, state$topic_current),
      error = function(e) NULL
    )
    if (!is.null(problem)) {
      return(list(state = state, problem = problem, completed = FALSE))
    }
    # Skip this difficulty/topic on generation failure
    state$current_topic_idx <- state$current_topic_idx + 1L
    state$topic_low <- 1L
    state$topic_high <- 5L
    state$topic_current <- 3L
    state$topic_correct <- 0L
    state$topic_asked <- 0L
  }
  list(state = state, problem = NULL, completed = TRUE)
}

#' Finalize placement and persist results
#' @keywords internal
finalize_placement <- function(state, student, pool) {
  # Apply placements to student model
  for (tid in names(state$topic_placements)) {
    tp <- state$topic_placements[[tid]]
    student$topics[[tid]]$difficulty <- tp$start_difficulty
    if (tp$status == "skip") {
      student$topics[[tid]]$mastery_state <- "mastered"
      student$topics[[tid]]$ease_factor <- 2.5
      student$topics[[tid]]$interval <- 7
      student$topics[[tid]]$repetition <- 3L
      student$topics[[tid]]$next_review <- Sys.time() + 7 * 86400
    } else if (tp$questions_asked > 0) {
      student$topics[[tid]]$mastery_state <- "in_progress"
    }
  }

  fisherapp::save_student_model(pool, student)
  fisherapp::mark_placement_completed(pool, student$student_id)

  list(
    placement_active = FALSE,
    completed        = TRUE,
    questions_asked  = state$total_asked,
    placements       = state$topic_placements
  )
}

#' Skip placement test (start at beginner level)
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_placement_skip <- function(req, res, pool) {
  body <- req$body
  if (is.null(body$student_id)) {
    return(bad_request(res, "student_id is required"))
  }

  student <- fisherapp::load_student_model(pool, body$student_id)
  if (is.null(student)) {
    return(not_found(res, "Student not found"))
  }

  fisherapp::mark_placement_completed(pool, body$student_id)

  list(
    student_id = body$student_id,
    skipped    = TRUE
  )
}

#' Reset placement for retake
#'
#' @param req Plumber request
#' @param res Plumber response
#' @param pool Database pool
handle_placement_reset <- function(req, res, pool) {
  body <- req$body
  if (is.null(body$student_id)) {
    return(bad_request(res, "student_id is required"))
  }

  student <- fisherapp::load_student_model(pool, body$student_id)
  if (is.null(student)) {
    return(not_found(res, "Student not found"))
  }

  fisherapp::reset_placement(pool, body$student_id)

  list(
    student_id      = body$student_id,
    needs_placement = TRUE
  )
}

# --- Topic handlers ---

#' List all topics
#'
#' @param res Plumber response
handle_list_topics <- function(res) {
  graph <- fisherapp::load_knowledge_graph()
  active <- fisherapp::get_active_topics(graph)
  topics <- lapply(active, function(tid) {
    topic <- fisherapp::get_topic(tid, graph)
    list(
      topic_id      = tid,
      title         = topic$title,
      prerequisites = topic$prerequisites,
      skills        = topic$skills
    )
  })
  topics
}

# Null-coalescing operator
`%||%` <- function(x, y) if (is.null(x)) y else x
