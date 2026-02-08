# =============================================================================
# Mastery Evaluation — Determines topic mastery state
# =============================================================================

#' Evaluate mastery state for a topic
#'
#' Mastery criteria:
#' \itemize{
#'   \item 85%+ accuracy in the last N results (N >= min_window)
#'   \item Across at least 2 distinct sessions
#'   \item Current working difficulty >= 3
#' }
#'
#' @param topic_state A topic_state list
#' @param accuracy_threshold Numeric, default 0.85
#' @param min_window Integer, minimum attempts in window, default 8
#' @param min_sessions Integer, minimum distinct sessions, default 2
#' @param min_difficulty Integer, minimum difficulty level, default 3
#' @return Character: "not_started", "in_progress", or "mastered"
#' @export
evaluate_mastery <- function(topic_state,
                             accuracy_threshold = 0.85,
                             min_window = 8L,
                             min_sessions = 2L,
                             min_difficulty = 3L) {
  # If no attempts, remain not_started
  if (topic_state$attempt_count == 0L) {
    return("not_started")
  }

  # If already mastered, stay mastered (mastery is sticky unless we add

  # an explicit "un-master" mechanism in the future)
  if (topic_state$mastery_state == "mastered") {
    return("mastered")
  }

  results <- topic_state$last_n_results

  # Need enough data
  if (length(results) < min_window) {
    return("in_progress")
  }

  # Check accuracy over the window
  accuracy <- mean(results)
  if (accuracy < accuracy_threshold) {
    return("in_progress")
  }

  # Need multiple sessions
  if (topic_state$session_count < min_sessions) {
    return("in_progress")
  }

  # Need to be working at difficulty 3+
  if (topic_state$difficulty < min_difficulty) {
    return("in_progress")
  }

  "mastered"
}

#' Check if all prerequisites for a topic are mastered
#'
#' @param student A \code{student_model} object
#' @param topic_id Character topic ID
#' @param graph Optional knowledge graph (avoids re-loading)
#' @return Logical
#' @export
prerequisites_met <- function(student, topic_id, graph = NULL) {
  prereqs <- get_prerequisites(topic_id, graph)
  if (length(prereqs) == 0) return(TRUE)

  all(vapply(prereqs, function(pid) {
    ts <- student$topics[[pid]]
    if (is.null(ts)) return(FALSE)
    ts$mastery_state == "mastered"
  }, logical(1)))
}
