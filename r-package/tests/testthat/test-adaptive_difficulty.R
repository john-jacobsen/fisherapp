test_that("adjust_difficulty holds with insufficient data", {
  ts <- init_topic_state("test")
  ts$difficulty <- 3L
  ts$last_n_results <- c(1L, 1L)  # fewer than window
  expect_equal(adjust_difficulty(ts), 3L)
})

test_that("adjust_difficulty promotes on high accuracy", {
  ts <- init_topic_state("test")
  ts$difficulty <- 2L
  ts$last_n_results <- c(1L, 1L, 1L, 1L)  # 100%
  expect_equal(adjust_difficulty(ts), 3L)
})

test_that("adjust_difficulty demotes on low accuracy", {
  ts <- init_topic_state("test")
  ts$difficulty <- 3L
  ts$last_n_results <- c(0L, 0L, 0L, 0L)  # 0%
  expect_equal(adjust_difficulty(ts), 2L)
})

test_that("adjust_difficulty holds on mixed results", {
  ts <- init_topic_state("test")
  ts$difficulty <- 3L
  ts$last_n_results <- c(1L, 0L, 1L, 0L)  # 50%
  expect_equal(adjust_difficulty(ts), 3L)
})

test_that("adjust_difficulty caps at 5", {
  ts <- init_topic_state("test")
  ts$difficulty <- 5L
  ts$last_n_results <- c(1L, 1L, 1L, 1L)
  expect_equal(adjust_difficulty(ts), 5L)
})

test_that("adjust_difficulty floors at 1", {
  ts <- init_topic_state("test")
  ts$difficulty <- 1L
  ts$last_n_results <- c(0L, 0L, 0L, 0L)
  expect_equal(adjust_difficulty(ts), 1L)
})

test_that("adjust_difficulty uses only last window results", {
  ts <- init_topic_state("test")
  ts$difficulty <- 3L
  ts$last_n_results <- c(0L, 0L, 0L, 0L, 1L, 1L, 1L, 1L)  # last 4 are all correct
  expect_equal(adjust_difficulty(ts), 4L)
})
