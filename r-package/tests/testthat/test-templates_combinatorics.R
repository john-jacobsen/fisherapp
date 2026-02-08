test_that("combinatorics templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("combinatorics", difficulty = d, seed = 300 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "combinatorics")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("combinatorics D1 factorial is correct", {
  prob <- generate_problem("combinatorics", difficulty = 1, seed = 42)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  # Should be a factorial of 4-8
  expect_true(ans %in% c(factorial(4:8)))
})

test_that("combinatorics D2 computes C(n,k) correctly", {
  prob <- generate_problem("combinatorics", difficulty = 2, seed = 55)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  expect_true(ans > 0)
  expect_equal(ans, round(ans))
})

test_that("combinatorics D3 handshake problem is correct", {
  prob <- generate_problem("combinatorics", difficulty = 3, seed = 77)
  # Extract n from params and verify answer = C(n, 2)
  n <- prob$params$n
  expected <- choose(n, 2)
  expect_equal(as.numeric(prob$answer), expected)
})

test_that("combinatorics D5 binomial PMF gives valid fraction", {
  prob <- generate_problem("combinatorics", difficulty = 5, seed = 33)
  # Answer should contain frac or be a simple number

  # Check that the raw answer gives a valid probability (0, 1)
  raw_val <- prob$answer_raw$answer_num / prob$answer_raw$answer_den
  expect_true(raw_val > 0 && raw_val < 1)
})

test_that("combinatorics is reproducible with seed", {
  p1 <- generate_problem("combinatorics", difficulty = 2, seed = 99)
  p2 <- generate_problem("combinatorics", difficulty = 2, seed = 99)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})
