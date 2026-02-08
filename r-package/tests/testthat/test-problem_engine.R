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
