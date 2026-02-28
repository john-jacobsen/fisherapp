"""
On-the-fly problem generator service.
Generates fresh, randomized problems at request time for each supported node.

Each generator returns a dict:
  {
    "problem_text":    str,   # displayed to student
    "correct_answer":  str,   # compared by answer_checker
    "answer_type":     str,   # "symbolic" | "numeric" | "multiple_choice"
    "difficulty":      float,
  }
"""
import random
from fractions import Fraction
from math import factorial as math_factorial, comb as math_comb, gcd


# ─── Fraction generators ──────────────────────────────────────────────────────

def _gen_frac_simplify():
    factor = random.randint(2, 7)
    a = random.randint(1, 9) * factor
    b = random.randint(2, 10) * factor
    while a == b:
        b = random.randint(2, 10) * factor
    f = Fraction(a, b)
    return {
        "problem_text": f"Simplify: \\(\\frac{{{a}}}{{{b}}}\\)",
        "correct_answer": f"{f.numerator}/{f.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.3,
    }


def _gen_frac_add_like():
    d = random.randint(3, 12)
    a = random.randint(1, d - 1)
    b = random.randint(1, d - 1)
    op = random.choice(['+', '-'])
    result = Fraction(a, d) + Fraction(b, d) if op == '+' else Fraction(a, d) - Fraction(b, d)
    if result < 0:
        a, b = b, a
        result = abs(result)
    return {
        "problem_text": f"Calculate: \\(\\frac{{{a}}}{{{d}}} {op} \\frac{{{b}}}{{{d}}}\\)",
        "correct_answer": f"{result.numerator}/{result.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.3,
    }


def _gen_frac_common_denom():
    pairs = [(2, 3), (3, 4), (4, 6), (2, 5), (3, 5), (4, 5), (6, 9), (2, 7), (3, 8)]
    a, b = random.choice(pairs)
    lcd = a * b // gcd(a, b)
    return {
        "problem_text": f"Find the LCD of \\(\\frac{{1}}{{{a}}}\\) and \\(\\frac{{1}}{{{b}}}\\).",
        "correct_answer": str(lcd),
        "answer_type": "numeric",
        "difficulty": 0.3,
    }


def _gen_frac_add_unlike():
    a = Fraction(random.randint(1, 5), random.randint(2, 8))
    b = Fraction(random.randint(1, 5), random.randint(2, 8))
    while a.denominator == b.denominator:
        b = Fraction(random.randint(1, 5), random.randint(2, 8))
    op = random.choice(['+', '-'])
    result = a + b if op == '+' else a - b
    if result < 0:
        op = '+' if op == '-' else '-'
        result = abs(result)
        a, b = b, a
    return {
        "problem_text": f"Calculate: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} {op} \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
        "correct_answer": f"{result.numerator}/{result.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.5,
    }


def _gen_frac_multiply():
    a = Fraction(random.randint(1, 6), random.randint(2, 8))
    b = Fraction(random.randint(1, 6), random.randint(2, 8))
    result = a * b
    return {
        "problem_text": f"Multiply: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\times \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
        "correct_answer": f"{result.numerator}/{result.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.5,
    }


def _gen_frac_divide():
    a = Fraction(random.randint(1, 6), random.randint(2, 8))
    b = Fraction(random.randint(1, 6), random.randint(2, 8))
    result = a / b
    return {
        "problem_text": f"Divide: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\div \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
        "correct_answer": f"{result.numerator}/{result.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.5,
    }


# ─── Order of operations ──────────────────────────────────────────────────────

