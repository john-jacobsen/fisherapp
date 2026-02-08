test_that("parse_student_answer handles fractions", {
  result <- fisherapp:::parse_student_answer("3/4")
  expect_equal(result$num, 3)
  expect_equal(result$den, 4)

  result <- fisherapp:::parse_student_answer("-3/4")
  expect_equal(result$num, -3)
  expect_equal(result$den, 4)
})

test_that("parse_student_answer handles LaTeX fractions", {
  result <- fisherapp:::parse_student_answer("\\frac{3}{4}")
  expect_equal(result$num, 3)
  expect_equal(result$den, 4)
})

test_that("parse_student_answer handles decimals and integers", {
  result <- fisherapp:::parse_student_answer("0.75")
  expect_equal(result$value, 0.75)

  result <- fisherapp:::parse_student_answer("42")
  expect_equal(result$value, 42)

  result <- fisherapp:::parse_student_answer("-3")
  expect_equal(result$value, -3)
})

test_that("parse_student_answer returns NULL for garbage", {
  expect_null(fisherapp:::parse_student_answer("abc"))
  expect_null(fisherapp:::parse_student_answer(""))
})

test_that("to_numeric handles various raw formats", {
  expect_equal(fisherapp:::to_numeric(0.75), 0.75)
  expect_equal(fisherapp:::to_numeric(list(num = 3, den = 4)), 0.75)
  expect_equal(fisherapp:::to_numeric(list(answer_num = 3, answer_den = 4)), 0.75)
  expect_equal(fisherapp:::to_numeric(list(answer_value = 42)), 42)
  expect_equal(fisherapp:::to_numeric(list(value = 0.5)), 0.5)
  expect_true(is.na(fisherapp:::to_numeric(list())))
})

test_that("compare_answers detects equivalent forms", {
  raw <- list(answer_num = 3, answer_den = 4)

  expect_true(fisherapp:::compare_answers("3/4", raw))
  expect_true(fisherapp:::compare_answers("6/8", raw))
  expect_true(fisherapp:::compare_answers("0.75", raw))
  expect_true(fisherapp:::compare_answers("\\frac{3}{4}", raw))
  expect_true(fisherapp:::compare_answers("\\frac{6}{8}", raw))

  expect_false(fisherapp:::compare_answers("1/2", raw))
  expect_false(fisherapp:::compare_answers("0.5", raw))
  expect_false(fisherapp:::compare_answers("abc", raw))
})

test_that("check_answer returns correct structure", {
  # Register a dummy template for this test
  dummy <- list(
    template_id = "answer_check_test_d1",
    topic_id = "answer_check_test",
    difficulty = 1L,
    params = list(a = function() 3),
    constraint = NULL,
    statement = function(p) "What is 3/4?",
    solve = function(p) list(
      steps = c("The answer is 3/4."),
      answer_num = 3, answer_den = 4
    ),
    format_answer = function(sol) "\\frac{3}{4}"
  )
  register_template(dummy)

  prob <- generate_problem("answer_check_test", 1)
  result <- check_answer(prob, "0.75")
  expect_true(result$correct)
  expect_equal(result$correct_answer, "\\frac{3}{4}")
  expect_true(length(result$solution_steps) >= 1)

  result2 <- check_answer(prob, "1/3")
  expect_false(result2$correct)

  rm("answer_check_test_d1", envir = fisherapp:::.template_registry)
})
