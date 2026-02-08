test_that("solving_equations templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("solving_equations", difficulty = d, seed = 100 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "solving_equations")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("solving_equations D2 produces correct answer", {
  prob <- generate_problem("solving_equations", difficulty = 2, seed = 42)
  # The answer should be an integer (the value of x)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  expect_equal(ans, round(ans))
})

test_that("solving_equations D3 clears fractions correctly", {
  prob <- generate_problem("solving_equations", difficulty = 3, seed = 55)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  expect_equal(ans, round(ans))
})

test_that("solving_equations D4 z-score problem has valid answer", {
  prob <- generate_problem("solving_equations", difficulty = 4, seed = 77)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
})

test_that("solving_equations is reproducible with seed", {
  p1 <- generate_problem("solving_equations", difficulty = 3, seed = 99)
  p2 <- generate_problem("solving_equations", difficulty = 3, seed = 99)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})
