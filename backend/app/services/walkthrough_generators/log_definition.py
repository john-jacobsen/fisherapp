"""
Generator for the log-definition walkthrough.

Teaches the definition of a logarithm:  log_b(x) = y  means  b^y = x.

The walkthrough uses THREE independent clean examples so each step tests the
idea on fresh numbers:

  pair A  (base_a, exp_a, val_a)   step 2 — evaluate log_{base_a}(val_a)
  pair B  (base_b, exp_b, val_b)   step 3 — evaluate log_{base_b}(val_b)
  pair C  (base_c, exp_c, val_c)   step 4 — write the LOG form of base_c^exp_c = val_c

Every pair is a clean exact power: val = base ** exp with base in {2, 3, 5, 10}
and exp in {2, 3, 4}, so every logarithm evaluates to a whole exponent.

The three bases are drawn WITHOUT replacement so the examples feel distinct.

Step 1 (definition) and step 5 (conceptual close) are multiple-choice with
fixed lettered / prose options, so their options are unique on every draw
regardless of the numbers.

Returned variables (all int):
  base_a, exp_a, val_a
  base_b, exp_b, val_b
  base_c, exp_c, val_c
"""
import random


def generate() -> dict:
    bases = random.sample([2, 3, 5, 10], 3)   # distinct bases, no replacement
    base_a, base_b, base_c = bases

    exp_a = random.randint(2, 4)
    exp_b = random.randint(2, 4)
    exp_c = random.randint(2, 4)

    return {
        'base_a': base_a, 'exp_a': exp_a, 'val_a': base_a ** exp_a,
        'base_b': base_b, 'exp_b': exp_b, 'val_b': base_b ** exp_b,
        'base_c': base_c, 'exp_c': exp_c, 'val_c': base_c ** exp_c,
    }
