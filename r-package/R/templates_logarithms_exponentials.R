# =============================================================================
# Problem Templates — Logarithms and Exponentials (5 difficulty levels)
# =============================================================================

#' Register all logarithms and exponentials templates
#' @keywords internal
register_logarithms_exponentials_templates <- function() {

  # ---------------------------------------------------------------------------
  # Difficulty 1: Recognition — Convert between exponential and log form
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "log_exp_d1_convert",
    topic_id = "logarithms_exponentials",
    difficulty = 1L,
    description = "Convert between exponential and logarithmic form",
    params = list(
      base = function() sample(c(2L, 3L, 5L, 10L), 1),
      exp  = function() sample(2:4, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      result <- as.integer(p$base ^ p$exp)
      paste0("Rewrite $", p$base, "^{", p$exp, "} = ", result,
             "$ in logarithmic form.")
    },
    solve = function(p) {
      result <- as.integer(p$base ^ p$exp)
      steps <- c(
        "Step 1: The relationship $b^n = x$ is equivalent to $\\log_b(x) = n$.",
        paste0("Step 2: Here $b = ", p$base, "$, $n = ", p$exp, "$, $x = ", result, "$."),
        paste0("Step 3: Therefore: $\\log_{", p$base, "}(", result, ") = ", p$exp, "$.")
      )
      list(steps = steps, answer_value = p$exp)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 2: Routine — Apply a single log rule
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "log_exp_d2_simplify",
    topic_id = "logarithms_exponentials",
    difficulty = 2L,
    description = "Simplify an expression using a single log rule",
    params = list(
      rule = function() sample(c("ln_e", "log_power", "e_ln"), 1),
      n    = function() sample(2:8, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      switch(p$rule,
        ln_e = paste0("Simplify $\\ln(e^{", p$n, "})$."),
        log_power = paste0("Simplify $\\log_{2}(2^{", p$n, "})$."),
        e_ln = paste0("Simplify $e^{\\ln ", p$n, "}$.")
      )
    },
    solve = function(p) {
      switch(p$rule,
        ln_e = {
          steps <- c(
            "Step 1: $\\ln$ and $e^x$ are inverse functions: $\\ln(e^a) = a$.",
            paste0("Step 2: $\\ln(e^{", p$n, "}) = ", p$n, "$.")
          )
          list(steps = steps, answer_value = p$n)
        },
        log_power = {
          steps <- c(
            "Step 1: $\\log_b(b^a) = a$ since logarithm and exponentiation are inverses.",
            paste0("Step 2: $\\log_{2}(2^{", p$n, "}) = ", p$n, "$.")
          )
          list(steps = steps, answer_value = p$n)
        },
        e_ln = {
          steps <- c(
            "Step 1: $e^{\\ln a} = a$ since $e^x$ and $\\ln$ are inverses.",
            paste0("Step 2: $e^{\\ln ", p$n, "} = ", p$n, "$.")
          )
          list(steps = steps, answer_value = p$n)
        }
      )
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 3: Multi-step — Solve exponential equation using logs
  # a^(bx + c) = a^d => bx + c = d => x = (d - c)/b
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "log_exp_d3_solve_exp",
    topic_id = "logarithms_exponentials",
    difficulty = 3L,
    description = "Solve an exponential equation using logarithms",
    params = list(
      base = function() sample(c(2L, 3L, 5L), 1),
      b    = function() sample(2:4, 1),
      c_val = function() sample(c(-3:-1, 1:3), 1),
      x    = function() sample(1:5, 1)
    ),
    constraint = function(p) {
      rhs_exp <- p$b * p$x + p$c_val
      rhs_exp >= 1 && rhs_exp <= 6
    },
    statement = function(p) {
      rhs_exp <- p$b * p$x + p$c_val
      rhs <- as.integer(p$base ^ rhs_exp)
      c_str <- if (p$c_val > 0) paste0(" + ", p$c_val) else paste0(" - ", abs(p$c_val))
      paste0("Solve for $x$: $", p$base, "^{", p$b, "x", c_str, "} = ", rhs, "$.")
    },
    solve = function(p) {
      rhs_exp <- p$b * p$x + p$c_val
      rhs <- as.integer(p$base ^ rhs_exp)
      c_str <- if (p$c_val > 0) paste0(" + ", p$c_val) else paste0(" - ", abs(p$c_val))

      steps <- c(
        paste0("Step 1: Rewrite the right side as a power of ", p$base, ": $",
               rhs, " = ", p$base, "^{", rhs_exp, "}$."),
        paste0("Step 2: Since the bases are equal, set exponents equal: $",
               p$b, "x", c_str, " = ", rhs_exp, "$."),
        paste0("Step 3: Solve for $x$: $", p$b, "x = ", rhs_exp - p$c_val, "$."),
        paste0("Step 4: $x = ", latex_frac(rhs_exp - p$c_val, p$b), " = ", p$x, "$.")
      )
      list(steps = steps, answer_value = p$x)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 4: Transfer — Half-life / exponential decay problem
  # N(t) = N0 * e^{-kt}, solve for t when N(t) = N0/2
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "log_exp_d4_halflife",
    topic_id = "logarithms_exponentials",
    difficulty = 4L,
    description = "Solve an exponential decay half-life problem",
    params = list(
      k_num = function() sample(c(1L, 2L, 3L, 5L), 1),
      k_den = function() sample(c(10L, 100L), 1)
    ),
    constraint = function(p) {
      gcd(p$k_num, p$k_den) == 1
    },
    statement = function(p) {
      k_str <- latex_frac(p$k_num, p$k_den)
      paste0("A radioactive substance decays according to $N(t) = N_0 e^{-",
             k_str, " t}$, where $t$ is in years. ",
             "How many years until half the original amount remains? ",
             "Express your answer in terms of $\\ln 2$.")
    },
    solve = function(p) {
      k_str <- latex_frac(p$k_num, p$k_den)
      # N0/2 = N0 * e^{-kt} => 1/2 = e^{-kt} => ln(1/2) = -kt
      # => -ln(2) = -kt => t = ln(2)/k = ln(2) * k_den / k_num
      coeff <- simplify_fraction(p$k_den, p$k_num)

      steps <- c(
        paste0("Step 1: Set $N(t) = \\dfrac{N_0}{2}$: $\\dfrac{N_0}{2} = N_0 e^{-",
               k_str, " t}$."),
        paste0("Step 2: Divide by $N_0$: $\\dfrac{1}{2} = e^{-", k_str, " t}$."),
        paste0("Step 3: Take $\\ln$ of both sides: $\\ln\\left(\\dfrac{1}{2}\\right) = -",
               k_str, " t$."),
        paste0("Step 4: Since $\\ln(1/2) = -\\ln 2$: $-\\ln 2 = -", k_str, " t$."),
        paste0("Step 5: Solve: $t = \\dfrac{\\ln 2}{", k_str, "} = ",
               latex_frac(coeff$num, coeff$den), " \\ln 2$ years.")
      )
      # Answer is (k_den/k_num) * ln(2)
      list(
        steps = steps,
        answer_num = coeff$num,
        answer_den = coeff$den,
        # Store numeric value for answer checking
        answer_value = (coeff$num / coeff$den) * log(2)
      )
    },
    format_answer = function(sol) {
      paste0(latex_frac(sol$answer_num, sol$answer_den), " \\ln 2")
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 5: Synthesis — Log-likelihood, differentiate, solve for MLE
  # L(p) = p^k * (1-p)^(n-k), find MLE p-hat = k/n
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "log_exp_d5_mle",
    topic_id = "logarithms_exponentials",
    difficulty = 5L,
    description = "Derive the MLE from a binomial log-likelihood",
    params = list(
      n = function() sample(5:12, 1),
      k = function() sample(1:4, 1)
    ),
    constraint = function(p) {
      p$k < p$n && p$k >= 1
    },
    statement = function(p) {
      paste0("Given a likelihood function $L(p) = p^{", p$k,
             "}(1-p)^{", p$n - p$k, "}$ for $0 < p < 1$:\n\n",
             "(a) Write the log-likelihood $\\ell(p) = \\ln L(p)$.\n\n",
             "(b) Find $\\dfrac{d\\ell}{dp}$, set it equal to zero, ",
             "and solve for $\\hat{p}$.\n\n",
             "Give $\\hat{p}$ as a simplified fraction.")
    },
    solve = function(p) {
      nk <- p$n - p$k
      result <- simplify_fraction(p$k, p$n)

      steps <- c(
        paste0("Step 1: (a) $\\ell(p) = \\ln L(p) = ", p$k, "\\ln p + ", nk,
               "\\ln(1 - p)$."),
        paste0("Step 2: (b) Differentiate: $\\dfrac{d\\ell}{dp} = \\dfrac{", p$k,
               "}{p} - \\dfrac{", nk, "}{1 - p}$."),
        paste0("Step 3: Set equal to zero: $\\dfrac{", p$k, "}{p} = \\dfrac{", nk,
               "}{1 - p}$."),
        paste0("Step 4: Cross-multiply: $", p$k, "(1 - p) = ", nk, "p$."),
        paste0("Step 5: Expand: $", p$k, " - ", p$k, "p = ", nk, "p$."),
        paste0("Step 6: Combine: $", p$k, " = ", p$k, "p + ", nk, "p = ",
               p$n, "p$."),
        paste0("Step 7: Solve: $\\hat{p} = ", latex_frac(result$num, result$den), "$.")
      )
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))
}
