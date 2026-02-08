test_that("register_template validates required fields", {
  expect_error(register_template(list()), "missing required fields")
})

test_that("register and retrieve templates works", {
  # Create a dummy template
  dummy <- list(
    template_id = "test_dummy_d1",
    topic_id = "test_topic",
    difficulty = 1L,
    params = list(a = function() sample(1:10, 1)),
    constraint = NULL,
    statement = function(p) paste("What is", p$a, "+ 1?"),
    solve = function(p) list(steps = c(paste(p$a, "+ 1 =", p$a + 1)),
                              answer_value = p$a + 1),
    format_answer = function(sol) as.character(sol$answer_value)
  )

  register_template(dummy)
  expect_true("test_dummy_d1" %in% list_templates())

  templates <- get_templates("test_topic", difficulty = 1)
  expect_equal(length(templates), 1)
  expect_equal(templates[[1]]$template_id, "test_dummy_d1")

  # Cleanup
  rm("test_dummy_d1", envir = fisherapp:::.template_registry)
})
