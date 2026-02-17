# =============================================================================
# Problem Templates — Order of Operations (5 difficulty levels)
# =============================================================================

#' Register all order of operations templates
#' @keywords internal
register_order_of_operations_templates <- function() {

  # ---------------------------------------------------------------------------
  # Difficulty 1: Recognition — Evaluate a + b * c
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "ooo_d1_identify",
    topic_id = "order_of_operations",
    difficulty = 1L,
    description = "Evaluate a simple expression requiring multiplication before addition",
    params = list(
      a = function() sample(2:9, 1),
      b = function() sample(2:9, 1),
      c = function() sample(2:9, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      paste0("Evaluate $", p$a, " + ", p$b, " \\times ", p$c, "$.")
    },
    solve = function(p) {
      prod_bc <- p$b * p$c
      result <- p$a + prod_bc
      steps <- c(
        paste0("Step 1: By order of operations (PEMDAS), perform multiplication before addition."),
        paste0("Step 2: First, multiply: $", p$b, " \\times ", p$c, " = ", prod_bc, "$."),
        paste0("Step 3: Then, add: $", p$a, " + ", prod_bc, " = ", result, "$.")
      )
      list(steps = steps, answer_value = result)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 2: Routine — Evaluate (a - b)^2 + c * d
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "ooo_d2_basic",
    topic_id = "order_of_operations",
    difficulty = 2L,
    description = "Evaluate an expression with parentheses, exponent, and multiplication",
    params = list(
      a = function() sample(5:15, 1),
      b = function() sample(1:4, 1),
      c = function() sample(2:6, 1),
      d = function() sample(2:6, 1)
    ),
    constraint = function(p) {
      p$a > p$b
    },
    statement = function(p) {
      paste0("Evaluate $(", p$a, " - ", p$b, ")^{2} + ", p$c, " \\times ", p$d, "$.")
    },
    solve = function(p) {
      diff_ab <- p$a - p$b
      sq <- diff_ab^2
      prod_cd <- p$c * p$d
      result <- sq + prod_cd
      steps <- c(
        paste0("Step 1: Parentheses: $", p$a, " - ", p$b, " = ", diff_ab, "$."),
        paste0("Step 2: Exponent: $", diff_ab, "^{2} = ", sq, "$."),
        paste0("Step 3: Multiplication: $", p$c, " \\times ", p$d, " = ", prod_cd, "$."),
        paste0("Step 4: Addition: $", sq, " + ", prod_cd, " = ", result, "$.")
      )
      list(steps = steps, answer_value = result)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 3: Multi-step — [(a - b)^2 - (c + d)^2] / e^f
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "ooo_d3_nested",
    topic_id = "order_of_operations",
    difficulty = 3L,
    description = "Evaluate a nested expression with brackets, exponents, and division",
    params = list(
      a = function() sample(8:15, 1),
      b = function() sample(1:4, 1),
      c = function() sample(1:4, 1),
      d = function() sample(1:4, 1),
      e = function() 2L,
      f = function() sample(2:3, 1)
    ),
    constraint = function(p) {
      left <- (p$a - p$b)^2
      right <- (p$c + p$d)^2
      denom <- p$e^p$f
      left > right && (left - right) %% denom == 0
    },
    statement = function(p) {
      paste0("Evaluate $\\dfrac{(", p$a, " - ", p$b, ")^{2} - (",
             p$c, " + ", p$d, ")^{2}}{", p$e, "^{", p$f, "}}$.")
    },
    solve = function(p) {
      diff_ab <- p$a - p$b
      sq_left <- diff_ab^2
      sum_cd <- p$c + p$d
      sq_right <- sum_cd^2
      numerator <- sq_left - sq_right
      denom <- p$e^p$f
      result <- numerator %/% denom

      steps <- c(
        paste0("Step 1: Parentheses: $", p$a, " - ", p$b, " = ", diff_ab,
               "$ and $", p$c, " + ", p$d, " = ", sum_cd, "$."),
        paste0("Step 2: Exponents: $", diff_ab, "^{2} = ", sq_left,
               "$ and $", sum_cd, "^{2} = ", sq_right, "$."),
        paste0("Step 3: Subtraction in numerator: $", sq_left, " - ", sq_right,
               " = ", numerator, "$."),
        paste0("Step 4: Exponent in denominator: $", p$e, "^{", p$f, "} = ", denom, "$."),
        paste0("Step 5: Division: $", latex_frac(numerator, denom), " = ", result, "$.")
      )

      if (numerator %% denom == 0) {
        list(steps = steps, answer_value = result)
      } else {
        frac <- simplify_fraction(numerator, denom)
        list(steps = steps, answer_num = frac$num, answer_den = frac$den)
      }
    },
    format_answer = function(sol) {
      if (!is.null(sol$answer_value)) {
        as.character(sol$answer_value)
      } else {
        latex_frac(sol$answer_num, sol$answer_den)
      }
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 4: Transfer — Compute a z-score z = (x - mu) / sigma
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "ooo_d4_zscore",
    topic_id = "order_of_operations",
    difficulty = 4L,
    description = "Compute a z-score applying order of operations to a statistics formula",
    params = list(
      x     = function() sample(60:100, 1),
      mu    = function() sample(65:85, 1),
      sigma = function() sample(c(5L, 8L, 10L, 12L, 15L), 1)
    ),
    constraint = function(p) {
      (p$x - p$mu) %% p$sigma == 0
    },
    statement = function(p) {
      paste0("A student scores $x = ", p$x,
             "$ on an exam with mean $\\mu = ", p$mu,
             "$ and standard deviation $\\sigma = ", p$sigma,
             "$. Compute the z-score using $z = \\dfrac{x - \\mu}{\\sigma}$.")
    },
    solve = function(p) {
      diff_val <- p$x - p$mu
      z <- diff_val / p$sigma

      steps <- c(
        paste0("Step 1: Subtract the mean (parentheses first): $x - \\mu = ",
               p$x, " - ", p$mu, " = ", diff_val, "$."),
        paste0("Step 2: Divide by the standard deviation: $z = ",
               latex_frac(diff_val, p$sigma), "$.")
      )

      if (diff_val %% p$sigma == 0) {
        steps <- c(steps, paste0("Step ", length(steps) + 1, ": Simplify: $z = ", z, "$."))
        list(steps = steps, answer_value = z)
      } else {
        frac <- simplify_fraction(diff_val, p$sigma)
        steps <- c(steps, paste0("Step ", length(steps) + 1, ": Simplify: $z = ", latex_frac(frac$num, frac$den), "$."))
        list(steps = steps, answer_num = frac$num, answer_den = frac$den)
      }
    },
    format_answer = function(sol) {
      if (!is.null(sol$answer_value)) {
        as.character(sol$answer_value)
      } else {
        latex_frac(sol$answer_num, sol$answer_den)
      }
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 5: Synthesis — Compute sample variance of 4 integers
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "ooo_d5_variance",
    topic_id = "order_of_operations",
    difficulty = 5L,
    description = "Compute the sample variance of four integers step by step",
    params = list(
      x1 = function() sample(1:20, 1),
      x2 = function() sample(1:20, 1),
      x3 = function() sample(1:20, 1),
      x4 = function() sample(1:20, 1)
    ),
    constraint = function(p) {
      # Require the sum to be divisible by 4 so xbar is a whole number
      total <- p$x1 + p$x2 + p$x3 + p$x4
      total %% 4 == 0 &&
        # Ensure not all values are the same (variance would be zero)
        length(unique(c(p$x1, p$x2, p$x3, p$x4))) > 1
    },
    statement = function(p) {
      paste0("Compute the sample variance of the data set ",
             "$\\{", p$x1, ",\\, ", p$x2, ",\\, ", p$x3, ",\\, ", p$x4, "\\}$ ",
             "using $s^{2} = \\dfrac{1}{n-1}\\displaystyle\\sum_{i=1}^{n}(x_i - \\bar{x})^{2}$.")
    },
    solve = function(p) {
      vals <- c(p$x1, p$x2, p$x3, p$x4)
      n <- 4L
      total <- sum(vals)
      xbar <- total / n

      devs <- vals - xbar
      sq_devs <- devs^2
      ss <- sum(sq_devs)
      # n - 1 = 3
      denom <- n - 1L

      # Build step-by-step
      steps <- c(
        paste0("Step 1: Compute the mean: $\\bar{x} = ",
               latex_frac(total, n), " = ", xbar, "$."),
        paste0("Step 2: Compute each deviation $(x_i - \\bar{x})$:"),
        paste0("Step 3: $", vals[1], " - ", xbar, " = ", devs[1], "$, ",
               "$", vals[2], " - ", xbar, " = ", devs[2], "$, ",
               "$", vals[3], " - ", xbar, " = ", devs[3], "$, ",
               "$", vals[4], " - ", xbar, " = ", devs[4], "$."),
        paste0("Step 4: Square the deviations:"),
        paste0("Step 5: $(", devs[1], ")^{2} = ", sq_devs[1], "$, ",
               "$(", devs[2], ")^{2} = ", sq_devs[2], "$, ",
               "$(", devs[3], ")^{2} = ", sq_devs[3], "$, ",
               "$(", devs[4], ")^{2} = ", sq_devs[4], "$."),
        paste0("Step 6: Sum of squared deviations: $",
               paste(sq_devs, collapse = " + "), " = ", ss, "$."),
        paste0("Step 7: Divide by $n - 1 = ", denom,
               "$: $s^{2} = ", latex_frac(ss, denom), "$.")
      )

      frac <- simplify_fraction(ss, denom)

      if (frac$den == 1L) {
        steps <- c(steps, paste0("Step ", length(steps) + 1, ": Simplify: $s^{2} = ", frac$num, "$."))
        list(steps = steps, answer_num = frac$num, answer_den = 1L)
      } else {
        steps <- c(steps, paste0("Step ", length(steps) + 1, ": Simplify: $s^{2} = ",
                                 latex_frac(frac$num, frac$den), "$."))
        list(steps = steps, answer_num = frac$num, answer_den = frac$den)
      }
    },
    format_answer = function(sol) {
      if (sol$answer_den == 1L) {
        as.character(sol$answer_num)
      } else {
        latex_frac(sol$answer_num, sol$answer_den)
      }
    }
  ))
}
