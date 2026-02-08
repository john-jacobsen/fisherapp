test_that("latex_frac formats fractions correctly", {
  expect_equal(latex_frac(3, 4), "\\frac{3}{4}")
  expect_equal(latex_frac(5, 1), "5")
  expect_equal(latex_frac(-3, 4), "-\\frac{3}{4}")
  expect_equal(latex_frac(0, 5), "\\frac{0}{5}")
})

test_that("latex_exp formats exponents correctly", {
  expect_equal(latex_exp("x", 3), "x^{3}")
  expect_equal(latex_exp("x", 1), "x")
  expect_equal(latex_exp(2, 5), "2^{5}")
  expect_equal(latex_exp("x", 0), "x^{0}")
})

test_that("latex_sum formats summation correctly", {
  result <- latex_sum("i", 1, "n", "x_i")
  expect_equal(result, "\\sum_{i=1}^{n} x_i")
})

test_that("latex_display and latex_inline wrap correctly", {
  expect_equal(latex_display("x^2"), "$$x^2$$")
  expect_equal(latex_inline("x^2"), "$x^2$")
})
