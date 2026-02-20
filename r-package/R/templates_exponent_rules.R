# =============================================================================
# Problem Templates — Exponent Rules (5 difficulty levels)
# =============================================================================

#' Register all exponent rules templates
#' @keywords internal
register_exponent_rules_templates <- function() {

  # ---------------------------------------------------------------------------
  # Difficulty 1: Recognition — Evaluate b^n for small values
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "exp_rules_d1_evaluate",
    topic_id = "exponent_rules",
    difficulty = 1L,
    description = "Evaluate a base raised to a small exponent (0, 1, 2, or 3)",
    params = list(
      base = function() sample(2:9, 1),
      exp  = function() sample(0:3, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      if (p$exp == 0L) {
        paste0("What is $", p$base, "^{0}$?")
      } else {
        paste0("Evaluate $", latex_exp(p$base, p$exp), "$.")
      }
    },
    solve = function(p) {
      result <- as.integer(p$base ^ p$exp)
      if (p$exp == 0L) {
        steps <- c(
          "Step 1: Any nonzero number raised to the power 0 equals 1.",
          paste0("Step 2: $", p$base, "^{0} = 1$.")
        )
      } else if (p$exp == 1L) {
        steps <- c(
          "Step 1: Any number raised to the power 1 equals itself.",
          paste0("Step 2: $", p$base, "^{1} = ", result, "$.")
        )
      } else {
        expansion <- paste(rep(p$base, p$exp), collapse = " \\times ")
        steps <- c(
          paste0("Step 1: Expand: $", latex_exp(p$base, p$exp), " = ", expansion, "$."),
          paste0("Step 2: Multiply: $", expansion, " = ", result, "$.")
        )
      }
      list(steps = steps, answer_value = result)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 2: Routine — Simplify x^a * x^b or x^a / x^b (single rule)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "exp_rules_d2_single_rule",
    topic_id = "exponent_rules",
    difficulty = 2L,
    description = "Apply the product or quotient rule for exponents",
    params = list(
      a    = function() sample(2:8, 1),
      b    = function() sample(2:8, 1),
      rule = function() sample(c("product", "quotient"), 1)
    ),
    constraint = function(p) {
      # For quotient rule, ensure a > b so the exponent stays positive
      if (p$rule == "quotient") p$a > p$b else TRUE
    },
    statement = function(p) {
      if (p$rule == "product") {
        paste0("Simplify $", latex_exp("x", p$a), " \\cdot ",
               latex_exp("x", p$b), "$.")
      } else {
        paste0("Simplify $\\dfrac{", latex_exp("x", p$a), "}{",
               latex_exp("x", p$b), "}$.")
      }
    },
    solve = function(p) {
      if (p$rule == "product") {
        result <- p$a + p$b
        steps <- c(
          "Step 1: Apply the product rule: $x^a \\cdot x^b = x^{a+b}$.",
          paste0("Step 2: $", latex_exp("x", p$a), " \\cdot ", latex_exp("x", p$b),
                 " = x^{", p$a, "+", p$b, "} = ", latex_exp("x", result), "$.")
        )
      } else {
        result <- p$a - p$b
        steps <- c(
          "Step 1: Apply the quotient rule: $\\dfrac{x^a}{x^b} = x^{a-b}$.",
          paste0("Step 2: $\\dfrac{", latex_exp("x", p$a), "}{", latex_exp("x", p$b),
                 "} = x^{", p$a, "-", p$b, "} = ", latex_exp("x", result), "$.")
        )
      }
      list(steps = steps, answer_value = result,
           answer_expr = paste0("x^{", result, "}"))
    },
    format_answer = function(sol) {
      paste0("x^{", sol$answer_value, "}")
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 3: Multi-step — Simplify (c * x^a)^b / (d * x^e)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "exp_rules_d3_multi_rule",
    topic_id = "exponent_rules",
    difficulty = 3L,
    description = "Apply power rule to numerator then quotient rule",
    params = list(
      c_val = function() sample(2:5, 1),
      a     = function() sample(2:5, 1),
      b     = function() sample(2:3, 1),
      d_val = function() sample(2:6, 1),
      e     = function() sample(1:4, 1)
    ),
    constraint = function(p) {
      # Ensure the final exponent on x is positive
      (p$a * p$b) > p$e
    },
    statement = function(p) {
      paste0("Simplify $\\dfrac{(", p$c_val, latex_exp("x", p$a),
             ")^{", p$b, "}}{", p$d_val, latex_exp("x", p$e), "}$.")
    },
    solve = function(p) {
      # Step 1: Power rule on numerator: (c * x^a)^b = c^b * x^{a*b}
      coeff_num_raw <- as.integer(p$c_val ^ p$b)
      exp_num <- p$a * p$b

      # Step 2: Form fraction of coefficients and apply quotient rule on x
      coeff <- simplify_fraction(coeff_num_raw, p$d_val)
      exp_result <- exp_num - p$e

      steps <- c(
        paste0("Step 1: Apply the power rule to the numerator: ",
               "$(", p$c_val, latex_exp("x", p$a), ")^{", p$b, "} = ",
               coeff_num_raw, latex_exp("x", exp_num), "$."),
        paste0("Step 2: Divide the coefficients: $\\dfrac{", coeff_num_raw, "}{",
               p$d_val, "} = ", latex_frac(coeff$num, coeff$den), "$."),
        paste0("Step 3: Apply the quotient rule for $x$: $x^{", exp_num, " - ",
               p$e, "} = ", latex_exp("x", exp_result), "$."),
        paste0("Step 4: Result: $", latex_frac(coeff$num, coeff$den),
               latex_exp("x", exp_result), "$.")
      )
      coeff_str <- if (coeff$den == 1L) as.character(coeff$num) else
                     paste0(coeff$num, "/", coeff$den)
      list(
        steps = steps,
        coeff_num = coeff$num,
        coeff_den = coeff$den,
        exp_result = exp_result,
        answer_expr = paste0(coeff_str, "x^{", exp_result, "}")
      )
    },
    format_answer = function(sol) {
      coeff_str <- latex_frac(sol$coeff_num, sol$coeff_den)
      paste0(coeff_str, latex_exp("x", sol$exp_result))
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 4: Transfer — Population doubling problem
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "exp_rules_d4_applied",
    topic_id = "exponent_rules",
    difficulty = 4L,
    description = "Population doubling word problem using exponent rules",
    params = list(
      t_double = function() sample(2:5, 1),
      multiplier = function() sample(2:5, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      T_years <- p$t_double * p$multiplier
      paste0("A bacterial population in a Berkeley biology lab starts at $P_0$ ",
             "cells and doubles every ", p$t_double, " hours. ",
             "Write a simplified expression for the population after ",
             T_years, " hours. ",
             "Express your answer in the form $P_0 \\cdot 2^k$ and give the ",
             "value of $k$.")
    },
    solve = function(p) {
      T_years <- p$t_double * p$multiplier
      k <- as.integer(T_years / p$t_double)

      steps <- c(
        paste0("Step 1: The population doubles every ", p$t_double, " hours, so after ",
               "$T$ hours the number of doublings is $\\dfrac{T}{",
               p$t_double, "}$."),
        paste0("Step 2: After ", T_years, " hours: $\\dfrac{", T_years, "}{",
               p$t_double, "} = ", k, "$ doublings."),
        paste0("Step 3: The population is $P_0 \\cdot 2^{", k, "}$.")
      )
      list(steps = steps, answer_value = k)
    },
    format_answer = function(sol) {
      paste0("P_0 \\cdot 2^{", sol$answer_value, "}")
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 5: Synthesis — Compute C(n,k) * p^k * (1-p)^(n-k)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "exp_rules_d5_binomial_term",
    topic_id = "exponent_rules",
    difficulty = 5L,
    description = "Evaluate a binomial probability term using exponent rules",
    params = list(
      n    = function() sample(4:8, 1),
      k    = function() sample(1:3, 1),
      p_den = function() sample(c(2L, 3L, 4L), 1)
    ),
    constraint = function(p) {
      p$k < p$n && p$k >= 1
    },
    statement = function(p) {
      p_str <- latex_frac(1L, p$p_den)
      q_num <- p$p_den - 1L
      q_str <- latex_frac(q_num, p$p_den)
      paste0("In a Stat 134 problem, compute the binomial probability term:\n\n",
             "$$\\binom{", p$n, "}{", p$k, "} \\left(", p_str,
             "\\right)^{", p$k, "} \\left(", q_str,
             "\\right)^{", p$n - p$k, "}$$\n\n",
             "Give your answer as a simplified fraction.")
    },
    solve = function(p) {
      C_nk <- choose_safe(p$n, p$k)

      # p^k = (1/p_den)^k = 1 / p_den^k
      pk_num <- 1L
      pk_den <- as.integer(p$p_den ^ p$k)

      # (1-p)^(n-k) = ((p_den-1)/p_den)^(n-k)
      q_num_base <- p$p_den - 1L
      nk <- p$n - p$k
      qnk_num <- as.integer(q_num_base ^ nk)
      qnk_den <- as.integer(p$p_den ^ nk)

      # Multiply all together: C(n,k) * (pk_num/pk_den) * (qnk_num/qnk_den)
      # = C(n,k) * qnk_num / (pk_den * qnk_den)
      # Note: pk_den * qnk_den = p_den^k * p_den^(n-k) = p_den^n
      total_num <- as.integer(C_nk) * pk_num * qnk_num
      total_den <- pk_den * qnk_den
      result <- simplify_fraction(total_num, total_den)

      p_str <- latex_frac(1L, p$p_den)
      q_str <- latex_frac(q_num_base, p$p_den)

      steps <- c(
        paste0("Step 1: Compute $\\binom{", p$n, "}{", p$k, "} = ", C_nk, "$."),
        paste0("Step 2: Compute $\\left(", p_str, "\\right)^{", p$k, "} = ",
               latex_frac(pk_num, pk_den), "$."),
        paste0("Step 3: Compute $\\left(", q_str, "\\right)^{", nk, "} = ",
               latex_frac(qnk_num, qnk_den), "$."),
        paste0("Step 4: Multiply: $", C_nk, " \\times ", latex_frac(pk_num, pk_den),
               " \\times ", latex_frac(qnk_num, qnk_den), " = ",
               latex_frac(total_num, total_den), "$."),
        paste0("Step 5: Simplify: $", latex_frac(result$num, result$den), "$.")
      )
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))
}
