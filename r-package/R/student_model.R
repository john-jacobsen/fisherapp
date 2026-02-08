# =============================================================================
# Student Model — S3 classes for student state tracking
# =============================================================================

#' Create a new student model
#'
#' Initializes a student with all active topics set to "not_started" and
#' SM-2 defaults. The student model is an in-memory value object; every
#' function that modifies it returns an updated copy.
#'
#' @param student_id Character. Optional; auto-generated UUID if NULL.
#' @return A \code{student_model} S3 object
#' @export
create_student_model <- function(student_id = NULL) {
  if (is.null(student_id)) {
    student_id <- uuid::UUIDgenerate()
  }

  active <- get_active_topics()
  topics <- stats::setNames(
    lapply(active, init_topic_state),
    active
  )

  structure(
    list(
      student_id      = student_id,
      created_at      = Sys.time(),
      topics          = topics,
      current_session = NULL,
      session_history = list(),
      total_attempts  = 0L,
      total_correct   = 0L
    ),
    class = "student_model"
  )
}

#' Initialize topic state for one topic
#'
#' Sets SM-2 defaults: ease factor 2.5, interval 0, not_started mastery.
#'
#' @param topic_id Character topic ID
#' @return A topic_state list
#' @keywords internal
init_topic_state <- function(topic_id) {
  list(
    topic_id            = topic_id,
    mastery_state       = "not_started",
    difficulty          = 1L,
    ease_factor         = 2.5,
    interval            = 0,
    repetition          = 0L,
    next_review         = Sys.time(),
    last_n_results      = integer(0),
    session_count       = 0L,
    attempt_count       = 0L,
    correct_count       = 0L,
    consecutive_wrong   = 0L,
    last_difficulty_wrong = NA_integer_
  )
}

#' Get the topic state for a student on a specific topic
#'
#' @param student A \code{student_model} object
#' @param topic_id Character topic ID
#' @return A topic_state list
#' @export
get_topic_state <- function(student, topic_id) {
  ts <- student$topics[[topic_id]]
  if (is.null(ts)) {
    stop("Unknown topic: ", topic_id)
  }
  ts
}

#' Summarize student progress across all topics
#'
#' @param student A \code{student_model} object
#' @return A data.frame with one row per topic
#' @export
student_progress <- function(student) {
  rows <- lapply(names(student$topics), function(tid) {
    ts <- student$topics[[tid]]
    accuracy <- if (ts$attempt_count > 0) {
      round(ts$correct_count / ts$attempt_count, 3)
    } else {
      NA_real_
    }
    data.frame(
      topic_id      = tid,
      mastery       = ts$mastery_state,
      difficulty    = ts$difficulty,
      accuracy      = accuracy,
      attempts      = ts$attempt_count,
      sessions      = ts$session_count,
      ease_factor   = round(ts$ease_factor, 2),
      next_review   = as.character(ts$next_review),
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

#' Print method for student_model
#'
#' @param x A \code{student_model} object
#' @param ... Additional arguments (ignored)
#' @export
print.student_model <- function(x, ...) {
  cat("=== Student Model ===\n")
  cat("ID:", x$student_id, "\n")
  cat("Total attempts:", x$total_attempts,
      "| Correct:", x$total_correct, "\n")

  mastered <- sum(vapply(x$topics,
    function(ts) ts$mastery_state == "mastered", logical(1)))
  in_prog <- sum(vapply(x$topics,
    function(ts) ts$mastery_state == "in_progress", logical(1)))
  not_st <- sum(vapply(x$topics,
    function(ts) ts$mastery_state == "not_started", logical(1)))

  cat("Topics: ", mastered, " mastered, ", in_prog, " in progress, ",
      not_st, " not started\n", sep = "")

  if (!is.null(x$current_session)) {
    cat("Active session:", x$current_session$session_id, "\n")
  }
  cat("Sessions completed:", length(x$session_history), "\n")
  invisible(x)
}
