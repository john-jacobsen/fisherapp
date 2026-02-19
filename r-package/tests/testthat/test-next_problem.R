test_that("select_next_topic returns root topic for new student", {
  s <- create_student_model()
  result <- select_next_topic(s)
  expect_equal(result$topic_id, "fraction_arithmetic")
  expect_equal(result$difficulty, 1L)
})

test_that("select_next_topic returns in_progress topic", {
  s <- create_student_model()
  s$topics[["fraction_arithmetic"]]$mastery_state <- "in_progress"
  s$topics[["fraction_arithmetic"]]$difficulty <- 3L
  s$topics[["fraction_arithmetic"]]$last_n_results <- c(1L, 1L, 1L, 1L)
  result <- select_next_topic(s)
  expect_equal(result$topic_id, "fraction_arithmetic")
})

test_that("select_next_topic returns new topic when prereqs met", {
  s <- create_student_model()
  s$topics[["fraction_arithmetic"]]$mastery_state <- "mastered"
  s$topics[["fraction_arithmetic"]]$next_review <- Sys.time() + 100000
  result <- select_next_topic(s)
  # Should be exponent_rules (first topic with prereq = fraction_arithmetic)
  expect_equal(result$topic_id, "exponent_rules")
  expect_equal(result$difficulty, 1L)
})

test_that("select_next_topic returns review topic when due", {
  s <- create_student_model()
  # Mark fraction_arithmetic as mastered but overdue
  s$topics[["fraction_arithmetic"]]$mastery_state <- "mastered"
  s$topics[["fraction_arithmetic"]]$difficulty <- 3L
  s$topics[["fraction_arithmetic"]]$next_review <- Sys.time() - 1000
  result <- select_next_topic(s)
  expect_equal(result$topic_id, "fraction_arithmetic")
  expect_equal(result$difficulty, 3L)
})

test_that("select_next_topic never returns topic with unmet prereqs", {
  s <- create_student_model()
  # Mark fraction_arithmetic as in_progress, not mastered
  s$topics[["fraction_arithmetic"]]$mastery_state <- "in_progress"
  result <- select_next_topic(s)
  # Should still be fraction_arithmetic, not exponent_rules
  expect_equal(result$topic_id, "fraction_arithmetic")
})

test_that("select_next_topic returns mastered topic when all mastered and not due", {
  s <- create_student_model()
  for (tid in names(s$topics)) {
    s$topics[[tid]]$mastery_state <- "mastered"
    s$topics[[tid]]$difficulty <- 3L
    s$topics[[tid]]$next_review <- Sys.time() + 100000
  }
  result <- select_next_topic(s)
  # Bucket 4: should still return a mastered topic for practice
  expect_false(is.null(result))
  expect_true(result$topic_id %in% names(s$topics))
  expect_equal(result$difficulty, 3L)
})

test_that("next_problem_for_student returns fisherapp_problem", {
  s <- create_student_model()
  prob <- next_problem_for_student(s)
  expect_s3_class(prob, "fisherapp_problem")
  expect_equal(prob$topic_id, "fraction_arithmetic")
})

test_that("next_problem_for_student returns problem even when all mastered", {
  s <- create_student_model()
  for (tid in names(s$topics)) {
    s$topics[[tid]]$mastery_state <- "mastered"
    s$topics[[tid]]$difficulty <- 3L
    s$topics[[tid]]$next_review <- Sys.time() + 100000
  }
  prob <- next_problem_for_student(s)
  # Bucket 4 fallback: should still generate a problem
  expect_s3_class(prob, "fisherapp_problem")
})
