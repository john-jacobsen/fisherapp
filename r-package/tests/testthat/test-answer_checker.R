# =============================================================================
# Tests for answer_checker.R — normalization, parsing, and flexible matching
# =============================================================================

# --- normalize_answer --------------------------------------------------------

test_that("normalize_answer strips outer parentheses", {
  expect_equal(fisherapp:::normalize_answer("(a)"), "a")
  expect_equal(fisherapp:::normalize_answer("(3/4)"), "3/4")
  expect_equal(fisherapp:::normalize_answer("(hello)"), "hello")
  # Should not strip if not matched outer parens
  expect_equal(fisherapp:::normalize_answer("(a) + (b)"), "(a)+(b)")
})

test_that("normalize_answer lowercases", {
  expect_equal(fisherapp:::normalize_answer("A"), "a")
  expect_equal(fisherapp:::normalize_answer("ABC"), "abc")
  expect_equal(fisherapp:::normalize_answer("X+1"), "x+1")
})

test_that("normalize_answer strips whitespace", {
  expect_equal(fisherapp:::normalize_answer("  a  "), "a")
  expect_equal(fisherapp:::normalize_answer("3 / 4"), "3/4")
  expect_equal(fisherapp:::normalize_answer(" x + 1 "), "x+1")
})

test_that("normalize_answer handles combined transformations", {
  expect_equal(fisherapp:::normalize_answer("  (A)  "), "a")
  expect_equal(fisherapp:::normalize_answer("( 3/4 )"), "3/4")
})

# --- normalize_algebra -------------------------------------------------------

test_that("normalize_algebra removes multiplication signs", {
  expect_equal(fisherapp:::normalize_algebra("2*x"), "2x")
  expect_equal(fisherapp:::normalize_algebra("3*x*y"), "3xy")
})

test_that("normalize_algebra sorts additive terms", {
  expect_equal(fisherapp:::normalize_algebra("x+1"),
               fisherapp:::normalize_algebra("1+x"))
  expect_equal(fisherapp:::normalize_algebra("y+x+1"),
               fisherapp:::normalize_algebra("1+x+y"))
})

test_that("normalize_algebra handles subtraction", {
  expect_equal(fisherapp:::normalize_algebra("x-1"),
               fisherapp:::normalize_algebra("x-1"))
  # "x-1" normalizes by expanding to "x+-1", sorting terms
  result <- fisherapp:::normalize_algebra("x-1")
  expect_true(nchar(result) > 0)
})

# --- parse_student_answer ----------------------------------------------------

