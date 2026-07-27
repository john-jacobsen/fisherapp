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


def _fmt_signed(value) -> str:
    """
    Render a signed additive term for display: ' + 3', ' - 2', or '' for 0.

    Prevents artifacts like 'x + -2' when a constant is negative. Use as
    f"x{_fmt_signed(a)}" to get 'x + 3', 'x - 2', or bare 'x'.
    """
    if value == 0:
        return ""
    if value > 0:
        return f" + {value}"
    return f" - {abs(value)}"


# ─── Fraction generators ──────────────────────────────────────────────────────

def _gen_frac_simplify():
    variant = random.choice(["standard", "large_gcf", "word"])
    if variant == "standard":
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
                {"level": 1, "text": "Find the GCF of the numerator and denominator, then divide both."},
                {"level": 2, "text": f"Find the GCF of {a} and {b}."},
                {"level": 3, "text": f"GCF({a},{b}) = {actual_gcf}. \\(\\frac{{{a}}}{{{b}}} = \\frac{{{f.numerator}}}{{{f.denominator}}}\\)"},
            ],
        }
    elif variant == "large_gcf":
        # numerator and denominator share a large common factor
        factor = random.randint(5, 12)
        p = random.randint(2, 7)
        q = random.randint(2, 7)
        while p == q or gcd(p, q) > 1:
            q = random.randint(2, 7)
        a, b = p * factor, q * factor
        f = Fraction(a, b)
        return {
            "problem_text": f"Simplify: \\(\\frac{{{a}}}{{{b}}}\\)",
            "correct_answer": f"{f.numerator}/{f.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Look for a large common factor — both numbers may share a factor bigger than 2."},
                {"level": 2, "text": f"Both {a} and {b} are divisible by {factor}."},
                {"level": 3, "text": f"Divide both by {factor}: \\(\\frac{{{p}}}{{{q}}}\\)"},
            ],
        }
    else:  # word problem
        factor = random.randint(2, 6)
        p = random.randint(1, 7)
        q = random.randint(2, 9)
        while p == q or gcd(p, q) > 1:
            q = random.randint(2, 9)
        a, b = p * factor, q * factor
        f = Fraction(a, b)
        actual_gcf = gcd(a, b)
        contexts = [
            (f"A recipe uses {a} cups of flour out of a bag containing {b} cups. What fraction of the bag was used, in simplest form?"),
            (f"A class has {a} students who passed out of {b} total. Write this as a simplified fraction."),
            (f"{a} out of {b} marbles are red. Simplify this fraction."),
        ]
        return {
            "problem_text": random.choice(contexts),
            "correct_answer": f"{f.numerator}/{f.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Write the fraction, then simplify by dividing numerator and denominator by their GCF."},
                {"level": 2, "text": f"The fraction is \\(\\frac{{{a}}}{{{b}}}\\). Find the GCF of {a} and {b}."},
                {"level": 3, "text": f"GCF = {actual_gcf}. \\(\\frac{{{a}}}{{{b}}} = \\frac{{{f.numerator}}}{{{f.denominator}}}\\)"},
            ],
        }


