# =============================================================================
# Database Adapter — Bridge between PostgreSQL and in-memory student_model
# =============================================================================

#' Create a new student in the database
#'
#' Inserts a student row, then initializes mastery_states for all active topics.
#'
#' @param con A DBI connection or pool object
#' @param email Character email address
#' @param password_hash Character hashed password
#' @param display_name Character display name (optional)
#' @param institution_id UUID string (optional)
#' @param course_id UUID string (optional)
#' @return A \code{student_model} object
#' @export
create_student_in_db <- function(con, email, password_hash,
                                 display_name = NULL,
                                 institution_id = NULL,
                                 course_id = NULL) {
  student <- create_student_model()

  DBI::dbWithTransaction(con, {
    DBI::dbExecute(con,
      "INSERT INTO students (student_id, email, password_hash, display_name,
                             institution_id, course_id, total_attempts, total_correct)
       VALUES ($1, $2, $3, $4, $5, $6, 0, 0)",
      params = list(
        student$student_id, email, password_hash,
        display_name, institution_id, course_id
      )
    )

    # Initialize mastery_states for all active topics
    active <- get_active_topics()
    for (tid in active) {
      DBI::dbExecute(con,
        "INSERT INTO mastery_states (student_id, topic_id)
         VALUES ($1, $2)",
        params = list(student$student_id, tid)
      )
    }
  })

  student
}

#' Load a student model from the database
#'
#' Reconstructs a full \code{student_model} S3 object from PostgreSQL rows.
#'
#' @param con A DBI connection or pool object
#' @param student_id Character UUID
#' @return A \code{student_model} object, or NULL if not found
#' @export
load_student_model <- function(con, student_id) {
  # 1. Load student row
  student_row <- DBI::dbGetQuery(con,
    "SELECT student_id, total_attempts, total_correct, created_at
     FROM students WHERE student_id = $1",
    params = list(student_id)
  )
  if (nrow(student_row) == 0) return(NULL)

  # 2. Load mastery states
  mastery_rows <- DBI::dbGetQuery(con,
    "SELECT topic_id, mastery_state, difficulty, attempt_count, correct_count,
            session_count, consecutive_wrong, last_n_results,
            ease_factor, sm2_interval, repetition, next_review
     FROM mastery_states WHERE student_id = $1",
    params = list(student_id)
  )

  # 3. Build topics list
  active <- get_active_topics()
  topics <- stats::setNames(
    lapply(active, function(tid) {
      row_idx <- which(mastery_rows$topic_id == tid)
      if (length(row_idx) == 1) {
        row <- mastery_rows[row_idx, ]
        # Parse last_n_results from PostgreSQL array
        lnr <- parse_pg_int_array(row$last_n_results)
        list(
          topic_id            = tid,
          mastery_state       = row$mastery_state,
          difficulty          = as.integer(row$difficulty),
          ease_factor         = as.numeric(row$ease_factor),
          interval            = as.numeric(row$sm2_interval),
          repetition          = as.integer(row$repetition),
          next_review         = as.POSIXct(row$next_review, tz = "UTC"),
          last_n_results      = lnr,
          session_count       = as.integer(row$session_count),
          attempt_count       = as.integer(row$attempt_count),
          correct_count       = as.integer(row$correct_count),
          consecutive_wrong   = as.integer(row$consecutive_wrong),
          last_difficulty_wrong = NA_integer_
        )
      } else {
        init_topic_state(tid)
      }
    }),
    active
  )

  # 4. Check for active session
  session_row <- DBI::dbGetQuery(con,
    "SELECT session_id, started_at, is_placement, problems_served, problems_correct
     FROM sessions
     WHERE student_id = $1 AND ended_at IS NULL
     ORDER BY started_at DESC LIMIT 1",
    params = list(student_id)
  )

  current_session <- NULL
  if (nrow(session_row) == 1) {
    # Load topics attempted from problem_attempts for this session
    attempted <- DBI::dbGetQuery(con,
      "SELECT DISTINCT topic_id FROM problem_attempts WHERE session_id = $1",
      params = list(session_row$session_id[1])
    )
    current_session <- structure(
      list(
        session_id       = session_row$session_id[1],
        student_id       = student_id,
        started_at       = as.POSIXct(session_row$started_at[1], tz = "UTC"),
        ended_at         = NULL,
        topics_attempted = attempted$topic_id,
        attempts         = list(),
        problems_served  = as.integer(session_row$problems_served[1]),
        problems_correct = as.integer(session_row$problems_correct[1]),
        is_placement     = as.logical(session_row$is_placement[1])
      ),
      class = "tutor_session"
    )
  }

  structure(
    list(
      student_id      = student_id,
      created_at      = as.POSIXct(student_row$created_at[1], tz = "UTC"),
      topics          = topics,
      current_session = current_session,
      session_history = list(),
      total_attempts  = as.integer(student_row$total_attempts[1]),
      total_correct   = as.integer(student_row$total_correct[1])
    ),
    class = "student_model"
  )
}

