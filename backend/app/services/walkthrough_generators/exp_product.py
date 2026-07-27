"""
Generator for the exp-product walkthrough.

Product rule for exponents with integer coefficients:
    (a x^m)(b x^n) = (a*b) x^(m+n)

Constraints:
  - coefficients a, b ∈ [2, 5] (>= 2 so the coefficient always shows and the
    "multiply the coefficients" step is non-trivial; never 1, so no `1x` artifact)
  - exponents m, n ∈ [2, 6]
  - new_exp = m + n ∈ [4, 12] (always >= 2, so the final power is never x^1 or x^0
    and the exact_form answer is always the clean form  Nx^{K})
  - new_coeff = a * b ∈ [4, 25]

Display strings are built in Python so the exponent braces are literal:
  display_original = "(2x^{3})(4x^{5})"     (the problem)
  display_answer   = "8x^{8}"               (exact_form target, never contains '.')

MC option text is structurally distinct on every draw, so no distinctness guard
is needed. The numeric-step distractor conditions use the safe expression grammar.

Returned variables:
  a, b               coefficients of the two factors
  m, n               exponents of the two factors
  new_coeff          a * b (product of the coefficients)
  new_exp            m + n (sum of the exponents)
  sum_coeff          a + b (the "added the coefficients" distractor for step 3)
  prod_exp           m * n (the "multiplied the exponents" distractor for step 2)
  display_original   LaTeX for the unsimplified product
  display_answer     LaTeX for the simplified power (exact_form target)
"""
import random


def generate() -> dict:
    a = random.randint(2, 5)
    b = random.randint(2, 5)
    m = random.randint(2, 6)
    n = random.randint(2, 6)

    new_coeff = a * b
    new_exp = m + n

    display_original = f'({a}x^{{{m}}})({b}x^{{{n}}})'
    display_answer = f'{new_coeff}x^{{{new_exp}}}'

    return {
        'a': a,
        'b': b,
        'm': m,
        'n': n,
        'new_coeff': new_coeff,
        'new_exp': new_exp,
        'sum_coeff': a + b,
        'prod_exp': m * n,
        'display_original': display_original,
        'display_answer': display_answer,
    }
