#!/usr/bin/env python3
"""
Generate parameterized algebra problems for Fisher App knowledge nodes.
Fills nodes that have < MIN_PROBLEMS problems with up to MIN_PROBLEMS generated problems.

Usage (from project root):
    docker compose run --rm backend python scripts/generate_problems.py
"""
import uuid
import random
from fractions import Fraction
from math import factorial as math_factorial, comb as math_comb

MIN_PROBLEMS = 10


# ─── Generator functions ──────────────────────────────────────────────────────

def frac_simplify_problems(count=8):
    """Simplifying fractions — node: frac-simplify"""
    problems = []
    for _ in range(count):
        factor = random.randint(2, 6)
        a = random.randint(1, 8) * factor
        b = random.randint(2, 9) * factor
        while a == b:
            b = random.randint(2, 9) * factor
        f = Fraction(a, b)
        problems.append({
            "statement": f"Simplify the fraction: \\frac{{{a}}}{{{b}}}",
            "correct_answer": f"{f.numerator}/{f.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.3,
        })
    return problems


def frac_add_like_problems(count=8):
    """Adding fractions with like denominators — node: frac-add-like"""
    problems = []
    ops = [('+', lambda a, b: a + b), ('-', lambda a, b: a - b)]
    for _ in range(count):
        d = random.randint(3, 12)
        a = random.randint(1, d - 1)
        b = random.randint(1, d - 1)
        op_sym, op_fn = random.choice(ops)
        result = op_fn(Fraction(a, d), Fraction(b, d))
        if result < 0:
            a, b = b, a
            result = op_fn(Fraction(a, d), Fraction(b, d))
        problems.append({
            "statement": f"Calculate: \\frac{{{a}}}{{{d}}} {op_sym} \\frac{{{b}}}{{{d}}}",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.3,
        })
    return problems


def frac_common_denom_problems(count=8):
    """Finding common denominators — node: frac-common-denom"""
    problems = []
    pairs = [(2, 3), (3, 4), (4, 6), (2, 5), (3, 5), (4, 5), (6, 9), (2, 7), (3, 8)]
    for a, b in random.sample(pairs, min(count, len(pairs))):
        import math
        lcd = a * b // math.gcd(a, b)
        problems.append({
            "statement": f"Find the LCD of \\frac{{1}}{{{a}}} and \\frac{{1}}{{{b}}}.",
            "correct_answer": str(lcd),
            "answer_type": "numeric",
            "difficulty": 0.3,
        })
    return problems


def frac_add_unlike_problems(count=8):
    """Adding fractions with unlike denominators — node: frac-add-unlike"""
    problems = []
    for _ in range(count):
        a = Fraction(random.randint(1, 5), random.randint(2, 8))
        b = Fraction(random.randint(1, 5), random.randint(2, 8))
        while a.denominator == b.denominator:
            b = Fraction(random.randint(1, 5), random.randint(2, 8))
        op_sym = random.choice(['+', '-'])
        result = a + b if op_sym == '+' else a - b
        if result < 0:
            op_sym = '+' if op_sym == '-' else '-'
            result = abs(result)
            a, b = b, a
        problems.append({
            "statement": f"Calculate: \\frac{{{a.numerator}}}{{{a.denominator}}} {op_sym} \\frac{{{b.numerator}}}{{{b.denominator}}}",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
        })
    return problems


def frac_multiply_problems(count=8):
    """Multiplying fractions — node: frac-multiply"""
    problems = []
    for _ in range(count):
        a = Fraction(random.randint(1, 6), random.randint(2, 8))
        b = Fraction(random.randint(1, 6), random.randint(2, 8))
        result = a * b
        problems.append({
            "statement": f"Multiply: \\frac{{{a.numerator}}}{{{a.denominator}}} \\times \\frac{{{b.numerator}}}{{{b.denominator}}}",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
        })
    return problems


def frac_divide_problems(count=8):
    """Dividing fractions — node: frac-divide"""
    problems = []
    for _ in range(count):
        a = Fraction(random.randint(1, 6), random.randint(2, 8))
        b = Fraction(random.randint(1, 6), random.randint(2, 8))
        result = a / b
        problems.append({
            "statement": f"Divide: \\frac{{{a.numerator}}}{{{a.denominator}}} \\div \\frac{{{b.numerator}}}{{{b.denominator}}}",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
        })
    return problems


