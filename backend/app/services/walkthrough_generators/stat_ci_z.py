"""
Generator for the stat-ci-z walkthrough.

Constructs a confidence interval for a population mean using a z-interval
(known population standard deviation, large sample).

Constraints:
  - n is a perfect square from a fixed list so sqrt(n) is a clean integer
  - sigma is divisible by sqrt_n so standard_error is a whole number
  - lower bound > 0

Returned variables:
  xbar             sample mean (integer, 40-200)
  sigma            population standard deviation (integer, 5-30)
  n                sample size (perfect square from [36,49,64,100,144,225,400])
  sqrt_n           integer square root of n
  conf_level       confidence level as percentage (90, 95, or 99)
  z_star           critical z value (1.645, 1.96, or 2.576)
  z_star_index     0-based index of z_star in the MC option list [1.645, 1.96, 2.576, 1.28]
  standard_error   sigma // sqrt_n (whole number)
  margin_of_error  z_star * standard_error, rounded to 2 decimal places
  lower            xbar - margin_of_error
  upper            xbar + margin_of_error
  alpha            100 - conf_level (whole number)
  alpha_half       alpha / 2 (e.g. 2.5 for 95%)
"""
import random
from math import isqrt

_Z_STARS = {90: 1.645, 95: 1.96, 99: 2.576}
# z* scaled to integer thousandths, for exact half-way rounding detection.
_Z_STARS_MILLI = {90: 1645, 95: 1960, 99: 2576}
_Z_STAR_INDICES = {90: 0, 95: 1, 99: 2}
_N_VALUES = [36, 49, 64, 100, 144, 225, 400]
_CONF_LEVELS = [90, 95, 99]


def generate() -> dict:
    for _ in range(10000):
        xbar = random.randint(40, 200)
        sigma = random.randint(5, 30)
        n = random.choice(_N_VALUES)
        conf_level = random.choice(_CONF_LEVELS)

        sqrt_n = isqrt(n)
        if sqrt_n * sqrt_n != n:
            continue

        if sigma % sqrt_n != 0:
            continue

        standard_error = sigma // sqrt_n
        z_star = _Z_STARS[conf_level]

        # Rounding coherence: z* × SE is exact in thousandths. Reject any case
        # whose thousandths digit is 5 — a genuine half-way point where the
        # correct 2-dp rounding is ambiguous (e.g. 1.645×1 = 1.645, which
        # 1.64 and 1.65 BOTH land within the ±0.01 checker tolerance). This
        # only ever fires for 90% (z*=1.645) with an odd standard error;
        # every 95%/99% product already lands cleanly.
        moe_milli = _Z_STARS_MILLI[conf_level] * standard_error
        if moe_milli % 10 == 5:
            continue

        margin_of_error = round(z_star * standard_error, 2)
        lower = round(xbar - margin_of_error, 2)
        upper = round(xbar + margin_of_error, 2)

        if lower <= 0:
            continue

        alpha = 100 - conf_level
        alpha_half = alpha / 2

        return {
            'xbar': xbar,
            'sigma': sigma,
            'n': n,
            'sqrt_n': sqrt_n,
            'conf_level': conf_level,
            'z_star': z_star,
            'z_star_index': _Z_STAR_INDICES[conf_level],
            'standard_error': standard_error,
            'margin_of_error': margin_of_error,
            'lower': lower,
            'upper': upper,
            'alpha': alpha,
            'alpha_half': alpha_half,
        }

    # Fallback: xbar=120, sigma=12, n=36 → sqrt_n=6, SE=2, 95% → MOE=3.92
    return {
        'xbar': 120, 'sigma': 12, 'n': 36, 'sqrt_n': 6,
        'conf_level': 95, 'z_star': 1.96, 'z_star_index': 1,
        'standard_error': 2, 'margin_of_error': 3.92,
        'lower': 116.08, 'upper': 123.92,
        'alpha': 5, 'alpha_half': 2.5,
    }
