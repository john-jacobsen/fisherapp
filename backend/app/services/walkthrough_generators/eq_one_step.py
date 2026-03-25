"""
Generator for the eq-one-step walkthrough.

Produces a one-step linear equation of the form  ax = b  where:
  - a is a non-zero integer in [-12, 12], not ±1 (so division is non-trivial)
  - solution = b / a is a non-zero integer in [-10, 10]
  - b = a * solution

Returns:
  a              — the coefficient of x (may be negative)
  b              — the right-hand side
  solution       — the integer solution
  abs_a          — |a| (useful in feedback messages)
  operation_name — "multiplication"
  operation_inverse — "division"
"""
import random

_VALID_A = [i for i in range(-12, 13) if i not in (0, 1, -1)]


def generate() -> dict:
    for _ in range(2000):
        a = random.choice(_VALID_A)
        solution = random.randint(-10, 10)
        if solution == 0:
            continue          # skip x = 0 (trivial)
        b = a * solution
        break
    else:
        # Safe fallback
        a, b, solution = 3, 12, 4

    return {
        'a': a,
        'b': b,
        'solution': solution,
        'abs_a': abs(a),
        'operation_name': 'multiplication',
        'operation_inverse': 'division',
    }
