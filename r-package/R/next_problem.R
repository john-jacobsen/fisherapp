# =============================================================================
# Next Problem Selection — Orchestrates topic and difficulty choice
# =============================================================================

#' Select the next topic and difficulty for a student
#'
#' Priority order:
#' \enumerate{
#'   \item Mastered topics due for spaced review (most overdue first)
#'   \item In-progress topics (first in topological order, at adjusted difficulty)
#'   \item New topics whose prerequisites are all mastered (topological order, difficulty 1)
#' }
#'
#' @param student A \code{student_model} object
#' @param current_time POSIXct (default: now)
#' @param graph Optional knowledge graph
#' @return List with \code{topic_id} and \code{difficulty}, or NULL if nothing available
#' @export
select_next_topic <- function(student, current_time = Sys.time(), graph = NULL) {
  if (is.null(graph)) graph <- load_knowledge_graph()
  topo_order <- get_topic_order(graph)

  # Bucket 1: Mastered topics due for review
  due_reviews <- character(0)
  due_times <- numeric(0)
  for (tid in topo_order) {
    ts <- student$topics[[tid]]
    if (!is.null(ts) && ts$mastery_state == "mastered" &&
        is_due_for_review(ts, current_time)) {
      due_reviews <- c(due_reviews, tid)
      due_times <- c(due_times, as.numeric(ts$next_review))
    }
  }
  if (length(due_reviews) > 0) {
    # Pick the most overdue (earliest next_review)
    chosen <- due_reviews[which.min(due_times)]
    ts <- student$topics[[chosen]]
    return(list(topic_id = chosen, difficulty = ts$difficulty))
  }

  # Bucket 2: In-progress topics (topological order)
  for (tid in topo_order) {
    ts <- student$topics[[tid]]
    if (!is.null(ts) && ts$mastery_state == "in_progress") {
      new_diff <- adjust_difficulty(ts)
      return(list(topic_id = tid, difficulty = new_diff))
    }
  }

  # Bucket 3: New topics with prereqs met (topological order)
  for (tid in topo_order) {
    ts <- student$topics[[tid]]
    if (!is.null(ts) && ts$mastery_state == "not_started" &&
        prerequisites_met(student, tid, graph)) {
      return(list(topic_id = tid, difficulty = 1L))
    }
  }

  # Nothing available
  NULL
}

#' Generate the next problem for a student
#'
#' Calls \code{\link{select_next_topic}} then \code{\link{generate_problem}}.
#'
#' @param student A \code{student_model} object
#' @param current_time POSIXct (default: now)
#' @param graph Optional knowledge graph
#' @return A \code{fisherapp_problem} object, or NULL if no topics available
#' @export
next_problem_for_student <- function(student, current_time = Sys.time(),
                                     graph = NULL) {
  selection <- select_next_topic(student, current_time, graph)
  if (is.null(selection)) return(NULL)
  generate_problem(selection$topic_id, selection$difficulty)
}
