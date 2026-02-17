# =============================================================================
# Answer Checker — Equivalence-aware answer checking with flexible matching
# =============================================================================

#' Normalize an answer string for comparison
#'
#' Strips outer parentheses, whitespace, normalizes case, and removes
#' common formatting artifacts. Applied to both student and expected answers
#' before comparison.
#'
#' @param answer Character string
#' @return Normalized character string
#' @keywords internal
normalize_answer <- function(answer) {
  answer <- trimws(as.character(answer))
  answer <- tolower(answer)
  # Strip outer parentheses: "(a)" -> "a", "(3/4)" -> "3/4"
  # Only strip if the content has no unmatched inner parens
  answer <- gsub("^\\(([^()]+)\\)$", "\\1", answer)
  # Normalize LaTeX artifacts that MathLive may produce
  answer <- gsub("\\\\dfrac", "\\\\frac", answer)   # \dfrac -> \frac
  answer <- gsub("\\\\left\\s*", "", answer)          # \left( -> (
  answer <- gsub("\\\\right\\s*", "", answer)         # \right) -> )
  answer <- gsub("\\\\cdot", "*", answer)             # \cdot -> *
  answer <- gsub("\\\\times", "*", answer)            # \times -> *
  answer <- gsub("\\\\,", "", answer)                 # thin space
  answer <- gsub("\\\\;", "", answer)                 # medium space
  answer <- gsub("\\\\!", "", answer)                 # negative thin space
  # Remove spaces around operators
  answer <- gsub("\\s+", "", answer)
  answer
}

#' Check a student's answer against the correct answer
#'
#' Handles equivalent forms: "3/4" = "6/8" = "0.75" = "\\frac{3}{4}".
#' Also accepts letter answers, strips parentheses, and normalizes case.
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
#' Uses a multi-strategy approach:
#' 1. Letter answer matching (if answer_raw contains answer_letter)
#' 2. Numeric comparison with tolerance
#' 3. Normalized string comparison for algebraic expressions
#'
#' @param student_answer Character string
#' @param correct_raw The raw answer object from the template's solve function
#' @return Logical
#' @keywords internal
compare_answers <- function(student_answer, correct_raw) {
  student_answer <- trimws(as.character(student_answer))
  if (nchar(student_answer) == 0) return(FALSE)

  normalized_student <- normalize_answer(student_answer)

  # Strategy 1: Letter answer matching
  if (is.list(correct_raw) && !is.null(correct_raw$answer_letter)) {
    correct_letter <- normalize_answer(correct_raw$answer_letter)
    if (normalized_student == correct_letter) return(TRUE)
  }

  # Strategy 2: Numeric comparison
  parsed <- parse_student_answer(student_answer)
  if (!is.null(parsed)) {
    correct_numeric <- to_numeric(correct_raw)
    student_numeric <- to_numeric(parsed)
    if (!is.na(correct_numeric) && !is.na(student_numeric)) {
      if (isTRUE(all.equal(correct_numeric, student_numeric,
                           tolerance = 1e-9))) {
        return(TRUE)
      }
    }
  }

  # Strategy 3: Algebraic string comparison (after normalization)
  if (is.list(correct_raw) && !is.null(correct_raw$answer_expr)) {
    correct_expr <- normalize_algebra(correct_raw$answer_expr)
    student_expr <- normalize_algebra(student_answer)
    if (correct_expr == student_expr) return(TRUE)
  }

  FALSE
}

#' Normalize an algebraic expression for comparison
#'
#' Handles equivalent algebraic forms: "2*x" = "2x", "x+1" = "1+x",
#' removes unnecessary multiplication signs, and sorts commutative terms.
#'
#' @param expr Character string
#' @return Normalized character string
#' @keywords internal
normalize_algebra <- function(expr) {
  expr <- normalize_answer(expr)

  # Remove explicit multiplication signs: "2*x" -> "2x"
  expr <- gsub("\\*", "", expr)

  # Sort additive terms: split on +, sort, rejoin
  # Handle subtraction by converting "a-b" to "a+-b"
  expr_expanded <- gsub("-", "+-", expr)
  terms <- strsplit(expr_expanded, "\\+")[[1]]
  terms <- terms[nchar(terms) > 0]  # Remove empty strings
  terms <- sort(terms)
  paste(terms, collapse = "+")
}

#' Parse a student answer string into a structured form
#'
#' Supports: "3/4", "0.75", ".5", "3", "-2/5", "\\frac{3}{4}", "\\frac{-3}{4}"
#'
#' @param answer Character string
#' @return List with either num/den or value, or NULL if unparseable
#' @keywords internal
parse_student_answer <- function(answer) {
  answer <- normalize_answer(answer)

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

  # Try plain fraction: num/den (also handles ".5/2" style)
  m <- regmatches(answer,
    regexec("^(-?\\d*\\.?\\d+)/(-?\\d*\\.?\\d+)$", answer))[[1]]
  if (length(m) == 3) {
    num_val <- suppressWarnings(as.numeric(m[2]))
    den_val <- suppressWarnings(as.numeric(m[3]))
    if (!is.na(num_val) && !is.na(den_val) && den_val != 0) {
      return(list(value = num_val / den_val))
    }
  }

  # Try \sqrt{n} -> evaluate to numeric
  m <- regmatches(answer,
    regexec("^\\\\sqrt\\{(-?\\d+\\.?\\d*)\\}$", answer))[[1]]
  if (length(m) == 2) {
    val <- suppressWarnings(as.numeric(m[2]))
    if (!is.na(val) && val >= 0) return(list(value = sqrt(val)))
  }

  # Try sqrt(n) -> evaluate to numeric
  m <- regmatches(answer,
    regexec("^sqrt\\((-?\\d+\\.?\\d*)\\)$", answer))[[1]]
  if (length(m) == 2) {
    val <- suppressWarnings(as.numeric(m[2]))
    if (!is.na(val) && val >= 0) return(list(value = sqrt(val)))
  }

  # Try decimal or integer (including leading dot like ".5")
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
