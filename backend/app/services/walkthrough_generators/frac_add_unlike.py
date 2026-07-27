"""
Generator for the frac-add-unlike walkthrough.

Add or subtract two proper fractions with UNLIKE denominators, then simplify.

Constraints:
  - b, d ∈ [2, 9], b != d, with a manageable LCD (<= 40)
  - proper fractions: a ∈ [1, b-1], c ∈ [1, d-1]
  - subtraction keeps the result strictly positive (n1 > n2)
  - the combined fraction does NOT reduce to an integer (simp_den != 1) so the
    final answer is a genuine simplified fraction the strict form can check

Returned variables:
  a, b, c, d        the two fractions a/b (op) c/d
  op                '+' or '-'
  op_word           'plus' or 'minus' (grammatical prose)
  lcd               least common denominator = lcm(b, d)
  m1, m2            multipliers lcd//b and lcd//d
  n1, n2            converted numerators a*m1 and c*m2
  total             n1 (op) n2  (numerator over the LCD before simplifying)
  gcf_final         gcd(total, lcd)
  simp_num, simp_den   total/gcf_final over lcd/gcf_final (simplified answer)
  prod_bd           b*d (the "product, not least" distractor for step 1)
"""
import random
from math import gcd


def _lcm(x, y):
    return x * y // gcd(x, y)


def generate() -> dict:
    for _ in range(5000):
        b = random.randint(2, 9)
        d = random.randint(2, 9)
        if b == d:
            continue
        lcd = _lcm(b, d)
        if lcd > 40:
            continue

        a = random.randint(1, b - 1)
        c = random.randint(1, d - 1)
        op = random.choice(['+', '-'])

        m1, m2 = lcd // b, lcd // d
        n1, n2 = a * m1, c * m2

        if op == '-':
            if n1 <= n2:
                continue  # keep the result strictly positive
            total = n1 - n2
        else:
            total = n1 + n2

        if total == 0:
            continue

        g = gcd(total, lcd)
        simp_num, simp_den = total // g, lcd // g
        if simp_den == 1:
            continue  # avoid an integer result — need a real simplified fraction

        return {
            'a': a, 'b': b, 'c': c, 'd': d,
            'op': op,
            'op_word': 'plus' if op == '+' else 'minus',
            'lcd': lcd,
            'm1': m1, 'm2': m2,
            'n1': n1, 'n2': n2,
            'total': total,
            'gcf_final': g,
            'simp_num': simp_num,
            'simp_den': simp_den,
            'prod_bd': b * d,
        }

    # Fallback: 1/2 + 1/3 = 5/6
    return {
        'a': 1, 'b': 2, 'c': 1, 'd': 3,
        'op': '+', 'op_word': 'plus',
        'lcd': 6, 'm1': 3, 'm2': 2, 'n1': 3, 'n2': 2,
        'total': 5, 'gcf_final': 1, 'simp_num': 5, 'simp_den': 6,
        'prod_bd': 6,
    }