def _gen_frac_add_like():
    variant = random.choice(["add", "subtract", "word"])
    d = random.randint(3, 12)
    a = random.randint(1, d - 1)
    b = random.randint(1, d - 1)
    if variant == "add":
        result = Fraction(a, d) + Fraction(b, d)
        return {
            "problem_text": f"Calculate: \\(\\frac{{{a}}}{{{d}}} + \\frac{{{b}}}{{{d}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Same denominator: add numerators and keep the denominator."},
                {"level": 2, "text": f"Add numerators: {a} + {b} = {a+b}. Keep denominator {d}."},
                {"level": 3, "text": f"\\(\\frac{{{a+b}}}{{{d}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    elif variant == "subtract":
        if a < b:
            a, b = b, a
        result = Fraction(a, d) - Fraction(b, d)
        return {
            "problem_text": f"Calculate: \\(\\frac{{{a}}}{{{d}}} - \\frac{{{b}}}{{{d}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Same denominator: subtract numerators and keep the denominator."},
                {"level": 2, "text": f"Subtract numerators: {a} - {b} = {a-b}. Keep denominator {d}."},
                {"level": 3, "text": f"\\(\\frac{{{a-b}}}{{{d}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    else:  # word
        result = Fraction(a, d) + Fraction(b, d)
        contexts = [
            f"Maria ate \\(\\frac{{{a}}}{{{d}}}\\) of a pizza and then \\(\\frac{{{b}}}{{{d}}}\\) more. What total fraction did she eat?",
            f"A tank is \\(\\frac{{{a}}}{{{d}}}\\) full. You add \\(\\frac{{{b}}}{{{d}}}\\) more. What fraction is it now?",
        ]
        return {
            "problem_text": random.choice(contexts),
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The fractions have the same denominator — add the numerators."},
                {"level": 2, "text": f"\\(\\frac{{{a}}}{{{d}}} + \\frac{{{b}}}{{{d}}}\\): add {a} + {b}."},
                {"level": 3, "text": f"\\(\\frac{{{a+b}}}{{{d}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }


def _gen_frac_common_denom():
    pairs = [(2, 3), (3, 4), (4, 6), (2, 5), (3, 5), (4, 5), (6, 9), (2, 7), (3, 8)]
    a, b = random.choice(pairs)
    lcd = a * b // gcd(a, b)
    a_mults = list(range(a, lcd + 1, a))
    b_mults = list(range(b, lcd + 1, b))
    variant = random.choice(["find_lcd", "rewrite", "three_denoms"])
    if variant == "find_lcd":
        return {
            "problem_text": f"Find the LCD of \\(\\frac{{1}}{{{a}}}\\) and \\(\\frac{{1}}{{{b}}}\\).",
            "correct_answer": str(lcd),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "The LCD is the smallest number that is a multiple of both denominators."},
                {"level": 2, "text": f"Find the LCM of {a} and {b}."},
                {"level": 3, "text": f"Multiples of {a}: {', '.join(map(str, a_mults))}. Multiples of {b}: {', '.join(map(str, b_mults))}. LCD = {lcd}."},
            ],
        }
    elif variant == "rewrite":
        # Ask to rewrite a/denom_a with LCD as denominator
        p = random.randint(1, a - 1) if a > 1 else 1
        new_num = p * (lcd // a)
        return {
            "problem_text": f"Rewrite \\(\\frac{{{p}}}{{{a}}}\\) with denominator {lcd}.",
            "correct_answer": str(new_num),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Multiply numerator and denominator by the same number to get the target denominator."},
                {"level": 2, "text": f"{lcd} ÷ {a} = {lcd // a}. Multiply numerator by {lcd // a}."},
                {"level": 3, "text": f"\\(\\frac{{{p}}}{{{a}}} = \\frac{{{p} \\times {lcd//a}}}{{{a} \\times {lcd//a}}} = \\frac{{{new_num}}}{{{lcd}}}\\)"},
            ],
        }
    else:  # three_denoms
        # Use pairs of denominators that divide a common number
        triples = [(2, 3, 4, 12), (2, 4, 6, 12), (3, 4, 6, 12), (2, 5, 10, 10), (3, 6, 9, 18)]
        d1, d2, d3, lcm3 = random.choice(triples)
        return {
            "problem_text": f"Find the LCD of \\(\\frac{{1}}{{{d1}}}\\), \\(\\frac{{1}}{{{d2}}}\\), and \\(\\frac{{1}}{{{d3}}}\\).",
            "correct_answer": str(lcm3),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Find the LCM of all three denominators."},
                {"level": 2, "text": f"Find LCM of {d1} and {d2} first, then find LCM of that result with {d3}."},
                {"level": 3, "text": f"LCM({d1},{d2}) = {d1*d2//gcd(d1,d2)}, then LCM with {d3} = {lcm3}."},
            ],
        }


def _gen_frac_add_unlike():
    variant = random.choice(["add", "subtract", "word"])
    a = Fraction(random.randint(1, 5), random.randint(2, 8))
    b = Fraction(random.randint(1, 5), random.randint(2, 8))
    while a.denominator == b.denominator:
        b = Fraction(random.randint(1, 5), random.randint(2, 8))
    lcd = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    a_new_num = a.numerator * (lcd // a.denominator)
    b_new_num = b.numerator * (lcd // b.denominator)
    if variant == "subtract":
        result = a - b
        if result < 0:
            a, b = b, a
            result = abs(result)
            a_new_num, b_new_num = b_new_num, a_new_num
        return {
            "problem_text": f"Calculate: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} - \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Find a common denominator before subtracting."},
                {"level": 2, "text": f"LCD of {a.denominator} and {b.denominator} is {lcd}."},
                {"level": 3, "text": f"\\(\\frac{{{a_new_num}}}{{{lcd}}} - \\frac{{{b_new_num}}}{{{lcd}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    elif variant == "word":
        result = a + b
        contexts = [
            f"A recipe calls for \\(\\frac{{{a.numerator}}}{{{a.denominator}}}\\) cup of sugar and \\(\\frac{{{b.numerator}}}{{{b.denominator}}}\\) cup of honey. How much sweetener in total?",
            f"You walk \\(\\frac{{{a.numerator}}}{{{a.denominator}}}\\) mile in the morning and \\(\\frac{{{b.numerator}}}{{{b.denominator}}}\\) mile in the afternoon. How far total?",
        ]
        return {
            "problem_text": random.choice(contexts),
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Add the fractions — find a common denominator first."},
                {"level": 2, "text": f"LCD of {a.denominator} and {b.denominator} is {lcd}."},
                {"level": 3, "text": f"\\(\\frac{{{a_new_num}}}{{{lcd}}} + \\frac{{{b_new_num}}}{{{lcd}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    else:  # add
        result = a + b
        return {
            "problem_text": f"Calculate: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} + \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Find a common denominator, then add numerators."},
                {"level": 2, "text": f"LCD of {a.denominator} and {b.denominator} is {lcd}."},
                {"level": 3, "text": f"\\(\\frac{{{a_new_num}}}{{{lcd}}} + \\frac{{{b_new_num}}}{{{lcd}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }


def _gen_frac_multiply():
    variant = random.choice(["standard", "whole_times_frac", "frac_of_whole"])
    if variant == "standard":
        a = Fraction(random.randint(1, 6), random.randint(2, 8))
        b = Fraction(random.randint(1, 6), random.randint(2, 8))
        result = a * b
        return {
            "problem_text": f"Multiply: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\times \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Multiply numerators together and denominators together."},
                {"level": 2, "text": f"Numerators: {a.numerator} × {b.numerator}. Denominators: {a.denominator} × {b.denominator}."},
                {"level": 3, "text": f"\\(\\frac{{{a.numerator * b.numerator}}}{{{a.denominator * b.denominator}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    elif variant == "whole_times_frac":
        n = random.randint(2, 9)
        a = Fraction(random.randint(1, 5), random.randint(2, 7))
        result = Fraction(n) * a
        return {
            "problem_text": f"Multiply: \\({n} \\times \\frac{{{a.numerator}}}{{{a.denominator}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Write the whole number as a fraction over 1, then multiply."},
                {"level": 2, "text": f"\\(\\frac{{{n}}}{{1}} \\times \\frac{{{a.numerator}}}{{{a.denominator}}} = \\frac{{{n*a.numerator}}}{{{a.denominator}}}\\)"},
                {"level": 3, "text": f"\\({n} \\times \\frac{{{a.numerator}}}{{{a.denominator}}} = \\frac{{{n*a.numerator}}}{{{a.denominator}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    else:  # frac_of_whole
        a = Fraction(random.randint(1, 4), random.randint(3, 7))
        # make whole divisible so result is integer
        whole = a.denominator * random.randint(2, 5)
        result = a * whole
        return {
            "problem_text": f"What is \\(\\frac{{{a.numerator}}}{{{a.denominator}}}\\) of {whole}?",
            "correct_answer": str(int(result)),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "'Of' means multiply. Multiply the fraction by the whole number."},
                {"level": 2, "text": f"\\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\times {whole} = \\frac{{{a.numerator * whole}}}{{{a.denominator}}}\\)"},
                {"level": 3, "text": f"\\(\\frac{{{a.numerator * whole}}}{{{a.denominator}}} = {int(result)}\\)"},
            ],
        }


def _gen_frac_divide():
    variant = random.choice(["standard", "whole_div_frac", "frac_div_whole"])
    if variant == "standard":
        a = Fraction(random.randint(1, 6), random.randint(2, 8))
        b = Fraction(random.randint(1, 6), random.randint(2, 8))
        result = a / b
        return {
            "problem_text": f"Divide: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\div \\frac{{{b.numerator}}}{{{b.denominator}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "To divide fractions, multiply by the reciprocal of the divisor."},
                {"level": 2, "text": f"Flip the second fraction: \\(\\frac{{{b.denominator}}}{{{b.numerator}}}\\). Then multiply."},
                {"level": 3, "text": f"\\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\times \\frac{{{b.denominator}}}{{{b.numerator}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    elif variant == "whole_div_frac":
        n = random.randint(2, 8)
        a = Fraction(random.randint(1, 4), random.randint(2, 6))
        result = Fraction(n) / a
        return {
            "problem_text": f"Divide: \\({n} \\div \\frac{{{a.numerator}}}{{{a.denominator}}}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Write the whole number as a fraction over 1, then multiply by the reciprocal."},
                {"level": 2, "text": f"\\(\\frac{{{n}}}{{1}} \\div \\frac{{{a.numerator}}}{{{a.denominator}}} = \\frac{{{n}}}{{1}} \\times \\frac{{{a.denominator}}}{{{a.numerator}}}\\)"},
                {"level": 3, "text": f"\\(= \\frac{{{n*a.denominator}}}{{{a.numerator}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    else:  # frac_div_whole
        a = Fraction(random.randint(1, 5), random.randint(2, 7))
        n = random.randint(2, 6)
        result = a / n
        return {
            "problem_text": f"Divide: \\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\div {n}\\)",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Dividing by a whole number is the same as multiplying by its reciprocal."},
                {"level": 2, "text": f"\\(\\frac{{{a.numerator}}}{{{a.denominator}}} \\div {n} = \\frac{{{a.numerator}}}{{{a.denominator}}} \\times \\frac{{1}}{{{n}}}\\)"},
                {"level": 3, "text": f"\\(= \\frac{{{a.numerator}}}{{{a.denominator * n}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }


# ─── Order of operations ──────────────────────────────────────────────────────

def _gen_order_pemdas():
    choice = random.randint(0, 4)
    if choice == 0:
        a, b, c = random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)
        return {
            "problem_text": f"Evaluate: \\({a} + {b} \\times {c}\\)",
            "correct_answer": str(a + b * c),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "PEMDAS: multiplication before addition."},
                {"level": 2, "text": f"Multiply first: {b} × {c} = {b*c}. Then add {a}."},
                {"level": 3, "text": f"\\({a} + {b*c} = {a + b*c}\\)"},
            ],
        }
    elif choice == 1:
        a, b, c = random.randint(2, 8), random.randint(2, 5), random.randint(2, 5)
        result = a - b * c
        # make sure result > 0
        if result <= 0:
            a = b * c + random.randint(1, 5)
            result = a - b * c
        return {
            "problem_text": f"Evaluate: \\({a} - {b} \\times {c}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "PEMDAS: multiplication before subtraction."},
                {"level": 2, "text": f"Multiply first: {b} × {c} = {b*c}. Then subtract from {a}."},
                {"level": 3, "text": f"\\({a} - {b*c} = {result}\\)"},
            ],
        }
    elif choice == 2:
        a, b = random.randint(2, 5), random.randint(1, 9)
        return {
            "problem_text": f"Evaluate: \\({a}^2 + {b}\\)",
            "correct_answer": str(a ** 2 + b),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "PEMDAS: exponents before addition."},
                {"level": 2, "text": f"Compute {a}² = {a**2} first, then add {b}."},
                {"level": 3, "text": f"\\({a**2} + {b} = {a**2 + b}\\)"},
            ],
        }
    elif choice == 3:
        # a + b^2 - c
        a, b = random.randint(2, 5), random.randint(2, 4)
        c = random.randint(1, 5)
        result = a + b ** 2 - c
        if result <= 0:
            c = 1
            result = a + b ** 2 - c
        return {
            "problem_text": f"Evaluate: \\({a} + {b}^2 - {c}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "PEMDAS: exponent first, then left-to-right addition and subtraction."},
                {"level": 2, "text": f"Compute {b}² = {b**2} first, then: {a} + {b**2} - {c}."},
                {"level": 3, "text": f"\\({a} + {b**2} - {c} = {result}\\)"},
            ],
        }
    else:
        # (a + b) × c - d
        a, b, c, d = random.randint(2, 5), random.randint(2, 5), random.randint(2, 4), random.randint(1, 6)
        result = (a + b) * c - d
        return {
            "problem_text": f"Evaluate: \\(({a} + {b}) \\times {c} - {d}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "PEMDAS: parentheses first, then multiplication, then subtraction."},
                {"level": 2, "text": f"Inside parens: {a}+{b}={a+b}. Then {a+b}×{c}={( a+b)*c}. Then subtract {d}."},
                {"level": 3, "text": f"\\({(a+b)*c} - {d} = {result}\\)"},
            ],
        }


def _gen_order_nested():
    variant = random.choice(["mul_after_add", "sub_in_parens", "nested_parens", "double_parens"])
    if variant == "mul_after_add":
        a, b, c = random.randint(2, 6), random.randint(2, 6), random.randint(2, 4)
        return {
            "problem_text": f"Evaluate: \\(({a} + {b}) \\times {c}\\)",
            "correct_answer": str((a + b) * c),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Parentheses first, then multiply."},
                {"level": 2, "text": f"{a} + {b} = {a+b}. Then multiply by {c}."},
                {"level": 3, "text": f"\\({a+b} \\times {c} = {(a+b)*c}\\)"},
            ],
        }
    elif variant == "sub_in_parens":
        b, c = random.randint(3, 8), random.randint(2, 4)
        a = b + random.randint(1, 5)
        result = (a - b) * c
        return {
            "problem_text": f"Evaluate: \\(({a} - {b}) \\times {c}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Evaluate inside the parentheses first."},
                {"level": 2, "text": f"{a} - {b} = {a-b}. Then multiply by {c}."},
                {"level": 3, "text": f"\\({a-b} \\times {c} = {result}\\)"},
            ],
        }
    elif variant == "nested_parens":
        a, b, c, d = random.randint(2, 5), random.randint(1, 4), random.randint(2, 4), random.randint(1, 5)
        inner = a + b
        result = inner * c + d
        return {
            "problem_text": f"Evaluate: \\(({a} + {b}) \\times {c} + {d}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Parentheses → multiplication → addition."},
                {"level": 2, "text": f"({a}+{b})={inner}, then {inner}×{c}={inner*c}, then +{d}."},
                {"level": 3, "text": f"\\({inner*c} + {d} = {result}\\)"},
            ],
        }
    else:  # double_parens: (a+b)*(c-d)
        c, d = random.randint(3, 8), random.randint(1, 3)
        a, b = random.randint(2, 5), random.randint(2, 5)
        result = (a + b) * (c - d)
        return {
            "problem_text": f"Evaluate: \\(({a} + {b}) \\times ({c} - {d})\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Evaluate both sets of parentheses first, then multiply."},
                {"level": 2, "text": f"({a}+{b})={a+b}, ({c}-{d})={c-d}. Then multiply."},
                {"level": 3, "text": f"\\({a+b} \\times {c-d} = {result}\\)"},
            ],
        }


