test_that("start_session creates valid session", {
  s <- create_student_model()
  s <- start_session(s)
  expect_s3_class(s$current_session, "tutor_session")
  expect_true(nchar(s$current_session$session_id) > 0)
  expect_equal(s$current_session$problems_served, 0L)
  expect_equal(length(s$current_session$topics_attempted), 0)
  expect_equal(length(s$current_session$templates_served), 0)
})

test_that("get_next_problem tracks templates_served", {
  s <- create_student_model()
  s <- start_session(s)
  result <- get_next_problem(s)
  s <- result$student
  expect_equal(length(s$current_session$templates_served), 1)
  expect_true(nchar(s$current_session$templates_served[1]) > 0)

  # Second problem should add to the list
  result2 <- get_next_problem(s)
  s <- result2$student
  expect_equal(length(s$current_session$templates_served), 2)
})

test_that("submit_answer updates student state on correct answer", {
  s <- create_student_model()
  s <- start_session(s)
  prob <- generate_problem("fraction_arithmetic", 2, seed = 42)
  result <- submit_answer(s, prob, prob$answer)
  s <- result$student

  ts <- s$topics[["fraction_arithmetic"]]
  expect_equal(ts$attempt_count, 1L)
  expect_equal(ts$correct_count, 1L)
  expect_equal(ts$consecutive_wrong, 0L)
  expect_equal(length(ts$last_n_results), 1)
  expect_equal(ts$last_n_results[1], 1L)
  expect_equal(ts$mastery_state, "in_progress")
  expect_equal(s$total_attempts, 1L)
  expect_equal(s$total_correct, 1L)
  expect_true(result$result$correct)
})

test_that("submit_answer updates student state on wrong answer", {
  s <- create_student_model()
  s <- start_session(s)
  prob <- generate_problem("fraction_arithmetic", 2, seed = 42)
  result <- submit_answer(s, prob, "wrong_answer")
  s <- result$student

  ts <- s$topics[["fraction_arithmetic"]]
  expect_equal(ts$attempt_count, 1L)
  expect_equal(ts$correct_count, 0L)
  expect_equal(ts$consecutive_wrong, 1L)
  expect_equal(ts$last_n_results[1], 0L)
  expect_equal(s$total_attempts, 1L)
  expect_equal(s$total_correct, 0L)
  expect_false(result$result$correct)
})

test_that("submit_answer increments session counters", {
  s <- create_student_model()
  s <- start_session(s)
  prob <- generate_problem("fraction_arithmetic", 2, seed = 42)
  result <- submit_answer(s, prob, prob$answer)
  s <- result$student

  expect_equal(s$current_session$problems_served, 1L)
  expect_equal(s$current_session$problems_correct, 1L)
  expect_equal(length(s$current_session$attempts), 1)
})

test_that("submit_answer tracks session topics", {
  s <- create_student_model()
  s <- start_session(s)
  prob <- generate_problem("fraction_arithmetic", 2, seed = 42)
  result <- submit_answer(s, prob, prob$answer)
  s <- result$student

  expect_true("fraction_arithmetic" %in% s$current_session$topics_attempted)
  expect_equal(s$topics[["fraction_arithmetic"]]$session_count, 1L)
})

test_that("session_count only increments once per session per topic", {
  s <- create_student_model()
  s <- start_session(s)

  # Submit two answers on same topic
  prob1 <- generate_problem("fraction_arithmetic", 2, seed = 42)
  result <- submit_answer(s, prob1, prob1$answer)
  s <- result$student

  prob2 <- generate_problem("fraction_arithmetic", 2, seed = 43)
  result <- submit_answer(s, prob2, prob2$answer)
  s <- result$student

  expect_equal(s$topics[["fraction_arithmetic"]]$session_count, 1L)
})

