# =============================================================================
# Problem Templates — Combinatorics (5 difficulty levels)
# =============================================================================

#' Register all combinatorics templates
#' @keywords internal
register_combinatorics_templates <- function() {

  # ---------------------------------------------------------------------------
  # Difficulty 1: Recognition — Evaluate factorial; perm vs. combo
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "combo_d1_factorial",
    topic_id = "combinatorics",
    difficulty = 1L,
    description = "Evaluate a factorial and identify permutation vs. combination",
    params = list(
      n = function() sample(4:8, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      paste0("Compute $", p$n, "!$ .\n\n",
             "Also: A club of ", p$n + 5, " people elects a president, ",
             "vice president, and secretary. Is this a permutation or ",
             "combination problem?")
    },
    solve = function(p) {
      fact <- factorial_safe(p$n)
      expansion <- paste(seq(p$n, 1), collapse = " \\times ")

      steps <- c(
        paste0("Step 1: $", p$n, "! = ", expansion, " = ", fact, "$."),
        "Step 2: Since the officers have distinct roles (president, vice president, secretary), order matters.",
        "Step 3: This is a permutation problem."
      )
      list(steps = steps, answer_value = fact)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 2: Routine — Compute C(n, k)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "combo_d2_choose",
    topic_id = "combinatorics",
    difficulty = 2L,
    description = "Compute a single combination C(n, k)",
    params = list(
      n = function() sample(5:12, 1),
      k = function() sample(2:4, 1)
    ),
    constraint = function(p) {
      p$k < p$n
    },
    statement = function(p) {
      paste0("Compute $\\binom{", p$n, "}{", p$k, "}$.")
    },
    solve = function(p) {
      result <- choose_safe(p$n, p$k)

      # Show the factorial formula and cancellation
      num_terms <- paste(seq(p$n, p$n - p$k + 1), collapse = " \\times ")
      den_terms <- paste(seq(p$k, 1), collapse = " \\times ")
      k_fact <- factorial_safe(p$k)

      steps <- c(
        paste0("Step 1: $\\binom{", p$n, "}{", p$k, "} = \\dfrac{", p$n, "!}{",
               p$k, "!(", p$n, " - ", p$k, ")!}$."),
        paste0("Step 2: $= \\dfrac{", num_terms, "}{", den_terms, "}",
               " = \\dfrac{", prod(seq(p$n, p$n - p$k + 1)), "}{", k_fact, "}",
               " = ", result, "$.")
      )
      list(steps = steps, answer_value = result)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 3: Multi-step — Simplify C(n,2) and apply to handshake problem
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "combo_d3_handshake",
    topic_id = "combinatorics",
    difficulty = 3L,
    description = "Count handshakes in a room using combinations",
    params = list(
      n = function() sample(6:15, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      paste0("In a room of ", p$n, " people, everyone shakes hands with ",
             "everyone else exactly once. How many handshakes occur?\n\n",
             "Express your solution using the combination formula, then compute.")
    },
    solve = function(p) {
      result <- choose_safe(p$n, 2)

      steps <- c(
        "Step 1: Each handshake involves choosing 2 people from the group.",
        "Step 2: Order does not matter (A shaking B's hand = B shaking A's hand).",
        paste0("Step 3: Number of handshakes $= \\binom{", p$n, "}{2} = ",
               "\\dfrac{", p$n, " \\times ", p$n - 1, "}{2} = ",
               "\\dfrac{", p$n * (p$n - 1), "}{2} = ", result, "$.")
      )
      list(steps = steps, answer_value = result)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 4: Transfer — Hypergeometric probability (jury selection)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "combo_d4_hypergeometric",
    topic_id = "combinatorics",
    difficulty = 4L,
    description = "Compute a hypergeometric probability using combinations",
    params = list(
      men   = function() sample(8:15, 1),
      women = function() sample(8:15, 1),
      panel = function() sample(5:8, 1),
      target_women = function() sample(2:4, 1)
    ),
    constraint = function(p) {
      p$target_women <= p$women &&
      p$target_women <= p$panel &&
      (p$panel - p$target_women) <= p$men &&
      (p$men + p$women) >= p$panel
    },
    statement = function(p) {
      total <- p$men + p$women
      paste0("A committee of ", p$panel, " is selected at random from a group of ",
             p$men, " men and ", p$women, " women. What is the probability that ",
             "the committee contains exactly ", p$target_women, " women? ",
             "Give your answer as a simplified fraction.")
    },
    solve = function(p) {
      total <- p$men + p$women
      target_men <- p$panel - p$target_women

      c_women <- choose_safe(p$women, p$target_women)
      c_men <- choose_safe(p$men, target_men)
      c_total <- choose_safe(total, p$panel)

      num <- c_women * c_men
      result <- simplify_fraction(num, c_total)

      steps <- c(
        paste0("Step 1: Ways to choose ", p$target_women, " women from ", p$women,
               ": $\\binom{", p$women, "}{", p$target_women, "} = ", c_women, "$."),
        paste0("Step 2: Ways to choose ", target_men, " men from ", p$men,
               ": $\\binom{", p$men, "}{", target_men, "} = ", c_men, "$."),
        paste0("Step 3: Total ways to choose ", p$panel, " from ", total,
               ": $\\binom{", total, "}{", p$panel, "} = ", c_total, "$."),
        paste0("Step 4: $P = \\dfrac{", c_women, " \\times ", c_men, "}{", c_total,
               "} = \\dfrac{", num, "}{", c_total, "}$."),
        paste0("Step 5: Simplify: $", latex_frac(result$num, result$den), "$.")
      )
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 5: Synthesis — Compute binomial PMF P(X = k)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "combo_d5_binomial_pmf",
    topic_id = "combinatorics",
    difficulty = 5L,
    description = "Compute P(X = k) for X ~ Binomial(n, p) using combinatorics",
    params = list(
      n     = function() sample(5:10, 1),
      k     = function() sample(2:4, 1),
      p_num = function() sample(1:3, 1),
      p_den = function() sample(c(4L, 5L, 10L), 1)
    ),
    constraint = function(p) {
      p$k <= p$n && p$p_num < p$p_den &&
      gcd(p$p_num, p$p_den) == 1
    },
    statement = function(p) {
      p_str <- latex_frac(p$p_num, p$p_den)
      paste0("Let $X \\sim \\text{Binomial}(", p$n, ", ", p_str, ")$. ",
             "Compute $P(X = ", p$k, ")$ using the formula\n\n",
             "$$P(X = k) = \\binom{n}{k} p^k (1-p)^{n-k}$$\n\n",
             "Give your answer as a simplified fraction.")
    },
    solve = function(p) {
      C_nk <- choose_safe(p$n, p$k)
      nk <- p$n - p$k
      q_num <- p$p_den - p$p_num
      q_den <- p$p_den

      # p^k
      pk_num <- as.integer(p$p_num ^ p$k)
      pk_den <- as.integer(p$p_den ^ p$k)

      # (1-p)^(n-k)
      qnk_num <- as.integer(q_num ^ nk)
      qnk_den <- as.integer(q_den ^ nk)

      # C(n,k) * p^k * (1-p)^(n-k)
      total_num <- as.integer(C_nk) * pk_num * qnk_num
      total_den <- pk_den * qnk_den
      result <- simplify_fraction(total_num, total_den)

      p_str <- latex_frac(p$p_num, p$p_den)
      q_str <- latex_frac(q_num, q_den)

      steps <- c(
        paste0("Step 1: $\\binom{", p$n, "}{", p$k, "} = ", C_nk, "$."),
        paste0("Step 2: $p^k = \\left(", p_str, "\\right)^{", p$k, "} = ",
               latex_frac(pk_num, pk_den), "$."),
        paste0("Step 3: $(1-p)^{n-k} = \\left(", q_str, "\\right)^{", nk, "} = ",
               latex_frac(qnk_num, qnk_den), "$."),
        paste0("Step 4: $P(X = ", p$k, ") = ", C_nk, " \\times ",
               latex_frac(pk_num, pk_den), " \\times ",
               latex_frac(qnk_num, qnk_den), " = ",
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
