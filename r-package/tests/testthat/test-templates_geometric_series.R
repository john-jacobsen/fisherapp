test_that("geometric_series templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("geometric_series", difficulty = d, seed = 400 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "geometric_series")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("geometric_series D1 identifies correct common ratio", {
  prob <- generate_problem("geometric_series", difficulty = 1, seed = 42)
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
  expect_true(ans %in% c(2, 3, -2))
})

test_that("geometric_series D2 finite sum is correct", {
  prob <- generate_problem("geometric_series", difficulty = 2, seed = 55)
  # Verify by direct computation
  a <- prob$params$a
  r <- prob$params$r
  n <- prob$params$n
  expected <- a * (r^n - 1) / (r - 1)
  expect_equal(as.numeric(prob$answer), expected)
})

test_that("geometric_series D3 tail sum gives valid fraction", {
  prob <- generate_problem("geometric_series", difficulty = 3, seed = 77)
  raw_val <- prob$answer_raw$answer_num / prob$answer_raw$answer_den
  expect_true(raw_val > 0 && raw_val < 1)
})

test_that("geometric_series D4 tail probability is valid", {
  prob <- generate_problem("geometric_series", difficulty = 4, seed = 33)
  raw_val <- prob$answer_raw$answer_num / prob$answer_raw$answer_den
  expect_true(raw_val > 0 && raw_val < 1)
})

test_that("geometric_series D5 PMF verification gives 1", {
  prob <- generate_problem("geometric_series", difficulty = 5, seed = 88)
  expect_equal(prob$answer, "1")
})

test_that("geometric_series is reproducible with seed", {
  p1 <- generate_problem("geometric_series", difficulty = 3, seed = 99)
  p2 <- generate_problem("geometric_series", difficulty = 3, seed = 99)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})
