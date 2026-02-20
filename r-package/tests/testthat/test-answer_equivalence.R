# =============================================================================
# Tests: Equivalent answer form acceptance (Fix 2)
# =============================================================================

test_that("0/8 is equivalent to 0", {
  raw_value <- list(answer_value = 0)
  expect_true(fisherapp:::compare_answers("0/8", raw_value))

  raw_num_den <- list(answer_num = 0, answer_den = 1)
  expect_true(fisherapp:::compare_answers("0/8", raw_num_den))
})

test_that("1/2 is equivalent to 0.5", {
  raw <- list(answer_num = 1, answer_den = 2)
  expect_true(fisherapp:::compare_answers("0.5", raw))
  expect_true(fisherapp:::compare_answers("1/2", raw))
  expect_true(fisherapp:::compare_answers(".5", raw))
})

test_that("x^3 is equivalent to x^{3}", {
  raw <- list(answer_expr = "x^{3}")
  expect_true(fisherapp:::compare_answers("x^3", raw))
  expect_true(fisherapp:::compare_answers("x^{3}", raw))
})

test_that("2x is equivalent to 2*x", {
  raw <- list(answer_expr = "2x")
  expect_true(fisherapp:::compare_answers("2*x", raw))
  expect_true(fisherapp:::compare_answers("2x", raw))
  expect_true(fisherapp:::compare_answers("2*X", raw))
})

test_that("(a) is equivalent to a", {
  raw <- list(answer_letter = "a", answer_value = 0.5)
  expect_true(fisherapp:::compare_answers("(a)", raw))
  expect_true(fisherapp:::compare_answers("a", raw))
  expect_true(fisherapp:::compare_answers("A", raw))
})

test_that("27x^11/4 is equivalent to 6.75x^11", {
  raw_fraction <- list(answer_expr = "27x^{11}/4")
  expect_true(fisherapp:::compare_answers("27x^11/4", raw_fraction),
              label = "27x^11/4 vs answer_expr 27x^{11}/4")
  result_decimal <- fisherapp:::compare_answers("6.75x^11", raw_fraction)
  cat("6.75x^11 vs 27x^{11}/4:", result_decimal, "\n")
  expect_true(result_decimal,
              label = "6.75x^11 vs answer_expr 27x^{11}/4")
})