# ─── Exponents ────────────────────────────────────────────────────────────────

def _gen_exp_product():
    variant = random.choice(["simplify", "numeric_base", "find_exponent"])
    if variant == "simplify":
        a, b = random.randint(2, 6), random.randint(2, 6)
        return {
            "problem_text": f"Simplify: \\(x^{{{a}}} \\cdot x^{{{b}}}\\)",
            "correct_answer": f"x**{a + b}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Product rule: \\(x^a \\cdot x^b = x^{a+b}\\). Add the exponents."},
                {"level": 2, "text": f"Add the exponents: {a} + {b} = {a+b}."},
                {"level": 3, "text": f"\\(x^{{{a}}} \\cdot x^{{{b}}} = x^{{{a+b}}}\\)"},
            ],
        }
    elif variant == "numeric_base":
        base = random.randint(2, 4)
        a, b = random.randint(2, 4), random.randint(2, 4)  # >= 2: no ^{1} in display
        result = base ** (a + b)
        return {
            "problem_text": f"Simplify: \\({base}^{{{a}}} \\cdot {base}^{{{b}}}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Product rule: add the exponents when the bases are the same."},
                {"level": 2, "text": f"\\({base}^{{{a}}} \\cdot {base}^{{{b}}} = {base}^{{{a+b}}}\\). Compute \\({base}^{{{a+b}}}\\)."},
                {"level": 3, "text": f"\\({base}^{{{a+b}}} = {result}\\)"},
            ],
        }
    else:  # find_exponent
        a, b = random.randint(2, 5), random.randint(2, 5)
        total = a + b
        return {
            "problem_text": f"\\(x^{{{a}}} \\cdot x^n = x^{{{total}}}\\). What is \\(n\\)?",
            "correct_answer": str(b),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Product rule: the exponents add. So solve for n."},
                {"level": 2, "text": f"{a} + n = {total}. Solve for n."},
                {"level": 3, "text": f"n = {total} - {a} = {b}"},
            ],
        }


def _gen_exp_power():
    variant = random.choice(["simplify_sym", "numeric_eval", "find_exp"])
    if variant == "simplify_sym":
        a, b = random.randint(2, 4), random.randint(2, 4)
        return {
            "problem_text": f"Simplify: \\((x^{{{a}}})^{{{b}}}\\)",
            "correct_answer": f"x**{a * b}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Power rule: \\((x^a)^b = x^{a \\cdot b}\\). Multiply the exponents."},
                {"level": 2, "text": f"Multiply: {a} × {b} = {a*b}."},
                {"level": 3, "text": f"\\((x^{{{a}}})^{{{b}}} = x^{{{a*b}}}\\)"},
            ],
        }
    elif variant == "numeric_eval":
        base = random.randint(2, 3)
        a, b = random.randint(2, 3), random.randint(2, 3)
        result = base ** (a * b)
        return {
            "problem_text": f"Evaluate: \\(({base}^{{{a}}})^{{{b}}}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Power rule: multiply the exponents, then evaluate."},
                {"level": 2, "text": f"\\(({base}^{{{a}}})^{{{b}}} = {base}^{{{a*b}}}\\). Now compute \\({base}^{{{a*b}}}\\)."},
                {"level": 3, "text": f"\\({base}^{{{a*b}}} = {result}\\)"},
            ],
        }
    else:  # find_exp: (x^a)^? = x^c
        a = random.randint(2, 4)
        b = random.randint(2, 4)
        c = a * b
        return {
            "problem_text": f"\\((x^{{{a}}})^n = x^{{{c}}}\\). What is \\(n\\)?",
            "correct_answer": str(b),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Power rule: multiply exponents. So a × n = c."},
                {"level": 2, "text": f"{a} × n = {c}. Divide both sides by {a}."},
                {"level": 3, "text": f"n = {c} ÷ {a} = {b}"},
            ],
        }


def _gen_exp_negative():
    variant = random.choice(["evaluate", "simplify_sym", "find_base"])
    if variant == "evaluate":
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
                {"level": 2, "text": f"\\({base}^{{-{exp}}} = \\frac{{1}}{{{base}^{{{exp}}}}} = \\frac{{1}}{{{base**exp}}}\\)."},
                {"level": 3, "text": f"\\({base}^{{-{exp}}} = \\frac{{{result.numerator}}}{{{result.denominator}}}\\)"},
            ],
        }
    elif variant == "simplify_sym":
        exp = random.randint(1, 4)
        return {
            "problem_text": f"Simplify: \\(x^{{-{exp}}}\\)",
            "correct_answer": f"1/x**{exp}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Negative exponent rule: \\(x^{-n} = \\frac{1}{x^n}\\)."},
                {"level": 2, "text": f"Move x to the denominator and change the sign of the exponent."},
                {"level": 3, "text": f"\\(x^{{-{exp}}} = \\frac{{1}}{{x^{{{exp}}}}}\\)"},
            ],
        }
    else:  # find_base: 1/base^exp as fraction → identify base
        base = random.randint(2, 4)
        exp = random.randint(2, 3)
        val = base ** exp
        return {
            "problem_text": f"\\(b^{{-{exp}}} = \\frac{{1}}{{{val}}}\\). What is \\(b\\)?",
            "correct_answer": str(base),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": f"\\(b^{{-{exp}}} = \\frac{{1}}{{b^{{{exp}}}}}\\), so \\(b^{{{exp}}} = {val}\\)."},
                {"level": 2, "text": f"What number raised to the {exp} gives {val}?"},
                {"level": 3, "text": f"\\({base}^{{{exp}}} = {val}\\), so \\(b = {base}\\)."},
            ],
        }


