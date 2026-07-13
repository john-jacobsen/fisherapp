"""
Generator for the linalg-row-reduce walkthrough.

Produces a 2×2 linear system that row-reduces cleanly with a single
integer elimination step R2 ← R2 − (a2/a1)·R1.

System: a1·x + b1·y = c1  and  a2·x + b2·y = c2

Constraints:
  - a1, b1, b2 ∈ [-6, 6] \ {0}
  - a2 = a1 × multiplier, so a1 | a2 and |a2| ≤ 6
  - multiplier is a nonzero integer
  - new_b2 = b2 − multiplier·b1 ≠ 0  (guarantees unique solution)
  - det = a1·new_b2 ≠ 0  (automatic from above)
  - x_sol, y_sol ∈ [-5, 5]  (integer solutions, generated first for exact arithmetic)
  - {multiplier, a2, a1} all distinct  (Step 2 MC options must be unique)
  - a1 ≠ b1  (distinguishes the "correct matrix" option from the "swapped columns" distractor)
  - |c1|, |c2| ≤ 30  (keeps displayed numbers readable)

Approach: generate solutions first, then build the system so that
  c1 = a1·x_sol + b1·y_sol  and  c2 = a2·x_sol + b2·y_sol.
  After elimination: new_c2 = new_b2·y_sol — always an exact integer.
"""
import random


def generate() -> dict:
    for _ in range(5000):
        x_sol = random.randint(-5, 5)
        y_sol = random.randint(-5, 5)

        a1 = random.choice([i for i in range(-6, 7) if i != 0])

        max_mult = 6 // abs(a1)
        if max_mult < 1:
            continue
        possible_mults = [i for i in range(-max_mult, max_mult + 1) if i != 0]
        multiplier = random.choice(possible_mults)
        a2 = a1 * multiplier

        # MC distinctness for Step 2: {multiplier, a2, a1} must all differ
        if len({multiplier, a2, a1}) < 3:
            continue

        b1 = random.choice([i for i in range(-6, 7) if i != 0])

        # a1 ≠ b1 keeps the "swapped columns" MC distractor visually distinct
        if a1 == b1:
            continue

        # b2 must keep new_b2 ≠ 0  (b2 ≠ multiplier·b1)
        b2_candidates = [i for i in range(-6, 7) if i != 0 and i != multiplier * b1]
        if not b2_candidates:
            continue
        b2 = random.choice(b2_candidates)

        new_b2 = b2 - multiplier * b1
        if new_b2 == 0:
            continue  # safety guard

        c1 = a1 * x_sol + b1 * y_sol
        c2 = a2 * x_sol + b2 * y_sol
        new_c2 = c2 - multiplier * c1  # equals new_b2 * y_sol — always exact

        # Keep displayed values readable
        if abs(c1) > 30 or abs(c2) > 30:
            continue

        return {
            'a1': a1, 'b1': b1, 'c1': c1,
            'a2': a2, 'b2': b2, 'c2': c2,
            'multiplier': multiplier,
            'new_b2': new_b2,
            'new_c2': new_c2,
            'x_sol': x_sol,
            'y_sol': y_sol,
            'abs_multiplier': abs(multiplier),
        }

    # Fallback: 2x + 3y = 8, 4x + y = 6 → multiplier=2, x=1, y=2
    # new_b2 = 1 − 2·3 = −5,  new_c2 = 6 − 2·8 = −10
    return {
        'a1': 2, 'b1': 3, 'c1': 8,
        'a2': 4, 'b2': 1, 'c2': 6,
        'multiplier': 2,
        'new_b2': -5,
        'new_c2': -10,
        'x_sol': 1,
        'y_sol': 2,
        'abs_multiplier': 2,
    }