def _gen_order_pemdas():
    choice = random.randint(0, 2)
    if choice == 0:
        a, b, c = random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)
        return {
            "problem_text": f"Evaluate: \\({a} + {b} \\times {c}\\)",
            "correct_answer": str(a + b * c),
            "answer_type": "numeric", "difficulty": 0.4,
        }
    elif choice == 1:
        b = random.randint(2, 4)
        a = b * random.randint(2, 6)
        return {
            "problem_text": f"Evaluate: \\({a} \\div {b}\\)",
            "correct_answer": str(a // b),
            "answer_type": "numeric", "difficulty": 0.3,
        }
    else:
        a, b = random.randint(2, 5), random.randint(1, 9)
        return {
            "problem_text": f"Evaluate: \\({a}^2 + {b}\\)",
            "correct_answer": str(a ** 2 + b),
            "answer_type": "numeric", "difficulty": 0.4,
        }


def _gen_order_nested():
    a, b, c = random.randint(2, 6), random.randint(2, 6), random.randint(2, 4)
    return {
        "problem_text": f"Evaluate: \\(({a} + {b}) \\times {c}\\)",
        "correct_answer": str((a + b) * c),
        "answer_type": "numeric", "difficulty": 0.5,
    }


# ─── Exponents ────────────────────────────────────────────────────────────────

def _gen_exp_product():
    a, b = random.randint(2, 6), random.randint(2, 6)
    return {
        "problem_text": f"Simplify: \\(x^{{{a}}} \\cdot x^{{{b}}}\\)",
        "correct_answer": f"x**{a + b}",
        "answer_type": "symbolic", "difficulty": 0.4,
    }


def _gen_exp_power():
    a, b = random.randint(2, 4), random.randint(2, 4)
    return {
        "problem_text": f"Simplify: \\((x^{{{a}}})^{{{b}}}\\)",
        "correct_answer": f"x**{a * b}",
        "answer_type": "symbolic", "difficulty": 0.4,
    }


def _gen_exp_negative():
    base = random.randint(2, 5)
    exp = random.randint(1, 3)
    result = Fraction(1, base ** exp)
    return {
        "problem_text": f"Evaluate: \\({base}^{{-{exp}}}\\)",
        "correct_answer": f"{result.numerator}/{result.denominator}",
        "answer_type": "symbolic", "difficulty": 0.5,
    }


def _gen_exp_combined():
    a, b = random.randint(3, 6), random.randint(1, 3)
    net = a - b
    ans = f"x**{net}" if net != 1 else "x"
    return {
        "problem_text": f"Simplify: \\(\\frac{{x^{{{a}}}}}{{x^{{{b}}}}}\\)",
        "correct_answer": ans,
        "answer_type": "symbolic", "difficulty": 0.6,
    }


# ─── Equations ────────────────────────────────────────────────────────────────

def _gen_eq_one_step():
    x = random.randint(1, 15)
    if random.choice([True, False]):
        b = random.randint(1, 12)
        return {
            "problem_text": f"Solve for \\(x\\): \\(x + {b} = {x + b}\\)",
            "correct_answer": str(x), "answer_type": "numeric", "difficulty": 0.3,
        }
    else:
        a = random.randint(2, 8)
        return {
            "problem_text": f"Solve for \\(x\\): \\({a}x = {a * x}\\)",
            "correct_answer": str(x), "answer_type": "numeric", "difficulty": 0.3,
        }


def _gen_eq_two_step():
    a = random.randint(2, 6)
    x = random.randint(1, 10)
    b = random.randint(1, 10)
    c = a * x + b
    return {
        "problem_text": f"Solve for \\(x\\): \\({a}x + {b} = {c}\\)",
        "correct_answer": str(x), "answer_type": "numeric", "difficulty": 0.5,
    }


def _gen_eq_fractions():
    a = random.randint(2, 5)
    x = random.randint(2, 10)
    return {
        "problem_text": f"Solve for \\(x\\): \\(\\frac{{{a}x}}{{{a}}} = {x}\\)",
        "correct_answer": str(x), "answer_type": "numeric", "difficulty": 0.6,
    }


def _gen_eq_distribution():
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    x = random.randint(1, 8)
    c = a * (x + b)
    return {
        "problem_text": f"Solve for \\(x\\): \\({a}(x + {b}) = {c}\\)",
        "correct_answer": str(x), "answer_type": "numeric", "difficulty": 0.6,
    }


# ─── Logarithms ───────────────────────────────────────────────────────────────

def _gen_log_exponential():
    base = random.randint(2, 5)
    exp = random.randint(2, 4)
    return {
        "problem_text": f"Evaluate: \\({base}^{{{exp}}}\\)",
        "correct_answer": str(base ** exp), "answer_type": "numeric", "difficulty": 0.3,
    }


def _gen_log_definition():
    pairs = [(2, 4, 2), (2, 8, 3), (2, 16, 4), (3, 9, 2), (3, 27, 3),
             (10, 100, 2), (5, 25, 2), (10, 1000, 3)]
    base, val, result = random.choice(pairs)
    return {
        "problem_text": f"Evaluate: \\(\\log_{{{base}}}({val})\\)",
        "correct_answer": str(result), "answer_type": "numeric", "difficulty": 0.5,
    }


def _gen_log_rules():
    combos = [(2, 4, 8, 5), (3, 9, 27, 5), (2, 8, 4, 5), (2, 4, 16, 6)]
    base, a, b, result = random.choice(combos)
    return {
        "problem_text": f"Simplify: \\(\\log_{{{base}}}({a}) + \\log_{{{base}}}({b})\\)",
        "correct_answer": str(result), "answer_type": "numeric", "difficulty": 0.6,
    }


# ─── Summation ────────────────────────────────────────────────────────────────

def _gen_sum_sigma():
    n = random.randint(3, 8)
    total = n * (n + 1) // 2
    return {
        "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{n}}} i\\)",
        "correct_answer": str(total), "answer_type": "numeric", "difficulty": 0.5,
    }


def _gen_sum_arithmetic():
    n = random.randint(4, 12)
    total = n * (n + 1) // 2
    return {
        "problem_text": f"Find the sum: \\(1 + 2 + 3 + \\cdots + {n}\\)",
        "correct_answer": str(total), "answer_type": "numeric", "difficulty": 0.5,
    }


def _gen_sum_nested():
    m = random.randint(2, 4)
    n = random.randint(2, 4)
    total = (m * (m + 1) // 2) * (n * (n + 1) // 2)
    return {
        "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{m}}} \\sum_{{j=1}}^{{{n}}} i \\cdot j\\)",
        "correct_answer": str(total), "answer_type": "numeric", "difficulty": 0.7,
    }


# ─── Combinatorics ────────────────────────────────────────────────────────────

def _gen_comb_counting():
    a, b = random.randint(2, 6), random.randint(2, 6)
    return {
        "problem_text": f"A bag has {a} colors and {b} sizes. How many color-size combinations are possible?",
        "correct_answer": str(a * b), "answer_type": "numeric", "difficulty": 0.3,
    }


def _gen_comb_permutations():
    pairs = [(4, 4), (5, 3), (6, 2), (5, 5), (4, 2)]
    n, r = random.choice(pairs)
    result = math_factorial(n) // math_factorial(n - r)
    return {
        "problem_text": f"How many ways can {r} items be chosen in order from {n} distinct items?",
        "correct_answer": str(result), "answer_type": "numeric", "difficulty": 0.5,
    }


def _gen_comb_combinations():
    pairs = [(5, 2), (6, 2), (7, 3), (8, 3), (10, 2), (5, 3)]
    n, r = random.choice(pairs)
    result = math_comb(n, r)
    return {
        "problem_text": f"Calculate \\(C({n}, {r})\\) — the number of ways to choose {r} items from {n}.",
        "correct_answer": str(result), "answer_type": "numeric", "difficulty": 0.5,
    }


# ─── Geometric sequences ──────────────────────────────────────────────────────

def _gen_geo_sequences():
    a = random.randint(1, 5)
    r = random.randint(2, 4)
    n = random.randint(4, 6)
    term = a * r ** (n - 1)
    return {
        "problem_text": f"A geometric sequence has first term {a} and ratio {r}. Find the {n}th term.",
        "correct_answer": str(term), "answer_type": "numeric", "difficulty": 0.5,
    }


def _gen_geo_finite():
    a = random.randint(1, 4)
    r = random.randint(2, 3)
    n = random.randint(3, 5)
    total = a * (r ** n - 1) // (r - 1)
    return {
        "problem_text": f"Find the sum of the first {n} terms of a geometric series with \\(a={a}\\), \\(r={r}\\).",
        "correct_answer": str(total), "answer_type": "numeric", "difficulty": 0.6,
    }


# ─── Node → generator mapping ─────────────────────────────────────────────────

GENERATORS = {
    "frac-simplify":     _gen_frac_simplify,
    "frac-add-like":     _gen_frac_add_like,
    "frac-common-denom": _gen_frac_common_denom,
    "frac-add-unlike":   _gen_frac_add_unlike,
    "frac-multiply":     _gen_frac_multiply,
    "frac-divide":       _gen_frac_divide,
    "order-pemdas":      _gen_order_pemdas,
    "order-nested":      _gen_order_nested,
    "exp-product":       _gen_exp_product,
    "exp-power":         _gen_exp_power,
    "exp-negative":      _gen_exp_negative,
    "exp-combined":      _gen_exp_combined,
    "eq-one-step":       _gen_eq_one_step,
    "eq-two-step":       _gen_eq_two_step,
    "eq-fractions":      _gen_eq_fractions,
    "eq-distribution":   _gen_eq_distribution,
    "log-exponential":   _gen_log_exponential,
    "log-definition":    _gen_log_definition,
    "log-rules":         _gen_log_rules,
    "sum-sigma":         _gen_sum_sigma,
    "sum-arithmetic":    _gen_sum_arithmetic,
    "sum-nested":        _gen_sum_nested,
    "comb-counting":     _gen_comb_counting,
    "comb-permutations": _gen_comb_permutations,
    "comb-combinations": _gen_comb_combinations,
    "geo-sequences":     _gen_geo_sequences,
    "geo-finite":        _gen_geo_finite,
}


def generate_problem(node_id: str) -> dict | None:
    """
    Generate a fresh problem for the given node_id.
    Returns a dict with problem_text, correct_answer, answer_type, difficulty.
    Returns None if no generator exists for this node.
    """
    gen = GENERATORS.get(node_id)
    if gen is None:
        return None
    try:
        return gen()
    except Exception:
        return None
