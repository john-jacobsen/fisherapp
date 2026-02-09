# =============================================================================
# Problem Templates — Summation Notation
# =============================================================================

#' Register all summation notation templates
#' @keywords internal
register_summation_notation_templates <- function() {

  # ---------------------------------------------------------------------------
  # D1: Recognition — Identify components of sigma notation
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "sum_d1_identify",
    topic_id = "summation_notation",
    difficulty = 1L,
    description = "Identify index, bounds, and number of terms in sigma notation",
    params = list(
      lower = function() sample(1:3, 1),
      upper = function() sample(5:10, 1),
      coeff = function() sample(2:5, 1),
      constant = function() sample(-3:5, 1)
    ),
    constraint = function(p) p$constant != 0,
    statement = function(p) {
      sign <- if (p$constant > 0) "+" else "-"
      paste0("Consider $", latex_sum("i", p$lower, p$upper,
             paste0(p$coeff, "i ", sign, " ", abs(p$constant))),
             "$. How many terms are in this sum?")
    },
    solve = function(p) {
      n_terms <- p$upper - p$lower + 1L
      list(
        steps = c(
          paste0("The index variable is $i$."),
          paste0("The lower bound is ", p$lower, " and the upper bound is ", p$upper, "."),
          paste0("Number of terms = upper - lower + 1 = ", p$upper, " - ", p$lower, " + 1 = ", n_terms, ".")
        ),
        answer_value = n_terms
      )
    },
    format_answer = function(sol) as.character(sol$answer_value)
  ))

  # ---------------------------------------------------------------------------
  # D2: Routine — Evaluate sum of i^2
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "sum_d2_evaluate",
    topic_id = "summation_notation",
    difficulty = 2L,
    description = "Evaluate a finite sum of i^2",
    params = list(
      n = function() sample(4:7, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      paste0("Evaluate $", latex_sum("i", 1, p$n, "i^2"), "$.")
    },
    solve = function(p) {
      terms <- seq_len(p$n)^2
      total <- sum(terms)
      expansion <- paste(paste0(seq_len(p$n), "^2"), collapse = " + ")
      values <- paste(terms, collapse = " + ")
      list(
        steps = c(
          paste0("Expand: $", expansion, "$."),
          paste0("Evaluate each term: $", values, "$."),
          paste0("Sum: $", total, "$.")
        ),
        answer_value = total
      )
    },
    format_answer = function(sol) as.character(sol$answer_value)
  ))

  # ---------------------------------------------------------------------------
  # D3: Multi-step — Apply linearity of summation
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "sum_d3_linearity",
    topic_id = "summation_notation",
    difficulty = 3L,
    description = "Apply linearity of summation to evaluate sum(ai + b)",
    params = list(
      a = function() sample(2:5, 1),
      b = function() sample(c(-5:-1, 1:5), 1),
      n = function() sample(4:8, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      sign <- if (p$b > 0) "+" else "-"
      body <- paste0(p$a, "i ", sign, " ", abs(p$b))
      paste0("Evaluate $", latex_sum("i", 1, p$n, paste0("(", body, ")")),
             "$ by applying linearity of summation.")
    },
    solve = function(p) {
      sum_i <- p$n * (p$n + 1L) / 2L
      result <- p$a * sum_i + p$n * p$b
      sign_b <- if (p$b > 0) "+" else "-"
      list(
        steps = c(
          paste0("Apply linearity: $", p$a, "\\sum_{i=1}^{", p$n, "} i ",
                 sign_b, " ", abs(p$b), " \\cdot ", p$n, "$."),
          paste0("Use the formula $\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$:"),
          paste0("$\\sum_{i=1}^{", p$n, "} i = \\frac{", p$n, " \\cdot ", p$n + 1L,
                 "}{2} = ", sum_i, "$."),
          paste0("Compute: $", p$a, " \\cdot ", sum_i, " ", sign_b, " ",
                 abs(p$b), " \\cdot ", p$n, " = ", p$a * sum_i, " ",
                 sign_b, " ", abs(p$b * p$n), " = ", result, "$.")
        ),
        answer_value = result
      )
    },
    format_answer = function(sol) as.character(sol$answer_value)
  ))

  # ---------------------------------------------------------------------------
  # D4: Transfer — Compute E(X) from probability table
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "sum_d4_expected_value",
    topic_id = "summation_notation",
    difficulty = 4L,
    description = "Compute expected value from a probability distribution",
    params = list(
      # Generate 4 probabilities summing to 1 with denominator 10
      p1 = function() sample(1:4, 1),
      p2 = function() sample(1:4, 1),
      p3 = function() sample(1:4, 1)
    ),
    constraint = function(p) {
      p4 <- 10L - p$p1 - p$p2 - p$p3
      p4 >= 1 && p4 <= 4
    },
    statement = function(p) {
      p4 <- 10L - p$p1 - p$p2 - p$p3
      paste0("A discrete random variable $X$ has the distribution:\n\n",
             "| $x$ | 1 | 2 | 3 | 4 |\n",
             "|---|---|---|---|---|\n",
             "| $P(X=x)$ | $", latex_frac(p$p1, 10), "$ | $",
             latex_frac(p$p2, 10), "$ | $",
             latex_frac(p$p3, 10), "$ | $",
             latex_frac(p4, 10), "$ |\n\n",
             "Compute $E(X) = \\sum_{x} x \\cdot P(X=x)$.")
    },
    solve = function(p) {
      p4 <- 10L - p$p1 - p$p2 - p$p3
      probs <- c(p$p1, p$p2, p$p3, p4)
      # E(X) = sum(x * P(x)) = (1*p1 + 2*p2 + 3*p3 + 4*p4) / 10
      num <- 1L * probs[1] + 2L * probs[2] + 3L * probs[3] + 4L * probs[4]
      result <- simplify_fraction(num, 10L)

      terms <- paste(paste0(1:4, " \\cdot ", sapply(probs, function(p) latex_frac(p, 10))), collapse = " + ")
      list(
        steps = c(
          paste0("$E(X) = ", terms, "$."),
          paste0("$= ", latex_frac(1L * probs[1], 10), " + ",
                 latex_frac(2L * probs[2], 10), " + ",
                 latex_frac(3L * probs[3], 10), " + ",
                 latex_frac(4L * probs[4], 10), "$."),
          paste0("$= ", latex_frac(num, 10), "$."),
          if (result$den != 10) paste0("Simplify: $", latex_frac(result$num, result$den), "$.") else NULL
        ),
        answer_num = result$num,
        answer_den = result$den
      )
    },
    format_answer = function(sol) latex_frac(sol$answer_num, sol$answer_den)
  ))

  # ---------------------------------------------------------------------------
  # D5: Synthesis — Show sum of deviations from mean is zero
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "sum_d5_algebraic",
    topic_id = "summation_notation",
    difficulty = 5L,
    description = "Verify sum of deviations from the mean equals zero",
    params = list(
      x1 = function() sample(1:15, 1),
      x2 = function() sample(1:15, 1),
      x3 = function() sample(1:15, 1),
      x4 = function() sample(1:15, 1)
    ),
    constraint = function(p) {
      (p$x1 + p$x2 + p$x3 + p$x4) %% 4 == 0 &&
      length(unique(c(p$x1, p$x2, p$x3, p$x4))) >= 3
    },
    statement = function(p) {
      paste0("Given the data $\\{", p$x1, ", ", p$x2, ", ", p$x3, ", ", p$x4,
             "\\}$, compute $\\bar{x}$ and verify that $",
             latex_sum("i", 1, 4, "(x_i - \\bar{x})"), " = 0$.")
    },
    solve = function(p) {
      vals <- c(p$x1, p$x2, p$x3, p$x4)
      xbar <- sum(vals) / 4L
      devs <- vals - xbar

      list(
        steps = c(
          paste0("$\\bar{x} = \\frac{", paste(vals, collapse = " + "), "}{4} = ",
                 "\\frac{", sum(vals), "}{4} = ", xbar, "$."),
          paste0("Deviations: ",
                 paste(paste0("$(", vals, " - ", xbar, ") = ", devs, "$"), collapse = ", "),
                 "."),
          paste0("Sum of deviations: $", paste(devs, collapse = " + "), " = ",
                 sum(devs), "$.")
        ),
        answer_value = 0
      )
    },
    format_answer = function(sol) "0"
  ))
}
