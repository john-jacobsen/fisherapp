"""
Algebra problem generators for Fisher App 3.0.
Covers 12 nodes: alg-linear-graphs through alg-radical-equations.

Drop this file at: backend/app/services/generators/algebra.py
Then in problem_generator.py, add:
    from .generators.algebra import GENERATORS as ALGEBRA_GENERATORS
    GENERATORS.update(ALGEBRA_GENERATORS)
"""
import random
from fractions import Fraction
from math import gcd


# ─── alg-linear-graphs ────────────────────────────────────────────────────────

def _gen_alg_linear_graphs():
    """Graph a linear equation — identify a point on the line."""
    m = random.choice([-3, -2, -1, 1, 2, 3])
    b = random.randint(-5, 5)
    x = random.randint(-3, 3)
    y = m * x + b
    b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    m_str = str(m) if m != 1 and m != -1 else ("-" if m == -1 else "")
    return {
        "problem_text": (
            f"The line \\(y = {m_str}x {b_str}\\) passes through the point "
            f"\\((x, y)\\) when \\(x = {x}\\). What is \\(y\\)?"
        ),
        "correct_answer": str(y),
        "answer_type": "numeric",
        "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "To find a point on a line, substitute the x-value into the equation and evaluate."},
            {"level": 2, "text": f"Substitute \\(x = {x}\\) into \\(y = {m_str}x {b_str}\\)."},
            {"level": 3, "text": f"\\(y = {m}({x}) + ({b}) = {m*x} + ({b}) = {y}\\)"},
        ],
    }


# ─── alg-slope ────────────────────────────────────────────────────────────────

def _gen_alg_slope():
    """Slope between two points, or slope-intercept form."""
    choice = random.randint(0, 1)
    if choice == 0:
        # Slope from two points
        x1, y1 = random.randint(-4, 4), random.randint(-4, 4)
        run = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        rise = random.randint(-4, 4)
        x2, y2 = x1 + run, y1 + rise
        slope = Fraction(rise, run)
        return {
            "problem_text": (
                f"Find the slope of the line through \\(({x1}, {y1})\\) and \\(({x2}, {y2})\\)."
            ),
            "correct_answer": f"{slope.numerator}/{slope.denominator}" if slope.denominator != 1 else str(slope.numerator),
            "answer_type": "symbolic",
            "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Slope is rise over run: \\(m = \\frac{y_2 - y_1}{x_2 - x_1}\\)."},
                {"level": 2, "text": f"Rise: \\({y2} - {y1} = {rise}\\). Run: \\({x2} - {x1} = {run}\\)."},
                {"level": 3, "text": f"\\(m = \\frac{{{rise}}}{{{run}}} = {slope}\\)"},
            ],
        }
    else:
        # Identify slope from y = mx + b
        m = random.choice([-3, -2, -1, 1, 2, 3])
        b = random.randint(-6, 6)
        b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        m_str = str(m) if abs(m) != 1 else ("-" if m == -1 else "")
        return {
            "problem_text": f"What is the slope of the line \\(y = {m_str}x {b_str}\\)?",
            "correct_answer": str(m),
            "answer_type": "numeric",
            "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "In slope-intercept form \\(y = mx + b\\), \\(m\\) is the slope."},
                {"level": 2, "text": f"The equation is in \\(y = mx + b\\) form. Identify the coefficient of \\(x\\)."},
                {"level": 3, "text": f"The coefficient of \\(x\\) is \\({m}\\), so the slope is \\({m}\\)."},
            ],
        }


# ─── alg-systems-sub ──────────────────────────────────────────────────────────

def _gen_alg_systems_sub():
    """Solve a 2x2 linear system by substitution."""
    x = random.randint(1, 6)
    y = random.randint(1, 6)
    a = random.randint(1, 3)
    b = random.randint(1, 3)
    c1 = y - a * x
    c2 = b * x + y
    c1_str = f"+ {c1}" if c1 >= 0 else f"- {abs(c1)}"
    a_str = str(a) if a != 1 else ""
    return {
        "problem_text": (
            f"Solve the system by substitution: "
            f"\\(y = {a_str}x {c1_str}\\) and \\({b}x + y = {c2}\\). "
            f"Enter the value of \\(x\\)."
        ),
        "correct_answer": str(x),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Substitution: the first equation already gives y in terms of x — plug it into the second."},
            {"level": 2, "text": f"Replace \\(y\\) in the second equation with \\({a}x {c1_str}\\), then solve for \\(x\\)."},
            {"level": 3, "text": (
                f"\\({b}x + ({a}x {c1_str}) = {c2} "
                f"\\Rightarrow {a+b}x {c1_str} = {c2} "
                f"\\Rightarrow {a+b}x = {c2 - c1} "
                f"\\Rightarrow x = {x}\\)"
            )},
        ],
    }


