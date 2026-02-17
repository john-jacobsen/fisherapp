# =============================================================================
# Problem Templates — Solving Equations (5 difficulty levels)
# =============================================================================

#' Register all solving equations templates
#' @keywords internal
register_solving_equations_templates <- function() {

  # ---------------------------------------------------------------------------
  # Difficulty 1: Recognition — Identify operation to isolate variable
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "solve_eq_d1_identify",
    topic_id = "solving_equations",
    difficulty = 1L,
    description = "Identify the operation needed to isolate x in a one-step equation",
    params = list(
      op   = function() sample(c("add", "sub", "mul", "div"), 1),
      a    = function() sample(2:12, 1),
      ans  = function() sample(2:15, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      eq <- switch(p$op,
        add = paste0("$x + ", p$a, " = ", p$ans + p$a, "$"),
        sub = paste0("$x - ", p$a, " = ", p$ans - p$a, "$"),
        mul = paste0("$", p$a, "x = ", p$a * p$ans, "$"),
        div = paste0("$\\dfrac{x}{", p$a, "} = ", p$ans, "$")
      )
      paste0("What operation isolates $x$ in: ", eq, "?\n\n",
             "(a) Add ", p$a, " to both sides\n",
             "(b) Subtract ", p$a, " from both sides\n",
             "(c) Multiply both sides by ", p$a, "\n",
             "(d) Divide both sides by ", p$a)
    },
    solve = function(p) {
      correct <- switch(p$op,
        add = "(b)",
        sub = "(a)",
        mul = "(d)",
        div = "(c)"
      )
      explanation <- switch(p$op,
        add = paste0("Since ", p$a, " is added to $x$, subtract ", p$a,
                     " from both sides to isolate $x$."),
        sub = paste0("Since ", p$a, " is subtracted from $x$, add ", p$a,
                     " to both sides to isolate $x$."),
        mul = paste0("Since $x$ is multiplied by ", p$a, ", divide both sides by ",
                     p$a, " to isolate $x$."),
        div = paste0("Since $x$ is divided by ", p$a, ", multiply both sides by ",
                     p$a, " to isolate $x$.")
      )
      steps <- c(
        "Step 1: To isolate $x$, apply the inverse operation.",
        paste0("Step 2: ", explanation),
        paste0("Step 3: The answer is ", correct, ".")
      )
      list(steps = steps, answer_value = p$ans)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 2: Routine — Solve ax + b = c
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "solve_eq_d2_linear",
    topic_id = "solving_equations",
    difficulty = 2L,
    description = "Solve a straightforward multi-step linear equation",
    params = list(
      a = function() sample(2:9, 1),
      b = function() sample(c(-9:-2, 2:9), 1),
      x = function() sample(-8:8, 1)
    ),
    constraint = function(p) {
      p$x != 0
    },
    statement = function(p) {
      rhs <- p$a * p$x + p$b
      b_str <- if (p$b > 0) paste0(" + ", p$b) else paste0(" - ", abs(p$b))
      paste0("Solve for $x$: $", p$a, "x", b_str, " = ", rhs, "$.")
    },
    solve = function(p) {
      rhs <- p$a * p$x + p$b
      b_str <- if (p$b > 0) paste0(" + ", p$b) else paste0(" - ", abs(p$b))
      after_sub <- rhs - p$b
      sub_op <- if (p$b > 0) {
        paste0("Subtract ", p$b, " from both sides")
      } else {
        paste0("Add ", abs(p$b), " to both sides")
      }

      steps <- c(
        paste0("Step 1: ", sub_op, ": $", p$a, "x = ", after_sub, "$."),
        paste0("Step 2: Divide both sides by ", p$a, ": $x = ",
               latex_frac(after_sub, p$a), "$."),
        paste0("Step 3: $x = ", p$x, "$.")
      )
      list(steps = steps, answer_value = p$x)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 3: Multi-step — Solve equation with fractions
  # (a*x + b) / c = d, clearing fractions
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "solve_eq_d3_fractions",
    topic_id = "solving_equations",
    difficulty = 3L,
    description = "Solve an equation requiring clearing fractions",
    params = list(
      a = function() sample(2:5, 1),
      b = function() sample(c(-6:-1, 1:6), 1),
      c_val = function() sample(2:6, 1),
      x = function() sample(-5:5, 1)
    ),
    constraint = function(p) {
      p$x != 0 &&
      # Ensure rhs is an integer for clean problems
      (p$a * p$x + p$b) %% p$c_val == 0
    },
    statement = function(p) {
      rhs <- (p$a * p$x + p$b) / p$c_val
      b_str <- if (p$b > 0) paste0(" + ", p$b) else paste0(" - ", abs(p$b))
      paste0("Solve for $x$: $\\dfrac{", p$a, "x", b_str, "}{", p$c_val,
             "} = ", rhs, "$.")
    },
    solve = function(p) {
      rhs <- (p$a * p$x + p$b) / p$c_val
      b_str <- if (p$b > 0) paste0(" + ", p$b) else paste0(" - ", abs(p$b))
      cleared <- rhs * p$c_val

      sub_op <- if (p$b > 0) {
        paste0("Subtract ", p$b, " from both sides")
      } else {
        paste0("Add ", abs(p$b), " to both sides")
      }
      after_sub <- cleared - p$b

      steps <- c(
        paste0("Step 1: Multiply both sides by ", p$c_val, ": $", p$a, "x", b_str,
               " = ", cleared, "$."),
        paste0("Step 2: ", sub_op, ": $", p$a, "x = ", after_sub, "$."),
        paste0("Step 3: Divide both sides by ", p$a, ": $x = ",
               latex_frac(after_sub, p$a), "$."),
        paste0("Step 4: $x = ", p$x, "$.")
      )
      list(steps = steps, answer_value = p$x)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 4: Transfer — Rearrange a statistics formula
  # z = (x - mu) / sigma, solve for x (or mu, or sigma)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "solve_eq_d4_zscore",
    topic_id = "solving_equations",
    difficulty = 4L,
    description = "Rearrange the z-score formula to solve for a specified variable",
    params = list(
      target = function() sample(c("x", "mu", "sigma"), 1),
      z_val  = function() sample(c(-3:-1, 1:3), 1),
      mu     = function() sample(seq(10, 100, by = 10), 1),
      sigma  = function() sample(c(2, 5, 10, 15, 20), 1)
    ),
    constraint = NULL,
    statement = function(p) {
      x_val <- p$mu + p$z_val * p$sigma
      base <- "The z-score formula is $z = \\dfrac{x - \\mu}{\\sigma}$."

      if (p$target == "x") {
        paste0(base, " Given $z = ", p$z_val, "$, $\\mu = ", p$mu,
               "$, and $\\sigma = ", p$sigma, "$, solve for $x$.")
      } else if (p$target == "mu") {
        paste0(base, " Given $z = ", p$z_val, "$, $x = ", x_val,
               "$, and $\\sigma = ", p$sigma, "$, solve for $\\mu$.")
      } else {
        paste0(base, " Given $z = ", p$z_val, "$, $x = ", x_val,
               "$, and $\\mu = ", p$mu, "$, solve for $\\sigma$.")
      }
    },
    solve = function(p) {
      x_val <- p$mu + p$z_val * p$sigma

      if (p$target == "x") {
        steps <- c(
          "Step 1: Start with $z = \\dfrac{x - \\mu}{\\sigma}$.",
          "Step 2: Multiply both sides by $\\sigma$: $z\\sigma = x - \\mu$.",
          "Step 3: Add $\\mu$ to both sides: $x = \\mu + z\\sigma$.",
          paste0("Step 4: Substitute: $x = ", p$mu, " + (", p$z_val, ")(", p$sigma,
                 ") = ", p$mu, " + ", p$z_val * p$sigma, " = ", x_val, "$.")
        )
        list(steps = steps, answer_value = x_val)
      } else if (p$target == "mu") {
        steps <- c(
          "Step 1: Start with $z = \\dfrac{x - \\mu}{\\sigma}$.",
          "Step 2: Multiply both sides by $\\sigma$: $z\\sigma = x - \\mu$.",
          "Step 3: Rearrange: $\\mu = x - z\\sigma$.",
          paste0("Step 4: Substitute: $\\mu = ", x_val, " - (", p$z_val, ")(", p$sigma,
                 ") = ", x_val, " - ", p$z_val * p$sigma, " = ", p$mu, "$.")
        )
        list(steps = steps, answer_value = p$mu)
      } else {
        steps <- c(
          "Step 1: Start with $z = \\dfrac{x - \\mu}{\\sigma}$.",
          "Step 2: Multiply both sides by $\\sigma$: $z\\sigma = x - \\mu$.",
          "Step 3: Divide both sides by $z$: $\\sigma = \\dfrac{x - \\mu}{z}$.",
          paste0("Step 4: Substitute: $\\sigma = \\dfrac{", x_val, " - ", p$mu, "}{",
                 p$z_val, "} = \\dfrac{", x_val - p$mu, "}{", p$z_val,
                 "} = ", p$sigma, "$.")
        )
        list(steps = steps, answer_value = p$sigma)
      }
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 5: Synthesis — Find standardizing constants a, b
  # E(aX + b) = a*E(X) + b = 0 and Var(aX + b) = a^2*Var(X) = 1
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "solve_eq_d5_standardize",
    topic_id = "solving_equations",
    difficulty = 5L,
    description = "Find constants to standardize a random variable",
    params = list(
      mu_num = function() sample(c(-8:-1, 1:8), 1),
      mu_den = function() sample(1:4, 1),
      var_num = function() sample(c(1, 4, 9, 16, 25), 1)
    ),
    constraint = function(p) {
      gcd(abs(p$mu_num), p$mu_den) == 1
    },
    statement = function(p) {
      mu_str <- if (p$mu_den == 1) as.character(p$mu_num) else {
        latex_frac(p$mu_num, p$mu_den)
      }
      paste0("A random variable $X$ has $E(X) = ", mu_str, "$ and ",
             "$\\text{Var}(X) = ", p$var_num, "$. ",
             "Using the rules $E(aX + b) = aE(X) + b$ and ",
             "$\\text{Var}(aX + b) = a^2\\text{Var}(X)$, find constants ",
             "$a > 0$ and $b$ such that $Y = aX + b$ has $E(Y) = 0$ and ",
             "$\\text{Var}(Y) = 1$.")
    },
    solve = function(p) {
      # a^2 * Var(X) = 1 => a = 1/sqrt(Var(X))
      sd_val <- sqrt(p$var_num)
      # Since var_num is a perfect square, sd_val is an integer
      sd_int <- as.integer(sd_val)

      # a = 1/sd_int
      a_num <- 1L
      a_den <- sd_int

      # b = -a * mu = -(1/sd_int) * (mu_num/mu_den) = -mu_num / (sd_int * mu_den)
      b_num_raw <- -p$mu_num
      b_den_raw <- sd_int * p$mu_den
      b_frac <- simplify_fraction(b_num_raw, b_den_raw)

      mu_str <- if (p$mu_den == 1) as.character(p$mu_num) else {
        latex_frac(p$mu_num, p$mu_den)
      }

      a_str <- latex_frac(a_num, a_den)
      b_str <- latex_frac(b_frac$num, b_frac$den)

      steps <- c(
        paste0("Step 1: From $\\text{Var}(aX + b) = a^2 \\text{Var}(X) = 1$:"),
        paste0("Step 2: $a^2 \\cdot ", p$var_num, " = 1 \\Rightarrow a^2 = ",
               latex_frac(1L, p$var_num),
               " \\Rightarrow a = ", a_str, "$ (taking $a > 0$)."),
        paste0("Step 3: From $E(aX + b) = aE(X) + b = 0$:"),
        paste0("Step 4: $b = -aE(X) = -", a_str, " \\cdot ", mu_str, " = ", b_str, "$."),
        paste0("Step 5: Therefore $a = ", a_str, "$ and $b = ", b_str, "$.")
      )
      list(
        steps = steps,
        a_num = a_num, a_den = a_den,
        b_num = b_frac$num, b_den = b_frac$den,
        # For answer checking, use a as the primary answer
        answer_num = a_num, answer_den = a_den
      )
    },
    format_answer = function(sol) {
      paste0("a = ", latex_frac(sol$a_num, sol$a_den),
             ", \\; b = ", latex_frac(sol$b_num, sol$b_den))
    }
  ))
}
