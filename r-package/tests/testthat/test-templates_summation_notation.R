test_that("summation_notation templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("summation_notation", difficulty = d, seed = 600 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "summation_notation")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("summation_notation D1 recognition gives numeric answer", {
  prob <- generate_problem("summation_notation", difficulty = 1, seed = 42)
  # D1 should be a simple sum — answer is numeric
  ans <- as.numeric(prob$answer)
  expect_false(is.na(ans))
})

test_that("summation_notation D2 routine gives valid answer", {
  prob <- generate_problem("summation_notation", difficulty = 2, seed = 55)
  expect_true(nchar(prob$answer) > 0)
})

test_that("summation_notation D3 multi-step has multiple solution steps", {
  prob <- generate_problem("summation_notation", difficulty = 3, seed = 77)
  expect_true(length(prob$solution_steps) >= 2)
})

test_that("summation_notation D4 expected value gives valid fraction or integer", {
  prob <- generate_problem("summation_notation", difficulty = 4, seed = 33)
  # D4 expected value — answer should be a fraction or integer
  expect_true(grepl("frac|^-?\\d+$", prob$answer))
})

test_that("summation_notation answer checker accepts correct answer", {
  prob <- generate_problem("summation_notation", difficulty = 2, seed = 88)
  result <- check_answer(prob, prob$answer)
  expect_true(result$correct)
})

test_that("summation_notation is reproducible with seed", {
  p1 <- generate_problem("summation_notation", difficulty = 3, seed = 99)
  p2 <- generate_problem("summation_notation", difficulty = 3, seed = 99)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})

test_that("summation_notation produces different problems with different seeds", {
  p1 <- generate_problem("summation_notation", difficulty = 2, seed = 1)
  p2 <- generate_problem("summation_notation", difficulty = 2, seed = 2)
  expect_false(p1$statement == p2$statement && p1$answer == p2$answer)
})
