"""
Generator for the frac-simplify walkthrough.

Returns template variables for a fraction-simplification problem:
  numerator, denominator   — the unsimplified fraction
  gcf                      — their greatest common factor
  simplified_num/den       — the reduced form
  smallest_common_factor   — smallest prime factor of gcf (used in feedback)
"""
import random
from math import gcd


def _smallest_prime_factor(n: int) -> int:
    if n < 2:
        return n
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return i
    return n


def generate() -> dict:
    for _ in range(2000):
        numerator = random.randint(4, 48)
        denominator = random.randint(4, 48)
        g = gcd(numerator, denominator)
        if g <= 1:
            continue
        simplified_num = numerator // g
        simplified_den = denominator // g
        # Require a non-trivial simplified fraction
        if simplified_den == 1 or simplified_num == simplified_den:
            continue
        smallest_common = _smallest_prime_factor(g)
        break
    else:
        # Safe fallback: 18/24 = 3/4, GCF=6
        numerator, denominator = 18, 24
        g = gcd(numerator, denominator)
        simplified_num = numerator // g
        simplified_den = denominator // g
        smallest_common = _smallest_prime_factor(g)

    return {
        'numerator': numerator,
        'denominator': denominator,
        'gcf': g,
        'simplified_num': simplified_num,
        'simplified_den': simplified_den,
        'smallest_common_factor': smallest_common,
    }
