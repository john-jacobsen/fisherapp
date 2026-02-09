# =============================================================================
# Plumber Middleware — CORS, error handling, logging
# =============================================================================

#' Add CORS headers to all responses
#'
#' @param req Request object
#' @param res Response object
cors_filter <- function(req, res) {
  res$setHeader("Access-Control-Allow-Origin", "*")
  res$setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
  res$setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization")

  # Handle preflight

  if (req$REQUEST_METHOD == "OPTIONS") {
    res$status <- 200
    return(list())
  }

  plumber::forward()
}

#' Wrap handler responses in a consistent JSON envelope
#'
#' On success: {"status": "ok", "data": ...}
#' On error:   {"status": "error", "message": "..."}
#'
#' @param handler Function to wrap
#' @return Wrapped function
wrap_handler <- function(handler) {
  function(...) {
    tryCatch(
      {
        result <- handler(...)
        list(status = "ok", data = result)
      },
      error = function(e) {
        list(status = "error", message = conditionMessage(e))
      }
    )
  }
}

#' Log incoming requests
#'
#' @param req Request object
#' @param res Response object
log_filter <- function(req, res) {
  message(sprintf("[%s] %s %s",
    format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
    req$REQUEST_METHOD,
    req$PATH_INFO
  ))
  plumber::forward()
}

#' Set a 400 error response
#'
#' @param res Response object
#' @param message Error message
#' @return Error list
bad_request <- function(res, message) {
  res$status <- 400
  list(status = "error", message = message)
}

#' Set a 404 error response
#'
#' @param res Response object
#' @param message Error message
#' @return Error list
not_found <- function(res, message) {
  res$status <- 404
  list(status = "error", message = message)
}
