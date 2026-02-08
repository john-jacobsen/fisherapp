test_that("map_quality returns 5 for correct at working difficulty", {
  expect_equal(map_quality(TRUE, 3, 3), 5L)
  expect_equal(map_quality(TRUE, 4, 3), 5L)
})

test_that("map_quality returns 4 for correct one level below", {
  expect_equal(map_quality(TRUE, 2, 3), 4L)
})

test_that("map_quality returns 3 for correct two+ levels below", {
  expect_equal(map_quality(TRUE, 1, 3), 3L)
  expect_equal(map_quality(TRUE, 1, 5), 3L)
})

test_that("map_quality returns 2 for first incorrect", {
  expect_equal(map_quality(FALSE, 3, 3, 0L), 2L)
})

test_that("map_quality returns 1 for repeated incorrect", {
  expect_equal(map_quality(FALSE, 3, 3, 1L), 1L)
  expect_equal(map_quality(FALSE, 3, 3, 2L), 1L)
})

test_that("map_quality returns 0 for 3+ consecutive wrong", {
  expect_equal(map_quality(FALSE, 3, 3, 3L), 0L)
  expect_equal(map_quality(FALSE, 3, 3, 5L), 0L)
})

test_that("sm2_update with quality 5 increases interval and EF", {
  ts <- init_topic_state("test")
  ts$repetition <- 2L
  ts$interval <- 6
  ts$ease_factor <- 2.5
  updated <- sm2_update(ts, 5L)
  expect_true(updated$ease_factor > 2.5)
  expect_true(updated$interval > 6)
  expect_equal(updated$repetition, 3L)
})

test_that("sm2_update first repetition gives interval 1", {
  ts <- init_topic_state("test")
  updated <- sm2_update(ts, 4L)
  expect_equal(updated$interval, 1)
  expect_equal(updated$repetition, 1L)
})

test_that("sm2_update second repetition gives interval 6", {
  ts <- init_topic_state("test")
  ts$repetition <- 1L
  ts$interval <- 1
  updated <- sm2_update(ts, 4L)
  expect_equal(updated$interval, 6)
  expect_equal(updated$repetition, 2L)
})

test_that("sm2_update with quality < 3 resets repetition", {
  ts <- init_topic_state("test")
  ts$repetition <- 5L
  ts$interval <- 30
  updated <- sm2_update(ts, 2L)
  expect_equal(updated$repetition, 0L)
  expect_equal(updated$interval, 1)
})

test_that("sm2_update EF never drops below 1.3", {
  ts <- init_topic_state("test")
  ts$ease_factor <- 1.4
  updated <- sm2_update(ts, 0L)
  expect_true(updated$ease_factor >= 1.3)
})

test_that("sm2_update sets next_review in the future", {
  ts <- init_topic_state("test")
  now <- Sys.time()
  updated <- sm2_update(ts, 4L, review_time = now)
  expect_true(updated$next_review > now)
})

test_that("is_due_for_review returns TRUE when overdue", {
  ts <- init_topic_state("test")
  ts$next_review <- Sys.time() - 100
  expect_true(is_due_for_review(ts))
})

test_that("is_due_for_review returns FALSE when not yet due", {
  ts <- init_topic_state("test")
  ts$next_review <- Sys.time() + 100000
  expect_false(is_due_for_review(ts))
})