#' Save a student model back to the database
#'
#' Updates the students table and upserts all mastery_states.
#' Should be called after any state-changing operation (submit_answer, etc.).
#'
#' @param con A DBI connection or pool object
#' @param student A \code{student_model} object
#' @export
save_student_model <- function(con, student) {
  DBI::dbWithTransaction(con, {
    # 1. Update student totals
    DBI::dbExecute(con,
      "UPDATE students SET total_attempts = $1, total_correct = $2
       WHERE student_id = $3",
      params = list(student$total_attempts, student$total_correct,
                    student$student_id)
    )

    # 2. Upsert mastery states for each topic
    for (tid in names(student$topics)) {
      ts <- student$topics[[tid]]
      next_rev <- if (inherits(ts$next_review, "POSIXt")) {
        format(ts$next_review, "%Y-%m-%d %H:%M:%S", tz = "UTC")
      } else {
        NULL
      }
      lnr_pg <- format_pg_int_array(ts$last_n_results)

      DBI::dbExecute(con,
        "INSERT INTO mastery_states
           (student_id, topic_id, mastery_state, difficulty,
            attempt_count, correct_count, session_count, consecutive_wrong,
            last_n_results, ease_factor, sm2_interval, repetition,
            next_review, updated_at)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, now())
         ON CONFLICT (student_id, topic_id)
         DO UPDATE SET
           mastery_state = EXCLUDED.mastery_state,
           difficulty = EXCLUDED.difficulty,
           attempt_count = EXCLUDED.attempt_count,
           correct_count = EXCLUDED.correct_count,
           session_count = EXCLUDED.session_count,
           consecutive_wrong = EXCLUDED.consecutive_wrong,
           last_n_results = EXCLUDED.last_n_results,
           ease_factor = EXCLUDED.ease_factor,
           sm2_interval = EXCLUDED.sm2_interval,
           repetition = EXCLUDED.repetition,
           next_review = EXCLUDED.next_review,
           updated_at = now()",
        params = list(
          student$student_id, tid, ts$mastery_state, ts$difficulty,
          ts$attempt_count, ts$correct_count, ts$session_count,
          ts$consecutive_wrong, lnr_pg, ts$ease_factor,
          ts$interval, ts$repetition, next_rev
        )
      )
    }

    # 3. Update session if active
    if (!is.null(student$current_session)) {
      sess <- student$current_session
      DBI::dbExecute(con,
        "UPDATE sessions SET problems_served = $1, problems_correct = $2
         WHERE session_id = $3",
        params = list(sess$problems_served, sess$problems_correct,
                      sess$session_id)
      )
    }
  })

  invisible(student)
}

