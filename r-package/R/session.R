# =============================================================================
# Session Management — The user-facing tutoring loop
# =============================================================================

#' Start a new tutoring session
#'
#' @param student A \code{student_model} object
#' @return Updated \code{student_model} with an active session
#' @export
start_session <- function(student) {
  session <- structure(
    list(
      session_id       = uuid::UUIDgenerate(),
      student_id       = student$student_id,
      started_at       = Sys.time(),
      ended_at         = NULL,
      topics_attempted = character(0),
      attempts         = list(),
      problems_served  = 0L,
      problems_correct = 0L,
      is_placement     = FALSE,
      templates_served = character(0)
    ),
    class = "tutor_session"
  )
  student$current_session <- session
  student
}

#' Get the next problem in the current session
#'
#' Checks for stuck-loop conditions before delegating to
#' \code{\link{next_problem_for_student}}.
#'
#' @param student A \code{student_model} object (with active session)
#' @return List with \code{problem}, \code{intervention}, and \code{student}
#' @export
get_next_problem <- function(student) {
  if (is.null(student$current_session)) {
    stop("No active session. Call start_session() first.")
  }

  # Determine next topic selection
  selection <- select_next_topic(student)

  if (is.null(selection)) {
    return(list(
      problem      = NULL,
      intervention = list(type = "session_complete",
                          message = "All topics mastered and none due for review."),
      student      = student
    ))
  }

  # Check for stuck condition on the selected topic
  ts <- student$topics[[selection$topic_id]]
  stuck <- detect_stuck(ts)

  if (!is.null(stuck)) {
    # Apply intervention
    if (stuck$type == "reduce_difficulty") {
      student$topics[[selection$topic_id]]$difficulty <-
        max(1L, ts$difficulty - 1L)
      student$topics[[selection$topic_id]]$consecutive_wrong <- 0L
      selection$difficulty <- student$topics[[selection$topic_id]]$difficulty
    } else if (stuck$type == "route_prerequisite") {
      # Switch to the prerequisite topic
      selection$topic_id <- stuck$redirect_topic
      prereq_ts <- student$topics[[selection$topic_id]]
      selection$difficulty <- if (!is.null(prereq_ts)) prereq_ts$difficulty else 1L
      student$topics[[ts$topic_id]]$consecutive_wrong <- 0L
    } else if (stuck$type == "worked_example") {
      # Generate a problem but mark it as a worked example
      student$topics[[selection$topic_id]]$consecutive_wrong <- 0L
    }
  }

  problem <- generate_problem(selection$topic_id, selection$difficulty,
    exclude_templates = student$current_session$templates_served)

  # Track the served template
  student$current_session$templates_served <- c(
    student$current_session$templates_served, problem$template_id)

  list(
    problem      = problem,
    intervention = stuck,
    student      = student
  )
}

#' Submit an answer and update all state
#'
#' Orchestrates the full pipeline: check answer, map quality, update SM-2,
#' update performance window, evaluate mastery, adjust difficulty.
#'
#' @param student A \code{student_model} object
#' @param problem A \code{fisherapp_problem} object
#' @param answer Character. The student's answer.
#' @return List with \code{result}, \code{student}, \code{mastery_changed},
#'   and \code{new_mastery}
#' @export
submit_answer <- function(student, problem, answer) {
  if (is.null(student$current_session)) {
    stop("No active session. Call start_session() first.")
  }

  # 1. Check the answer
  result <- check_answer(problem, answer)
  topic_id <- problem$topic_id
  ts <- student$topics[[topic_id]]
  old_mastery <- ts$mastery_state

  # 2. Update last_n_results (sliding window of 10)
  ts$last_n_results <- c(ts$last_n_results, as.integer(result$correct))
  if (length(ts$last_n_results) > 10L) {
    ts$last_n_results <- utils::tail(ts$last_n_results, 10L)
  }

  # 3. Update counters
  ts$attempt_count <- ts$attempt_count + 1L
  if (result$correct) {
    ts$correct_count <- ts$correct_count + 1L
    ts$consecutive_wrong <- 0L
    ts$last_difficulty_wrong <- NA_integer_
  } else {
    if (!is.na(ts$last_difficulty_wrong) &&
        ts$last_difficulty_wrong == problem$difficulty) {
      ts$consecutive_wrong <- ts$consecutive_wrong + 1L
    } else {
      ts$consecutive_wrong <- 1L
    }
    ts$last_difficulty_wrong <- problem$difficulty
  }

  # 4. Track session topic (increment session_count on first encounter)
  if (!(topic_id %in% student$current_session$topics_attempted)) {
    student$current_session$topics_attempted <- c(
      student$current_session$topics_attempted, topic_id)
    ts$session_count <- ts$session_count + 1L
  }

  # 5. Map to SM-2 quality and update schedule
  quality <- map_quality(result$correct, problem$difficulty,
                         ts$difficulty, ts$consecutive_wrong)
  ts <- sm2_update(ts, quality)

  # 6. Set mastery to in_progress if was not_started
  if (ts$mastery_state == "not_started") {
    ts$mastery_state <- "in_progress"
  }

  # 7. Adjust difficulty
  ts$difficulty <- adjust_difficulty(ts)

  # 8. Evaluate mastery
  ts$mastery_state <- evaluate_mastery(ts)

  # 9. Write back topic state
  student$topics[[topic_id]] <- ts

  # 10. Update session log
  student$current_session$problems_served <-
    student$current_session$problems_served + 1L
  if (result$correct) {
    student$current_session$problems_correct <-
      student$current_session$problems_correct + 1L
  }
  student$current_session$attempts[[
    length(student$current_session$attempts) + 1]] <- list(
    problem_id = problem$problem_id,
    topic_id   = topic_id,
    difficulty = problem$difficulty,
    correct    = result$correct,
    timestamp  = Sys.time()
  )

  # 11. Update global stats
  student$total_attempts <- student$total_attempts + 1L
  if (result$correct) {
    student$total_correct <- student$total_correct + 1L
  }

  mastery_changed <- (old_mastery != ts$mastery_state)

  list(
    result          = result,
    student         = student,
    mastery_changed = mastery_changed,
    new_mastery     = if (mastery_changed) ts$mastery_state else NULL
  )
}

