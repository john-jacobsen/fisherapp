test_that("evaluate_mastery returns not_started for new topic", {
  ts <- init_topic_state("test")
  expect_equal(evaluate_mastery(ts), "not_started")
})

test_that("evaluate_mastery returns in_progress with some attempts", {
  ts <- init_topic_state("test")
  ts$attempt_count <- 3L
  ts$last_n_results <- c(1L, 1L, 0L)
  ts$mastery_state <- "in_progress"
  expect_equal(evaluate_mastery(ts), "in_progress")
})

test_that("evaluate_mastery returns mastered when all criteria met", {
  ts <- init_topic_state("test")
  ts$attempt_count <- 10L
  ts$mastery_state <- "in_progress"
  ts$last_n_results <- c(1L, 1L, 1L, 1L, 1L, 1L, 1L, 1L, 0L, 1L)  # 90%
  ts$session_count <- 3L
  ts$difficulty <- 4L
  expect_equal(evaluate_mastery(ts), "mastered")
})

test_that("evaluate_mastery rejects if accuracy below 85%", {
  ts <- init_topic_state("test")
  ts$attempt_count <- 10L
  ts$mastery_state <- "in_progress"
  ts$last_n_results <- c(1L, 1L, 1L, 1L, 1L, 1L, 0L, 0L, 0L, 0L)  # 60%
  ts$session_count <- 3L
  ts$difficulty <- 4L
  expect_equal(evaluate_mastery(ts), "in_progress")
})

test_that("evaluate_mastery rejects if fewer than min_window attempts", {
  ts <- init_topic_state("test")
  ts$attempt_count <- 5L
  ts$mastery_state <- "in_progress"
  ts$last_n_results <- c(1L, 1L, 1L, 1L, 1L)  # 100% but too few
  ts$session_count <- 3L
  ts$difficulty <- 4L
  expect_equal(evaluate_mastery(ts), "in_progress")
})

test_that("evaluate_mastery rejects if only 1 session", {
  ts <- init_topic_state("test")
  ts$attempt_count <- 10L
  ts$mastery_state <- "in_progress"
  ts$last_n_results <- rep(1L, 10)
  ts$session_count <- 1L
  ts$difficulty <- 4L
  expect_equal(evaluate_mastery(ts), "in_progress")
})

test_that("evaluate_mastery rejects if difficulty < 3", {
  ts <- init_topic_state("test")
  ts$attempt_count <- 10L
  ts$mastery_state <- "in_progress"
  ts$last_n_results <- rep(1L, 10)
  ts$session_count <- 3L
  ts$difficulty <- 2L
  expect_equal(evaluate_mastery(ts), "in_progress")
})

test_that("evaluate_mastery keeps mastered state sticky", {
  ts <- init_topic_state("test")
  ts$mastery_state <- "mastered"
  ts$attempt_count <- 1L
  expect_equal(evaluate_mastery(ts), "mastered")
})

test_that("prerequisites_met returns TRUE for root topic", {
  s <- create_student_model()
  expect_true(prerequisites_met(s, "fraction_arithmetic"))
})

test_that("prerequisites_met returns FALSE when prereqs not mastered", {
  s <- create_student_model()
  expect_false(prerequisites_met(s, "exponent_rules"))
})

test_that("prerequisites_met returns TRUE when all prereqs mastered", {
  s <- create_student_model()
  s$topics[["fraction_arithmetic"]]$mastery_state <- "mastered"
  expect_true(prerequisites_met(s, "exponent_rules"))
})

test_that("prerequisites_met handles multi-prereq topics", {
  s <- create_student_model()
  s$topics[["fraction_arithmetic"]]$mastery_state <- "mastered"
  # order_of_operations needs fraction_arithmetic AND exponent_rules
  expect_false(prerequisites_met(s, "order_of_operations"))
  s$topics[["exponent_rules"]]$mastery_state <- "mastered"
  expect_true(prerequisites_met(s, "order_of_operations"))
})
