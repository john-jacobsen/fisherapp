test_that("fraction_arithmetic templates generate valid problems at all difficulties", {
  for (d in 1:5) {
    prob <- generate_problem("fraction_arithmetic", difficulty = d, seed = 200 + d)
    expect_s3_class(prob, "fisherapp_problem")
    expect_equal(prob$topic_id, "fraction_arithmetic")
    expect_equal(prob$difficulty, d)
    expect_true(nchar(prob$statement) > 0)
    expect_true(length(prob$solution_steps) >= 1)
    expect_true(nchar(prob$answer) > 0)
  }
})

test_that("fraction_arithmetic D1 recognition gives valid answer", {
  prob <- generate_problem("fraction_arithmetic", difficulty = 1, seed = 42)
  # D1 recognition may be multiple choice "(a)" or a fraction/integer
  expect_true(nchar(prob$answer) > 0)
})

test_that("fraction_arithmetic D1 correct answer position is randomized across seeds", {
  # Generate multiple instances and collect the answer letters
  answers <- character(20)
  for (i in seq_along(answers)) {
    prob <- generate_problem("fraction_arithmetic", difficulty = 1, seed = i * 7)
    answers[i] <- prob$answer
  }
  # The correct answer should NOT always be "(a)" — all three positions should appear
  unique_positions <- unique(answers)
  expect_gt(length(unique_positions), 1,
            label = "correct answer should appear in more than one position")
})

test_that("fraction_arithmetic D2 subtraction gives valid answer", {
  prob <- generate_problem("fraction_arithmetic", difficulty = 2, seed = 55)
  expect_true(nchar(prob$answer) > 0)
})

test_that("fraction_arithmetic D3 multi-step gives valid answer", {
  prob <- generate_problem("fraction_arithmetic", difficulty = 3, seed = 77)
  expect_true(nchar(prob$answer) > 0)
  expect_true(length(prob$solution_steps) >= 2)
})

test_that("fraction_arithmetic D4 transfer is NOT a probability problem", {
  for (seed in c(10, 20, 30, 40, 50)) {
    prob <- generate_problem("fraction_arithmetic", difficulty = 4, seed = seed)
    # Should not mention marbles, probability, or drawing
    stmt <- tolower(prob$statement)
    expect_false(grepl("marble|probability|draw.*marble", stmt),
                 label = paste0("D4 seed ", seed, " should not be a probability problem"))
  }
})

test_that("fraction_arithmetic D5 synthesis is NOT a summation notation problem", {
  for (seed in c(10, 20, 30, 40, 50)) {
    prob <- generate_problem("fraction_arithmetic", difficulty = 5, seed = seed)
    # Should not have sigma/sum notation as the primary structure
    stmt <- prob$statement
    expect_false(grepl("\\\\sum_\\{i=", stmt),
                 label = paste0("D5 seed ", seed, " should not be a summation problem"))
  }
})

test_that("fraction_arithmetic D5 synthesis gives valid answer", {
  prob <- generate_problem("fraction_arithmetic", difficulty = 5, seed = 33)
  expect_true(nchar(prob$answer) > 0)
  expect_true(length(prob$solution_steps) >= 2)
})

test_that("fraction_arithmetic answer checker accepts correct answer", {
  prob <- generate_problem("fraction_arithmetic", difficulty = 2, seed = 88)
  result <- check_answer(prob, prob$answer)
  expect_true(result$correct)
})

test_that("fraction_arithmetic is reproducible with seed", {
  p1 <- generate_problem("fraction_arithmetic", difficulty = 3, seed = 99)
  p2 <- generate_problem("fraction_arithmetic", difficulty = 3, seed = 99)
  expect_equal(p1$answer, p2$answer)
  expect_equal(p1$statement, p2$statement)
})

test_that("fraction_arithmetic produces different problems with different seeds", {
  p1 <- generate_problem("fraction_arithmetic", difficulty = 2, seed = 1)
  p2 <- generate_problem("fraction_arithmetic", difficulty = 2, seed = 2)
  # At least the statement or answer should differ

  expect_false(p1$statement == p2$statement && p1$answer == p2$answer)
})