#' End the current session
#'
#' Archives the session to session_history and clears current_session.
#'
#' @param student A \code{student_model} object
#' @return Updated \code{student_model}
#' @export
end_session <- function(student) {
  if (is.null(student$current_session)) {
    stop("No active session to end.")
  }
  student$current_session$ended_at <- Sys.time()
  student$session_history[[length(student$session_history) + 1]] <-
    student$current_session
  student$current_session <- NULL
  student
}

#' Detect stuck-loop condition and determine intervention
#'
#' Stuck if 3+ consecutive wrong on same topic at same difficulty.
#'
#' @param topic_state A topic_state list
#' @param threshold Integer, consecutive wrong threshold (default 3)
#' @return NULL if not stuck, or a list with \code{type} and \code{message}
#' @keywords internal
detect_stuck <- function(topic_state, threshold = 3L) {
  if (topic_state$consecutive_wrong < threshold) {
    return(NULL)
  }

  # If we can lower difficulty, do that

  if (topic_state$difficulty > 1L) {
    return(list(
      type    = "reduce_difficulty",
      message = paste0("Let's try an easier version of ",
                       topic_state$topic_id, ".")
    ))
  }

  # At difficulty 1, try routing to a prerequisite
  prereqs <- tryCatch(
    get_prerequisites(topic_state$topic_id),
    error = function(e) character(0)
  )
  if (length(prereqs) > 0) {
    return(list(
      type            = "route_prerequisite",
      message         = paste0("Let's review a prerequisite: ", prereqs[1], "."),
      redirect_topic  = prereqs[1]
    ))
  }

  # Root topic at difficulty 1 — worked example
  list(
    type    = "worked_example",
    message = "Here's a worked example to study before trying again."
  )
}

#' Simulate a complete tutoring session
#'
#' For testing and demonstration. Generates problems and simulates answers
#' based on a given probability of correctness.
#'
#' @param student A \code{student_model} object
#' @param n_problems Integer, number of problems to simulate
#' @param correct_rate Numeric 0-1, probability of correct answer
#' @param seed Integer for reproducibility
#' @return List with \code{student} (updated) and \code{summary} (data.frame)
#' @export
simulate_session <- function(student, n_problems = 20L,
                             correct_rate = 0.7, seed = NULL) {
  if (!is.null(seed)) set.seed(seed)
  student <- start_session(student)
  log_entries <- list()

  for (i in seq_len(n_problems)) {
    result <- get_next_problem(student)
    student <- result$student

    if (is.null(result$problem)) break

    # Simulate student answer
    is_correct <- stats::runif(1) < correct_rate
    answer <- if (is_correct) result$problem$answer else "wrong_answer"

    submit_result <- submit_answer(student, result$problem, answer)
    student <- submit_result$student

    log_entries[[i]] <- data.frame(
      problem_num = i,
      topic_id    = result$problem$topic_id,
      difficulty  = result$problem$difficulty,
      correct     = submit_result$result$correct,
      mastery_changed = submit_result$mastery_changed,
      intervention = if (!is.null(result$intervention)) result$intervention$type else NA_character_,
      stringsAsFactors = FALSE
    )
  }

  student <- end_session(student)
  summary_df <- if (length(log_entries) > 0) do.call(rbind, log_entries) else data.frame()

  list(student = student, summary = summary_df)
}

#' Run an interactive tutoring session from the R console
#'
#' Prompts the student to answer problems via \code{readline}.
#' Type "quit" to end the session.
#'
#' @param student Optional \code{student_model}. Created fresh if NULL.
#' @return Final \code{student_model} (invisible)
#' @export
interactive_session <- function(student = NULL) {
  if (is.null(student)) student <- create_student_model()
  student <- start_session(student)

  cat("=== Interactive Tutoring Session ===\n")
  cat("Type your answer, or 'quit' to end.\n\n")

  repeat {
    result <- get_next_problem(student)
    student <- result$student

    if (is.null(result$problem)) {
      cat("\nNo more problems available. Session complete!\n")
      break
    }

    if (!is.null(result$intervention)) {
      cat("[Intervention: ", result$intervention$message, "]\n\n", sep = "")
    }

    cat("--- Problem ---\n")
    cat(result$problem$statement, "\n\n")

    answer <- readline("Your answer: ")
    if (tolower(trimws(answer)) == "quit") break

    submit_result <- submit_answer(student, result$problem, answer)
    student <- submit_result$student

    if (submit_result$result$correct) {
      cat("Correct!\n\n")
    } else {
      cat("Incorrect. The answer is: ", submit_result$result$correct_answer, "\n")
      cat("Solution:\n")
      for (step in submit_result$result$solution_steps) {
        cat("  ", step, "\n")
      }
      cat("\n")
    }

    if (submit_result$mastery_changed) {
      cat("[Mastery update: ", result$problem$topic_id, " -> ",
          submit_result$new_mastery, "]\n\n", sep = "")
    }
  }

  student <- end_session(student)
  cat("\n=== Session Summary ===\n")
  cat("Problems:", student$session_history[[length(student$session_history)]]$problems_served, "\n")
  cat("Correct:", student$session_history[[length(student$session_history)]]$problems_correct, "\n")
  print(student)
  invisible(student)
}
