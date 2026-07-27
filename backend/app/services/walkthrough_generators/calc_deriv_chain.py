"""
Generator for the calc-deriv-chain walkthrough (the chain rule).

Returns template variables for a chain-rule differentiation problem of the form:
    f(x) = (a*x + b)^n
whose derivative, by the chain rule, is:
    f'(x) = n * a * (a*x + b)^(n-1)

Parameter ranges (chosen so every number stays clean and positive):
    a in [2, 5]   (never 1, so the inner "a x" never needs a hidden coefficient)
    b in [1, 6]   (always positive, so the inner term is always "a x + b")
    n in [2, 5]

Derived:
    coeff   = n * a          (the derivative's leading coefficient)
    new_exp = n - 1          (the reduced exponent)

Display strings handle the new_exp == 1 edge case (drop the "^1"):
    display_derivative:  "8(2x+3)^{2}"  when new_exp >= 2
                         "4(2x+3)"      when new_exp == 1

Because a >= 2, coeff = n*a is always >= 4, so there is never a coefficient
artifact (no leading 1 to strip). Because b >= 1, the inner term is always
"a x + b" with a genuine "+ b", so there is no sign artifact either.

Multiple-choice steps (1 and 6) use structurally-distinct TEXT options, so they
are unique for every draw regardless of the sampled numbers — no distinctness
guard is required.
"""
import random


def _display_derivative(coeff: int, a: int, b: int, new_exp: int) -> str:
    inner = f'{a}x+{b}'
    if new_exp == 1:
        return f'{coeff}({inner})'
    return f'{coeff}({inner})^{{{new_exp}}}'


def generate() -> dict:
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    n = random.randint(2, 5)

    coeff = n * a
    new_exp = n - 1

    display_inner = f'{a}x + {b}'
    display_original = f'({a}x + {b})^{{{n}}}'
    display_derivative = _display_derivative(coeff, a, b, new_exp)

    return {
        'a': a,
        'b': b,
        'n': n,
        'coeff': coeff,
        'new_exp': new_exp,
        'display_inner': display_inner,
        'display_original': display_original,
        'display_derivative': display_derivative,
    }