test_that("end_session archives and clears current session", {
  s <- create_student_model()
  s <- start_session(s)
  prob <- generate_problem("fraction_arithmetic", 2, seed = 42)
  result <- submit_answer(s, prob, prob$answer)
  s <- result$student
  s <- end_session(s)

  expect_null(s$current_session)
  expect_equal(length(s$session_history), 1)
  expect_true(!is.null(s$session_history[[1]]$ended_at))
})

test_that("end_session errors without active session", {
  s <- create_student_model()
  expect_error(end_session(s), "No active session")
})

test_that("detect_stuck returns NULL below threshold", {
  ts <- init_topic_state("test")
  ts$consecutive_wrong <- 2L
  ts$difficulty <- 3L
  expect_null(detect_stuck(ts))
})

test_that("detect_stuck returns reduce_difficulty when possible", {
  ts <- init_topic_state("test")
  ts$consecutive_wrong <- 3L
  ts$difficulty <- 3L
  result <- detect_stuck(ts)
  expect_equal(result$type, "reduce_difficulty")
})

test_that("detect_stuck returns route_prerequisite at difficulty 1", {
  ts <- init_topic_state("exponent_rules")
  ts$consecutive_wrong <- 3L
  ts$difficulty <- 1L
  result <- detect_stuck(ts)
  expect_equal(result$type, "route_prerequisite")
  expect_true(!is.null(result$redirect_topic))
})

test_that("detect_stuck returns worked_example for root at difficulty 1", {
  ts <- init_topic_state("fraction_arithmetic")
  ts$consecutive_wrong <- 3L
  ts$difficulty <- 1L
  result <- detect_stuck(ts)
  expect_equal(result$type, "worked_example")
})

test_that("get_next_problem errors without active session", {
  s <- create_student_model()
  expect_error(get_next_problem(s), "No active session")
})

test_that("get_next_problem returns problem for new student", {
  s <- create_student_model()
  s <- start_session(s)
  result <- get_next_problem(s)
  expect_s3_class(result$problem, "fisherapp_problem")
  expect_null(result$intervention)
})

test_that("simulate_session produces expected results", {
  s <- create_student_model()
  result <- simulate_session(s, n_problems = 10, correct_rate = 0.8, seed = 42)
  expect_true(nrow(result$summary) > 0)
  expect_true(nrow(result$summary) <= 10)
  expect_true(result$student$total_attempts > 0)
  expect_equal(length(result$student$session_history), 1)
  expect_null(result$student$current_session)
})

test_that("simulate_session is reproducible with seed", {
  s1 <- create_student_model(student_id = "test")
  s2 <- create_student_model(student_id = "test")
  r1 <- simulate_session(s1, n_problems = 5, correct_rate = 0.7, seed = 99)
  r2 <- simulate_session(s2, n_problems = 5, correct_rate = 0.7, seed = 99)
  expect_equal(r1$summary$correct, r2$summary$correct)
  expect_equal(r1$student$total_attempts, r2$student$total_attempts)
  expect_equal(r1$student$total_correct, r2$student$total_correct)
})

test_that("full integration: multi-problem session updates state correctly", {
  s <- create_student_model()
  # Start at D2 so answers are numeric (D1 uses multiple choice format)
  s$topics[["fraction_arithmetic"]]$difficulty <- 2L
  s$topics[["fraction_arithmetic"]]$mastery_state <- "in_progress"
  s$topics[["fraction_arithmetic"]]$last_n_results <- c(1L, 1L, 1L, 1L)
  s <- start_session(s)

  for (i in 1:5) {
    prob <- generate_problem("fraction_arithmetic", 2, seed = 100 + i)
    submit_result <- submit_answer(s, prob, prob$answer)
    s <- submit_result$student
  }

  expect_equal(s$total_attempts, 5L)
  expect_equal(s$total_correct, 5L)
  expect_equal(s$current_session$problems_served, 5L)

  ts <- s$topics[["fraction_arithmetic"]]
  expect_equal(ts$mastery_state, "in_progress")
  expect_true(ts$attempt_count >= 5)
})
