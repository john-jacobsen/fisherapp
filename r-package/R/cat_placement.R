# =============================================================================
# Computer-Adaptive Placement Test (CAT)
# =============================================================================

#' Run a Computer-Adaptive Placement Test
#'
#' Walks the knowledge graph in topological order, testing each topic with
#' adaptive difficulty. Starts at difficulty 3 per topic, moves up on correct,
#' down on incorrect. Updates the student model with placement results.
#'
#' @param student A \code{student_model} object
#' @param answer_fn Function that takes a \code{fisherapp_problem} and returns
#'   a character answer string. For simulation: use \code{function(p) p$answer}
#'   (always correct) or a custom function. For interactive: see
#'   \code{\link{interactive_placement}}.
#' @param max_questions Integer, cap on total questions (default 25)
#' @param questions_per_topic Integer, max questions per topic (default 3)
#' @param graph Optional knowledge graph
#' @return List with \code{student} (updated) and \code{cat_result}
#' @export
run_placement_test <- function(student, answer_fn,
                               max_questions = 25L,
                               questions_per_topic = 3L,
                               graph = NULL) {
  if (is.null(graph)) graph <- load_knowledge_graph()
  topo_order <- get_topic_order(graph)
  total_asked <- 0L
  attempt_log <- list()
  topic_placements <- list()

  for (topic_id in topo_order) {
    if (total_asked >= max_questions) break

    low <- 1L
    high <- 5L
    current <- 3L
    topic_correct <- 0L
    topic_asked <- 0L

    for (q in seq_len(questions_per_topic)) {
      if (total_asked >= max_questions) break

      problem <- tryCatch(
        generate_problem(topic_id, current),
        error = function(e) NULL
      )
      if (is.null(problem)) next

      response <- answer_fn(problem)
      result <- check_answer(problem, response)

      total_asked <- total_asked + 1L
      topic_asked <- topic_asked + 1L

      attempt_log[[total_asked]] <- list(
        question_num = total_asked,
        topic_id     = topic_id,
        difficulty   = current,
        correct      = result$correct
      )

      if (result$correct) {
        topic_correct <- topic_correct + 1L
        low <- current
        current <- min(5L, current + 1L)
      } else {
        high <- current
        current <- max(1L, current - 1L)
      }

      # Early stop if bounds converge
      if (high - low <= 1L) break
    }

    # Determine placement
    accuracy <- if (topic_asked > 0) topic_correct / topic_asked else 0
    if (accuracy >= 0.85 && low >= 4L) {
      status <- "skip"
      start_difficulty <- 5L
    } else {
      status <- "placed"
      start_difficulty <- max(1L, low)
    }

    topic_placements[[topic_id]] <- list(
      status             = status,
      start_difficulty   = start_difficulty,
      estimated_accuracy = accuracy,
      questions_asked    = topic_asked
    )

    # Apply to student model
    student$topics[[topic_id]]$difficulty <- start_difficulty
    if (status == "skip") {
      student$topics[[topic_id]]$mastery_state <- "mastered"
      # Set SM-2 to a healthy state
      student$topics[[topic_id]]$ease_factor <- 2.5
      student$topics[[topic_id]]$interval <- 7
      student$topics[[topic_id]]$repetition <- 3L
      student$topics[[topic_id]]$next_review <- Sys.time() + 7 * 86400
    } else if (topic_asked > 0) {
      student$topics[[topic_id]]$mastery_state <- "in_progress"
    }
  }

  cat_result <- structure(
    list(
      student_id       = student$student_id,
      questions_asked  = total_asked,
      topic_placements = topic_placements,
      attempt_log      = attempt_log
    ),
    class = "cat_result"
  )

  list(student = student, cat_result = cat_result)
}

#' Run an interactive placement test from the R console
#'
#' Prompts the student to answer via \code{readline}.
#'
#' @param student A \code{student_model} object. Created fresh if NULL.
#' @param max_questions Integer (default 25)
#' @return List with \code{student} and \code{cat_result}
#' @export
interactive_placement <- function(student = NULL, max_questions = 25L) {
  if (is.null(student)) student <- create_student_model()

  cat("=== Placement Test ===\n")
  cat("Answer each question. This determines where you start.\n\n")

  answer_fn <- function(problem) {
    cat("--- Question ---\n")
    cat(problem$statement, "\n\n")
    readline("Your answer: ")
  }

  result <- run_placement_test(student, answer_fn, max_questions)

  cat("\n=== Placement Complete ===\n")
  cat("Questions answered:", result$cat_result$questions_asked, "\n\n")
  for (tid in names(result$cat_result$topic_placements)) {
    tp <- result$cat_result$topic_placements[[tid]]
    cat(tid, ": ", tp$status, " (start difficulty ", tp$start_difficulty,
        ", accuracy ", round(tp$estimated_accuracy * 100), "%)\n", sep = "")
  }

  result
}

#' Print method for cat_result
#'
#' @param x A \code{cat_result} object
#' @param ... Additional arguments (ignored)
#' @export
print.cat_result <- function(x, ...) {
  cat("=== CAT Placement Result ===\n")
  cat("Questions asked:", x$questions_asked, "\n\n")
  for (tid in names(x$topic_placements)) {
    tp <- x$topic_placements[[tid]]
    cat(sprintf("  %-30s %s (diff %d, acc %.0f%%)\n",
                tid, tp$status, tp$start_difficulty,
                tp$estimated_accuracy * 100))
  }
  invisible(x)
}
