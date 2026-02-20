# =============================================================================
# Tests: Problem cache — no expiration (Fix 3)
# =============================================================================
# Sourced with working directory = project root

library(testthat)
source("api/R/problem_cache.R")

make_fake_problem <- function(id = "test-id-123") {
  list(problem_id = id, topic_id = "fraction_arithmetic", difficulty = 2,
       statement = "Compute 1/2 + 1/3", answer = "5/6",
       solution_steps = c("Step 1"),
       answer_raw = list(answer_num = 5, answer_den = 6))
}

test_that("cached problem is returned immediately", {
  prob <- make_fake_problem("pid-immediate")
  cache_problem(prob)
  result <- get_cached_problem("pid-immediate")
  expect_equal(result$problem_id, "pid-immediate")
  remove_cached_problem("pid-immediate")
})

test_that("cached problem is still accessible after simulated long delay", {
  prob <- make_fake_problem("pid-old")
  cache_problem(prob)
  # Backdate the entry 24 hours beyond any TTL
  .problem_cache[["pid-old"]]$created_at <- Sys.time() - 86400
  result <- get_cached_problem("pid-old")
  expect_false(is.null(result),
               label = "problem should still be accessible after 24 hours")
  expect_equal(result$problem_id, "pid-old")
  remove_cached_problem("pid-old")
})

test_that("placement state is still accessible after simulated long delay", {
  state <- list(student_id = "s1", topic_order = c("fraction_arithmetic"),
                topic_idx = 1L, complete = FALSE, results = list())
  cache_placement_state("student-old", state)
  .placement_cache[["student-old"]]$created_at <- Sys.time() - 86400
  result <- get_placement_state("student-old")
  expect_false(is.null(result),
               label = "placement state should still be accessible after 24 hours")
  remove_placement_state("student-old")
})

test_that("clean_cache does not remove any entries", {
  prob <- make_fake_problem("pid-clean-test")
  cache_problem(prob)
  .problem_cache[["pid-clean-test"]]$created_at <- Sys.time() - 86400
  clean_cache()
  result <- get_cached_problem("pid-clean-test")
  expect_false(is.null(result), label = "clean_cache should not evict entries")
  remove_cached_problem("pid-clean-test")
})
