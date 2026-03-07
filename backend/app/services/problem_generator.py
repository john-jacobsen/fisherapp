"""
On-the-fly problem generator service.
Generates fresh, randomized problems at request time for each supported node.

Each generator returns a dict:
  {
    "problem_text":    str,   # displayed to student
    "correct_answer":  str,   # compared by answer_checker
    "answer_type":     str,   # "symbolic" | "numeric" | "multiple_choice"
    "difficulty":      float,
    "hints": [
        {"level": 1, "text": "...conceptual hint..."},
        {"level": 2, "text": "...strategic hint with actual numbers..."},
        {"level": 3, "text": "...full worked solution with actual numbers..."},
    ]
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
    actual_gcf = gcd(a, b)
    return {
        "problem_text": f"Simplify: \\(\\frac{{{a}}}{{{b}}}\\)",
        "correct_answer": f"{f.numerator}/{f.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "To simplify a fraction, find a number that divides both the numerator and denominator evenly."},
            {"level": 2, "text": f"Find the greatest common factor (GCF) of {a} and {b}."},
            {"level": 3, "text": f"The GCF of {a} and {b} is {actual_gcf}. Divide both by {actual_gcf}: \\(\\frac{{{a} \\div {actual_gcf}}}{{{b} \\div {actual_gcf}}} = \\frac{{{f.numerator}}}{{{f.denominator}}}\\)"},
        ],
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
        "hints": [
            {"level": 1, "text": "When fractions have the same denominator, just add (or subtract) the numerators and keep the denominator."},
            {"level": 2, "text": f"The denominators are both {d}. {'Add' if op == '+' else 'Subtract'} the numerators: {a} {op} {b}."},
            {"level": 3, "text": f"\\(\\frac{{{a}}}{{{d}}} {op} \\frac{{{b}}}{{{d}}} = \\frac{{{a} {op} {b}}}{{{d}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
        ],
    }


def _gen_frac_common_denom():
    pairs = [(2, 3), (3, 4), (4, 6), (2, 5), (3, 5), (4, 5), (6, 9), (2, 7), (3, 8)]
    a, b = random.choice(pairs)
    lcd = a * b // gcd(a, b)
    a_mults = list(range(a, lcd + 1, a))
    b_mults = list(range(b, lcd + 1, b))
    return {
        "problem_text": f"Find the LCD of \\(\\frac{{1}}{{{a}}}\\) and \\(\\frac{{1}}{{{b}}}\\).",
        "correct_answer": str(lcd),
        "answer_type": "numeric",
        "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "The LCD is the smallest number that is a multiple of both denominators."},
            {"level": 2, "text": f"Find the LCM of {a} and {b}. Think about what multiples they share."},
            {"level": 3, "text": (
                f"Multiples of {a}: {', '.join(map(str, a_mults))}. "
                f"Multiples of {b}: {', '.join(map(str, b_mults))}. "
                f"The LCD is {lcd}."
            )},
        ],
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
    lcd = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    a_new_num = a.numerator * (lcd // a.denominator)
    b_new_num = b.numerator * (lcd // b.denominator)
    return {
        "problem_text": f"Calculate: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} {op} \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
        "correct_answer": f"{result.numerator}/{result.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "To add fractions with different denominators, first find a common denominator."},
            {"level": 2, "text": f"Find the LCD of {a.denominator} and {b.denominator}. Then rewrite both fractions with that denominator."},
            {"level": 3, "text": (
                f"LCD({a.denominator}, {b.denominator}) = {lcd}. "
                f"Rewrite: \\(\\frac{{{a_new_num}}}{{{lcd}}} {op} \\frac{{{b_new_num}}}{{{lcd}}} "
                f"= \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"
            )},
        ],
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
        "hints": [
            {"level": 1, "text": "To multiply fractions, multiply the numerators together and the denominators together."},
            {"level": 2, "text": f"Multiply numerators: {a.numerator} \u00d7 {b.numerator}. Multiply denominators: {a.denominator} \u00d7 {b.denominator}."},
            {"level": 3, "text": f"\\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\times \\frac{{{b.numerator}}}{{{b.denominator}}} = \\frac{{{a.numerator * b.numerator}}}{{{a.denominator * b.denominator}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
        ],
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
        "hints": [
            {"level": 1, "text": "To divide fractions, multiply the first fraction by the reciprocal (flip) of the second."},
            {"level": 2, "text": f"Flip the second fraction: \\(\\frac{{{b.denominator}}}{{{b.numerator}}}\\). Then multiply."},
            {"level": 3, "text": f"\\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\div \\frac{{{b.numerator}}}{{{b.denominator}}} = \\frac{{{a.numerator}}}{{{a.denominator}}} \\times \\frac{{{b.denominator}}}{{{b.numerator}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
        ],
    }


# ─── Order of operations ──────────────────────────────────────────────────────

def _gen_order_pemdas():
    choice = random.randint(0, 2)
    if choice == 0:
        a, b, c = random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)
        return {
            "problem_text": f"Evaluate: \\({a} + {b} \\times {c}\\)",
            "correct_answer": str(a + b * c),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Remember PEMDAS: multiplication comes before addition."},
                {"level": 2, "text": f"Multiply first: \\({b} \\times {c} = {b*c}\\). Then add {a}."},
                {"level": 3, "text": f"\\({a} + {b} \\times {c} = {a} + {b*c} = {a + b*c}\\)"},
            ],
        }
    elif choice == 1:
        b = random.randint(2, 4)
        a = b * random.randint(2, 6)
        return {
            "problem_text": f"Evaluate: \\({a} \\div {b}\\)",
            "correct_answer": str(a // b),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Division is straightforward \u2014 divide the numerator by the denominator."},
                {"level": 2, "text": f"Divide {a} by {b}."},
                {"level": 3, "text": f"\\({a} \\div {b} = {a // b}\\)"},
            ],
        }
    else:
        a, b = random.randint(2, 5), random.randint(1, 9)
        return {
            "problem_text": f"Evaluate: \\({a}^2 + {b}\\)",
            "correct_answer": str(a ** 2 + b),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Evaluate exponents before addition (PEMDAS: E before A)."},
                {"level": 2, "text": f"Calculate \\({a}^2\\) first, then add {b}."},
                {"level": 3, "text": f"\\({a}^2 + {b} = {a**2} + {b} = {a**2 + b}\\)"},
            ],
        }


def _gen_order_nested():
    a, b, c = random.randint(2, 6), random.randint(2, 6), random.randint(2, 4)
    return {
        "problem_text": f"Evaluate: \\(({a} + {b}) \\times {c}\\)",
        "correct_answer": str((a + b) * c),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Evaluate what's inside parentheses first."},
            {"level": 2, "text": f"Add \\({a} + {b} = {a+b}\\) first (inside parentheses), then multiply."},
            {"level": 3, "text": f"\\(({a} + {b}) \\times {c} = {a+b} \\times {c} = {(a+b)*c}\\)"},
        ],
    }


# ─── Exponents ────────────────────────────────────────────────────────────────

def _gen_exp_product():
    a, b = random.randint(2, 6), random.randint(2, 6)
    return {
        "problem_text": f"Simplify: \\(x^{{{a}}} \\cdot x^{{{b}}}\\)",
        "correct_answer": f"x**{a + b}",
        "answer_type": "symbolic",
        "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "Product rule: \\(x^a \\cdot x^b = x^{a+b}\\). Add the exponents."},
            {"level": 2, "text": f"Add the exponents: \\({a} + {b} = {a+b}\\)."},
            {"level": 3, "text": f"\\(x^{{{a}}} \\cdot x^{{{b}}} = x^{{{a}+{b}}} = x^{{{a+b}}}\\)"},
        ],
    }


def _gen_exp_power():
    a, b = random.randint(2, 4), random.randint(2, 4)
    return {
        "problem_text": f"Simplify: \\((x^{{{a}}})^{{{b}}}\\)",
        "correct_answer": f"x**{a * b}",
        "answer_type": "symbolic",
        "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "Power rule: \\((x^a)^b = x^{a \\cdot b}\\). Multiply the exponents."},
            {"level": 2, "text": f"Multiply the exponents: \\({a} \\times {b} = {a*b}\\)."},
            {"level": 3, "text": f"\\((x^{{{a}}})^{{{b}}} = x^{{{a} \\cdot {b}}} = x^{{{a*b}}}\\)"},
        ],
    }


def _gen_exp_negative():
    base = random.randint(2, 5)
    exp = random.randint(1, 3)
    result = Fraction(1, base ** exp)
    return {
        "problem_text": f"Evaluate: \\({base}^{{-{exp}}}\\)",
        "correct_answer": f"{result.numerator}/{result.denominator}",
        "answer_type": "symbolic",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Negative exponent rule: \\(x^{-n} = \\frac{1}{x^n}\\)."},
            {"level": 2, "text": f"Apply: \\({base}^{{-{exp}}} = \\frac{{1}}{{{base}^{{{exp}}}}} = \\frac{{1}}{{{base**exp}}}\\)."},
            {"level": 3, "text": f"\\({base}^{{-{exp}}} = \\frac{{1}}{{{base}^{{{exp}}}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
        ],
    }


def _gen_exp_combined():
    a, b = random.randint(3, 6), random.randint(1, 3)
    net = a - b
    ans = f"x**{net}" if net != 1 else "x"
    return {
        "problem_text": f"Simplify: \\(\\frac{{x^{{{a}}}}}{{x^{{{b}}}}}\\)",
        "correct_answer": ans,
        "answer_type": "symbolic",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Quotient rule: \\(\\frac{x^a}{x^b} = x^{a-b}\\). Subtract the exponents."},
            {"level": 2, "text": f"Subtract the exponents: \\({a} - {b} = {net}\\)."},
            {"level": 3, "text": f"\\(\\frac{{x^{{{a}}}}}{{x^{{{b}}}}} = x^{{{a}-{b}}} = x^{{{net}}}\\)"},
        ],
    }


# ─── Equations ────────────────────────────────────────────────────────────────

def _gen_eq_one_step():
    x = random.randint(1, 15)
    if random.choice([True, False]):
        b = random.randint(1, 12)
        return {
            "problem_text": f"Solve for \\(x\\): \\(x + {b} = {x + b}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "To solve for x, perform the inverse operation on both sides."},
                {"level": 2, "text": f"Subtract {b} from both sides."},
                {"level": 3, "text": f"\\(x + {b} = {x+b} \\Rightarrow x = {x+b} - {b} = {x}\\)"},
            ],
        }
    else:
        a = random.randint(2, 8)
        return {
            "problem_text": f"Solve for \\(x\\): \\({a}x = {a * x}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "To solve for x, divide both sides by the coefficient."},
                {"level": 2, "text": f"Divide both sides by {a}."},
                {"level": 3, "text": f"\\({a}x = {a*x} \\Rightarrow x = \\frac{{{a*x}}}{{{a}}} = {x}\\)"},
            ],
        }


def _gen_eq_two_step():
    a = random.randint(2, 6)
    x = random.randint(1, 10)
    b = random.randint(1, 10)
    c = a * x + b
    return {
        "problem_text": f"Solve for \\(x\\): \\({a}x + {b} = {c}\\)",
        "correct_answer": str(x),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Use two steps: first undo addition/subtraction, then undo multiplication/division."},
            {"level": 2, "text": f"Step 1: Subtract {b} from both sides. Step 2: Divide by {a}."},
            {"level": 3, "text": f"\\({a}x + {b} = {c} \\Rightarrow {a}x = {c-b} \\Rightarrow x = {x}\\)"},
        ],
    }


def _gen_eq_fractions():
    a = random.randint(2, 5)
    x = random.randint(2, 10)
    return {
        "problem_text": f"Solve for \\(x\\): \\(\\frac{{{a}x}}{{{a}}} = {x}\\)",
        "correct_answer": str(x),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "If both sides have the same denominator, the numerators must be equal."},
            {"level": 2, "text": f"Since both sides are over {a}, just set the numerators equal."},
            {"level": 3, "text": f"\\(\\frac{{{a}x}}{{{a}}} = {x} \\Rightarrow x = {x}\\)"},
        ],
    }


def _gen_eq_distribution():
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    x = random.randint(1, 8)
    c = a * (x + b)
    return {
        "problem_text": f"Solve for \\(x\\): \\({a}(x + {b}) = {c}\\)",
        "correct_answer": str(x),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "First distribute (multiply through the parentheses), then solve like a normal equation."},
            {"level": 2, "text": f"Distribute: \\({a}(x + {b}) = {a}x + {a*b}\\). Then solve."},
            {"level": 3, "text": f"\\({a}(x + {b}) = {c} \\Rightarrow {a}x + {a*b} = {c} \\Rightarrow {a}x = {c - a*b} \\Rightarrow x = {x}\\)"},
        ],
    }


# ─── Logarithms ───────────────────────────────────────────────────────────────

def _gen_log_exponential():
    base = random.randint(2, 5)
    exp = random.randint(2, 4)
    multiplication_str = " \\cdot ".join([str(base)] * exp)
    return {
        "problem_text": f"Evaluate: \\({base}^{{{exp}}}\\)",
        "correct_answer": str(base ** exp),
        "answer_type": "numeric",
        "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "To evaluate an exponential, multiply the base by itself the number of times shown by the exponent."},
            {"level": 2, "text": f"Multiply {base} by itself {exp} times."},
            {"level": 3, "text": f"\\({base}^{{{exp}}} = {multiplication_str} = {base**exp}\\)"},
        ],
    }


def _gen_log_definition():
    pairs = [(2, 4, 2), (2, 8, 3), (2, 16, 4), (3, 9, 2), (3, 27, 3),
             (10, 100, 2), (5, 25, 2), (10, 1000, 3)]
    base, val, result = random.choice(pairs)
    return {
        "problem_text": f"Evaluate: \\(\\log_{{{base}}}({val})\\)",
        "correct_answer": str(result),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "\\(\\log_b(x) = n\\) means \\(b^n = x\\). Use this definition."},
            {"level": 2, "text": f"Ask: what power of {base} gives {val}?"},
            {"level": 3, "text": f"\\({base}^{{{result}}} = {val}\\), so \\(\\log_{{{base}}}({val}) = {result}\\)"},
        ],
    }


def _gen_log_rules():
    combos = [(2, 4, 8, 5), (3, 9, 27, 5), (2, 4, 4, 4), (2, 4, 16, 6)]
    base, a, b, result = random.choice(combos)
    return {
        "problem_text": f"Simplify: \\(\\log_{{{base}}}({a}) + \\log_{{{base}}}({b})\\)",
        "correct_answer": str(result),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Product rule for logarithms: \\(\\log(a) + \\log(b) = \\log(a \\cdot b)\\)."},
            {"level": 2, "text": f"Combine: \\(\\log_{{{base}}}({a}) + \\log_{{{base}}}({b}) = \\log_{{{base}}}({a} \\cdot {b}) = \\log_{{{base}}}({a*b})\\)."},
            {"level": 3, "text": f"\\(\\log_{{{base}}}({a*b}) = {result}\\) since \\({base}^{{{result}}} = {a*b}\\)"},
        ],
    }


# ─── Summation ────────────────────────────────────────────────────────────────

def _gen_sum_sigma():
    n = random.randint(3, 8)
    total = n * (n + 1) // 2
    return {
        "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{n}}} i\\)",
        "correct_answer": str(total),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "\\(\\Sigma\\) notation means add up all values of the expression as the index goes from bottom to top."},
            {"level": 2, "text": f"Add the integers from 1 to {n}: \\(1 + 2 + 3 + \\cdots + {n}\\)."},
            {"level": 3, "text": f"Use the formula \\(\\frac{{n(n+1)}}{{2}}\\): \\(\\frac{{{n} \\cdot {n+1}}}{{2}} = {total}\\)"},
        ],
    }


def _gen_sum_arithmetic():
    n = random.randint(4, 12)
    total = n * (n + 1) // 2
    return {
        "problem_text": f"Find the sum: \\(1 + 2 + 3 + \\cdots + {n}\\)",
        "correct_answer": str(total),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "The sum of integers from 1 to n is \\(\\frac{n(n+1)}{2}\\)."},
            {"level": 2, "text": f"Apply the formula with \\(n = {n}\\)."},
            {"level": 3, "text": f"\\(\\frac{{{n} \\times {n+1}}}{{2}} = \\frac{{{n*(n+1)}}}{{2}} = {total}\\)"},
        ],
    }


def _gen_sum_nested():
    m = random.randint(2, 4)
    n = random.randint(2, 4)
    total = (m * (m + 1) // 2) * (n * (n + 1) // 2)
    return {
        "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{m}}} \\sum_{{j=1}}^{{{n}}} i \\cdot j\\)",
        "correct_answer": str(total),
        "answer_type": "numeric",
        "difficulty": 0.7,
        "hints": [
            {"level": 1, "text": "For double sums, evaluate the inner sum first, then the outer sum."},
            {"level": 2, "text": f"Inner sum \\(\\sum_{{j=1}}^{{{n}}} j = {n*(n+1)//2}\\). Then outer sum \\(\\sum_{{i=1}}^{{{m}}}\\)."},
            {"level": 3, "text": f"Inner sum \\(= {n*(n+1)//2}\\). Outer: \\({m*(m+1)//2} \\times {n*(n+1)//2} = {total}\\)"},
        ],
    }


# ─── Combinatorics ────────────────────────────────────────────────────────────

def _gen_comb_counting():
    a, b = random.randint(2, 6), random.randint(2, 6)
    return {
        "problem_text": f"A bag has {a} colors and {b} sizes. How many color-size combinations are possible?",
        "correct_answer": str(a * b),
        "answer_type": "numeric",
        "difficulty": 0.3,
        "hints": [
            {"level": 1, "text": "Fundamental counting principle: multiply the number of choices for each decision."},
            {"level": 2, "text": f"Multiply: {a} colors \u00d7 {b} sizes."},
            {"level": 3, "text": f"\\({a} \\times {b} = {a*b}\\) combinations"},
        ],
    }


def _gen_comb_permutations():
    pairs = [(4, 4), (5, 3), (6, 2), (5, 5), (4, 2)]
    n, r = random.choice(pairs)
    result = math_factorial(n) // math_factorial(n - r)
    return {
        "problem_text": f"How many ways can {r} items be chosen in order from {n} distinct items?",
        "correct_answer": str(result),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "\\(P(n,r) = \\frac{n!}{(n-r)!}\\) \u2014 count ordered arrangements."},
            {"level": 2, "text": f"\\(P({n},{r}) = \\frac{{{n}!}}{{{n-r}!}} = {n} \\times {n-1} \\times \\cdots \\times {n-r+1}\\)."},
            {"level": 3, "text": f"\\(P({n},{r}) = {result}\\)"},
        ],
    }


def _gen_comb_combinations():
    pairs = [(5, 2), (6, 2), (7, 3), (8, 3), (10, 2), (5, 3)]
    n, r = random.choice(pairs)
    result = math_comb(n, r)
    return {
        "problem_text": f"Calculate \\(C({n}, {r})\\) \u2014 the number of ways to choose {r} items from {n}.",
        "correct_answer": str(result),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "\\(C(n,r) = \\frac{n!}{r!(n-r)!}\\) \u2014 count unordered selections."},
            {"level": 2, "text": f"\\(C({n},{r}) = \\frac{{{n}!}}{{{r}! \\times {n-r}!}}\\)."},
            {"level": 3, "text": f"\\(C({n},{r}) = {result}\\)"},
        ],
    }


# ─── Geometric sequences ──────────────────────────────────────────────────────

def _gen_geo_sequences():
    a = random.randint(1, 5)
    r = random.randint(2, 4)
    n = random.randint(4, 6)
    term = a * r ** (n - 1)
    return {
        "problem_text": f"A geometric sequence has first term {a} and ratio {r}. Find the {n}th term.",
        "correct_answer": str(term),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "In a geometric sequence, the nth term is \\(a \\cdot r^{n-1}\\)."},
            {"level": 2, "text": f"Apply: \\(a = {a}\\), \\(r = {r}\\), \\(n = {n}\\). Compute \\({a} \\cdot {r}^{{{n-1}}}\\)."},
            {"level": 3, "text": f"\\({a} \\cdot {r}^{{{n-1}}} = {a} \\cdot {r**(n-1)} = {term}\\)"},
        ],
    }


def _gen_geo_finite():
    a = random.randint(1, 4)
    r = random.randint(2, 3)
    n = random.randint(3, 5)
    total = a * (r ** n - 1) // (r - 1)
    return {
        "problem_text": f"Find the sum of the first {n} terms of a geometric series with \\(a={a}\\), \\(r={r}\\).",
        "correct_answer": str(total),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "The sum of a finite geometric series is \\(S = \\frac{a(r^n - 1)}{r - 1}\\)."},
            {"level": 2, "text": f"Apply: \\(a = {a}\\), \\(r = {r}\\), \\(n = {n}\\)."},
            {"level": 3, "text": f"\\(S = \\frac{{{a}({r}^{{{n}}} - 1)}}{{{r} - 1}} = \\frac{{{a}({r**n}-1)}}{{{r-1}}} = {total}\\)"},
        ],
    }


# ─── Missing nodes: eq-quadratic, log-equations, geo-infinite ─────────────────

def _format_factor(r: int) -> str:
    """Return '(x - r)' or '(x + |r|)' for a root r."""
    if r > 0:
        return f"(x - {r})"
    elif r < 0:
        return f"(x + {abs(r)})"
    return "x"


def _gen_eq_quadratic():
    # Predefined root pairs that produce clean integer-coefficient problems
    pool = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 5), (3, 4), (3, 5),
            (-1, 2), (-1, 3), (-2, 3), (-1, 4), (-2, 5), (-3, 4), (-1, 5)]
    r1, r2 = random.choice(pool)
    b = -(r1 + r2)   # coefficient of x in x^2 + bx + c
    c = r1 * r2       # constant term

    # Build LaTeX equation string
    parts = ["x^2"]
    if b > 0:
        parts.append(f"+ {b}x")
    elif b < 0:
        parts.append(f"- {abs(b)}x")
    if c > 0:
        parts.append(f"+ {c}")
    elif c < 0:
        parts.append(f"- {abs(c)}")
    eq_str = " ".join(parts)

    roots = sorted([r1, r2])
    answer = f"{roots[0]}, {roots[1]}"

    return {
        "problem_text": f"Solve: \\({eq_str} = 0\\)",
        "correct_answer": answer,
        "answer_type": "symbolic",
        "difficulty": 0.7,
        "hints": [
            {"level": 1, "text": "Factor the quadratic: find two numbers that multiply to the constant term and add to the coefficient of x."},
            {"level": 2, "text": f"Find two numbers that multiply to {c} and add to {b}."},
            {"level": 3, "text": f"The numbers are {r1} and {r2}. Factored: \\({_format_factor(r1)}{_format_factor(r2)} = 0\\), so \\(x = {r1}\\) or \\(x = {r2}\\)."},
        ],
    }


def _gen_log_equations():
    # Solve log_b(x) = n → x = b^n
    pairs = [(2, 3, 8), (2, 4, 16), (2, 5, 32), (3, 2, 9), (3, 3, 27),
             (10, 2, 100), (5, 2, 25), (4, 2, 16), (2, 6, 64)]
    base, exp, val = random.choice(pairs)
    return {
        "problem_text": f"Solve for \\(x\\): \\(\\log_{{{base}}}(x) = {exp}\\)",
        "correct_answer": str(val),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "To solve \\(\\log_b(x) = n\\), rewrite in exponential form: \\(b^n = x\\)."},
            {"level": 2, "text": f"Rewrite: \\({base}^{{{exp}}} = x\\)."},
            {"level": 3, "text": f"\\({base}^{{{exp}}} = {val}\\), so \\(x = {val}\\)"},
        ],
    }


def _gen_geo_infinite():
    # Infinite geometric series S = a/(1-r), |r| < 1; all produce integer sums
    options = [
        (1, 1, 2, 2),   # a=1, r=1/2, S=2
        (2, 1, 2, 4),   # a=2, r=1/2, S=4
        (3, 1, 2, 6),   # a=3, r=1/2, S=6
        (2, 1, 3, 3),   # a=2, r=1/3, S=3
        (4, 1, 3, 6),   # a=4, r=1/3, S=6
        (3, 1, 4, 4),   # a=3, r=1/4, S=4
        (1, 2, 3, 3),   # a=1, r=2/3, S=3
        (2, 2, 3, 6),   # a=2, r=2/3, S=6
    ]
    a, r_num, r_den, total = random.choice(options)
    r_str = f"\\frac{{{r_num}}}{{{r_den}}}"
    denom_diff = r_den - r_num
    return {
        "problem_text": f"Find the sum of the infinite geometric series with \\(a={a}\\) and \\(r={r_str}\\).",
        "correct_answer": str(total),
        "answer_type": "numeric",
        "difficulty": 0.7,
        "hints": [
            {"level": 1, "text": "An infinite geometric series with \\(|r| < 1\\) converges to \\(S = \\frac{a}{1 - r}\\)."},
            {"level": 2, "text": f"Apply the formula: \\(S = \\frac{{{a}}}{{1 - \\frac{{{r_num}}}{{{r_den}}}}}\\)."},
            {"level": 3, "text": f"\\(1 - \\frac{{{r_num}}}{{{r_den}}} = \\frac{{{denom_diff}}}{{{r_den}}}\\), so \\(S = {a} \\div \\frac{{{denom_diff}}}{{{r_den}}} = {a} \\cdot \\frac{{{r_den}}}{{{denom_diff}}} = {total}\\)"},
        ],
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
    "eq-quadratic":      _gen_eq_quadratic,
    "log-exponential":   _gen_log_exponential,
    "log-definition":    _gen_log_definition,
    "log-rules":         _gen_log_rules,
    "log-equations":     _gen_log_equations,
    "sum-sigma":         _gen_sum_sigma,
    "sum-arithmetic":    _gen_sum_arithmetic,
    "sum-nested":        _gen_sum_nested,
    "comb-counting":     _gen_comb_counting,
    "comb-permutations": _gen_comb_permutations,
    "comb-combinations": _gen_comb_combinations,
    "geo-sequences":     _gen_geo_sequences,
    "geo-finite":        _gen_geo_finite,
    "geo-infinite":      _gen_geo_infinite,
}


def generate_problem(node_id: str) -> dict | None:
    """
    Generate a fresh problem for the given node_id.
    Returns a dict with problem_text, correct_answer, answer_type, difficulty, and hints.
    Returns None if no generator exists for this node.
    """
    gen = GENERATORS.get(node_id)
    if gen is None:
        return None
    try:
        return gen()
    except Exception:
        return None
