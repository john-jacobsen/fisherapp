"""
Precalculus problem generators for Fisher App 3.0.
Covers 5 nodes: precalc-functions through precalc-poly-func.

Drop this file at: backend/app/services/generators/precalculus.py
Then in problem_generator.py add:
    from .generators.precalculus import GENERATORS as PRECALC_GENERATORS
    GENERATORS.update(PRECALC_GENERATORS)
"""
import random
from fractions import Fraction
from math import gcd


def _lin(a, b):
    """Return clean display string for ax + b. Handles a=±1, b=0."""
    a_str = "" if a == 1 else ("-" if a == -1 else str(a))
    if b == 0:
        return f"{a_str}x"
    b_str = f"+ {b}" if b > 0 else f"- {abs(b)}"
    return f"{a_str}x {b_str}"


def _quadratic(b, c):
    """Return clean display for x^2 + bx + c, skipping zero terms."""
    parts = ["x^2"]
    if b == 1:    parts.append("+ x")
    elif b == -1: parts.append("- x")
    elif b > 0:   parts.append(f"+ {b}x")
    elif b < 0:   parts.append(f"- {abs(b)}x")
    if c > 0:     parts.append(f"+ {c}")
    elif c < 0:   parts.append(f"- {abs(c)}")
    return " ".join(parts)


def _cubic(a, b, c, d):
    """Return clean display for ax^3 + bx^2 + cx + d, skipping zero terms."""
    a_str = "" if a == 1 else str(a)
    parts = [f"{a_str}x^3"]
    for coef, var in [(b, "x^2"), (c, "x")]:
        if coef == 1:    parts.append(f"+ {var}")
        elif coef == -1: parts.append(f"- {var}")
        elif coef > 0:   parts.append(f"+ {coef}{var}")
        elif coef < 0:   parts.append(f"- {abs(coef)}{var}")
    if d > 0:   parts.append(f"+ {d}")
    elif d < 0: parts.append(f"- {abs(d)}")
    return " ".join(parts)


# ─── precalc-functions ────────────────────────────────────────────────────────

def _gen_precalc_functions():
    choice = random.randint(0, 2)
    if choice == 0:
        a = random.randint(2, 5)
        b = random.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6])
        x = random.randint(-4, 4)
        fx = a * x + b
        return {
            "problem_text": f"Let \\(f(x) = {_lin(a, b)}\\). Find \\(f({x})\\).",
            "correct_answer": str(fx),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "To evaluate a function, substitute the input value in place of \\(x\\)."},
                {"level": 2, "text": f"Replace \\(x\\) with \\({x}\\) in \\(f(x) = {_lin(a, b)}\\)."},
                {"level": 3, "text": f"\\(f({x}) = {a}({x}) + ({b}) = {a*x} + ({b}) = {fx}\\)"},
            ],
        }
    elif choice == 1:
        b = random.choice([-4,-3,-2,2,3,4])
        c = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
        x = random.randint(-3, 3)
        fx = x**2 + b*x + c
        return {
            "problem_text": f"Let \\(f(x) = {_quadratic(b, c)}\\). Find \\(f({x})\\).",
            "correct_answer": str(fx),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Substitute the input value for every \\(x\\) in the expression."},
                {"level": 2, "text": f"Replace each \\(x\\) with \\({x}\\) and compute term by term."},
                {"level": 3, "text": f"\\(({x})^2 + {b}({x}) + ({c}) = {x**2} + {b*x} + ({c}) = {fx}\\)"},
            ],
        }
    else:
        a = random.randint(1, 3)
        b = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
        x = random.randint(-4, 4)
        inner = a * x + b
        fx = abs(inner)
        return {
            "problem_text": f"Let \\(f(x) = |{_lin(a, b)}|\\). Find \\(f({x})\\).",
            "correct_answer": str(fx),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Substitute the value, evaluate inside the absolute value, then take the non-negative result."},
                {"level": 2, "text": f"First compute \\({a}({x}) + ({b}) = {inner}\\)."},
                {"level": 3, "text": f"\\(|{inner}| = {fx}\\)"},
            ],
        }


# ─── precalc-domain-range ─────────────────────────────────────────────────────

