test_that("generate_problem errors on missing templates", {
  expect_error(generate_problem("nonexistent_topic", 1),
               "No templates")
})

test_that("generate_problem produces valid structure with dummy template", {
  dummy <- list(
    template_id = "engine_test_d1",
    topic_id = "engine_test",
    difficulty = 1L,
    params = list(a = function() sample(2:9, 1)),
    constraint = NULL,
    statement = function(p) paste("What is", p$a, "* 2?"),
    solve = function(p) list(
      steps = c(paste(p$a, "* 2 =", p$a * 2)),
      answer_value = p$a * 2
    ),
    format_answer = function(sol) as.character(sol$answer_value)
  )
  register_template(dummy)

  prob <- generate_problem("engine_test", 1)
  expect_s3_class(prob, "fisherapp_problem")
  expect_equal(prob$topic_id, "engine_test")
  expect_equal(prob$difficulty, 1L)
  expect_true(nchar(prob$problem_id) > 0)
  expect_true(nchar(prob$statement) > 0)
  expect_true(length(prob$solution_steps) >= 1)
  expect_true(nchar(prob$answer) > 0)

  # Cleanup
  rm("engine_test_d1", envir = fisherapp:::.template_registry)
})

test_that("generate_problem with seed is reproducible", {
  dummy <- list(
    template_id = "seed_test_d1",
    topic_id = "seed_test",
    difficulty = 1L,
    params = list(a = function() sample(1:100, 1)),
    constraint = NULL,
    statement = function(p) paste("Number:", p$a),
    solve = function(p) list(steps = "done", answer_value = p$a),
    format_answer = function(sol) as.character(sol$answer_value)
  )
  register_template(dummy)

  p1 <- generate_problem("seed_test", 1, seed = 42)
  p2 <- generate_problem("seed_test", 1, seed = 42)
  expect_equal(p1$params$a, p2$params$a)
  expect_equal(p1$answer, p2$answer)

  rm("seed_test_d1", envir = fisherapp:::.template_registry)
})

test_that("problem_to_json produces valid JSON", {
  dummy <- list(
    template_id = "json_test_d1",
    topic_id = "json_test",
    difficulty = 1L,
    params = list(a = function() 5),
    constraint = NULL,
    statement = function(p) "What is 5 + 1?",
    solve = function(p) list(steps = c("5 + 1 = 6"), answer_value = 6),
    format_answer = function(sol) "6"
  )
  register_template(dummy)

  prob <- generate_problem("json_test", 1)
  json <- problem_to_json(prob)
  parsed <- jsonlite::fromJSON(json)
  expect_equal(parsed$topic_id, "json_test")
  expect_equal(parsed$statement, "What is 5 + 1?")

  # Without solution
  json2 <- problem_to_json(prob, include_solution = FALSE)
  parsed2 <- jsonlite::fromJSON(json2)
  expect_null(parsed2$answer)

  rm("json_test_d1", envir = fisherapp:::.template_registry)
})

# --- select_template / exclude_templates tests ------------------------------

test_that("select_template picks unseen templates when available", {
  # Register two templates for the same topic/difficulty
  t1 <- list(
    template_id = "sel_test_a", topic_id = "sel_test", difficulty = 1L,
    params = list(a = function() 1), constraint = NULL,
    statement = function(p) "A",
    solve = function(p) list(steps = "A", answer_value = 1),
    format_answer = function(sol) "1"
  )
  t2 <- list(
    template_id = "sel_test_b", topic_id = "sel_test", difficulty = 1L,
    params = list(a = function() 2), constraint = NULL,
    statement = function(p) "B",
    solve = function(p) list(steps = "B", answer_value = 2),
    format_answer = function(sol) "2"
  )
  register_template(t1)
  register_template(t2)

  # Excluding "sel_test_a" should always pick "sel_test_b"
  for (i in 1:10) {
    prob <- generate_problem("sel_test", 1, exclude_templates = "sel_test_a")
    expect_equal(prob$template_id, "sel_test_b")
  }

  rm("sel_test_a", "sel_test_b", envir = fisherapp:::.template_registry)
})

test_that("select_template falls back to least recently served when all excluded", {
  t1 <- list(
    template_id = "fb_test_a", topic_id = "fb_test", difficulty = 1L,
    params = list(a = function() 1), constraint = NULL,
    statement = function(p) "A",
    solve = function(p) list(steps = "A", answer_value = 1),
    format_answer = function(sol) "1"
  )
  register_template(t1)

  # Only one template and it's excluded — should still generate (fallback)
  prob <- generate_problem("fb_test", 1,
    exclude_templates = c("fb_test_a"))
  expect_equal(prob$template_id, "fb_test_a")

  rm("fb_test_a", envir = fisherapp:::.template_registry)
})

test_that("select_template maximizes gap with multiple seen templates", {
  t1 <- list(
    template_id = "gap_test_a", topic_id = "gap_test", difficulty = 1L,
    params = list(a = function() 1), constraint = NULL,
    statement = function(p) "A",
    solve = function(p) list(steps = "A", answer_value = 1),
    format_answer = function(sol) "1"
  )
  t2 <- list(
    template_id = "gap_test_b", topic_id = "gap_test", difficulty = 1L,
    params = list(a = function() 2), constraint = NULL,
    statement = function(p) "B",
    solve = function(p) list(steps = "B", answer_value = 2),
    format_answer = function(sol) "2"
  )
  register_template(t1)
  register_template(t2)

  # Both excluded. "a" was served first (position 1), "b" second (position 2)
  # Should pick "a" since it has the smaller last-position (most gap)
  prob <- generate_problem("gap_test", 1,
    exclude_templates = c("gap_test_a", "gap_test_b"))
  expect_equal(prob$template_id, "gap_test_a")

  # If "b" was served first and "a" second, should pick "b"
  prob2 <- generate_problem("gap_test", 1,
    exclude_templates = c("gap_test_b", "gap_test_a"))
  expect_equal(prob2$template_id, "gap_test_b")

  rm("gap_test_a", "gap_test_b", envir = fisherapp:::.template_registry)
})

test_that("generate_problem works with NULL exclude_templates", {
  prob <- generate_problem("fraction_arithmetic", 2, exclude_templates = NULL)
  expect_s3_class(prob, "fisherapp_problem")
})

test_that("generate_problem works with empty exclude_templates", {
  prob <- generate_problem("fraction_arithmetic", 2, exclude_templates = character(0))
  expect_s3_class(prob, "fisherapp_problem")
})
