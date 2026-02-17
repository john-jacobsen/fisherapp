# =============================================================================
# Problem Templates — Geometric Series (5 difficulty levels)
# =============================================================================

#' Register all geometric series templates
#' @keywords internal
register_geometric_series_templates <- function() {

  # ---------------------------------------------------------------------------
  # Difficulty 1: Recognition — Identify geometric sequence and common ratio
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "geo_series_d1_identify",
    topic_id = "geometric_series",
    difficulty = 1L,
    description = "Identify a geometric sequence and find its common ratio",
    params = list(
      a     = function() sample(2:6, 1),
      r     = function() sample(c(2L, 3L, -2L), 1),
      n_terms = function() 4L
    ),
    constraint = NULL,
    statement = function(p) {
      terms <- vapply(0:(p$n_terms - 1),
                      function(i) as.integer(p$a * p$r^i), integer(1))
      terms_str <- paste(terms, collapse = ", ")
      paste0("Is the sequence $", terms_str, ", \\ldots$ geometric? ",
             "If so, what is the common ratio $r$?")
    },
    solve = function(p) {
      terms <- vapply(0:(p$n_terms - 1),
                      function(i) as.integer(p$a * p$r^i), integer(1))
      steps <- c(
        paste0("Step 1: Check if each term divided by the previous is constant:"),
        paste0("Step 2: $\\dfrac{", terms[2], "}{", terms[1], "} = ", p$r, "$, ",
               "$\\dfrac{", terms[3], "}{", terms[2], "} = ", p$r, "$, ",
               "$\\dfrac{", terms[4], "}{", terms[3], "} = ", p$r, "$."),
        "Step 3: The ratio is constant, so this is a geometric sequence.",
        paste0("Step 4: The common ratio is $r = ", p$r, "$.")
      )
      list(steps = steps, answer_value = p$r)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 2: Routine — Compute a finite geometric sum
  # S = a * (1 - r^n) / (1 - r)
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "geo_series_d2_finite_sum",
    topic_id = "geometric_series",
    difficulty = 2L,
    description = "Compute a finite geometric sum using the formula",
    params = list(
      a    = function() sample(1:4, 1),
      r    = function() sample(c(2L, 3L), 1),
      n    = function() sample(4:6, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      paste0("Compute $", latex_sum("i", 0, p$n - 1,
             paste0(p$a, " \\cdot ", p$r, "^i")), "$.")
    },
    solve = function(p) {
      r_n <- as.integer(p$r ^ p$n)
      numerator <- p$a * (r_n - 1)
      denominator <- p$r - 1
      result <- as.integer(numerator / denominator)

      # Also show expansion
      terms <- vapply(0:(p$n - 1),
                      function(i) as.integer(p$a * p$r^i), integer(1))
      expansion <- paste(terms, collapse = " + ")

      steps <- c(
        paste0("Step 1: This is a finite geometric series with $a = ", p$a,
               "$, $r = ", p$r, "$, and $n = ", p$n, "$ terms."),
        paste0("Step 2: Use the formula: $S_n = a \\cdot \\dfrac{r^n - 1}{r - 1}$."),
        paste0("Step 3: $S_{", p$n, "} = ", p$a, " \\cdot \\dfrac{",
               p$r, "^{", p$n, "} - 1}{", p$r, " - 1} = ",
               p$a, " \\cdot \\dfrac{", r_n, " - 1}{", p$r - 1,
               "} = ", p$a, " \\cdot \\dfrac{", r_n - 1, "}{",
               p$r - 1, "} = ", result, "$."),
        paste0("Step 4: Verification: $", expansion, " = ", result, "$.")
      )
      list(steps = steps, answer_value = result)
    },
    format_answer = function(sol) {
      as.character(sol$answer_value)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 3: Multi-step — Compute a tail sum (infinite series starting at k)
  # sum_{i=k}^{inf} r^i = r^k / (1-r) for |r| < 1
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "geo_series_d3_tail_sum",
    topic_id = "geometric_series",
    difficulty = 3L,
    description = "Compute an infinite geometric tail sum starting at index k",
    params = list(
      r_den = function() sample(c(2L, 3L, 4L, 5L), 1),
      k     = function() sample(2:5, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      paste0("Compute $", latex_sum("i", p$k, "\\infty",
             paste0("\\left(", latex_frac(1L, p$r_den), "\\right)^i")),
             "$. Give your answer as a simplified fraction.")
    },
    solve = function(p) {
      # sum_{i=k}^{inf} (1/r_den)^i = (1/r_den)^k / (1 - 1/r_den)
      # = 1/r_den^k / ((r_den - 1)/r_den) = 1 / (r_den^k * (r_den - 1) / r_den)
      # = r_den / (r_den^k * (r_den - 1)) = 1 / (r_den^{k-1} * (r_den - 1))
      num <- 1L
      den <- as.integer(p$r_den^(p$k - 1) * (p$r_den - 1))
      result <- simplify_fraction(num, den)

      r_str <- latex_frac(1L, p$r_den)
      rk_den <- as.integer(p$r_den^p$k)

      steps <- c(
        paste0("Step 1: This is an infinite geometric series starting at $i = ", p$k, "$."),
        paste0("Step 2: Factor out the first term: $\\left(", r_str, "\\right)^{", p$k,
               "} \\cdot ", latex_sum("j", 0, "\\infty",
               paste0("\\left(", r_str, "\\right)^j")), "$."),
        paste0("Step 3: The infinite geometric sum $", latex_sum("j", 0, "\\infty",
               paste0("\\left(", r_str, "\\right)^j")),
               " = \\dfrac{1}{1 - ", r_str, "} = \\dfrac{1}{",
               latex_frac(p$r_den - 1L, p$r_den), "} = ",
               latex_frac(p$r_den, p$r_den - 1L), "$."),
        paste0("Step 4: Multiply: $", latex_frac(1L, rk_den), " \\times ",
               latex_frac(p$r_den, p$r_den - 1L), " = ",
               latex_frac(result$num, result$den), "$.")
      )
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 4: Transfer — Geometric distribution tail probability
  # P(X >= k) = (1-p)^{k-1} for geometric RV
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "geo_series_d4_geo_dist",
    topic_id = "geometric_series",
    difficulty = 4L,
    description = "Compute a geometric distribution tail probability",
    params = list(
      p_den = function() sample(c(2L, 3L, 4L, 6L), 1),
      k     = function() sample(3:5, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      p_str <- latex_frac(1L, p$p_den)
      paste0("A player flips a coin that lands heads with probability $p = ", p_str,
             "$ until the first heads appears. Let $X$ be the number of flips. ",
             "What is the probability that the first heads occurs on or after ",
             "the $", p$k, "$th flip?\n\n",
             "Use the fact that $P(X = k) = (1-p)^{k-1}p$ and express your ",
             "answer as a simplified fraction.")
    },
    solve = function(p) {
      # P(X >= k) = sum_{i=k}^{inf} (1-p)^{i-1} * p
      # = p * (1-p)^{k-1} / (1 - (1-p)) = (1-p)^{k-1}
      q_num <- p$p_den - 1L
      q_den <- p$p_den
      # (q_num/q_den)^{k-1}
      result_num <- as.integer(q_num ^ (p$k - 1))
      result_den <- as.integer(q_den ^ (p$k - 1))
      result <- simplify_fraction(result_num, result_den)

      p_str <- latex_frac(1L, p$p_den)
      q_str <- latex_frac(q_num, q_den)

      steps <- c(
        paste0("Step 1: $P(X \\geq ", p$k, ") = ",
               latex_sum("i", p$k, "\\infty",
               paste0("(1-p)^{i-1} \\cdot p")), "$."),
        paste0("Step 2: Factor: $= p \\cdot (1-p)^{", p$k - 1, "} \\cdot ",
               latex_sum("j", 0, "\\infty", "(1-p)^j"), "$."),
        paste0("Step 3: The infinite geometric sum equals $\\dfrac{1}{1-(1-p)} = \\dfrac{1}{p}$."),
        paste0("Step 4: So $P(X \\geq ", p$k, ") = p \\cdot (1-p)^{", p$k - 1,
               "} \\cdot \\dfrac{1}{p} = (1-p)^{", p$k - 1, "}$."),
        paste0("Step 5: Substitute $p = ", p_str, "$: $\\left(", q_str, "\\right)^{",
               p$k - 1, "} = ", latex_frac(result$num, result$den), "$.")
      )
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 5: Synthesis — Verify geometric PMF sums to 1
  # sum_{k=1}^{inf} (1-p)^{k-1} * p = 1
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "geo_series_d5_verify_pmf",
    topic_id = "geometric_series",
    difficulty = 5L,
    description = "Verify that the geometric PMF sums to 1",
    params = list(
      p_num = function() sample(1:3, 1),
      p_den = function() sample(c(4L, 5L, 6L, 8L, 10L), 1)
    ),
    constraint = function(p) {
      p$p_num < p$p_den && gcd(p$p_num, p$p_den) == 1
    },
    statement = function(p) {
      p_str <- latex_frac(p$p_num, p$p_den)
      q_num <- p$p_den - p$p_num
      q_str <- latex_frac(q_num, p$p_den)
      paste0("Let $X \\sim \\text{Geometric}(p)$ with $p = ", p_str,
             "$ and PMF $P(X = k) = (1-p)^{k-1}p$ for $k = 1, 2, 3, \\ldots$\n\n",
             "Verify that $", latex_sum("k", 1, "\\infty",
             paste0("\\left(", q_str, "\\right)^{k-1} \\cdot ", p_str)),
             " = 1$.\n\n",
             "Show each step of the derivation.")
    },
    solve = function(p) {
      q_num <- p$p_den - p$p_num
      p_str <- latex_frac(p$p_num, p$p_den)
      q_str <- latex_frac(q_num, p$p_den)

      # 1 / (1 - q/p_den) = 1 / (p_num/p_den) = p_den/p_num
      inv_str <- latex_frac(p$p_den, p$p_num)

      steps <- c(
        paste0("Step 1: $", latex_sum("k", 1, "\\infty",
               paste0("\\left(", q_str, "\\right)^{k-1} \\cdot ", p_str)), "$."),
        paste0("Step 2: Factor out the constant $p = ", p_str, "$:"),
        paste0("Step 3: $= ", p_str, " \\cdot ", latex_sum("k", 1, "\\infty",
               paste0("\\left(", q_str, "\\right)^{k-1}")), "$."),
        paste0("Step 4: Substitute $j = k - 1$: $= ", p_str, " \\cdot ",
               latex_sum("j", 0, "\\infty",
               paste0("\\left(", q_str, "\\right)^j")), "$."),
        paste0("Step 5: Apply the infinite geometric series formula ($|", q_str,
               "| < 1$):"),
        paste0("Step 6: $= ", p_str, " \\cdot \\dfrac{1}{1 - ", q_str, "} = ",
               p_str, " \\cdot \\dfrac{1}{", p_str, "} = ",
               p_str, " \\cdot ", inv_str, " = 1$.")
      )
      list(steps = steps, answer_value = 1)
    },
    format_answer = function(sol) {
      "1"
    }
  ))
}