def _gen_precalc_domain_range():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        a = random.randint(1, 6)
        return {
            "problem_text": f"What value of \\(x\\) is excluded from the domain of \\(f(x) = \\frac{{1}}{{x - {a}}}\\)?",
            "correct_answer": str(a),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "The domain excludes values that make the denominator equal to zero."},
                {"level": 2, "text": f"Set the denominator equal to zero: \\(x - {a} = 0\\)."},
                {"level": 3, "text": f"\\(x - {a} = 0 \\Rightarrow x = {a}\\). This value is excluded from the domain."},
            ],
        }
    elif variant == 1:
        a = random.randint(1, 8)
        return {
            "problem_text": f"What is the smallest value of \\(x\\) in the domain of \\(f(x) = \\sqrt{{x - {a}}}\\)?",
            "correct_answer": str(a),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "A square root requires the expression inside to be non-negative (≥ 0)."},
                {"level": 2, "text": f"Set \\(x - {a} \\geq 0\\) and solve for \\(x\\)."},
                {"level": 3, "text": f"\\(x - {a} \\geq 0 \\Rightarrow x \\geq {a}\\). The smallest value in the domain is \\(x = {a}\\)."},
            ],
        }
    else:
        a = random.randint(1, 8)
        return {
            "problem_text": f"What is the boundary value excluded from the domain of \\(f(x) = \\ln(x - {a})\\)?",
            "correct_answer": str(a),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "A logarithm requires its argument to be strictly positive: \\(\\ln(u)\\) is defined only for \\(u > 0\\)."},
                {"level": 2, "text": f"Set \\(x - {a} > 0\\). The boundary (excluded) value is where \\(x - {a} = 0\\)."},
                {"level": 3, "text": f"\\(x - {a} = 0 \\Rightarrow x = {a}\\). The domain is \\(x > {a}\\); the boundary \\({a}\\) is excluded."},
            ],
        }


# ─── precalc-composition ──────────────────────────────────────────────────────

def _gen_precalc_composition():
    a = random.randint(1, 4)
    b = random.choice([-4,-3,-2,-1,1,2,3,4])
    c = random.randint(1, 4)
    d = random.choice([-4,-3,-2,-1,1,2,3,4])
    x = random.randint(-2, 3)
    if random.randint(0, 1) == 0:
        gx = c * x + d
        fgx = a * gx + b
        return {
            "problem_text": f"Let \\(f(x) = {_lin(a,b)}\\) and \\(g(x) = {_lin(c,d)}\\). Find \\((f \\circ g)({x})\\).",
            "correct_answer": str(fgx),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "\\((f \\circ g)(x) = f(g(x))\\): evaluate \\(g\\) first, then feed the result into \\(f\\)."},
                {"level": 2, "text": f"First find \\(g({x}) = {c}({x}) + ({d}) = {gx}\\). Then find \\(f({gx})\\)."},
                {"level": 3, "text": f"\\(g({x}) = {gx}\\), then \\(f({gx}) = {a}({gx}) + ({b}) = {fgx}\\)."},
            ],
        }
    else:
        fx = a * x + b
        gfx = c * fx + d
        return {
            "problem_text": f"Let \\(f(x) = {_lin(a,b)}\\) and \\(g(x) = {_lin(c,d)}\\). Find \\(g(f({x}))\\).",
            "correct_answer": str(gfx),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "For \\(g(f(x))\\), evaluate \\(f\\) first, then plug that result into \\(g\\)."},
                {"level": 2, "text": f"First find \\(f({x}) = {a}({x}) + ({b}) = {fx}\\). Then find \\(g({fx})\\)."},
                {"level": 3, "text": f"\\(f({x}) = {fx}\\), then \\(g({fx}) = {c}({fx}) + ({d}) = {gfx}\\)."},
            ],
        }


# ─── precalc-inverse-func ─────────────────────────────────────────────────────

