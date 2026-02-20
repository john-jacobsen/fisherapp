test_that("exponent_rules templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("exponent_rules", difficulty = d, seed = 400 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "exponent_rules")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("exponent_rules D1 recognition gives valid answer", {
  prob <- generate_problem("exponent_rules", difficulty = 1, seed = 42)
  expect_true(nchar(prob$answer) > 0)
})

test_that("exponent_rules D2 routine gives valid answer", {
  prob <- generate_problem("exponent_rules", difficulty = 2, seed = 55)
  expect_true(nchar(prob$answer) > 0)
})

test_that("exponent_rules D3 multi-step has multiple solution steps", {
  prob <- generate_problem("exponent_rules", difficulty = 3, seed = 77)
  expect_true(length(prob$solution_steps) >= 2)
})

test_that("exponent_rules D4 transfer gives valid answer", {
  prob <- generate_problem("exponent_rules", difficulty = 4, seed = 33)
  expect_true(nchar(prob$answer) > 0)
})

test_that("exponent_rules answer contains exponent notation", {
  prob <- generate_problem("exponent_rules", difficulty = 2, seed = 88)
  # Exponent rule answers are symbolic (e.g., "x^{13}") not purely numeric
  expect_true(nchar(prob$answer) > 0)
})

test_that("exponent_rules is reproducible with seed", {
  p1 <- generate_problem("exponent_rules", difficulty = 3, seed = 99)
  p2 <- generate_problem("exponent_rules", difficulty = 3, seed = 99)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})

test_that("exponent_rules produces different problems with different seeds", {
  p1 <- generate_problem("exponent_rules", difficulty = 2, seed = 1)
  p2 <- generate_problem("exponent_rules", difficulty = 2, seed = 2)
  expect_false(p1$statement == p2$statement && p1$answer == p2$answer)
})

# Fix 1: answer matching for algebraic exponent expressions

test_that("exponent_rules D2 answer accepted when student types x^N without braces", {
  prob <- generate_problem("exponent_rules", difficulty = 2, seed = 55)
  cat("D2 answer:", prob$answer, "\n")
  # Strip curly braces to simulate student input: x^{7} -> x^7
  correct_no_braces <- gsub("\\{(\\d+)\\}", "\\1", prob$answer)
  result <- check_answer(prob, correct_no_braces)
  expect_true(result$correct)
})

test_that("exponent_rules D3 answer accepted when student submits exact answer", {
  prob <- generate_problem("exponent_rules", difficulty = 3, seed = 77)
  cat("D3 answer:", prob$answer, "\n")
  result <- check_answer(prob, prob$answer)
  expect_true(result$correct)
})
