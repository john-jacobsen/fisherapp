#!/usr/bin/env python3
"""
Generate parameterized algebra problems for Fisher App knowledge nodes.
Fills nodes that have < 10 problems with up to 10 generated problems.

Usage (from project root):
    docker compose run --rm backend python scripts/generate_problems.py
"""
import uuid
import random
from fractions import Fraction

MIN_PROBLEMS = 10


def frac_basic_problems(count=5):
    """Generate fraction simplification problems."""
    problems = []
    for _ in range(count):
        # Generate a reducible fraction
        factor = random.randint(2, 6)
        a = random.randint(1, 8) * factor
        b = random.randint(1, 8) * factor
        f = Fraction(a, b)
        problems.append({
            "statement": f"Simplify the fraction: {a}/{b}",
            "correct_answer": f"{f.numerator}/{f.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.3,
        })
    return problems


def frac_add_sub_problems(count=5):
    problems = []
    for _ in range(count):
        a = Fraction(random.randint(1, 6), random.randint(2, 8))
        b = Fraction(random.randint(1, 6), random.randint(2, 8))
        op = random.choice(["+", "-"])
        result = a + b if op == "+" else a - b
        if result < 0:
            result = abs(result)
            op = "+" if op == "-" else "-"
        problems.append({
            "statement": f"Calculate: {a.numerator}/{a.denominator} {op} {b.numerator}/{b.denominator}",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
        })
    return problems


def frac_mult_div_problems(count=5):
    problems = []
    for _ in range(count):
        a = Fraction(random.randint(1, 6), random.randint(2, 8))
        b = Fraction(random.randint(1, 6), random.randint(2, 8))
        op = random.choice(["x", "/"])
        result = a * b if op == "x" else a / b
        op_symbol = "\u00d7" if op == "x" else "\u00f7"
        problems.append({
            "statement": f"Calculate: {a.numerator}/{a.denominator} {op_symbol} {b.numerator}/{b.denominator}",
            "correct_answer": f"{result.numerator}/{result.denominator}",
            "answer_type": "symbolic",
            "difficulty": 0.5,
        })
    return problems


def exp_basic_problems(count=5):
    problems = []
    for _ in range(count):
        base = random.randint(2, 5)
        exp = random.randint(2, 4)
        problems.append({
            "statement": f"Evaluate: {base}^{exp}",
            "correct_answer": str(base ** exp),
            "answer_type": "numeric",
            "difficulty": 0.3,
        })
    return problems


def order_ops_problems(count=5):
    problems = []

    def make_problem():
        choice = random.randint(0, 2)
        if choice == 0:
            a = random.randint(2, 5)
            b = random.randint(2, 5)
            c = random.randint(2, 5)
            expr_display = f"{a} + {b} \u00d7 {c}"
            result = a + b * c
        elif choice == 1:
            a = random.randint(2, 8)
            b = random.randint(2, 8)
            c = random.randint(2, 5)
            expr_display = f"({a} + {b}) \u00d7 {c}"
            result = (a + b) * c
        else:
            a = random.randint(2, 6)
            b = random.randint(2, 8)
            expr_display = f"{a}\u00b2 + {b}"
            result = a ** 2 + b
        return expr_display, int(result)

    for _ in range(count):
        try:
            expr_display, result = make_problem()
            problems.append({
                "statement": f"Evaluate using the correct order of operations: {expr_display}",
                "correct_answer": str(result),
                "answer_type": "numeric",
                "difficulty": 0.5,
            })
        except Exception:
            pass
    return problems


def eq_linear_one_problems(count=5):
    problems = []
    for _ in range(count):
        # ax + b = c  =>  x = (c - b) / a
        a = random.randint(2, 6)
        x = random.randint(-5, 10)
        b = random.randint(-10, 10)
        c = a * x + b
        b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        problems.append({
            "statement": f"Solve for x: {a}x {b_str} = {c}",
            "correct_answer": str(x),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def log_basic_problems(count=5):
    problems = []
    pairs = [(2, 8, 3), (3, 9, 2), (10, 100, 2), (2, 16, 4), (5, 25, 2), (3, 27, 3)]
    for base, val, result in random.sample(pairs, min(count, len(pairs))):
        problems.append({
            "statement": f"Evaluate: log\u2082({val})" if base == 2 else f"Evaluate: log_{base}({val})",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def sigma_basic_problems(count=5):
    problems = []
    for _ in range(count):
        n = random.randint(3, 8)
        # Sum of i from 1 to n
        total = n * (n + 1) // 2
        problems.append({
            "statement": f"Evaluate: \u03a3(i) for i=1 to {n}",
            "correct_answer": str(total),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


def comb_basic_problems(count=5):
    from math import comb as math_comb
    problems = []
    pairs = [(5, 2), (6, 2), (7, 3), (8, 3), (10, 2), (10, 4)]
    for n, r in random.sample(pairs, min(count, len(pairs))):
        result = math_comb(n, r)
        problems.append({
            "statement": f"Calculate C({n}, {r}) \u2014 the number of ways to choose {r} items from {n}.",
            "correct_answer": str(result),
            "answer_type": "numeric",
            "difficulty": 0.5,
        })
    return problems


GENERATORS = {
    "frac_basic": frac_basic_problems,
    "frac_add_sub": frac_add_sub_problems,
    "frac_mult_div": frac_mult_div_problems,
    "exp_basic": exp_basic_problems,
    "order_ops": order_ops_problems,
    "eq_linear_one": eq_linear_one_problems,
    "log_basic": log_basic_problems,
    "sigma_basic": sigma_basic_problems,
    "comb_basic": comb_basic_problems,
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
        new_problems = generator(count=needed + 2)  # generate extra, deduplicate

        added = 0
        for p_data in new_problems:
            if added >= needed:
                break
            # Check for duplicate statement
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
        print(f"  {node.id}: added {added} generated problems (total now: {existing_count + added})")

    db.commit()
    db.close()
    print(f"\nDone. Total problems added: {total_added}")


if __name__ == "__main__":
    main()
