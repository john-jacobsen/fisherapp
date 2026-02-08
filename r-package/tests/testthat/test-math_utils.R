test_that("gcd works correctly", {
  expect_equal(gcd(12, 8), 4)
  expect_equal(gcd(7, 13), 1)
  expect_equal(gcd(0, 5), 5)
  expect_equal(gcd(5, 0), 5)
  expect_equal(gcd(-12, 8), 4)
  expect_equal(gcd(100, 75), 25)
})

test_that("lcd works correctly", {
  expect_equal(lcd(4, 6), 12)
  expect_equal(lcd(3, 5), 15)
  expect_equal(lcd(7, 7), 7)
  expect_equal(lcd(1, 12), 12)
  expect_equal(lcd(0, 5), 0)
})

test_that("simplify_fraction works correctly", {
  expect_equal(simplify_fraction(6, 8), list(num = 3, den = 4))
  expect_equal(simplify_fraction(3, 4), list(num = 3, den = 4))
  expect_equal(simplify_fraction(-6, 8), list(num = -3, den = 4))
  expect_equal(simplify_fraction(6, -8), list(num = -3, den = 4))
  expect_equal(simplify_fraction(0, 5), list(num = 0, den = 5))
  expect_equal(simplify_fraction(12, 4), list(num = 3, den = 1))
})

test_that("frac_add works correctly", {
  result <- frac_add(1, 3, 1, 6)
  expect_equal(result, list(num = 1, den = 2))

  result <- frac_add(2, 5, 1, 3)
  expect_equal(result, list(num = 11, den = 15))
})

test_that("frac_sub works correctly", {
  result <- frac_sub(3, 4, 1, 6)
  expect_equal(result, list(num = 7, den = 12))
})

test_that("frac_mul works correctly", {
  result <- frac_mul(2, 3, 3, 4)
  expect_equal(result, list(num = 1, den = 2))
})

test_that("frac_div works correctly", {
  result <- frac_div(2, 3, 4, 5)
  expect_equal(result, list(num = 5, den = 6))
})

test_that("choose_safe works correctly", {
  expect_equal(choose_safe(8, 3), 56)
  expect_equal(choose_safe(5, 0), 1)
  expect_equal(choose_safe(5, 5), 1)
  expect_equal(choose_safe(10, 1), 10)
})

test_that("perm works correctly", {
  expect_equal(perm(5, 3), 60)
  expect_equal(perm(5, 0), 1)
  expect_equal(perm(5, 1), 5)
})
