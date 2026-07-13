"""
Generator for the calc-deriv-power walkthrough.

Returns template variables for a power rule differentiation problem:
  f(x) = ax^n  where a ∈ [-8, 8] \ {0, 1, -1}, n ∈ [2, 7]

Derived:
  new_coeff = a * n
  new_exp   = n - 1

Display strings handle edge cases:
  display_original:   always 'ax^{n}' (since a is never ±1)
  display_derivative: handles new_exp == 1 (omit ^1), new_coeff == ±1 (omit the 1)

Distinctness constraint (CRITICAL for Step 1 multiple-choice):
  Step 1 presents {n}, {a}, {new_coeff}, {new_exp} as the four MC options.
  If any two of these share the same numeric value, the student sees duplicate
  options and cannot distinguish them. We therefore require all four to be
  distinct, and regenerate if any collision occurs. The most common collision
  is a == n (e.g. a=3, n=3 → options include two 3s), which is why a != n
  is the primary guard.
"""
import random

_VALID_A = [i for i in range(-8, 9) if i not in (0, 1, -1)]


def _display_derivative(new_coeff: int, new_exp: int) -> str:
    if new_exp == 1:
        if new_coeff == 1:
            return 'x'
        if new_coeff == -1:
            return '-x'
        return f'{new_coeff}x'
    if new_coeff == 1:
        return f'x^{{{new_exp}}}'
    if new_coeff == -1:
        return f'-x^{{{new_exp}}}'
    return f'{new_coeff}x^{{{new_exp}}}'


def generate() -> dict:
    # Regenerate until all four MC option values are distinct.
    # Primary constraint: a != n (prevents the most common duplicate).
    # Full constraint: len({n, a, new_coeff, new_exp}) == 4.
    while True:
        a = random.choice(_VALID_A)
        n = random.randint(2, 7)
        new_coeff = a * n
        new_exp = n - 1
        if len({n, a, new_coeff, new_exp}) == 4:
            break

    display_original = f'{a}x^{{{n}}}'
    display_derivative = _display_derivative(new_coeff, new_exp)

    return {
        'a': a,
        'n': n,
        'new_coeff': new_coeff,
        'new_exp': new_exp,
        'abs_a': abs(a),
        'abs_new_coeff': abs(new_coeff),
        'display_original': display_original,
        'display_derivative': display_derivative,
    }