def _gen_precalc_inverse_func():
    variant = random.choice([0, 1, 2])
    a = random.randint(2, 5)
    b = random.choice([-6,-5,-4,-3,-2,-1,1,2,3,4,5,6])
    if variant == 0:
        x_orig = random.randint(1, 8)
        y = a * x_orig + b
        return {
            "problem_text": f"Let \\(f(x) = {_lin(a, b)}\\). Find \\(f^{{-1}}({y})\\).",
            "correct_answer": str(x_orig),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "To find an inverse, swap \\(x\\) and \\(y\\) in \\(y = f(x)\\), then solve for \\(y\\)."},
                {"level": 2, "text": f"Swap: \\(x = {a}y + ({b})\\). Subtract \\({b}\\), then divide by \\({a}\\)."},
                {"level": 3, "text": f"\\(f^{{-1}}(x) = \\frac{{x - ({b})}}{{{a}}}\\). At \\(x = {y}\\): \\(\\frac{{{y} - ({b})}}{{{a}}} = \\frac{{{y-b}}}{{{a}}} = {x_orig}\\)."},
            ],
        }
    elif variant == 1:
        # Ask for f^{-1}(0): solve ax + b = 0 → x = -b/a (only if divisible)
        # Ensure b is divisible by a for clean integer answer
        b2 = a * random.randint(1, 4) * random.choice([-1, 1])
        x_at_zero = -b2 // a
        return {
            "problem_text": f"Let \\(f(x) = {_lin(a, b2)}\\). Find \\(f^{{-1}}(0)\\).",
            "correct_answer": str(x_at_zero),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "\\(f^{-1}(0)\\) is the value of \\(x\\) such that \\(f(x) = 0\\)."},
                {"level": 2, "text": f"Solve \\({_lin(a, b2)} = 0\\)."},
                {"level": 3, "text": f"\\({a}x = {-b2} \\Rightarrow x = {x_at_zero}\\)."},
            ],
        }
    else:
        # Intersection of f and f^{-1}: lies on y = x, so ax+b = x → (a-1)x = -b → x = -b/(a-1)
        # Ensure a != 1 (already since a >= 2) and (a-1)|b for integer answer
        b3 = (a - 1) * random.randint(1, 4) * random.choice([-1, 1])
        x_intersect = -b3 // (a - 1)
        return {
            "problem_text": (
                f"Let \\(f(x) = {_lin(a, b3)}\\). "
                f"Find the \\(x\\)-coordinate of the intersection of \\(y = f(x)\\) and \\(y = f^{{-1}}(x)\\)."
            ),
            "correct_answer": str(x_intersect),
            "answer_type": "numeric",
            "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "The graph of \\(f\\) and \\(f^{-1}\\) intersect on the line \\(y = x\\). Set \\(f(x) = x\\) and solve."},
                {"level": 2, "text": f"Set \\({_lin(a, b3)} = x\\): \\({a}x + ({b3}) = x \\Rightarrow {a-1}x = {-b3}\\)."},
                {"level": 3, "text": f"\\(x = \\frac{{{-b3}}}{{{a-1}}} = {x_intersect}\\)."},
            ],
        }


# ─── precalc-poly-func ────────────────────────────────────────────────────────

def _gen_precalc_poly_func():
    if random.randint(0, 1) == 0:
        a = random.randint(1, 3)
        b = random.choice([-3,-2,2,3])
        c = random.choice([-4,-3,-2,2,3,4])
        d = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
        x = random.randint(-2, 3)
        fx = a*x**3 + b*x**2 + c*x + d
        return {
            "problem_text": f"Let \\(p(x) = {_cubic(a,b,c,d)}\\). Find \\(p({x})\\).",
            "correct_answer": str(fx),
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Substitute the value in for \\(x\\) and evaluate each term, highest degree first."},
                {"level": 2, "text": f"Compute each term at \\(x = {x}\\): \\({a}({x})^3\\), \\({b}({x})^2\\), \\({c}({x})\\), \\({d}\\)."},
                {"level": 3, "text": f"\\({a*x**3} + {b*x**2} + {c*x} + {d} = {fx}\\)."},
            ],
        }
    else:
        roots = random.sample(range(-4, 6), 3)
        r1, r2, r3 = sorted(roots)
        s1 = r1+r2+r3; s2 = r1*r2+r1*r3+r2*r3; s3 = r1*r2*r3
        return {
            "problem_text": f"The polynomial \\(p(x) = {_cubic(1,-s1,s2,-s3)}\\) has how many real roots?",
            "correct_answer": "3",
            "answer_type": "numeric",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "A degree-3 polynomial with real coefficients has either 1 or 3 real roots."},
                {"level": 2, "text": f"Look for rational roots — try factors of the constant term \\({-s3}\\)."},
                {"level": 3, "text": f"Factors as \\((x - {r1})(x - {r2})(x - {r3})\\), giving 3 real roots: \\(x = {r1}, {r2}, {r3}\\)."},
            ],
        }


# ─── GENERATORS dict ──────────────────────────────────────────────────────────

GENERATORS = {
    "precalc-functions":    _gen_precalc_functions,
    "precalc-domain-range": _gen_precalc_domain_range,
    "precalc-composition":  _gen_precalc_composition,
    "precalc-inverse-func": _gen_precalc_inverse_func,
    "precalc-poly-func":    _gen_precalc_poly_func,
}
