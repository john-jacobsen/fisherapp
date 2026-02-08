test_that("logarithms_exponentials templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("logarithms_exponentials", difficulty = d, seed = 200 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "logarithms_exponentials")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("log_exp D1 conversion gives correct exponent", {
  prob <- generate_problem("logarithms_exponentials", difficulty = 1, seed = 42)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  # Answer should be a small integer (the exponent)
  expect_true(ans >= 2 && ans <= 4)
})

test_that("log_exp D2 simplification gives correct value", {
  prob <- generate_problem("logarithms_exponentials", difficulty = 2, seed = 55)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  expect_true(ans >= 2 && ans <= 8)
})

test_that("log_exp D3 exponential equation has integer solution", {
  prob <- generate_problem("logarithms_exponentials", difficulty = 3, seed = 77)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  expect_equal(ans, round(ans))
})

test_that("log_exp D5 MLE gives valid fraction", {
  prob <- generate_problem("logarithms_exponentials", difficulty = 5, seed = 33)
  # Answer should be a LaTeX fraction
  expect_true(grepl("frac", prob$answer) || grepl("^\\d+$", prob$answer))
})

test_that("logarithms_exponentials is reproducible with seed", {
  p1 <- generate_problem("logarithms_exponentials", difficulty = 4, seed = 88)
  p2 <- generate_problem("logarithms_exponentials", difficulty = 4, seed = 88)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})