# ─── alg-systems-elim ─────────────────────────────────────────────────────────

def _gen_alg_systems_elim():
    """Solve a 2x2 linear system by elimination."""
    x = random.randint(1, 5)
    y = random.randint(1, 5)
    a1 = random.randint(1, 3)
    b1 = random.randint(1, 3)
    a2 = random.randint(1, 3)
    b2 = random.randint(1, 3)
    # Ensure the system has a unique solution (non-parallel)
    while a1 * b2 == a2 * b1:
        a2 = random.randint(1, 3)
        b2 = random.randint(1, 3)
    c1 = a1 * x + b1 * y
    c2 = a2 * x + b2 * y
    return {
        "problem_text": (
            f"Solve by elimination: \\({a1}x + {b1}y = {c1}\\) and "
            f"\\({a2}x + {b2}y = {c2}\\). Enter the value of \\(x\\)."
        ),
        "correct_answer": str(x),
        "answer_type": "numeric",
        "difficulty": 0.7,
        "hints": [
            {"level": 1, "text": "Elimination: multiply one or both equations so a variable's coefficients match, then subtract to cancel it."},
            {"level": 2, "text": f"Multiply the first equation by {a2} and the second by {a1} to make the \\(x\\)-coefficients equal, then subtract."},
            {"level": 3, "text": (
                f"\\({a2}({a1}x + {b1}y) - {a1}({a2}x + {b2}y) = {a2*c1} - {a1*c2}\\) "
                f"\\(\\Rightarrow {a2*b1 - a1*b2}y = {a2*c1 - a1*c2}\\) "
                f"\\(\\Rightarrow y = {y}\\), then back-substitute to get \\(x = {x}\\)."
            )},
        ],
    }


# ─── alg-inequalities ─────────────────────────────────────────────────────────

def _gen_alg_inequalities():
    """Solve a linear inequality; answer is the boundary value."""
    x_bound = random.randint(1, 10)
    a = random.randint(2, 5)
    b = random.randint(1, 8)
    c = a * x_bound + b
    op = random.choice(['<', '>'])
    # Ask for boundary value only — avoids interval notation checker issue
    return {
        "problem_text": (
            f"Solve the inequality \\({a}x + {b} {op} {c}\\). "
            f"What value of \\(x\\) is the boundary (the solution to \\({a}x + {b} = {c}\\))?"
        ),
        "correct_answer": str(x_bound),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Solve a linear inequality the same way as an equation — isolate x. The boundary is where the two sides are equal."},
            {"level": 2, "text": f"Subtract {b} from both sides, then divide by {a}."},
            {"level": 3, "text": f"\\({a}x + {b} = {c} \\Rightarrow {a}x = {c - b} \\Rightarrow x = {x_bound}\\). The solution to the inequality is \\(x {op} {x_bound}\\)."},
        ],
    }


# ─── alg-poly-ops ─────────────────────────────────────────────────────────────

def _gen_alg_poly_ops():
    """Add or subtract polynomials — identify the coefficient of x."""
    a1 = random.randint(1, 6)
    a2 = random.randint(1, 6)
    b1 = random.randint(-6, 6)
    b2 = random.randint(-6, 6)
    op = random.choice(['+', '-'])
    if op == '+':
        coeff_x = a1 + a2
        const = b1 + b2
    else:
        coeff_x = a1 - a2
        const = b1 - b2

    b1_str = f"+ {b1}" if b1 >= 0 else f"- {abs(b1)}"
    b2_str = f"+ {b2}" if b2 >= 0 else f"- {abs(b2)}"
    const_str = f"+ {const}" if const >= 0 else f"- {abs(const)}"
    return {
        "problem_text": (
            f"Simplify \\(({a1}x {b1_str}) {op} ({a2}x {b2_str})\\). "
            f"What is the coefficient of \\(x\\)?"
        ),
        "correct_answer": str(coeff_x),
        "answer_type": "numeric",
        "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "Combine like terms: add (or subtract) the x-terms together, and the constant terms together."},
            {"level": 2, "text": f"x-terms: \\({a1}x {op} {a2}x\\). Constants: \\({b1} {op} {b2}\\)."},
            {"level": 3, "text": f"\\(({a1} {op} {a2})x {const_str} = {coeff_x}x {const_str}\\). The coefficient of \\(x\\) is \\({coeff_x}\\)."},
        ],
    }


