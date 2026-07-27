"""
Generator for the eq-two-step walkthrough.

Produces a two-step linear equation of the form  a*x + b = c  where:
  - a (the coefficient of x) is an integer in [2, 9]
  - b (the constant added) is a positive integer in [1, 9], so the equation
    always displays as "ax + b = c" and the first move is always "subtract b"
  - solution is a non-zero integer in [-8, 8]
  - c = a * solution + b, so every intermediate step is clean integer arithmetic

Returned variables (all int/str):
  a            coefficient of x
  b            constant added on the left
  c            right-hand side
  solution     the integer solution for x
  c_minus_b    c - b  (the right side after subtracting b; equals a*solution)
  c_plus_b     c + b  (distractor: student adds b instead of subtracting)
"""
import random


def generate() -> dict:
    for _ in range(2000):
        a = random.randint(2, 9)
        b = random.randint(1, 9)
        solution = random.randint(-8, 8)
        if solution == 0:
            continue                      # skip x = 0 (trivial)
        c = a * solution + b
        break
    else:
        # Safe fallback: 2x + 3 = 11  ->  x = 4
        a, b, solution = 2, 3, 4
        c = a * solution + b

    return {
        'a': a,
        'b': b,
        'c': c,
        'solution': solution,
        'c_minus_b': c - b,
        'c_plus_b': c + b,
    }
