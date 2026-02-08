# =============================================================================
# Problem Engine — Generic engine that reads templates and produces problems
# =============================================================================

#' @importFrom uuid UUIDgenerate
#' @importFrom jsonlite toJSON

#' Generate a randomized problem instance
#'
#' The core function of the fisherapp package. Selects a template matching
#' the requested topic and difficulty, draws random parameters, and produces
#' a complete problem with statement, solution steps, and answer.
#'
#' @param topic_id Character. One of the 8 active topic IDs.
#' @param difficulty Integer 1-5.
#' @param template_id Character. Optional specific template. If NULL, a random
#'   matching template is chosen.
#' @param seed Integer. Optional seed for reproducibility.
#' @return A \code{fisherapp_problem} object (S3 list) with fields:
#'   problem_id, topic_id, difficulty, template_id, statement, solution_steps,
#'   answer, answer_raw, prerequisites, params
#' @export
#' @examples
#' \dontrun{
#' prob <- generate_problem("fraction_arithmetic", difficulty = 2)
#' print(prob)
#' }
generate_problem <- function(topic_id, difficulty, template_id = NULL,
                             seed = NULL) {
  if (!is.null(seed)) set.seed(seed)

  # Find matching template(s)
  if (!is.null(template_id)) {
    tmpl <- .template_registry[[template_id]]
    if (is.null(tmpl)) stop("Template not found: ", template_id)
  } else {
    candidates <- get_templates(topic_id, difficulty)
    if (length(candidates) == 0) {
      stop("No templates for topic '", topic_id,
           "' at difficulty ", difficulty)
    }
    tmpl <- candidates[[sample.int(length(candidates), 1)]]
  }

  # Draw parameters with constraint checking
  params <- draw_params(tmpl, max_attempts = 100)

  # Build the problem
  statement <- tmpl$statement(params)
  solution <- tmpl$solve(params)
  answer_latex <- tmpl$format_answer(solution)

  # Get prerequisites from knowledge graph
  prereqs <- tryCatch(
    get_prerequisites(topic_id),
    error = function(e) character(0)
  )

  # Return structured problem object
  structure(
    list(
      problem_id = uuid::UUIDgenerate(),
      topic_id = topic_id,
      difficulty = as.integer(difficulty),
      template_id = tmpl$template_id,
      statement = statement,
      solution_steps = solution$steps,
      answer = answer_latex,
      answer_raw = solution,
      prerequisites = prereqs,
      params = params
    ),
    class = "fisherapp_problem"
  )
}

#' Draw parameters from a template, respecting constraints
#'
#' @param tmpl Template list object
#' @param max_attempts Maximum redraws before giving up
#' @return Named list of parameter values
#' @keywords internal
draw_params <- function(tmpl, max_attempts = 100) {
  for (i in seq_len(max_attempts)) {
    p <- lapply(tmpl$params, function(f) f())
    if (is.null(tmpl$constraint) || isTRUE(tmpl$constraint(p))) {
      return(p)
    }
  }
  stop("Could not satisfy template constraints after ",
       max_attempts, " attempts for template: ", tmpl$template_id)
}

#' Print method for fisherapp_problem objects
#'
#' @param x A fisherapp_problem object
#' @param ... Additional arguments (ignored)
#' @export
print.fisherapp_problem <- function(x, ...) {
  cat("=== Problem ===\n")
  cat(x$statement, "\n\n")
  cat("Topic:", x$topic_id, " | Difficulty:", x$difficulty, "\n")
  cat("Template:", x$template_id, "\n\n")
  cat("=== Solution ===\n")
  for (step in x$solution_steps) {
    cat(step, "\n")
  }
  cat("\nAnswer:", x$answer, "\n")
  invisible(x)
}

#' Convert a problem object to JSON (for API layer)
#'
#' Strips internal fields (answer_raw, params) that the frontend
#' should not receive.
#'
#' @param problem A fisherapp_problem object
#' @param include_solution Logical. If FALSE, omits solution_steps and answer
#'   (for when the student hasn't submitted yet).
#' @return JSON string
#' @export
problem_to_json <- function(problem, include_solution = TRUE) {
  obj <- list(
    problem_id = problem$problem_id,
    topic_id = problem$topic_id,
    difficulty = problem$difficulty,
    template_id = problem$template_id,
    statement = problem$statement,
    prerequisites = problem$prerequisites
  )
  if (include_solution) {
    obj$solution_steps <- problem$solution_steps
    obj$answer <- problem$answer
  }
  jsonlite::toJSON(obj, auto_unbox = TRUE, pretty = TRUE)
}