def _gen_exp_combined():
    variant = random.choice(["quotient_sym", "numeric_quotient", "mixed_rules"])
    if variant == "quotient_sym":
        # exponents >= 2 (no ^{1} in display) and net >= 2 (clean, non-trivial)
        b = random.randint(2, 3)
        a = random.randint(b + 2, 7)
        net = a - b
        ans = f"x**{net}" if net != 1 else "x"
        return {
            "problem_text": f"Simplify: \\(\\frac{{x^{{{a}}}}}{{x^{{{b}}}}}\\)",
            "correct_answer": ans,
            "answer_type": "symbolic",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Quotient rule: \\(\\frac{x^a}{x^b} = x^{a-b}\\)."},
                {"level": 2, "text": f"Subtract exponents: {a} - {b} = {net}."},
                {"level": 3, "text": f"\\(\\frac{{x^{{{a}}}}}{{x^{{{b}}}}} = x^{{{net}}}\\)"},
            ],
        }
    elif variant == "numeric_quotient":
        base = random.randint(2, 4)
        # exponents >= 2 (no ^{1} in display) and net >= 2 (no ^{1} in hints)
        b = random.randint(2, 3)
        a = random.randint(b + 2, 6)
        net = a - b
        result = base ** net
        return {
            "problem_text": f"Simplify: \\(\\frac{{{base}^{{{a}}}}}{{{base}^{{{b}}}}}\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Quotient rule: subtract exponents when bases are the same."},
                {"level": 2, "text": f"\\(\\frac{{{base}^{{{a}}}}}{{{base}^{{{b}}}}} = {base}^{{{a-b}}}\\). Compute \\({base}^{{{net}}}\\)."},
                {"level": 3, "text": f"\\({base}^{{{net}}} = {result}\\)"},
            ],
        }
    else:  # mixed_rules: x^a * x^b / x^c
        a, b, c = random.randint(2, 4), random.randint(2, 4), random.randint(2, 3)  # c>=2: no x^{1}
        net = a + b - c
        ans = f"x**{net}" if net != 1 else "x"
        return {
            "problem_text": f"Simplify: \\(\\frac{{x^{{{a}}} \\cdot x^{{{b}}}}}{{x^{{{c}}}}}\\)",
            "correct_answer": ans,
            "answer_type": "symbolic",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Use product rule on top first, then quotient rule."},
                {"level": 2, "text": f"Numerator: \\(x^{{{a}+{b}}} = x^{{{a+b}}}\\). Then divide: \\(x^{{{a+b}-{c}}}\\)."},
                {"level": 3, "text": f"\\(x^{{{a+b}-{c}}} = x^{{{net}}}\\)"},
            ],
        }


# ─── Equations ────────────────────────────────────────────────────────────────

def _gen_eq_one_step():
    x = random.randint(1, 15)
    variant = random.choice(["add", "subtract", "multiply", "divide"])
    if variant == "add":
        b = random.randint(1, 12)
        return {
            "problem_text": f"Solve for \\(x\\): \\(x + {b} = {x + b}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Perform the inverse operation on both sides."},
                {"level": 2, "text": f"Subtract {b} from both sides."},
                {"level": 3, "text": f"\\(x = {x+b} - {b} = {x}\\)"},
            ],
        }
    elif variant == "subtract":
        b = random.randint(1, 12)
        rhs = x - b if x > b else x + b
        sign = "-" if x > b else "+"
        bval = b
        if x <= b:
            x = b + random.randint(1, 8)
            rhs = x - bval
        return {
            "problem_text": f"Solve for \\(x\\): \\(x - {bval} = {rhs}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Perform the inverse operation on both sides."},
                {"level": 2, "text": f"Add {bval} to both sides."},
                {"level": 3, "text": f"\\(x = {rhs} + {bval} = {x}\\)"},
            ],
        }
    elif variant == "multiply":
        a = random.randint(2, 8)
        return {
            "problem_text": f"Solve for \\(x\\): \\({a}x = {a * x}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Divide both sides by the coefficient of x."},
                {"level": 2, "text": f"Divide both sides by {a}."},
                {"level": 3, "text": f"\\(x = \\frac{{{a*x}}}{{{a}}} = {x}\\)"},
            ],
        }
    else:  # divide: x/a = b
        a = random.randint(2, 8)
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{x}}{{{a}}} = {x}\\)",
            "correct_answer": str(x * a),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Multiply both sides by the denominator to isolate x."},
                {"level": 2, "text": f"Multiply both sides by {a}."},
                {"level": 3, "text": f"\\(x = {x} \\times {a} = {x*a}\\)"},
            ],
        }


def _gen_eq_two_step():
    variant = random.choice(["standard", "subtract", "distribute", "fraction_form"])
    if variant == "standard":
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
    elif variant == "subtract":
        a = random.randint(2, 6)
        x = random.randint(1, 10)
        b = random.randint(1, 10)
        c = a * x - b
        if c <= 0:
            c = a * x + b
            b = -b
        return {
            "problem_text": f"Solve for \\(x\\): \\({a}x - {abs(b)} = {c}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Use two steps: first undo addition/subtraction, then undo multiplication/division."},
                {"level": 2, "text": f"Step 1: Add {abs(b)} to both sides. Step 2: Divide by {a}."},
                {"level": 3, "text": f"\\({a}x - {abs(b)} = {c} \\Rightarrow {a}x = {c+abs(b)} \\Rightarrow x = {x}\\)"},
            ],
        }
    elif variant == "distribute":
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
                {"level": 1, "text": "Distribute first, then solve the resulting two-step equation."},
                {"level": 2, "text": f"Distribute: \\({a}x + {a*b} = {c}\\). Then subtract {a*b} and divide by {a}."},
                {"level": 3, "text": f"\\({a}(x+{b})={c} \\Rightarrow {a}x+{a*b}={c} \\Rightarrow {a}x={c-a*b} \\Rightarrow x={x}\\)"},
            ],
        }
    else:  # fraction_form
        b = random.randint(2, 5)
        c = random.randint(2, 8)
        a = random.randint(1, 6)
        x = b * c - a
        if x <= 0:
            a = 1
            x = b * c - a
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{x + {a}}}{{{b}}} = {c}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Multiply both sides by the denominator first, then subtract the constant."},
                {"level": 2, "text": f"Multiply both sides by {b}: \\(x + {a} = {b*c}\\). Then subtract {a}."},
                {"level": 3, "text": f"\\(\\frac{{x+{a}}}{{{b}}}={c} \\Rightarrow x+{a}={b*c} \\Rightarrow x={x}\\)"},
            ],
        }


