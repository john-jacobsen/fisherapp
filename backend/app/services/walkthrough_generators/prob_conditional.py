"""
Generator for the prob-conditional walkthrough.

Conditional probability from a two-way count table:

    P(A | B) = P(A ∩ B) / P(B) = #(A ∩ B) / #(B)

Scenario: a school surveys students on two yes/no attributes — owns a dog (B)
and plays a sport (A). The four cell counts are generated so that:

  - every cell is a positive integer (a genuine two-way table, no empty cells)
  - the conditioning group B is strictly larger than A∩B, so the final
    probability is a proper, non-integer fraction (denominator > 1)
  - #(A∩B) and #(B) share a common factor > 1, so simplifying the fraction is a
    real step; after dividing by the GCF the answer is fully reduced
    (gcd(simp_num, simp_den) == 1) with simp_den > 1 — exactly what the
    simplified_fraction strict form requires (and a decimal probe fails).

Returned variables:
  both          #(A ∩ B)  — dog owners who play a sport
  dog_only      dog owners who do NOT play a sport (B, not A)
  sport_only    sport players who do NOT own a dog (A, not B)
  neither       students in neither group
  count_B       #(B) = both + dog_only          (the conditioning group)
  count_A       #(A) = both + sport_only         (all sport players)
  count_notB    students without a dog = sport_only + neither
  grand_total   everyone surveyed = both + dog_only + sport_only + neither
  gcf           gcd(both, count_B)  (> 1 — the factor to simplify by)
  simp_num      both // gcf         (numerator of the reduced probability)
  simp_den      count_B // gcf      (denominator of the reduced probability, > 1)
"""
import random
from math import gcd


def generate() -> dict:
    for _ in range(5000):
        both = random.randint(2, 15)
        dog_only = random.randint(1, 15)
        count_B = both + dog_only

        gcf = gcd(both, count_B)          # == gcd(both, dog_only)
        if gcf < 2:
            continue                       # need a genuine simplification step

        simp_num = both // gcf
        simp_den = count_B // gcf
        if simp_den < 2:
            continue                       # keep P(A|B) a non-integer fraction
        if gcd(simp_num, simp_den) != 1:   # (guaranteed, but assert the contract)
            continue

        sport_only = random.randint(1, 15)
        neither = random.randint(1, 15)
        count_A = both + sport_only
        count_notB = sport_only + neither
        grand_total = both + dog_only + sport_only + neither

        # Keep the step-3 distractor values (count_A, count_B) distinct from
        # each other and from the correct count so feedback stays unambiguous.
        if count_A == count_B:
            continue

        return {
            'both': both,
            'dog_only': dog_only,
            'sport_only': sport_only,
            'neither': neither,
            'count_B': count_B,
            'count_A': count_A,
            'count_notB': count_notB,
            'grand_total': grand_total,
            'gcf': gcf,
            'simp_num': simp_num,
            'simp_den': simp_den,
        }

    # Deterministic fallback: 6/10 dog owners play a sport → 3/5.
    return {
        'both': 6, 'dog_only': 4, 'sport_only': 5, 'neither': 7,
        'count_B': 10, 'count_A': 11, 'count_notB': 12, 'grand_total': 22,
        'gcf': 2, 'simp_num': 3, 'simp_den': 5,
    }
