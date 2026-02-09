test_that("order_of_operations templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("order_of_operations", difficulty = d, seed = 500 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "order_of_operations")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("order_of_operations D1 recognition gives numeric answer", {
  prob <- generate_problem("order_of_operations", difficulty = 1, seed = 42)
  # D1 should produce a numeric answer
  ans <- as.numeric(gsub("\\\\frac\\{(-?\\d+)\\}\\{(\\d+)\\}", "\\1/\\2", prob$answer))
  expect_false(is.na(ans))
})

test_that("order_of_operations D2 routine gives valid answer", {
  prob <- generate_problem("order_of_operations", difficulty = 2, seed = 55)
  expect_true(nchar(prob$answer) > 0)
})

test_that("order_of_operations D3 multi-step has multiple solution steps", {
  prob <- generate_problem("order_of_operations", difficulty = 3, seed = 77)
  expect_true(length(prob$solution_steps) >= 2)
})

test_that("order_of_operations D5 synthesis gives valid answer", {
  prob <- generate_problem("order_of_operations", difficulty = 5, seed = 33)
  expect_true(nchar(prob$answer) > 0)
  expect_true(length(prob$solution_steps) >= 2)
})

test_that("order_of_operations answer checker accepts correct answer", {
  prob <- generate_problem("order_of_operations", difficulty = 2, seed = 88)
  result <- check_answer(prob, prob$answer)
  expect_true(result$correct)
})

test_that("order_of_operations is reproducible with seed", {
  p1 <- generate_problem("order_of_operations", difficulty = 3, seed = 99)
  p2 <- generate_problem("order_of_operations", difficulty = 3, seed = 99)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})

test_that("order_of_operations produces different problems with different seeds", {
  p1 <- generate_problem("order_of_operations", difficulty = 2, seed = 1)
  p2 <- generate_problem("order_of_operations", difficulty = 2, seed = 2)
  expect_false(p1$statement == p2$statement && p1$answer == p2$answer)
})