def _gen_eq_fractions():
    variant = random.choice(["simple", "nontrivial", "sum_num", "var_denom"])
    if variant == "simple":
        # x/a = b → x = ab
        a = random.randint(2, 7)
        b = random.randint(2, 9)
        x = a * b
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{x}}{{{a}}} = {b}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Multiply both sides by the denominator to isolate x."},
                {"level": 2, "text": f"Multiply both sides by {a}."},
                {"level": 3, "text": f"\\(\\frac{{x}}{{{a}}} = {b} \\Rightarrow x = {b} \\times {a} = {x}\\)"},
            ],
        }
    elif variant == "nontrivial":
        # ax/b = c where a ≠ b, integer answer
        b = random.randint(2, 6)
        a = random.randint(2, 6)
        while a == b:
            a = random.randint(2, 6)
        x = random.randint(1, 8) * b  # ensure x*a/b is integer
        c = x * a // b
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{{a}x}}{{{b}}} = {c}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Multiply both sides by the denominator, then divide by the coefficient of x."},
                {"level": 2, "text": f"Multiply both sides by {b}: \\({a}x = {c * b}\\). Then divide by {a}."},
                {"level": 3, "text": f"\\(\\frac{{{a}x}}{{{b}}} = {c} \\Rightarrow {a}x = {c*b} \\Rightarrow x = {x}\\)"},
            ],
        }
    elif variant == "sum_num":
        # (x + a)/b = c → x = bc - a. Keep 0 < a < bc so x stays a positive
        # integer and the numerator renders naturally (no "x + -2" artifact).
        b = random.randint(2, 5)
        c = random.randint(2, 8)
        a = random.randint(1, b * c - 1)
        x = b * c - a
        num = f"x{_fmt_signed(a)}"
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{{num}}}{{{b}}} = {c}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Multiply both sides by the denominator first, then isolate x."},
                {"level": 2, "text": f"Multiply both sides by {b}: \\({num} = {b*c}\\). Then subtract {a}."},
                {"level": 3, "text": f"\\(\\frac{{{num}}}{{{b}}} = {c} \\Rightarrow {num} = {b*c} \\Rightarrow x = {x}\\)"},
            ],
        }
    else:  # var_denom
        # a/x = b → x = a/b, ensure integer
        b = random.randint(2, 6)
        x = random.randint(2, 8)
        a = b * x
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{{a}}}{{x}} = {b}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Multiply both sides by x to clear the denominator, then solve."},
                {"level": 2, "text": f"Multiply both sides by x: \\({a} = {b}x\\). Then divide by {b}."},
                {"level": 3, "text": f"\\(\\frac{{{a}}}{{x}} = {b} \\Rightarrow {a} = {b}x \\Rightarrow x = {x}\\)"},
            ],
        }


def _gen_eq_distribution():
    variant = random.choice(["basic", "then_combine", "both_sides"])
    if variant == "basic":
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
                {"level": 1, "text": "First distribute (multiply through the parentheses), then solve."},
                {"level": 2, "text": f"Distribute: \\({a}x + {a*b} = {c}\\). Then subtract {a*b} and divide by {a}."},
                {"level": 3, "text": f"\\({a}(x+{b})={c} \\Rightarrow {a}x+{a*b}={c} \\Rightarrow {a}x={c-a*b} \\Rightarrow x={x}\\)"},
            ],
        }
    elif variant == "then_combine":
        a = random.randint(2, 4)
        b = random.randint(1, 5)
        d = random.randint(1, 8)
        x = random.randint(1, 8)
        c = a * (x + b) + d
        return {
            "problem_text": f"Solve for \\(x\\): \\({a}(x + {b}) + {d} = {c}\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Distribute first, then combine like terms, then isolate x."},
                {"level": 2, "text": f"Distribute: \\({a}x + {a*b} + {d} = {c}\\). Combine constants: \\({a}x + {a*b+d} = {c}\\)."},
                {"level": 3, "text": f"\\({a}x+{a*b+d}={c} \\Rightarrow {a}x={c-a*b-d} \\Rightarrow x={x}\\)"},
            ],
        }
    else:  # both_sides: a(x+b) = c(x+d)
        a = random.randint(2, 5)
        c = random.randint(2, 5)
        while c == a:
            c = random.randint(2, 5)
        b = random.randint(1, 6)
        d = random.randint(1, 6)
        # a*x + a*b = c*x + c*d → (a-c)*x = c*d - a*b
        # ensure integer x
        diff_ac = a - c
        rhs = c * d - a * b
        if diff_ac == 0 or rhs % diff_ac != 0:
            # fallback to basic if no clean solution
            x = random.randint(1, 8)
            cc = a * (x + b)
            return {
                "problem_text": f"Solve for \\(x\\): \\({a}(x + {b}) = {cc}\\)",
                "correct_answer": str(x),
                "answer_type": "numeric",
                "difficulty": 0.6,
                "hints": [
                    {"level": 1, "text": "Distribute first, then isolate x."},
                    {"level": 2, "text": f"Distribute: \\({a}x + {a*b} = {cc}\\)."},
                    {"level": 3, "text": f"\\({a}x={cc-a*b} \\Rightarrow x={x}\\)"},
                ],
            }
        x = rhs // diff_ac
        lhs_val = a * (x + b)
        rhs_val = c * (x + d)
        return {
            "problem_text": f"Solve for \\(x\\): \\({a}(x + {b}) = {c}(x + {d})\\)",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Distribute on both sides, then collect x terms on one side."},
                {"level": 2, "text": f"Distribute: \\({a}x + {a*b} = {c}x + {c*d}\\). Move x terms left: \\({diff_ac}x = {c*d - a*b}\\)."},
                {"level": 3, "text": f"\\({diff_ac}x = {rhs} \\Rightarrow x = {x}\\)"},
            ],
        }


# ─── Logarithms ───────────────────────────────────────────────────────────────

def _gen_log_exponential():
    """Generate problems that practice converting between exponential and log form."""
    pairs = [
        (2, 2, 4), (2, 3, 8), (2, 4, 16), (2, 5, 32),
        (3, 2, 9), (3, 3, 27), (3, 4, 81),
        (4, 2, 16), (4, 3, 64),
        (5, 2, 25), (5, 3, 125),
        (10, 2, 100), (10, 3, 1000),
    ]
    base, exp, result = random.choice(pairs)
    variant = random.choice(["to_log", "find_base", "find_exp"])

    if variant == "to_log":
        return {
            "problem_text": f"If \\({base}^{{{exp}}} = {result}\\), what is \\(\\log_{{{base}}}({result})\\)?",
            "correct_answer": str(exp),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\log_b(x) = n\\) means \\(b^n = x\\). Use this to convert."},
                {"level": 2, "text": f"Since \\({base}^{{{exp}}} = {result}\\), that means \\(\\log_{{{base}}}({result}) = ?\\)"},
                {"level": 3, "text": f"\\(\\log_{{{base}}}({result}) = {exp}\\) because \\({base}^{{{exp}}} = {result}\\)."},
            ],
        }
    elif variant == "find_base":
        return {
            "problem_text": f"\\(\\log_b({result}) = {exp}\\). What is \\(b\\)?",
            "correct_answer": str(base),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\log_b(x) = n\\) means \\(b^n = x\\). Rewrite as an exponential."},
                {"level": 2, "text": f"This means \\(b^{{{exp}}} = {result}\\). What value of \\(b\\) satisfies this?"},
                {"level": 3, "text": f"\\({base}^{{{exp}}} = {result}\\), so \\(b = {base}\\)."},
            ],
        }
    else:  # find_exp
        return {
            "problem_text": f"\\(\\log_{{{base}}}({result}) = x\\). What is \\(x\\)?",
            "correct_answer": str(exp),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\log_b(x) = n\\) means \\(b^n = x\\). Rewrite as an exponential."},
                {"level": 2, "text": f"This means \\({base}^x = {result}\\). What power of {base} gives {result}?"},
                {"level": 3, "text": f"\\({base}^{{{exp}}} = {result}\\), so \\(x = {exp}\\)."},
            ],
        }


def _gen_log_definition():
    pairs = [(2, 4, 2), (2, 8, 3), (2, 16, 4), (3, 9, 2), (3, 27, 3),
             (10, 100, 2), (5, 25, 2), (10, 1000, 3), (4, 16, 2), (2, 32, 5)]
    base, val, result = random.choice(pairs)
    variant = random.choice(["evaluate", "convert_to_exp", "find_argument"])
    if variant == "evaluate":
        return {
            "problem_text": f"Evaluate: \\(\\log_{{{base}}}({val})\\)",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(\\log_b(x) = n\\) means \\(b^n = x\\)."},
                {"level": 2, "text": f"What power of {base} gives {val}?"},
                {"level": 3, "text": f"\\({base}^{{{result}}} = {val}\\), so the answer is {result}."},
            ],
        }
    elif variant == "convert_to_exp":
        return {
            "problem_text": f"Write \\(\\log_{{{base}}}({val}) = {result}\\) in exponential form.",
            "correct_answer": f"{base}**{result}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\log_b(x) = n\\) converts to \\(b^n = x\\)."},
                {"level": 2, "text": f"Base {base}, exponent {result}, result {val}."},
                {"level": 3, "text": f"\\({base}^{{{result}}} = {val}\\)"},
            ],
        }
    else:  # find_argument: log_b(x) = n → find x
        return {
            "problem_text": f"\\(\\log_{{{base}}}(x) = {result}\\). What is \\(x\\)?",
            "correct_answer": str(val),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Rewrite in exponential form: \\(b^n = x\\)."},
                {"level": 2, "text": f"\\({base}^{{{result}}} = x\\)."},
                {"level": 3, "text": f"\\(x = {val}\\)"},
            ],
        }


