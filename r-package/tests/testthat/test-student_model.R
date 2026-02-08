test_that("create_student_model returns valid S3 class", {
  s <- create_student_model()
  expect_s3_class(s, "student_model")
  expect_true(nchar(s$student_id) > 0)
  expect_equal(s$total_attempts, 0L)
  expect_equal(s$total_correct, 0L)
  expect_null(s$current_session)
  expect_equal(length(s$session_history), 0)
})

test_that("create_student_model initializes all 8 active topics", {
  s <- create_student_model()
  expect_equal(length(s$topics), 8)
  expect_true("fraction_arithmetic" %in% names(s$topics))
  expect_true("geometric_series" %in% names(s$topics))
})

test_that("each topic_state has correct defaults", {
  s <- create_student_model()
  ts <- s$topics[["fraction_arithmetic"]]
  expect_equal(ts$topic_id, "fraction_arithmetic")
  expect_equal(ts$mastery_state, "not_started")
  expect_equal(ts$difficulty, 1L)
  expect_equal(ts$ease_factor, 2.5)
  expect_equal(ts$interval, 0)
  expect_equal(ts$repetition, 0L)
  expect_equal(ts$attempt_count, 0L)
  expect_equal(ts$correct_count, 0L)
  expect_equal(ts$session_count, 0L)
  expect_equal(ts$consecutive_wrong, 0L)
  expect_equal(length(ts$last_n_results), 0)
})

test_that("create_student_model accepts custom student_id", {
  s <- create_student_model(student_id = "test-id-123")
  expect_equal(s$student_id, "test-id-123")
})

test_that("get_topic_state retrieves correct topic", {
  s <- create_student_model()
  ts <- get_topic_state(s, "exponent_rules")
  expect_equal(ts$topic_id, "exponent_rules")
})

test_that("get_topic_state errors on invalid topic_id", {
  s <- create_student_model()
  expect_error(get_topic_state(s, "nonexistent_topic"), "Unknown topic")
})

test_that("student_progress returns data frame with expected columns", {
  s <- create_student_model()
  prog <- student_progress(s)
  expect_s3_class(prog, "data.frame")
  expect_equal(nrow(prog), 8)
  expect_true(all(c("topic_id", "mastery", "difficulty", "accuracy",
                     "attempts", "sessions", "ease_factor") %in% names(prog)))
})

test_that("student_progress shows all not_started for new student", {
  s <- create_student_model()
  prog <- student_progress(s)
  expect_true(all(prog$mastery == "not_started"))
  expect_true(all(is.na(prog$accuracy)))
})

test_that("print.student_model runs without error", {
  s <- create_student_model()
  expect_output(print(s), "Student Model")
})