def order_pemdas_problems(count=8):
    """Order of operations — node: order-pemdas"""
    problems = []
    for _ in range(count):
        choice = random.randint(0, 2)
        if choice == 0:
            a, b, c = random.randint(2, 5), random.randint(2, 5), random.randint(2, 5)
            expr = f"{a} + {b} \\times {c}"
            result = a + b * c
        elif choice == 1:
            a, b = random.randint(2, 9), random.randint(2, 4)
            expr = f"{a} \\div {b}"
            if a % b != 0:
                a = b * random.randint(2, 6)
            result = a // b
            expr = f"{a} \\div {b}"
        else:
            a, b = random.randint(2, 5), random.randint(1, 9)
            expr = f"{a}^2 + {b}"
            result = a ** 2 + b
        problems.append({
            "statement": f"Evaluate using the correct order of operations: ${expr}$",
            "correct_answer": str(int(result)),
            "answer_type": "numeric",
            "difficulty": 0.4,
        })
    return problems


def order_nested_problems(count=8):
    """Nested expressions — node: order-nested"""
    problems = []
    for _ in range(count):
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        c = random.randint(2, 4)
        result = (a + b) * c
        problems.append({
            "statement": f"Evaluate: $({a} + {b}) \\times {c}$",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def exp_product_problems(count=8):
    """Product rule for exponents — node: exp-product"""
    problems = []
    for _ in range(count):
        a, b = random.randint(2, 6), random.randint(2, 6)
        problems.append({
            "statement": f"Simplify: $x^{{{a}}} \\cdot x^{{{b}}}$",
            "correct_answer": f"x**{a+b}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
        })
    return problems


def exp_power_problems(count=8):
    """Power rule — node: exp-power"""
    problems = []
    for _ in range(count):
        a, b = random.randint(2, 4), random.randint(2, 4)
        problems.append({
            "statement": f"Simplify: $(x^{{{a}}})^{{{b}}}$",
            "correct_answer": f"x**{a*b}",
            "answer_type": "symbolic",
            "difficulty": 0.4,
        })
    return problems


def exp_negative_problems(count=8):
    """Negative exponents — node: exp-negative"""
    problems = []
    for _ in range(count):
        base = random.randint(2, 5)
        exp = random.randint(1, 3)
        result = Fraction(1, base ** exp)
        problems.append({
            "statement": f"Evaluate: ${base}^{{-{exp}}}$",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
        })
    return problems


def exp_combined_problems(count=8):
    """Combined exponent rules — node: exp-combined"""
    problems = []
    for _ in range(count):
        a, b = random.randint(2, 5), random.randint(1, 3)
        net = a - b
        problems.append({
            "statement": f"Simplify: $\\frac{{x^{{{a}}}}}{{x^{{{b}}}}}$",
            "correct_answer": f"x**{net}" if net != 1 else "x",
            "answer_type": "symbolic",
            "difficulty": 0.6,
        })
    return problems


def eq_one_step_problems(count=8):
    """One-step linear equations — node: eq-one-step"""
    problems = []
    for _ in range(count):
        a = random.randint(2, 8)
        x = random.randint(1, 15)
        b_str = f"+ {random.randint(1, 12)}"
        # Randomly choose add/subtract/multiply/divide
        choice = random.randint(0, 1)
        if choice == 0:
            b = random.randint(1, 12)
            c = x + b
            problems.append({
                "statement": f"Solve for x: $x + {b} = {c}$",
                "correct_answer": str(x),
                "answer_type": "numeric",
                "difficulty": 0.3,
            })
        else:
            problems.append({
                "statement": f"Solve for x: ${a}x = {a * x}$",
                "correct_answer": str(x),
                "answer_type": "numeric",
                "difficulty": 0.3,
            })
    return problems


def eq_two_step_problems(count=8):
    """Two-step linear equations — node: eq-two-step"""
    problems = []
    for _ in range(count):
        a = random.randint(2, 6)
        x = random.randint(1, 10)
        b = random.randint(1, 10)
        c = a * x + b
        problems.append({
            "statement": f"Solve for x: ${a}x + {b} = {c}$",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def eq_fractions_problems(count=8):
    """Equations with fractions — node: eq-fractions"""
    problems = []
    for _ in range(count):
        a = random.randint(2, 5)
        x = random.randint(2, 10)
        c = a * x
        problems.append({
            "statement": f"Solve for x: $\\frac{{{a}x}}{{{a}}} = {x}$",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.6,
        })
    return problems


def eq_distribution_problems(count=8):
    """Equations with distribution — node: eq-distribution"""
    problems = []
    for _ in range(count):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        x = random.randint(1, 8)
        c = a * (x + b)
        problems.append({
            "statement": f"Solve for x: ${a}(x + {b}) = {c}$",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.6,
        })
    return problems


def log_definition_problems(count=8):
    """Logarithm definition — node: log-definition"""
    pairs = [(2, 4, 2), (2, 8, 3), (2, 16, 4), (3, 9, 2), (3, 27, 3), (10, 100, 2), (5, 25, 2), (10, 1000, 3)]
    problems = []
    for base, val, result in random.sample(pairs, min(count, len(pairs))):
        problems.append({
            "statement": f"Evaluate: $\\log_{{{base}}}({val})$",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def log_exponential_problems(count=8):
    """Exponential functions — node: log-exponential"""
    problems = []
    for _ in range(count):
        base = random.randint(2, 5)
        exp = random.randint(2, 4)
        problems.append({
            "statement": f"Evaluate: ${base}^{{{exp}}}$",
            "correct_answer": str(base ** exp),
            "answer_type": "numeric",
            "difficulty": 0.3,
        })
    return problems


def log_rules_problems(count=8):
    """Logarithm rules — node: log-rules"""
    problems = []
    combos = [(2, 4, 8, 2, 3, 5), (3, 9, 27, 2, 3, 5), (2, 8, 4, 3, 2, 1)]
    for base, a, b, log_a, log_b, result in random.sample(combos, min(count // 2, len(combos))):
        problems.append({
            "statement": f"Simplify: $\\log_{{{base}}}({a}) + \\log_{{{base}}}({b})$",
            "correct_answer": str(log_a + log_b),
            "answer_type": "numeric",
            "difficulty": 0.6,
        })
    for _ in range(count - len(problems)):
        base = random.choice([2, 3, 10])
        exp = random.randint(2, 4)
        val = base ** exp
        problems.append({
            "statement": f"Evaluate: $\\log_{{{base}}}({val})$",
            "correct_answer": str(exp),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def sum_sigma_problems(count=8):
    """Sigma notation — node: sum-sigma"""
    problems = []
    for _ in range(count):
        n = random.randint(3, 8)
        total = n * (n + 1) // 2
        problems.append({
            "statement": f"Evaluate: $\\sum_{{i=1}}^{{{n}}} i$",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def sum_arithmetic_problems(count=8):
    """Arithmetic sums — node: sum-arithmetic"""
    problems = []
    for _ in range(count):
        n = random.randint(4, 12)
        total = n * (n + 1) // 2
        problems.append({
            "statement": f"Find the sum: $1 + 2 + 3 + \\cdots + {n}$",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def sum_nested_problems(count=8):
    """Nested sums — node: sum-nested"""
    problems = []
    for _ in range(count):
        m = random.randint(2, 4)
        n = random.randint(2, 4)
        total = (m * (m + 1) // 2) * (n * (n + 1) // 2)
        problems.append({
            "statement": f"Evaluate: $\\sum_{{i=1}}^{{{m}}} \\sum_{{j=1}}^{{{n}}} i \\cdot j$",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.7,
        })
    return problems


def comb_counting_problems(count=8):
    """Counting principles — node: comb-counting"""
    problems = []
    for _ in range(count):
        a = random.randint(2, 6)
        b = random.randint(2, 6)
        problems.append({
            "statement": f"A bag has {a} colors and {b} sizes. How many color-size combinations are possible?",
            "correct_answer": str(a * b),
            "answer_type": "numeric",
            "difficulty": 0.3,
        })
    return problems


def comb_permutations_problems(count=8):
    """Permutations — node: comb-permutations"""
    problems = []
    pairs = [(4, 4), (5, 3), (6, 2), (5, 5), (4, 2), (6, 3)]
    for n, r in random.sample(pairs, min(count, len(pairs))):
        result = math_factorial(n) // math_factorial(n - r)
        problems.append({
            "statement": f"How many ways can {r} items be chosen in order from {n} distinct items?",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def comb_combinations_problems(count=8):
    """Combinations — node: comb-combinations"""
    problems = []
    pairs = [(5, 2), (6, 2), (7, 3), (8, 3), (10, 2), (5, 3), (6, 4)]
    for n, r in random.sample(pairs, min(count, len(pairs))):
        result = math_comb(n, r)
        problems.append({
            "statement": f"Calculate $C({n}, {r})$ — the number of ways to choose {r} items from {n}.",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def geo_sequences_problems(count=8):
    """Geometric sequences — node: geo-sequences"""
    problems = []
    for _ in range(count):
        a = random.randint(1, 5)
        r = random.randint(2, 4)
        n = random.randint(4, 6)
        term = a * r ** (n - 1)
        problems.append({
            "statement": f"A geometric sequence has first term {a} and ratio {r}. Find the {n}th term.",
            "correct_answer": str(term),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def geo_finite_problems(count=8):
    """Finite geometric sums — node: geo-finite"""
    problems = []
    for _ in range(count):
        a = random.randint(1, 4)
        r = random.randint(2, 3)
        n = random.randint(3, 5)
        total = a * (r ** n - 1) // (r - 1)
        problems.append({
            "statement": f"Find the sum of the first {n} terms of a geometric series with $a={a}$, $r={r}$.",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.6,
        })
    return problems


# ─── Node → generator mapping ─────────────────────────────────────────────────

GENERATORS = {
    "frac-simplify":     frac_simplify_problems,
    "frac-add-like":     frac_add_like_problems,
    "frac-common-denom": frac_common_denom_problems,
    "frac-add-unlike":   frac_add_unlike_problems,
    "frac-multiply":     frac_multiply_problems,
    "frac-divide":       frac_divide_problems,
    "order-pemdas":      order_pemdas_problems,
    "order-nested":      order_nested_problems,
    "exp-product":       exp_product_problems,
    "exp-power":         exp_power_problems,
    "exp-negative":      exp_negative_problems,
    "exp-combined":      exp_combined_problems,
    "eq-one-step":       eq_one_step_problems,
    "eq-two-step":       eq_two_step_problems,
    "eq-fractions":      eq_fractions_problems,
    "eq-distribution":   eq_distribution_problems,
    "log-exponential":   log_exponential_problems,
    "log-definition":    log_definition_problems,
    "log-rules":         log_rules_problems,
    "sum-sigma":         sum_sigma_problems,
    "sum-arithmetic":    sum_arithmetic_problems,
    "sum-nested":        sum_nested_problems,
    "comb-counting":     comb_counting_problems,
    "comb-permutations": comb_permutations_problems,
    "comb-combinations": comb_combinations_problems,
    "geo-sequences":     geo_sequences_problems,
    "geo-finite":        geo_finite_problems,
}


def main():
    from app.database import SessionLocal
    from app.models.content import Problem
    from app.models.knowledge import KnowledgeNode

    db = SessionLocal()
    nodes = db.query(KnowledgeNode).all()
    total_added = 0

    for node in nodes:
        existing_count = db.query(Problem).filter(
            Problem.node_id == node.id,
        ).count()

        if existing_count >= MIN_PROBLEMS:
            print(f"  {node.id}: {existing_count} problems (OK)")
            continue

        generator = GENERATORS.get(node.id)
        if not generator:
            print(f"  {node.id}: {existing_count} problems (no generator)")
            continue

        needed = MIN_PROBLEMS - existing_count
        new_problems = generator(count=needed + 3)  # generate extra for dedup

        added = 0
        for p_data in new_problems:
            if added >= needed:
                break
            exists = db.query(Problem).filter(
                Problem.node_id == node.id,
                Problem.problem_text == p_data["statement"],
            ).first()
            if exists:
                continue

            prob = Problem(
                id=uuid.uuid4(),
                node_id=node.id,
                problem_text=p_data["statement"],
                answer_type=p_data["answer_type"],
                correct_answer=p_data["correct_answer"],
                difficulty=p_data.get("difficulty", 0.5),
                source="generator",
            )
            db.add(prob)
            added += 1
            total_added += 1

        db.flush()
        print(f"  {node.id}: added {added} generated problems (total: {existing_count + added})")

    db.commit()
    db.close()
    print(f"\nDone. Total problems added: {total_added}")


if __name__ == "__main__":
    main()
