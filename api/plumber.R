# =============================================================================
# BerkeleyStats Tutor — Plumber API
# =============================================================================

library(plumber)
library(fisherapp)

# Source helper modules
source("api/R/db_connection.R")
source("api/R/middleware.R")
source("api/R/problem_cache.R")
source("api/R/handlers.R")

# Initialize database connection pool
db_pool <- create_db_pool()

# Clean problem cache periodically (every 100 requests)
request_counter <- 0L

#* @apiTitle BerkeleyStats Tutor API
#* @apiDescription RESTful API for the BerkeleyStats adaptive tutoring system

# --- Filters ---

#* Log requests
#* @filter logger
function(req, res) {
  log_filter(req, res)
}

#* CORS headers
#* @filter cors
function(req, res) {
  cors_filter(req, res)
}

#* Request counter and periodic cache cleanup
#* @filter counter
function(req, res) {
  request_counter <<- request_counter + 1L
  if (request_counter %% 100L == 0L) {
    clean_cache()
  }
  plumber::forward()
}

# --- Health ---

#* Health check
#* @get /health
#* @serializer unboxedJSON
function() {
  list(status = "ok", timestamp = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"))
}

# --- Students ---

#* Register a new student
#* @post /students
#* @serializer unboxedJSON
function(req, res) {
  tryCatch(
    handle_register_student(req, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

#* Login
#* @post /students/login
#* @serializer unboxedJSON
function(req, res) {
  tryCatch(
    handle_login_student(req, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

#* Get student progress
#* @get /students/<student_id>/progress
#* @param student_id:character Student UUID
#* @serializer unboxedJSON
function(student_id, res) {
  tryCatch(
    handle_get_progress(student_id, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

# --- Sessions ---

#* Start a new tutoring session
#* @post /sessions
#* @serializer unboxedJSON
function(req, res) {
  tryCatch(
    handle_start_session(req, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

#* End a session
#* @post /sessions/<session_id>/end
#* @param session_id:character Session UUID
#* @serializer unboxedJSON
function(session_id, res) {
  tryCatch(
    handle_end_session(session_id, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

# --- Problems ---

#* Get next problem for a student
#* @get /problems/next
#* @param student_id:character Student UUID
#* @serializer unboxedJSON
function(student_id, res) {
  tryCatch(
    handle_get_next_problem(student_id, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

#* Submit an answer
#* @post /problems/check
#* @serializer unboxedJSON
function(req, res) {
  tryCatch(
    handle_check_answer(req, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

# --- Placement ---

#* Start a placement test
#* @post /placement/start
#* @serializer unboxedJSON
function(req, res) {
  tryCatch(
    handle_placement_start(req, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

#* Submit a placement answer
#* @post /placement/answer
#* @serializer unboxedJSON
function(req, res) {
  tryCatch(
    handle_placement_answer(req, res, db_pool),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}

# --- Topics ---

#* List all available topics
#* @get /topics
#* @serializer unboxedJSON
function(res) {
  tryCatch(
    handle_list_topics(res),
    error = function(e) {
      res$status <- 500
      list(status = "error", message = conditionMessage(e))
    }
  )
}