def _gen_log_rules():
    """
    Practice the log combination rules. The answer stays IN LOG FORM — a single
    logarithm — NOT the evaluated number (that is what log-definition/evaluation
    nodes are for). Change-of-base was removed here in FIXES-16 (14-8): it was
    wrongly added in FIXES-10 and belongs in its own node.

    answer_type is "log_form": the checker accepts any single logarithm with the
    same base and argument (e.g. \\log_2(32), log_2(4\\cdot8), \\log_{2}(32)) and
    REJECTS the evaluated number (5) — see answer_checker._check_log_form.
    """
    variant = random.choice(["product", "quotient", "power"])
    if variant == "product":
        # log_b(a) + log_b(c) = log_b(ac)
        combos = [(2, 4, 8), (3, 9, 27), (2, 4, 16), (2, 2, 8), (5, 5, 25), (2, 8, 16)]
        base, a, c = random.choice(combos)
        product = a * c
        return {
            "problem_text": f"Write as a single logarithm (do not evaluate): \\(\\log_{{{base}}}({a}) + \\log_{{{base}}}({c})\\)",
            "correct_answer": f"\\log_{{{base}}}({product})",
            "answer_type": "log_form",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Product rule: \\(\\log_b(a) + \\log_b(c) = \\log_b(ac)\\)."},
                {"level": 2, "text": f"Multiply the arguments: \\(\\log_{{{base}}}({a} \\cdot {c})\\)."},
                {"level": 3, "text": f"\\({a} \\cdot {c} = {product}\\), so the combined logarithm is \\(\\log_{{{base}}}({product})\\)."},
            ],
        }
    elif variant == "quotient":
        # log_b(a) - log_b(c) = log_b(a/c), with a/c an integer
        pairs = [(2, 16, 4), (2, 32, 8), (3, 27, 9), (2, 8, 2), (10, 1000, 10), (2, 16, 2)]
        base, a, c = random.choice(pairs)
        quotient = a // c
        return {
            "problem_text": f"Write as a single logarithm (do not evaluate): \\(\\log_{{{base}}}({a}) - \\log_{{{base}}}({c})\\)",
            "correct_answer": f"\\log_{{{base}}}({quotient})",
            "answer_type": "log_form",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Quotient rule: \\(\\log_b(a) - \\log_b(c) = \\log_b(a/c)\\)."},
                {"level": 2, "text": f"Divide the arguments: \\(\\log_{{{base}}}({a}/{c})\\)."},
                {"level": 3, "text": f"\\({a} / {c} = {quotient}\\), so the combined logarithm is \\(\\log_{{{base}}}({quotient})\\)."},
            ],
        }
    else:  # power: n * log_b(a) = log_b(a^n)
        pairs = [(2, 3, 2), (2, 2, 4), (3, 2, 3), (10, 3, 10), (5, 2, 3), (2, 4, 2)]
        base, exp, a = random.choice(pairs)
        powered = a ** exp
        return {
            "problem_text": f"Write as a single logarithm (do not evaluate): \\({exp} \\cdot \\log_{{{base}}}({a})\\)",
            "correct_answer": f"\\log_{{{base}}}({powered})",
            "answer_type": "log_form",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Power rule: \\(n \\cdot \\log_b(a) = \\log_b(a^n)\\)."},
                {"level": 2, "text": f"Move the coefficient to an exponent: \\(\\log_{{{base}}}({a}^{{{exp}}})\\)."},
                {"level": 3, "text": f"\\({a}^{{{exp}}} = {powered}\\), so the combined logarithm is \\(\\log_{{{base}}}({powered})\\)."},
            ],
        }


# ─── Summation ────────────────────────────────────────────────────────────────

def _gen_sum_sigma():
    variant = random.choice(["sum_i", "sum_const", "sum_i_squared"])
    if variant == "sum_i":
        n = random.randint(3, 8)
        total = n * (n + 1) // 2
        return {
            "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{n}}} i\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Sigma notation sums the expression as i goes from 1 to n."},
                {"level": 2, "text": f"Add 1 + 2 + ... + {n}. Use \\(\\frac{{n(n+1)}}{{2}}\\)."},
                {"level": 3, "text": f"\\(\\frac{{{n} \\cdot {n+1}}}{{2}} = {total}\\)"},
            ],
        }
    elif variant == "sum_const":
        n = random.randint(3, 8)
        c = random.randint(2, 6)
        total = c * n
        return {
            "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{n}}} {c}\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Summing a constant c from i=1 to n gives c×n."},
                {"level": 2, "text": f"Add {c} exactly {n} times."},
                {"level": 3, "text": f"\\({c} \\times {n} = {total}\\)"},
            ],
        }
    else:  # sum_i_squared: Σi² = n(n+1)(2n+1)/6
        n = random.randint(3, 6)
        total = n * (n + 1) * (2 * n + 1) // 6
        return {
            "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{n}}} i^2\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Formula: \\(\\sum_{{i=1}}^n i^2 = \\frac{{n(n+1)(2n+1)}}{{6}}\\)."},
                {"level": 2, "text": f"Plug in n={n}: \\(\\frac{{{n} \\cdot {n+1} \\cdot {2*n+1}}}{{6}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{n*(n+1)*(2*n+1)}}}{{6}} = {total}\\)"},
            ],
        }


def _gen_sum_arithmetic():
    variant = random.choice(["sum_1_to_n", "find_nth_term", "how_many_terms"])
    if variant == "sum_1_to_n":
        n = random.randint(4, 12)
        total = n * (n + 1) // 2
        return {
            "problem_text": f"Find the sum: \\(1 + 2 + 3 + \\cdots + {n}\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Sum of 1 to n: \\(\\frac{n(n+1)}{2}\\)."},
                {"level": 2, "text": f"Apply with n = {n}."},
                {"level": 3, "text": f"\\(\\frac{{{n} \\times {n+1}}}{{2}} = {total}\\)"},
            ],
        }
    elif variant == "find_nth_term":
        # arithmetic sequence: a, a+d, a+2d, ... find nth term
        a = random.randint(1, 8)
        d = random.randint(2, 6)
        n = random.randint(5, 10)
        term = a + (n - 1) * d
        return {
            "problem_text": f"An arithmetic sequence starts at {a} with common difference {d}. What is the {n}th term?",
            "correct_answer": str(term),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "nth term of arithmetic sequence: \\(a + (n-1)d\\)."},
                {"level": 2, "text": f"\\({a} + ({n}-1) \\times {d} = {a} + {(n-1)*d}\\)."},
                {"level": 3, "text": f"\\(= {term}\\)"},
            ],
        }
    else:  # how_many_terms: sum = n/2*(first+last)
        a = random.randint(1, 5)
        d = random.randint(2, 4)
        n = random.randint(4, 8)
        last = a + (n - 1) * d
        total = n * (a + last) // 2
        return {
            "problem_text": f"Find the sum of the arithmetic sequence: \\({a}, {a+d}, {a+2*d}, \\ldots, {last}\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Sum of arithmetic sequence: \\(S = \\frac{n}{2}(a_1 + a_n)\\)."},
                {"level": 2, "text": f"There are {n} terms. First={a}, last={last}."},
                {"level": 3, "text": f"\\(S = \\frac{{{n}}}{{2}} \\times ({a}+{last}) = \\frac{{{n}}}{{2}} \\times {a+last} = {total}\\)"},
            ],
        }


