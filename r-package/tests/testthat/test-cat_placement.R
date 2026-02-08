test_that("run_placement_test with perfect answers places topics", {
  s <- create_student_model()
  # answer_fn always gives correct answer
  result <- run_placement_test(s, answer_fn = function(p) p$answer,
                               max_questions = 25)
  expect_s3_class(result$cat_result, "cat_result")
  expect_true(result$cat_result$questions_asked > 0)
  expect_true(result$cat_result$questions_asked <= 25)

  # At least some topics should have high difficulty
  diffs <- vapply(result$cat_result$topic_placements,
                  function(tp) tp$start_difficulty, integer(1))
  expect_true(max(diffs) >= 3)
})

test_that("run_placement_test with all wrong places topics at difficulty 1", {
  s <- create_student_model()
  result <- run_placement_test(s, answer_fn = function(p) "wrong",
                               max_questions = 25)
  for (tid in names(result$cat_result$topic_placements)) {
    tp <- result$cat_result$topic_placements[[tid]]
    expect_equal(tp$status, "placed")
    expect_equal(tp$start_difficulty, 1L)
  }
})

test_that("run_placement_test respects max_questions cap", {
  s <- create_student_model()
  result <- run_placement_test(s, answer_fn = function(p) "wrong",
                               max_questions = 10)
  expect_true(result$cat_result$questions_asked <= 10)
})

test_that("run_placement_test updates student model", {
  s <- create_student_model()
  result <- run_placement_test(s, answer_fn = function(p) p$answer,
                               max_questions = 25)
  # At least some topics should have changed from not_started
  states <- vapply(result$student$topics,
                   function(ts) ts$mastery_state, character(1))
  expect_true(any(states != "not_started"))
})

test_that("run_placement_test follows topological order", {
  s <- create_student_model()
  result <- run_placement_test(s, answer_fn = function(p) "wrong",
                               max_questions = 25)
  # The attempt log should show topics in topological order
  topics_seen <- unique(vapply(result$cat_result$attempt_log,
                               function(a) a$topic_id, character(1)))
  topo <- get_topic_order()
  # topics_seen should be a subsequence of topo
  topo_indices <- match(topics_seen, topo)
  expect_true(all(!is.na(topo_indices)))
  expect_true(all(diff(topo_indices) > 0))
})

test_that("cat_result print method works", {
  s <- create_student_model()
  result <- run_placement_test(s, answer_fn = function(p) "wrong",
                               max_questions = 10)
  expect_output(print(result$cat_result), "CAT Placement Result")
})
