"""
Generator for the prob-bayes walkthrough.

Uses the natural frequency (hypothetical population) approach.
All intermediate counts — num_diseased, true_positives, false_positives —
must be whole numbers.  The generator picks parameters from curated lists
and rejects combinations where the arithmetic doesn't divide evenly.

Returned variables:
  prev_num, prev_den      Disease prevalence as a simple fraction prev_num/prev_den
  sensitivity             True positive rate as a percentage (e.g. 95)
  specificity             True negative rate as a percentage (e.g. 90)
  false_pos_rate          100 - specificity  (false positive rate as a %)
  population              10000 (fixed)
  num_diseased            population * prev_num / prev_den  (integer)
  num_healthy             population - num_diseased          (integer)
  true_positives          num_diseased * sensitivity / 100   (integer)
  false_positives         num_healthy * false_pos_rate / 100 (integer)
  total_positives         true_positives + false_positives   (integer)
  ppv_percent             100 * true_positives / total_positives, rounded to 1 dp
  ppv_fraction_num        numerator of PPV in lowest terms
  ppv_fraction_den        denominator of PPV in lowest terms
"""
import random
from math import gcd

POPULATION = 10000

# Prevalences (prev_num, prev_den) that divide evenly into 10000.
_PREVALENCES = [(1, 100), (1, 200), (1, 500), (2, 100), (5, 1000)]

_SENSITIVITIES = [90, 95, 98, 99]
_SPECIFICITIES = [90, 95, 98, 99]


def generate() -> dict:
    for _ in range(10000):
        prev_num, prev_den = random.choice(_PREVALENCES)
        sensitivity = random.choice(_SENSITIVITIES)
        specificity = random.choice(_SPECIFICITIES)
        false_pos_rate = 100 - specificity

        # num_diseased must be a whole number
        if (POPULATION * prev_num) % prev_den != 0:
            continue
        num_diseased = (POPULATION * prev_num) // prev_den
        num_healthy = POPULATION - num_diseased

        # true_positives must be a whole number
        if (num_diseased * sensitivity) % 100 != 0:
            continue
        true_positives = (num_diseased * sensitivity) // 100

        # false_positives must be a whole number
        if (num_healthy * false_pos_rate) % 100 != 0:
            continue
        false_positives = (num_healthy * false_pos_rate) // 100

        total_positives = true_positives + false_positives
        if total_positives == 0:
            continue

        ppv_percent = round(true_positives * 100 / total_positives, 1)

        # Problem should be interesting: not trivially 0% or 100%
        if ppv_percent <= 0 or ppv_percent >= 100:
            continue

        g = gcd(true_positives, total_positives)
        ppv_fraction_num = true_positives // g
        ppv_fraction_den = total_positives // g

        return {
            'prev_num': prev_num,
            'prev_den': prev_den,
            'sensitivity': sensitivity,
            'specificity': specificity,
            'false_pos_rate': false_pos_rate,
            'population': POPULATION,
            'num_diseased': num_diseased,
            'num_healthy': num_healthy,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'total_positives': total_positives,
            'ppv_percent': ppv_percent,
            'ppv_fraction_num': ppv_fraction_num,
            'ppv_fraction_den': ppv_fraction_den,
        }

    # Fallback: 1% prevalence, 95% sensitivity, 90% specificity
    # → 100 diseased, 9900 healthy, 95 TP, 990 FP, 1085 total, PPV ≈ 8.8%
    # gcd(95, 1085) = 5  →  19/217
    return {
        'prev_num': 1, 'prev_den': 100,
        'sensitivity': 95, 'specificity': 90, 'false_pos_rate': 10,
        'population': 10000,
        'num_diseased': 100, 'num_healthy': 9900,
        'true_positives': 95, 'false_positives': 990,
        'total_positives': 1085,
        'ppv_percent': 8.8,
        'ppv_fraction_num': 19, 'ppv_fraction_den': 217,
    }