def _gen_sum_nested():
    variant = random.choice(["double_ij", "double_const_i", "double_i_plus_j"])
    if variant == "double_ij":
        m = random.randint(2, 4)
        n = random.randint(2, 4)
        total = (m * (m + 1) // 2) * (n * (n + 1) // 2)
        return {
            "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{m}}} \\sum_{{j=1}}^{{{n}}} i \\cdot j\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Evaluate inner sum first (fixing i), then outer sum."},
                {"level": 2, "text": f"Inner: \\(i \\cdot \\sum_{{j=1}}^{{{n}}} j = i \\cdot {n*(n+1)//2}\\). Then outer: \\({n*(n+1)//2} \\cdot \\sum_{{i=1}}^{{{m}}} i\\)."},
                {"level": 3, "text": f"\\({n*(n+1)//2} \\times {m*(m+1)//2} = {total}\\)"},
            ],
        }
    elif variant == "double_const_i":
        m = random.randint(2, 4)
        n = random.randint(2, 4)
        # Σ_i Σ_j i = Σ_i (n*i) = n * m(m+1)/2
        total = n * (m * (m + 1) // 2)
        return {
            "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{m}}} \\sum_{{j=1}}^{{{n}}} i\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "The inner sum: i is constant with respect to j, so \\(\\sum_{{j=1}}^{{{n}}} i = {n} \\cdot i\\)."},
                {"level": 2, "text": f"Outer: \\(\\sum_{{i=1}}^{{{m}}} {n} \\cdot i = {n} \\cdot \\frac{{{m}({m+1})}}{{2}}\\)."},
                {"level": 3, "text": f"\\(= {n} \\times {m*(m+1)//2} = {total}\\)"},
            ],
        }
    else:  # double_i_plus_j: Σ_i Σ_j (i+j)
        m = random.randint(2, 3)
        n = random.randint(2, 3)
        total = sum(i + j for i in range(1, m + 1) for j in range(1, n + 1))
        return {
            "problem_text": f"Evaluate: \\(\\sum_{{i=1}}^{{{m}}} \\sum_{{j=1}}^{{{n}}} (i+j)\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.8,
            "hints": [
                {"level": 1, "text": "Split: \\(\\sum_i \\sum_j (i+j) = \\sum_i \\sum_j i + \\sum_i \\sum_j j\\)."},
                {"level": 2, "text": f"First part: {n}·Σi = {n}·{m*(m+1)//2}. Second part: {m}·Σj = {m}·{n*(n+1)//2}."},
                {"level": 3, "text": f"\\({n * (m*(m+1)//2)} + {m * (n*(n+1)//2)} = {total}\\)"},
            ],
        }


# ─── Combinatorics ────────────────────────────────────────────────────────────

def _gen_comb_counting():
    variant = random.choice(["color_size", "menu", "three_choices"])
    if variant == "color_size":
        a, b = random.randint(2, 6), random.randint(2, 6)
        return {
            "problem_text": f"A bag has {a} colors and {b} sizes. How many color-size combinations are possible?",
            "correct_answer": str(a * b),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Fundamental counting principle: multiply choices for each decision."},
                {"level": 2, "text": f"Multiply: {a} colors × {b} sizes."},
                {"level": 3, "text": f"\\({a} \\times {b} = {a*b}\\)"},
            ],
        }
    elif variant == "menu":
        mains = random.randint(3, 6)
        sides = random.randint(2, 5)
        drinks = random.randint(2, 4)
        total = mains * sides * drinks
        return {
            "problem_text": f"A restaurant offers {mains} main dishes, {sides} sides, and {drinks} drinks. How many different meals (one of each) are possible?",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Multiply the number of choices for each course."},
                {"level": 2, "text": f"{mains} × {sides} × {drinks}."},
                {"level": 3, "text": f"\\({mains} \\times {sides} \\times {drinks} = {total}\\)"},
            ],
        }
    else:  # three_choices: license plate style
        a, b, c = random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)
        total = a * b * c
        return {
            "problem_text": f"A code has 3 slots. The first can be {a} letters, the second {b} digits, the third {c} symbols. How many codes are possible?",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Multiply the number of choices for each slot."},
                {"level": 2, "text": f"{a} × {b} × {c}."},
                {"level": 3, "text": f"\\({a} \\times {b} \\times {c} = {total}\\)"},
            ],
        }


def _gen_comb_permutations():
    pairs = [(4, 4), (5, 3), (6, 2), (5, 5), (4, 2), (6, 3), (7, 2)]
    n, r = random.choice(pairs)
    result = math_factorial(n) // math_factorial(n - r)
    variant = random.choice(["abstract", "race", "arrangement"])
    if variant == "abstract":
        return {
            "problem_text": f"How many ways can {r} items be chosen in order from {n} distinct items?",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(P(n,r) = \\frac{n!}{(n-r)!}\\) — ordered selections."},
                {"level": 2, "text": f"\\(P({n},{r}) = {n} \\times {n-1} \\times \\cdots \\times {n-r+1}\\)."},
                {"level": 3, "text": f"\\(P({n},{r}) = {result}\\)"},
            ],
        }
    elif variant == "race":
        contexts = ["runners", "horses", "cars", "swimmers"]
        thing = random.choice(contexts)
        pos_words = {2: "first and second", 3: "gold, silver, and bronze", 4: "first four positions", 5: "top five"}
        pos = pos_words.get(r, f"top {r}")
        return {
            "problem_text": f"In a race with {n} {thing}, how many ways can the {pos} places be filled?",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Order matters — use permutations: \\(P(n,r) = \\frac{n!}{(n-r)!}\\)."},
                {"level": 2, "text": f"\\(P({n},{r}) = {n} \\times {n-1} \\times \\cdots\\)"},
                {"level": 3, "text": f"\\(P({n},{r}) = {result}\\)"},
            ],
        }
    else:  # arrangement of letters/objects
        return {
            "problem_text": f"How many different {r}-letter arrangements can be made from {n} distinct letters?",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Arrangements where order matters: \\(P(n,r)\\)."},
                {"level": 2, "text": f"\\(P({n},{r}) = \\frac{{{n}!}}{{{n-r}!}}\\)."},
                {"level": 3, "text": f"\\(= {result}\\)"},
            ],
        }


def _gen_comb_combinations():
    pairs = [(5, 2), (6, 2), (7, 3), (8, 3), (10, 2), (5, 3), (6, 3), (8, 2)]
    n, r = random.choice(pairs)
    result = math_comb(n, r)
    variant = random.choice(["abstract", "committee", "hand"])
    if variant == "abstract":
        return {
            "problem_text": f"Calculate \\(C({n}, {r})\\) — the number of ways to choose {r} items from {n}.",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(C(n,r) = \\frac{n!}{r!(n-r)!}\\) — unordered selections."},
                {"level": 2, "text": f"\\(C({n},{r}) = \\frac{{{n}!}}{{{r}! \\times {n-r}!}}\\)."},
                {"level": 3, "text": f"\\(C({n},{r}) = {result}\\)"},
            ],
        }
    elif variant == "committee":
        return {
            "problem_text": f"How many ways can a committee of {r} people be chosen from a group of {n}?",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Order doesn't matter for committees — use combinations \\(C(n,r)\\)."},
                {"level": 2, "text": f"\\(C({n},{r}) = \\frac{{{n}!}}{{{r}! \\cdot {n-r}!}}\\)."},
                {"level": 3, "text": f"\\(C({n},{r}) = {result}\\)"},
            ],
        }
    else:  # hand of cards
        return {
            "problem_text": f"From {n} books on a shelf, how many ways can you choose {r} to read (order doesn't matter)?",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Use combinations when order doesn't matter: \\(C(n,r)\\)."},
                {"level": 2, "text": f"\\(C({n},{r}) = \\frac{{{n}!}}{{{r}! \\cdot {n-r}!}}\\)."},
                {"level": 3, "text": f"\\(= {result}\\)"},
            ],
        }


# ─── Geometric sequences ──────────────────────────────────────────────────────

def _gen_geo_sequences():
    variant = random.choice(["find_nth", "find_ratio", "find_first"])
    if variant == "find_nth":
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
                {"level": 1, "text": "nth term: \\(a \\cdot r^{n-1}\\)."},
                {"level": 2, "text": f"\\({a} \\cdot {r}^{{{n-1}}}\\)."},
                {"level": 3, "text": f"\\(= {term}\\)"},
            ],
        }
    elif variant == "find_ratio":
        # Given two consecutive terms, find r
        a = random.randint(1, 5)
        r = random.randint(2, 5)
        t1 = a * r
        t2 = t1 * r
        return {
            "problem_text": f"In a geometric sequence, the 2nd term is {t1} and the 3rd term is {t2}. What is the common ratio?",
            "correct_answer": str(r),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "The common ratio r = (next term) / (current term)."},
                {"level": 2, "text": f"r = {t2} ÷ {t1}."},
                {"level": 3, "text": f"r = {r}"},
            ],
        }
    else:  # find_first term given nth term and ratio
        r = random.randint(2, 3)
        n = random.randint(3, 5)
        a = random.randint(1, 4)
        term = a * r ** (n - 1)
        return {
            "problem_text": f"A geometric sequence has common ratio {r}. Its {n}th term is {term}. What is the first term?",
            "correct_answer": str(a),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "nth term = a · r^(n-1). Solve for a."},
                {"level": 2, "text": f"a = {term} ÷ {r}^{{{n-1}}} = {term} ÷ {r**(n-1)}."},
                {"level": 3, "text": f"a = {a}"},
            ],
        }


