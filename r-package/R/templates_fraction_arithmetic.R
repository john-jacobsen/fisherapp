# =============================================================================
# Problem Templates — Fraction Arithmetic (8 topics, 5 difficulty levels)
# =============================================================================

#' Register all fraction arithmetic templates
#' @keywords internal
register_fraction_arithmetic_templates <- function() {

  # ---------------------------------------------------------------------------
  # Difficulty 1: Recognition — Identify equivalent fractions
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "frac_arith_d1_equiv",
    topic_id = "fraction_arithmetic",
    difficulty = 1L,
    description = "Identify the fraction equivalent to a given fraction",
    params = list(
      num        = function() sample(1:8, 1),
      den        = function() sample(2:12, 1),
      multiplier = function() sample(2:5, 1),
      correct_pos = function() sample(1:3, 1)   # randomize correct answer position
    ),
    constraint = function(p) {
      p$num < p$den && gcd(p$num, p$den) == 1
    },
    statement = function(p) {
      equiv_num  <- p$num * p$multiplier
      equiv_den  <- p$den * p$multiplier
      wrong1_num <- p$num + 1
      wrong1_den <- p$den + 1
      wrong2_num <- p$num * p$multiplier
      wrong2_den <- p$den * p$multiplier + 1
      # Place correct answer at correct_pos; wrong answers fill remaining spots
      fracs <- vector("list", 3)
      fracs[[p$correct_pos]] <- latex_frac(equiv_num, equiv_den)
      wrong_spots <- setdiff(1:3, p$correct_pos)
      fracs[[wrong_spots[1]]] <- latex_frac(wrong1_num, wrong1_den)
      fracs[[wrong_spots[2]]] <- latex_frac(wrong2_num, wrong2_den)
      paste0("Which of the following is equivalent to $",
             latex_frac(p$num, p$den), "$?\n\n",
             "(a) $", fracs[[1]], "$\n",
             "(b) $", fracs[[2]], "$\n",
             "(c) $", fracs[[3]], "$")
    },
    solve = function(p) {
      equiv_num <- p$num * p$multiplier
      equiv_den <- p$den * p$multiplier
      letter <- c("a", "b", "c")[p$correct_pos]
      list(
        steps = c(
          paste0("Step 1: Multiply numerator and denominator by ", p$multiplier, ":"),
          paste0("Step 2: $", latex_frac(p$num, p$den), " = ",
                 latex_frac(equiv_num, equiv_den), "$"),
          paste0("Step 3: The answer is (", letter, ").")
        ),
        answer_value = p$num / p$den,
        answer_letter = letter
      )
    },
    format_answer = function(sol) {
      paste0("(", sol$answer_letter, ")")
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 2: Routine — Add two fractions with unlike denominators
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "frac_arith_d2_add",
    topic_id = "fraction_arithmetic",
    difficulty = 2L,
    description = "Add two fractions with unlike denominators",
    params = list(
      n1 = function() sample(1:9, 1),
      d1 = function() sample(2:12, 1),
      n2 = function() sample(1:9, 1),
      d2 = function() sample(2:12, 1)
    ),
    constraint = function(p) {
      p$n1 < p$d1 && p$n2 < p$d2 && p$d1 != p$d2 &&
      gcd(p$n1, p$d1) == 1 && gcd(p$n2, p$d2) == 1
    },
    statement = function(p) {
      paste0("Compute $", latex_frac(p$n1, p$d1), " + ",
             latex_frac(p$n2, p$d2), "$ and simplify.")
    },
    solve = function(p) {
      l <- lcd(p$d1, p$d2)
      new_n1 <- p$n1 * (l / p$d1)
      new_n2 <- p$n2 * (l / p$d2)
      total_num <- new_n1 + new_n2
      result <- simplify_fraction(total_num, l)
      steps <- c(
        paste0("Step 1: Find the LCD of ", p$d1, " and ", p$d2, ": LCD = ", l, "."),
        paste0("Step 2: Rewrite: $", latex_frac(new_n1, l), " + ",
               latex_frac(new_n2, l), "$."),
        paste0("Step 3: Add numerators: $", latex_frac(total_num, l), "$.")
      )
      g <- gcd(abs(total_num), l)
      if (g > 1) {
        steps <- c(steps,
          paste0("Step ", length(steps) + 1, ": Simplify by dividing by ", g, ": $",
                 latex_frac(result$num, result$den), "$."))
      }
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 3: Multi-step — (a/b - c/d) * e/f
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "frac_arith_d3_chain",
    topic_id = "fraction_arithmetic",
    difficulty = 3L,
    description = "Chain subtraction and multiplication of fractions",
    params = list(
      n1 = function() sample(1:9, 1),
      d1 = function() sample(2:10, 1),
      n2 = function() sample(1:9, 1),
      d2 = function() sample(2:10, 1),
      n3 = function() sample(1:7, 1),
      d3 = function() sample(2:8, 1)
    ),
    constraint = function(p) {
      p$n1 < p$d1 && p$n2 < p$d2 && p$n3 < p$d3 &&
      p$d1 != p$d2 &&
      gcd(p$n1, p$d1) == 1 && gcd(p$n2, p$d2) == 1 &&
      gcd(p$n3, p$d3) == 1 &&
      # Ensure subtraction is positive
      (p$n1 / p$d1) > (p$n2 / p$d2)
    },
    statement = function(p) {
      paste0("Compute $\\left(", latex_frac(p$n1, p$d1), " - ",
             latex_frac(p$n2, p$d2), "\\right) \\times ",
             latex_frac(p$n3, p$d3), "$ and simplify.")
    },
    solve = function(p) {
      # Step 1: subtract
      sub_result <- frac_sub(p$n1, p$d1, p$n2, p$d2)
      # Step 2: multiply
      final <- frac_mul(sub_result$num, sub_result$den, p$n3, p$d3)

      steps <- c(
        paste0("Step 1: Subtract the fractions: $", latex_frac(p$n1, p$d1), " - ",
               latex_frac(p$n2, p$d2), " = ",
               latex_frac(sub_result$num, sub_result$den), "$."),
        paste0("Step 2: Multiply: $", latex_frac(sub_result$num, sub_result$den),
               " \\times ", latex_frac(p$n3, p$d3), " = ",
               latex_frac(sub_result$num * p$n3, sub_result$den * p$d3), "$."),
        paste0("Step 3: Simplify: $", latex_frac(final$num, final$den), "$.")
      )
      list(steps = steps, answer_num = final$num, answer_den = final$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 4: Transfer — Probability word problem with fractions
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "frac_arith_d4_probability",
    topic_id = "fraction_arithmetic",
    difficulty = 4L,
    description = "Drawing without replacement probability problem",
    params = list(
      red = function() sample(3:8, 1),
      blue = function() sample(2:7, 1)
    ),
    constraint = function(p) {
      p$red >= 3 && (p$red + p$blue) <= 15
    },
    statement = function(p) {
      total <- p$red + p$blue
      paste0("A bag contains ", p$red, " red marbles and ", p$blue,
             " blue marbles. You draw one marble, do not replace it, ",
             "then draw a second marble. What is the probability that ",
             "both marbles are red? Simplify your answer.")
    },
    solve = function(p) {
      total <- p$red + p$blue
      # P(both red) = (red/total) * ((red-1)/(total-1))
      num <- p$red * (p$red - 1)
      den <- total * (total - 1)
      result <- simplify_fraction(num, den)

      steps <- c(
        paste0("Step 1: Total marbles: ", p$red, " + ", p$blue, " = ", total, "."),
        paste0("Step 2: P(1st red) = $", latex_frac(p$red, total), "$."),
        paste0("Step 3: After drawing one red, there are ", p$red - 1,
               " red marbles out of ", total - 1, " total."),
        paste0("Step 4: P(2nd red | 1st red) = $", latex_frac(p$red - 1, total - 1), "$."),
        paste0("Step 5: P(both red) = $", latex_frac(p$red, total), " \\times ",
               latex_frac(p$red - 1, total - 1), " = ",
               latex_frac(num, den), "$."),
        paste0("Step 6: Simplify: $", latex_frac(result$num, result$den), "$.")
      )
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))

  # ---------------------------------------------------------------------------
  # Difficulty 5: Synthesis — Sum involving fractions and powers
  # ---------------------------------------------------------------------------
  register_template(list(
    template_id = "frac_arith_d5_synthesis",
    topic_id = "fraction_arithmetic",
    difficulty = 5L,
    description = "Evaluate a sum combining fractions with powers",
    params = list(
      upper = function() sample(3:5, 1)
    ),
    constraint = NULL,
    statement = function(p) {
      paste0("Evaluate $", latex_sum("i", 1, p$upper,
             "\\left(\\frac{i}{i+1} - \\left(\\frac{1}{2}\\right)^i\\right)"),
             "$.")
    },
    solve = function(p) {
      # Compute each term: i/(i+1) - (1/2)^i
      total_num <- 0L
      total_den <- 1L
      term_strs <- character()

      for (i in seq_len(p$upper)) {
        # i/(i+1) as fraction
        frac_part <- list(num = i, den = i + 1L)
        # (1/2)^i = 1/2^i
        pow_part <- list(num = 1L, den = 2L^i)
        # Subtract
        term <- frac_sub(frac_part$num, frac_part$den,
                          pow_part$num, pow_part$den)

        term_strs <- c(term_strs,
          paste0("Step ", i + 1, ": $i=", i, "$: $", latex_frac(i, i + 1L), " - ",
                 latex_frac(1L, 2L^i), " = ",
                 latex_frac(term$num, term$den), "$"))

        # Accumulate sum
        if (i == 1) {
          total_num <- term$num
          total_den <- term$den
        } else {
          acc <- frac_add(total_num, total_den, term$num, term$den)
          total_num <- acc$num
          total_den <- acc$den
        }
      }

      result <- simplify_fraction(total_num, total_den)
      steps <- c(
        "Step 1: Evaluate each term:",
        term_strs,
        paste0("Step ", length(term_strs) + 2, ": Sum all terms: $", latex_frac(result$num, result$den), "$.")
      )
      list(steps = steps, answer_num = result$num, answer_den = result$den)
    },
    format_answer = function(sol) {
      latex_frac(sol$answer_num, sol$answer_den)
    }
  ))
}
