# =============================================================================
# Answer Checker — Equivalence-aware answer checking
# =============================================================================

#' Check a student's answer against the correct answer
#'
#' Handles equivalent forms: "3/4" = "6/8" = "0.75" = "\\frac{3}{4}".
#'
#' @param problem A fisherapp_problem object (from \code{\link{generate_problem}})
#' @param student_answer Character string. The student's answer.
#' @return List with fields:
#'   \describe{
#'     \item{correct}{Logical. TRUE if the answer is correct.}
#'     \item{correct_answer}{Character. The correct answer in LaTeX format.}
#'     \item{solution_steps}{Character vector. The worked solution steps.}
#'   }
#' @export
check_answer <- function(problem, student_answer) {
  correct_raw <- problem$answer_raw
  is_correct <- compare_answers(student_answer, correct_raw)

  list(
    correct = is_correct,
    correct_answer = problem$answer,
    solution_steps = problem$solution_steps
  )
}

#' Compare a student answer to the correct answer
#'
#' Parses the student answer and compares numerically with tolerance.
#'
#' @param student_answer Character string
#' @param correct_raw The raw answer object from the template's solve function
#' @return Logical
#' @keywords internal
compare_answers <- function(student_answer, correct_raw) {
  student_answer <- trimws(as.character(student_answer))
  if (nchar(student_answer) == 0) return(FALSE)

  parsed <- parse_student_answer(student_answer)
  if (is.null(parsed)) return(FALSE)

  correct_numeric <- to_numeric(correct_raw)
  student_numeric <- to_numeric(parsed)

  if (is.na(correct_numeric) || is.na(student_numeric)) return(FALSE)

  isTRUE(all.equal(correct_numeric, student_numeric, tolerance = 1e-9))
}

#' Parse a student answer string into a structured form
#'
#' Supports: "3/4", "0.75", "3", "-2/5", "\\frac{3}{4}", "\\frac{-3}{4}"
#'
#' @param answer Character string
#' @return List with either num/den or value, or NULL if unparseable
#' @keywords internal
parse_student_answer <- function(answer) {
  answer <- trimws(answer)

  # Try LaTeX fraction: \frac{num}{den}
  m <- regmatches(answer,
    regexec("^-?\\\\frac\\{(-?\\d+)\\}\\{(-?\\d+)\\}$", answer))[[1]]
  if (length(m) == 3) {
    num <- as.integer(m[2])
    den <- as.integer(m[3])
    # Handle leading negative sign
    if (startsWith(answer, "-") && num > 0) num <- -num
    return(list(num = num, den = den))
  }

  # Try plain fraction: num/den
  m <- regmatches(answer,
    regexec("^(-?\\d+)/(-?\\d+)$", answer))[[1]]
  if (length(m) == 3) {
    return(list(num = as.integer(m[2]), den = as.integer(m[3])))
  }

  # Try decimal or integer
  val <- suppressWarnings(as.numeric(answer))
  if (!is.na(val)) return(list(value = val))

  NULL
}

#' Convert a raw answer to numeric for comparison
#'
#' Handles various answer formats from different template types.
#'
#' @param raw Answer object (list or numeric)
#' @return Numeric value, or NA
#' @keywords internal
to_numeric <- function(raw) {
  if (is.numeric(raw) && length(raw) == 1) return(as.numeric(raw))

  if (is.list(raw)) {
    # Direct numeric value
    if (!is.null(raw$value)) return(as.numeric(raw$value))
    # Fraction from answer checker parse
    if (!is.null(raw$num) && !is.null(raw$den)) {
      return(raw$num / raw$den)
    }
    # Fraction from template solve (answer_num/answer_den convention)
    if (!is.null(raw$answer_num) && !is.null(raw$answer_den)) {
      return(raw$answer_num / raw$answer_den)
    }
    # answer_value convention (for non-fraction answers)
    if (!is.null(raw$answer_value)) return(as.numeric(raw$answer_value))
  }

  NA_real_
}