# ─── alg-factoring-gcf ────────────────────────────────────────────────────────

def _gen_alg_factoring_gcf():
    """Factor out the GCF from a polynomial."""
    g = random.randint(2, 5)
    a = random.randint(2, 7)
    b = random.randint(1, 6)
    while gcd(a, b) != 1:
        b = random.randint(1, 6)
    ga, gb = g * a, g * b
    return {
        "problem_text": f"Factor out the GCF: \\({ga}x + {gb}\\). What is the GCF?",
        "correct_answer": str(g),
        "answer_type": "numeric",
        "difficulty": 0.4,
        "hints": [
            {"level": 1, "text": "The GCF is the largest number that divides evenly into all terms of the polynomial."},
            {"level": 2, "text": f"Find the GCF of {ga} and {gb}."},
            {"level": 3, "text": f"GCF({ga}, {gb}) = {g}. Factor: \\({g}({a}x + {b})\\)."},
        ],
    }


# ─── alg-factoring-quad ───────────────────────────────────────────────────────

def _gen_alg_factoring_quad():
    """Factor a monic quadratic — find the roots."""
    pool = [
        (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
        (2, 3), (2, 4), (2, 5), (3, 4), (3, 5),
        (-1, 2), (-1, 3), (-1, 4), (-2, 3), (-2, 5),
    ]
    r1, r2 = random.choice(pool)
    b = -(r1 + r2)
    c = r1 * r2
    roots = sorted([r1, r2])

    b_str = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
    c_str = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
    return {
        "problem_text": f"Factor \\(x^2 {b_str} {c_str}\\). Enter the two roots as \\(r_1, r_2\\) (smaller first).",
        "correct_answer": f"{roots[0]}, {roots[1]}",
        "answer_type": "symbolic",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "To factor \\(x^2 + bx + c\\), find two numbers that multiply to \\(c\\) and add to \\(b\\)."},
            {"level": 2, "text": f"Find two numbers that multiply to \\({c}\\) and add to \\({b}\\)."},
            {"level": 3, "text": f"The numbers are \\({r1}\\) and \\({r2}\\): factors are \\((x {'-' if r1 > 0 else '+'} {abs(r1)})(x {'-' if r2 > 0 else '+'} {abs(r2)}) = 0\\), so the roots are \\(x = {roots[0]}\\) and \\(x = {roots[1]}\\)."},
        ],
    }


# ─── alg-completing-square ────────────────────────────────────────────────────

def _gen_alg_completing_square():
    """Complete the square — find the value added to both sides."""
    # x^2 + bx = c  →  x^2 + bx + (b/2)^2 = c + (b/2)^2
    b = random.choice([2, 4, 6, 8, 10, -2, -4, -6])
    half_b = b // 2
    square = half_b ** 2
    c = random.randint(1, 10)
    b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    return {
        "problem_text": (
            f"Complete the square for \\(x^2 {b_str}x = {c}\\). "
            f"What number is added to both sides?"
        ),
        "correct_answer": str(square),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "To complete the square, take half the coefficient of \\(x\\), then square it."},
            {"level": 2, "text": f"Half of \\({b}\\) is \\({half_b}\\). Square it."},
            {"level": 3, "text": f"\\(\\left(\\frac{{{b}}}{{2}}\\right)^2 = ({half_b})^2 = {square}\\). Add \\({square}\\) to both sides: \\(x^2 {b_str}x + {square} = {c + square}\\)."},
        ],
    }


# ─── alg-rational-expr ────────────────────────────────────────────────────────

