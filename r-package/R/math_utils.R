# =============================================================================
# Math Utilities — Foundation for all template computations
# =============================================================================

#' Greatest Common Divisor (Euclidean algorithm)
#'
#' @param a Integer
#' @param b Integer
#' @return Integer GCD of a and b
#' @export
gcd <- function(a, b) {
  a <- abs(as.integer(a))
  b <- abs(as.integer(b))
  while (b != 0L) {
    t <- b
    b <- a %% b
    a <- t
  }
  a
}

#' Least Common Multiple
#'
#' @param a Integer
#' @param b Integer
#' @return Integer LCM of a and b
#' @export
lcd <- function(a, b) {
  a <- abs(as.integer(a))
  b <- abs(as.integer(b))
  if (a == 0L || b == 0L) return(0L)
  as.integer(a / gcd(a, b) * b)
}

#' Simplify a fraction to lowest terms
#'
#' @param num Integer numerator
#' @param den Integer denominator
#' @return Named list with \code{num} and \code{den} in lowest terms
#' @export
simplify_fraction <- function(num, den) {
  stopifnot(den != 0)
  num <- as.integer(num)
  den <- as.integer(den)
  if (den < 0L) {
    num <- -num
    den <- -den
  }
  if (num == 0L) return(list(num = 0L, den = den))
  g <- gcd(abs(num), den)
  list(num = num / g, den = den / g)
}

#' Add two fractions
#'
#' @param n1,d1 Numerator and denominator of first fraction
#' @param n2,d2 Numerator and denominator of second fraction
#' @return Simplified fraction as list(num, den)
#' @export
frac_add <- function(n1, d1, n2, d2) {
  num <- n1 * d2 + n2 * d1
  den <- d1 * d2
  simplify_fraction(num, den)
}

#' Subtract two fractions
#'
#' @param n1,d1 Numerator and denominator of first fraction
#' @param n2,d2 Numerator and denominator of second fraction
#' @return Simplified fraction as list(num, den)
#' @export
frac_sub <- function(n1, d1, n2, d2) {
  num <- n1 * d2 - n2 * d1
  den <- d1 * d2
  simplify_fraction(num, den)
}

#' Multiply two fractions
#'
#' @param n1,d1 Numerator and denominator of first fraction
#' @param n2,d2 Numerator and denominator of second fraction
#' @return Simplified fraction as list(num, den)
#' @export
frac_mul <- function(n1, d1, n2, d2) {
  simplify_fraction(n1 * n2, d1 * d2)
}

#' Divide two fractions
#'
#' @param n1,d1 Numerator and denominator of first fraction
#' @param n2,d2 Numerator and denominator of second fraction
#' @return Simplified fraction as list(num, den)
#' @export
frac_div <- function(n1, d1, n2, d2) {
  stopifnot(n2 != 0)
  simplify_fraction(n1 * d2, d1 * n2)
}

#' Safe factorial (integer only, max 20)
#'
#' @param n Non-negative integer
#' @return n!
#' @keywords internal
factorial_safe <- function(n) {
  stopifnot(n >= 0, n == floor(n), n <= 20)
  if (n == 0) return(1L)
  prod(seq_len(n))
}

#' Combinations C(n, k)
#'
#' @param n Total items
#' @param k Items to choose
#' @return Integer C(n, k)
#' @export
choose_safe <- function(n, k) {
  stopifnot(k >= 0, k <= n, n >= 0)
  # Use R's built-in choose for numerical stability
  as.integer(round(choose(n, k)))
}

#' Permutations P(n, k)
#'
#' @param n Total items
#' @param k Items to arrange
#' @return Integer P(n, k)
#' @export
perm <- function(n, k) {
  stopifnot(k >= 0, k <= n, n >= 0)
  if (k == 0) return(1L)
  as.integer(round(prod(seq(n, n - k + 1))))
}
