# =============================================================================
# LaTeX Formatting Utilities
# =============================================================================

#' @importFrom glue glue

#' Format a fraction as LaTeX
#'
#' @param num Integer numerator
#' @param den Integer denominator
#' @return LaTeX string
#' @export
latex_frac <- function(num, den) {
  if (den == 1) return(as.character(as.integer(num)))
  if (num < 0 && den > 0) {
    return(paste0("-\\frac{", abs(num), "}{", den, "}"))
  }
  paste0("\\frac{", num, "}{", den, "}")
}

#' Format an exponent as LaTeX
#'
#' @param base Character or numeric base
#' @param exp Integer exponent
#' @return LaTeX string
#' @export
latex_exp <- function(base, exp) {
  base <- as.character(base)
  if (exp == 1) return(base)
  if (exp == 0) return(paste0(base, "^{0}"))
  paste0(base, "^{", exp, "}")
}

#' Format a summation as LaTeX
#'
#' @param index Index variable name
#' @param lower Lower bound
#' @param upper Upper bound
#' @param body Summand expression (LaTeX)
#' @return LaTeX string
#' @export
latex_sum <- function(index, lower, upper, body) {
  paste0("\\sum_{", index, "=", lower, "}^{", upper, "} ", body)
}

#' Wrap expression in display math delimiters
#'
#' @param expr LaTeX expression string
#' @return String wrapped in $$ $$
#' @export
latex_display <- function(expr) {
  paste0("$$", expr, "$$")
}

#' Wrap expression in inline math delimiters
#'
#' @param expr LaTeX expression string
#' @return String wrapped in $ $
#' @export
latex_inline <- function(expr) {
  paste0("$", expr, "$")
}