def _gen_geo_finite():
    variant = random.choice(["find_sum", "find_n_terms", "explicit_series"])
    if variant == "find_sum":
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
                {"level": 1, "text": "\\(S_n = \\frac{a(r^n-1)}{r-1}\\)."},
                {"level": 2, "text": f"\\(S_{{{n}}} = \\frac{{{a}({r}^{{{n}}}-1)}}{{{r}-1}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{a}({r**n}-1)}}{{{r-1}}} = {total}\\)"},
            ],
        }
    elif variant == "find_n_terms":
        # Given a, r, and sum, find n
        a = random.randint(1, 3)
        r = random.randint(2, 3)
        n = random.randint(3, 5)
        total = a * (r ** n - 1) // (r - 1)
        return {
            "problem_text": f"A geometric series with \\(a={a}\\), \\(r={r}\\) has sum {total}. How many terms were added?",
            "correct_answer": str(n),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Use \\(S_n = \\frac{a(r^n-1)}{r-1}\\) and solve for n."},
                {"level": 2, "text": f"\\({total} = \\frac{{{a}({r}^n-1)}}{{{r-1}}}\\). Try small values of n."},
                {"level": 3, "text": f"n = {n} gives \\(S_{{{n}}} = {total}\\)."},
            ],
        }
    else:  # explicit_series: list terms, ask for sum
        a = random.randint(1, 3)
        r = random.randint(2, 3)
        n = random.randint(3, 4)
        terms = [a * r ** i for i in range(n)]
        total = sum(terms)
        terms_str = " + ".join(str(t) for t in terms)
        return {
            "problem_text": f"Find the sum: \\({terms_str}\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "This is a geometric series. Identify a and r, then use the sum formula."},
                {"level": 2, "text": f"a = {a}, r = {r}, n = {n}. Apply \\(S_n = \\frac{{a(r^n-1)}}{{r-1}}\\)."},
                {"level": 3, "text": f"\\(S_{{{n}}} = {total}\\)"},
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
    if b == 1:
        parts.append("+ x")
    elif b == -1:
        parts.append("- x")
    elif b > 0:
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
    pairs = [(2, 3, 8), (2, 4, 16), (2, 5, 32), (3, 2, 9), (3, 3, 27),
             (10, 2, 100), (5, 2, 25), (4, 2, 16), (2, 6, 64)]
    base, exp, val = random.choice(pairs)
    variant = random.choice(["solve_for_x", "solve_for_exp", "solve_both_sides"])
    if variant == "solve_for_x":
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\log_{{{base}}}(x) = {exp}\\)",
            "correct_answer": str(val),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Rewrite in exponential form: \\(\\log_b(x)=n \\Rightarrow b^n=x\\)."},
                {"level": 2, "text": f"\\({base}^{{{exp}}} = x\\)."},
                {"level": 3, "text": f"\\(x = {val}\\)"},
            ],
        }
    elif variant == "solve_for_exp":
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\log_{{{base}}}({val}) = x\\)",
            "correct_answer": str(exp),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Ask: what power of the base gives the argument?"},
                {"level": 2, "text": f"What power of {base} gives {val}?"},
                {"level": 3, "text": f"\\({base}^{{{exp}}} = {val}\\), so \\(x = {exp}\\)"},
            ],
        }
    else:  # log(x) = log(val) → x = val, or log(ax) = n form
        offset = random.randint(2, 5)
        new_val = val + offset  # log_base(x - offset) = exp → x - offset = val → x = val + offset
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\log_{{{base}}}(x - {offset}) = {exp}\\)",
            "correct_answer": str(new_val),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Rewrite in exponential form first, then solve for x."},
                {"level": 2, "text": f"\\(x - {offset} = {base}^{{{exp}}} = {val}\\)."},
                {"level": 3, "text": f"\\(x = {val} + {offset} = {new_val}\\)"},
            ],
        }


def _gen_geo_infinite():
    options = [
        (1, 1, 2, 2), (2, 1, 2, 4), (3, 1, 2, 6),
        (2, 1, 3, 3), (4, 1, 3, 6), (3, 1, 4, 4),
        (1, 2, 3, 3), (2, 2, 3, 6),
    ]
    a, r_num, r_den, total = random.choice(options)
    r_str = f"\\frac{{{r_num}}}{{{r_den}}}"
    denom_diff = r_den - r_num
    variant = random.choice(["find_sum", "find_ratio", "explicit_series"])
    if variant == "find_sum":
        return {
            "problem_text": f"Find the sum of the infinite geometric series with \\(a={a}\\) and \\(r={r_str}\\).",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "\\(S = \\frac{a}{1-r}\\) for \\(|r| < 1\\)."},
                {"level": 2, "text": f"\\(S = \\frac{{{a}}}{{1 - {r_str}}} = \\frac{{{a}}}{{\\frac{{{denom_diff}}}{{{r_den}}}}}\\)."},
                {"level": 3, "text": f"\\(S = {a} \\cdot \\frac{{{r_den}}}{{{denom_diff}}} = {total}\\)"},
            ],
        }
    elif variant == "find_ratio":
        # Given sum and first term, find r: r = 1 - a/S
        return {
            "problem_text": f"An infinite geometric series has first term {a} and sum {total}. What is the common ratio?",
            "correct_answer": f"{r_num}/{r_den}",
            "answer_type": "symbolic",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "From \\(S = \\frac{a}{1-r}\\), solve for r: \\(r = 1 - \\frac{a}{S}\\)."},
                {"level": 2, "text": f"\\(r = 1 - \\frac{{{a}}}{{{total}}} = 1 - \\frac{{{a}}}{{{total}}}\\)."},
                {"level": 3, "text": f"\\(r = {r_num}/{r_den}\\)"},
            ],
        }
    else:  # explicit: show first few terms — only use options where terms are integers
        int_options = [
            (2, 1, 2, 4),  # 2 + 1 + 1/2 + ... but let's use options with integer terms
            (4, 1, 2, 8),  # 4 + 2 + 1 + ...
            (3, 1, 3, 9//2),  # skip, not integer sum
        ]
        # Use only options where a, a*r, a*r^2 are all integers
        # With r=1/2: a must be divisible by 4 for 3 integer terms
        # Simple approach: just show 2 terms + ellipsis using exact fractions
        from fractions import Fraction as F
        rf = F(r_num, r_den)
        t1 = F(a)
        t2 = t1 * rf
        t3 = t2 * rf
        def fmt(f):
            if f.denominator == 1:
                return str(f.numerator)
            return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"
        return {
            "problem_text": f"Find the sum of the infinite series: \\({fmt(t1)} + {fmt(t2)} + {fmt(t3)} + \\cdots\\)",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Identify a and r, then use \\(S = \\frac{a}{1-r}\\)."},
                {"level": 2, "text": f"a = {a}, r = {r_str}. Use \\(S = \\frac{{a}}{{1-r}}\\)."},
                {"level": 3, "text": f"\\(S = {total}\\)"},
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

# ─── Extended generators (146 additional nodes) ───────────────────────────────
from .generators.algebra import GENERATORS as _ALGEBRA_GENERATORS
from .generators.precalculus import GENERATORS as _PRECALC_GENERATORS
from .generators.calculus import GENERATORS as _CALC_GENERATORS
from .generators.linear_algebra import GENERATORS as _LINALG_GENERATORS
from .generators.probability import GENERATORS as _PROB_GENERATORS
from .generators.statistics import GENERATORS as _STAT_GENERATORS

GENERATORS.update(_ALGEBRA_GENERATORS)
GENERATORS.update(_PRECALC_GENERATORS)
GENERATORS.update(_CALC_GENERATORS)
GENERATORS.update(_LINALG_GENERATORS)
GENERATORS.update(_PROB_GENERATORS)
GENERATORS.update(_STAT_GENERATORS)


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