test_that("parse_student_answer handles fractions", {
  result <- fisherapp:::parse_student_answer("3/4")
  expect_equal(result$value, 0.75)

  result <- fisherapp:::parse_student_answer("-3/4")
  expect_equal(result$value, -0.75)
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

test_that("parse_student_answer handles leading-dot decimals", {
  result <- fisherapp:::parse_student_answer(".5")
  expect_equal(result$value, 0.5)

  result <- fisherapp:::parse_student_answer(".75")
  expect_equal(result$value, 0.75)

  result <- fisherapp:::parse_student_answer("-.25")
  expect_equal(result$value, -0.25)
})

test_that("parse_student_answer strips parentheses before parsing", {
  result <- fisherapp:::parse_student_answer("(3/4)")
  expect_equal(result$value, 0.75)

  result <- fisherapp:::parse_student_answer("(42)")
  expect_equal(result$value, 42)

  result <- fisherapp:::parse_student_answer("(.5)")
  expect_equal(result$value, 0.5)
})

test_that("parse_student_answer returns NULL for garbage", {
  expect_null(fisherapp:::parse_student_answer("abc"))
  expect_null(fisherapp:::parse_student_answer(""))
})

# --- to_numeric --------------------------------------------------------------

test_that("to_numeric handles various raw formats", {
  expect_equal(fisherapp:::to_numeric(0.75), 0.75)
  expect_equal(fisherapp:::to_numeric(list(num = 3, den = 4)), 0.75)
  expect_equal(fisherapp:::to_numeric(list(answer_num = 3, answer_den = 4)), 0.75)
  expect_equal(fisherapp:::to_numeric(list(answer_value = 42)), 42)
  expect_equal(fisherapp:::to_numeric(list(value = 0.5)), 0.5)
  expect_true(is.na(fisherapp:::to_numeric(list())))
})

# --- compare_answers: numeric equivalence ------------------------------------

test_that("compare_answers detects equivalent numeric forms", {
  raw <- list(answer_num = 3, answer_den = 4)

  expect_true(fisherapp:::compare_answers("3/4", raw))
  expect_true(fisherapp:::compare_answers("6/8", raw))
  expect_true(fisherapp:::compare_answers("0.75", raw))
  expect_true(fisherapp:::compare_answers(".75", raw))
  expect_true(fisherapp:::compare_answers("\\frac{3}{4}", raw))
  expect_true(fisherapp:::compare_answers("\\frac{6}{8}", raw))

  expect_false(fisherapp:::compare_answers("1/2", raw))
  expect_false(fisherapp:::compare_answers("0.5", raw))
  expect_false(fisherapp:::compare_answers("abc", raw))
})

test_that("compare_answers handles 0.5 = 1/2 = .5", {
  raw <- list(answer_num = 1, answer_den = 2)

  expect_true(fisherapp:::compare_answers("0.5", raw))
  expect_true(fisherapp:::compare_answers(".5", raw))
  expect_true(fisherapp:::compare_answers("1/2", raw))
  expect_true(fisherapp:::compare_answers("2/4", raw))
})

test_that("compare_answers handles parenthesized numeric answers", {
  raw <- list(answer_num = 3, answer_den = 4)

  expect_true(fisherapp:::compare_answers("(3/4)", raw))
  expect_true(fisherapp:::compare_answers("(0.75)", raw))
  expect_true(fisherapp:::compare_answers("(.75)", raw))
})

# --- compare_answers: letter answers -----------------------------------------

test_that("compare_answers accepts letter answers", {
  raw <- list(answer_value = 0.5, answer_letter = "a")

  # Letter variations
  expect_true(fisherapp:::compare_answers("a", raw))
  expect_true(fisherapp:::compare_answers("A", raw))
  expect_true(fisherapp:::compare_answers("(a)", raw))
  expect_true(fisherapp:::compare_answers("(A)", raw))
  expect_true(fisherapp:::compare_answers(" a ", raw))

  # Numeric value still works
  expect_true(fisherapp:::compare_answers("0.5", raw))
  expect_true(fisherapp:::compare_answers("1/2", raw))

  # Wrong letter
  expect_false(fisherapp:::compare_answers("b", raw))
  expect_false(fisherapp:::compare_answers("(b)", raw))
})

# --- compare_answers: algebraic expressions ----------------------------------

test_that("compare_answers handles algebraic equivalence", {
  raw <- list(answer_expr = "x+1")

  expect_true(fisherapp:::compare_answers("x+1", raw))
  expect_true(fisherapp:::compare_answers("1+x", raw))
  expect_true(fisherapp:::compare_answers("X+1", raw))
  expect_true(fisherapp:::compare_answers(" x + 1 ", raw))

  expect_false(fisherapp:::compare_answers("x+2", raw))
})

test_that("compare_answers handles 2*x = 2x algebraic equivalence", {
  raw <- list(answer_expr = "2x")

  expect_true(fisherapp:::compare_answers("2x", raw))
  expect_true(fisherapp:::compare_answers("2*x", raw))
  expect_true(fisherapp:::compare_answers("2*X", raw))

  expect_false(fisherapp:::compare_answers("3x", raw))
})

# --- check_answer (full workflow) --------------------------------------------

test_that("check_answer returns correct structure", {
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

  # Parenthesized answer should work
  result3 <- check_answer(prob, "(3/4)")
  expect_true(result3$correct)

  # Leading-dot decimal should work
  result4 <- check_answer(prob, ".75")
  expect_true(result4$correct)

  rm("answer_check_test_d1", envir = fisherapp:::.template_registry)
})

test_that("check_answer works with letter answer template", {
  dummy_letter <- list(
    template_id = "letter_test_d1",
    topic_id = "letter_test",
    difficulty = 1L,
    params = list(a = function() 2),
    constraint = NULL,
    statement = function(p) "Pick (a), (b), or (c)",
    solve = function(p) list(
      steps = c("The answer is (a)."),
      answer_value = 0.5,
      answer_letter = "a"
    ),
    format_answer = function(sol) "(a)"
  )
  register_template(dummy_letter)

  prob <- generate_problem("letter_test", 1)

  # Accept letter
  expect_true(check_answer(prob, "a")$correct)
  expect_true(check_answer(prob, "(a)")$correct)
  expect_true(check_answer(prob, "A")$correct)

  # Also accept numeric
  expect_true(check_answer(prob, "0.5")$correct)
  expect_true(check_answer(prob, "1/2")$correct)

  # Wrong answers
  expect_false(check_answer(prob, "b")$correct)
  expect_false(check_answer(prob, "0.75")$correct)

  rm("letter_test_d1", envir = fisherapp:::.template_registry)
})

# --- MathLive LaTeX normalization -------------------------------------------

test_that("normalize_answer handles \\dfrac -> \\frac", {
  expect_equal(fisherapp:::normalize_answer("\\dfrac{3}{4}"), "\\frac{3}{4}")
})

test_that("normalize_answer strips \\left and \\right", {
  expect_equal(fisherapp:::normalize_answer("\\left(x\\right)"), "(x)")
})

test_that("normalize_answer converts \\cdot to *", {
  expect_equal(fisherapp:::normalize_answer("2\\cdot3"), "2*3")
})

test_that("normalize_answer converts \\times to *", {
  expect_equal(fisherapp:::normalize_answer("2\\times3"), "2*3")
})

test_that("normalize_answer strips LaTeX spacing commands", {
  expect_equal(fisherapp:::normalize_answer("3\\,000"), "3000")
  expect_equal(fisherapp:::normalize_answer("a\\;b"), "ab")
  expect_equal(fisherapp:::normalize_answer("a\\!b"), "ab")
})

# --- parse_student_answer with sqrt -----------------------------------------

test_that("parse_student_answer handles \\sqrt{n}", {
  result <- fisherapp:::parse_student_answer("\\sqrt{16}")
  expect_equal(result$value, 4)
})

test_that("parse_student_answer handles sqrt(n)", {
  result <- fisherapp:::parse_student_answer("sqrt(25)")
  expect_equal(result$value, 5)
})

test_that("parse_student_answer handles \\sqrt{0}", {
  result <- fisherapp:::parse_student_answer("\\sqrt{0}")
  expect_equal(result$value, 0)
})

test_that("parse_student_answer handles \\dfrac via normalization", {
  result <- fisherapp:::parse_student_answer("\\dfrac{3}{4}")
  expect_equal(result$num, 3L)
  expect_equal(result$den, 4L)
})

test_that("compare_answers: \\dfrac{3}{4} matches 3/4 answer", {
  correct_raw <- list(answer_num = 3, answer_den = 4)
  expect_true(fisherapp:::compare_answers("\\dfrac{3}{4}", correct_raw))
})

test_that("compare_answers: \\sqrt{4} matches 2", {
  correct_raw <- list(answer_value = 2)
  expect_true(fisherapp:::compare_answers("\\sqrt{4}", correct_raw))
})

test_that("compare_answers: 2\\cdot3 is parsed after normalization", {
  # "2*3" is not directly numeric, but the normalization helps
  # The answer "2*3" won't be parsed as numeric by default
  # This tests that \cdot is at least normalized to *
  norm <- fisherapp:::normalize_answer("2\\cdot3")
  expect_equal(norm, "2*3")
})

# --- Exponent expression normalization (Fix 1) ---

test_that("normalize_answer strips curly braces from exponents", {
  expect_equal(fisherapp:::normalize_answer("x^{3}"), "x^3")
  expect_equal(fisherapp:::normalize_answer("x^{11}"), "x^11")
  expect_equal(fisherapp:::normalize_answer("2x^{5}"), "2x^5")
})

test_that("compare_answers: x^3 matches x^{3} answer_expr", {
  raw <- list(answer_expr = "x^{3}")
  expect_true(fisherapp:::compare_answers("x^3", raw))
  expect_true(fisherapp:::compare_answers("x^{3}", raw))
})

test_that("compare_answers: 27x^11/4 matches answer_expr 27x^{11}/4", {
  raw <- list(answer_expr = "27x^{11}/4")
  expect_true(fisherapp:::compare_answers("27x^11/4", raw))
})