#' Save a session start to the database
#'
#' @param con A DBI connection or pool object
#' @param student A \code{student_model} with an active session
#' @export
save_session_start <- function(con, student) {
  sess <- student$current_session
  if (is.null(sess)) stop("No active session to save.")

  DBI::dbExecute(con,
    "INSERT INTO sessions (session_id, student_id, started_at, is_placement,
                           problems_served, problems_correct)
     VALUES ($1, $2, $3, $4, 0, 0)",
    params = list(
      sess$session_id, student$student_id,
      format(sess$started_at, "%Y-%m-%d %H:%M:%S", tz = "UTC"),
      sess$is_placement
    )
  )
  invisible(student)
}

#' Save a session end to the database
#'
#' @param con A DBI connection or pool object
#' @param student A \code{student_model} (session just ended, in session_history)
#' @param session_id Character UUID of the session to close
#' @export
save_session_end <- function(con, student, session_id) {
  # Find the session in history
  sess <- NULL
  for (s in student$session_history) {
    if (identical(s$session_id, session_id)) {
      sess <- s
      break
    }
  }
  if (is.null(sess)) stop("Session not found in history: ", session_id)

  DBI::dbExecute(con,
    "UPDATE sessions SET ended_at = $1, problems_served = $2, problems_correct = $3
     WHERE session_id = $4",
    params = list(
      format(sess$ended_at, "%Y-%m-%d %H:%M:%S", tz = "UTC"),
      sess$problems_served, sess$problems_correct,
      session_id
    )
  )
  invisible(student)
}

#' Save a problem attempt to the database
#'
#' @param con A DBI connection or pool object
#' @param session_id Character UUID
#' @param student_id Character UUID
#' @param problem A \code{fisherapp_problem} object
#' @param answer Character student's answer
#' @param result List from \code{check_answer()} with \code{correct}, etc.
#' @param attempt_number Integer, the attempt number within the session
#' @export
save_attempt <- function(con, session_id, student_id, problem,
                         answer, result, attempt_number) {
  DBI::dbExecute(con,
    "INSERT INTO problem_attempts
       (session_id, student_id, problem_id, topic_id, difficulty,
        student_answer, correct_answer, is_correct, attempt_number)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)",
    params = list(
      session_id, student_id, problem$problem_id,
      problem$topic_id, problem$difficulty,
      answer, problem$answer, result$correct,
      attempt_number
    )
  )
  invisible(NULL)
}

#' Look up a student by email
#'
#' @param con A DBI connection or pool object
#' @param email Character email address
#' @return A one-row data.frame with student_id and password_hash, or NULL
#' @export
lookup_student_by_email <- function(con, email) {
  row <- DBI::dbGetQuery(con,
    "SELECT student_id, password_hash FROM students WHERE email = $1",
    params = list(email)
  )
  if (nrow(row) == 0) return(NULL)
  row
}

# =============================================================================
# Internal helpers for PostgreSQL array formatting
# =============================================================================

#' Parse a PostgreSQL integer array string into an R integer vector
#' @param x Character, e.g. "{1,0,1,1}" or NULL
#' @return Integer vector
#' @keywords internal
parse_pg_int_array <- function(x) {
  if (is.null(x) || is.na(x) || x == "{}" || x == "") {
    return(integer(0))
  }
  # Handle both character "{1,0,1}" and already-parsed formats
  if (is.character(x)) {
    cleaned <- gsub("[{}]", "", x)
    if (nchar(cleaned) == 0) return(integer(0))
    as.integer(strsplit(cleaned, ",")[[1]])
  } else if (is.list(x)) {
    as.integer(unlist(x))
  } else {
    as.integer(x)
  }
}

#' Format an R integer vector as a PostgreSQL array literal
#' @param x Integer vector
#' @return Character, e.g. "{1,0,1,1}"
#' @keywords internal
format_pg_int_array <- function(x) {
  if (length(x) == 0) return("{}")
  paste0("{", paste(as.integer(x), collapse = ","), "}")
}