def _gen_alg_rational_expr():
    """Simplify a rational expression by canceling a common factor."""
    r = random.randint(1, 5)       # root to cancel
    a = random.randint(1, 4)       # leading coeff of numerator extra factor
    # Numerator: (x - r)(ax + b), Denominator: (x - r)(cx + d)
    b = random.randint(1, 5)
    c = random.randint(1, 4)
    d = random.randint(1, 5)
    while a == c and b == d:
        d = random.randint(1, 5)
    # Ask for the value of x that makes the original expression undefined
    return {
        "problem_text": (
            f"For what value of \\(x\\) is the expression "
            f"\\(\\frac{{(x - {r})({a}x + {b})}}{{(x - {r})({c}x + {d})}}\\) undefined?"
        ),
        "correct_answer": str(r),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "A rational expression is undefined when its denominator equals zero."},
            {"level": 2, "text": f"Set the denominator equal to zero: \\((x - {r})({c}x + {d}) = 0\\)."},
            {"level": 3, "text": f"\\(x - {r} = 0 \\Rightarrow x = {r}\\) (or \\(x = -\\frac{{{d}}}{{{c}}}\\)). The expression is undefined at \\(x = {r}\\) because that factor cannot be cancelled before evaluating."},
        ],
    }


# ─── alg-radical-simplify ─────────────────────────────────────────────────────

def _gen_alg_radical_simplify():
    """Simplify a square root by pulling out perfect square factors."""
    # Build sqrt(a^2 * b) where b is square-free
    a = random.randint(2, 6)
    b = random.choice([2, 3, 5, 6, 7])   # square-free
    radicand = a * a * b
    return {
        "problem_text": f"Simplify \\(\\sqrt{{{radicand}}}\\). Enter the coefficient outside the radical.",
        "correct_answer": str(a),
        "answer_type": "numeric",
        "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Factor the radicand into a perfect square times a remaining factor, then take the square root of the perfect square."},
            {"level": 2, "text": f"\\({radicand} = {a**2} \\times {b}\\). The perfect square part is \\({a**2}\\)."},
            {"level": 3, "text": f"\\(\\sqrt{{{radicand}}} = \\sqrt{{{a**2} \\times {b}}} = {a}\\sqrt{{{b}}}\\). The coefficient is \\({a}\\)."},
        ],
    }


# ─── alg-radical-equations ────────────────────────────────────────────────────

def _gen_alg_radical_equations():
    """Solve a radical equation of the form sqrt(ax + b) = c."""
    c = random.randint(2, 6)       # RHS (positive)
    a = random.randint(1, 4)
    x = random.randint(1, 8)
    b = c ** 2 - a * x
    b_str = f"+ {b}" if b > 0 else (f"- {abs(b)}" if b < 0 else "")
    inner = f"{a}x {b_str}".strip() if b != 0 else f"{a}x"
    return {
        "problem_text": f"Solve: \\(\\sqrt{{{inner}}} = {c}\\)",
        "correct_answer": str(x),
        "answer_type": "numeric",
        "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "To eliminate a square root, square both sides of the equation, then solve normally."},
            {"level": 2, "text": f"Square both sides: \\({inner} = {c}^2 = {c**2}\\)."},
            {"level": 3, "text": f"\\({inner} = {c**2} \\Rightarrow {a}x = {c**2 - b} \\Rightarrow x = {x}\\). Check: \\(\\sqrt{{{a}({x}){('+' + str(b)) if b > 0 else (('-' + str(abs(b))) if b < 0 else '')}}} = \\sqrt{{{c**2}}} = {c}\\) ✓"},
        ],
    }


# ─── GENERATORS dict ──────────────────────────────────────────────────────────

GENERATORS = {
    "alg-linear-graphs":    _gen_alg_linear_graphs,
    "alg-slope":            _gen_alg_slope,
    "alg-systems-sub":      _gen_alg_systems_sub,
    "alg-systems-elim":     _gen_alg_systems_elim,
    "alg-inequalities":     _gen_alg_inequalities,
    "alg-poly-ops":         _gen_alg_poly_ops,
    "alg-factoring-gcf":    _gen_alg_factoring_gcf,
    "alg-factoring-quad":   _gen_alg_factoring_quad,
    "alg-completing-square": _gen_alg_completing_square,
    "alg-rational-expr":    _gen_alg_rational_expr,
    "alg-radical-simplify": _gen_alg_radical_simplify,
    "alg-radical-equations": _gen_alg_radical_equations,
}
