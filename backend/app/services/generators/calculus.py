"""
Calculus problem generators for Fisher App 3.0.
Covers 20 nodes: calc-limits through mv-change-vars.

Drop at: backend/app/services/generators/calculus.py
In problem_generator.py add:
    from .generators.calculus import GENERATORS as CALC_GENERATORS
    GENERATORS.update(CALC_GENERATORS)
"""
import random
from fractions import Fraction
from math import gcd


# ── shared display helpers ────────────────────────────────────────────────────

def _xn(n):
    """x^n with n=1 simplified to x."""
    return "x" if n == 1 else f"x^{{{n}}}"

def _axn(a, n):
    """a*x^n with a=1 and n=1 edge cases handled."""
    x = _xn(n)
    if a == 1:   return x
    if a == -1:  return f"-{x}"
    return f"{a}{x}"

def _lin(a, b):
    """ax + b with a=±1 and b=0 handled."""
    x_part = "" if a == 1 else ("-" if a == -1 else str(a))
    x_part += "x"
    if b == 0:   return x_part
    return f"{x_part} + {b}" if b > 0 else f"{x_part} - {abs(b)}"

def _pm(n, first=False):
    """Return '+ n', '- |n|', or '' for building polynomial strings."""
    if n == 0:    return ""
    if first:     return f"-{abs(n)}" if n < 0 else str(n)
    return f"+ {n}" if n > 0 else f"- {abs(n)}"

def _pmx(coef):
    """Like _pm but for the x-coefficient: handles ±1 → '+ x' / '- x'."""
    if coef == 0:   return ""
    if coef == 1:   return "+ x"
    if coef == -1:  return "- x"
    return f"+ {coef}x" if coef > 0 else f"- {abs(coef)}x"

def _Axn(A, n):
    """Leading coefficient × x^n: handles A=±1."""
    x = _xn(n)
    if A == 1:   return x
    if A == -1:  return f"-{x}"
    return f"{A}{x}"

def _factor(a, b):
    """Return '(ax + b)' or '(ax - |b|)' or '(ax)' cleanly."""
    if b == 0:   return f"({_axn(a,1)})"
    return f"({_lin(a, b)})"


# ── calc-limits ───────────────────────────────────────────────────────────────

def _gen_calc_limits():
    choice = random.randint(0, 1)
    if choice == 0:
        # Direct substitution: lim_{x→a} (bx + c)
        a  = random.randint(-3, 4)
        b  = random.randint(2, 5)        # keep b≥2 to avoid 1x display
        c  = random.choice([-6,-4,-3,-2,-1,1,2,3,4,6])
        val = b*a + c
        return {
            "problem_text": f"Evaluate: \\(\\lim_{{x \\to {a}}} ({_lin(b,c)})\\)",
            "correct_answer": str(val),
            "answer_type": "numeric",
            "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "If the function is continuous at the point, the limit equals the function value — just substitute."},
                {"level": 2, "text": f"Substitute \\(x = {a}\\) directly into \\({_lin(b,c)}\\)."},
                {"level": 3, "text": f"\\({b}({a}) + ({c}) = {b*a} + ({c}) = {val}\\)"},
            ],
        }
    else:
        # Removable discontinuity: lim_{x→r} (x-r)(x+k)/(x-r) = r+k
        r = random.randint(-3, 4)
        k = random.randint(1, 5)
        val = r + k
        # numerator = x^2 + (k-r)x - rk
        bcoef = k - r
        ccoef = -r * k
        return {
            "problem_text": (
                f"Evaluate: \\(\\lim_{{x \\to {r}}} "
                f"\\frac{{x^2 {_pmx(bcoef)} {_pm(ccoef)}}}{{x {_pm(-r)}}}\\)"
            ),
            "correct_answer": str(val),
            "answer_type": "numeric",
            "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Direct substitution gives 0/0 — factor the numerator to cancel the common factor."},
                {"level": 2, "text": f"Factor: find two numbers multiplying to \\({ccoef}\\) and adding to \\({bcoef}\\)."},
                {"level": 3, "text": f"Numerator = \\((x {_pm(-r)})(x + {k})\\). Cancel \\((x {_pm(-r)})\\), leaving \\(x + {k}\\). At \\(x={r}\\): \\({val}\\)."},
            ],
        }


# ── calc-limit-laws ───────────────────────────────────────────────────────────

def _gen_calc_limit_laws():
    L1 = random.randint(1, 6)
    L2 = random.randint(1, 6)
    choice = random.randint(0, 2)
    if choice == 0:
        val = L1 + L2
        return {
            "problem_text": f"Given \\(\\lim_{{x \\to a}} f(x) = {L1}\\) and \\(\\lim_{{x \\to a}} g(x) = {L2}\\), find \\(\\lim_{{x \\to a}} [f(x) + g(x)]\\).",
            "correct_answer": str(val), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Sum law: \\(\\lim[f + g] = \\lim f + \\lim g\\)."},
                {"level": 2, "text": f"Add: \\({L1} + {L2}\\)."},
                {"level": 3, "text": f"\\({L1} + {L2} = {val}\\)."},
            ],
        }
    elif choice == 1:
        val = L1 * L2
        return {
            "problem_text": f"Given \\(\\lim_{{x \\to a}} f(x) = {L1}\\) and \\(\\lim_{{x \\to a}} g(x) = {L2}\\), find \\(\\lim_{{x \\to a}} [f(x) \\cdot g(x)]\\).",
            "correct_answer": str(val), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "Product law: \\(\\lim[f \\cdot g] = \\lim f \\cdot \\lim g\\)."},
                {"level": 2, "text": f"Multiply: \\({L1} \\times {L2}\\)."},
                {"level": 3, "text": f"\\({L1} \\times {L2} = {val}\\)."},
            ],
        }
    else:
        c = random.randint(2, 5)
        val = c * L1
        return {
            "problem_text": f"Given \\(\\lim_{{x \\to a}} f(x) = {L1}\\), find \\(\\lim_{{x \\to a}} {c} \\cdot f(x)\\).",
            "correct_answer": str(val), "answer_type": "numeric", "difficulty": 0.3,
            "hints": [
                {"level": 1, "text": "Constant multiple law: \\(\\lim[c \\cdot f] = c \\cdot \\lim f\\)."},
                {"level": 2, "text": f"Multiply: \\({c} \\cdot {L1}\\)."},
                {"level": 3, "text": f"\\({c} \\cdot {L1} = {val}\\)."},
            ],
        }


# ── calc-continuity ───────────────────────────────────────────────────────────

def _gen_calc_continuity():
    k = random.randint(1, 4)
    a = random.randint(2, 4)
    b = random.choice([-4,-3,-2,-1,1,2,3,4])
    left_val = a*k + b
    c = random.randint(2, 4)
    while c == a: c = random.randint(2, 4)
    d = left_val - c*k
    return {
        "problem_text": (
            f"A piecewise function is \\(f(x) = {_lin(a,b)}\\) for \\(x < {k}\\) "
            f"and \\(f(x) = {_lin(c,d)}\\) for \\(x \\geq {k}\\). "
            f"What is \\(f({k})\\)?"
        ),
        "correct_answer": str(left_val),
        "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Continuity at \\(x=k\\) requires the left limit, right limit, and function value to agree."},
            {"level": 2, "text": f"Evaluate the left piece at \\(x={k}\\): \\({a}({k}) + ({b})\\)."},
            {"level": 3, "text": f"Left: \\({a*k} + ({b}) = {left_val}\\). Right: \\({c*k} + ({d}) = {left_val}\\). Both agree: \\(f({k}) = {left_val}\\)."},
        ],
    }


# ── calc-deriv-def ────────────────────────────────────────────────────────────

def _gen_calc_deriv_def():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: f(x) = x², find f'(a)
        a = random.randint(1, 5)
        deriv = 2 * a
        return {
            "problem_text": f"Using the limit definition, find \\(f'({a})\\) for \\(f(x) = x^2\\).",
            "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Definition: \\(f'(a) = \\lim_{{h \\to 0}} \\frac{{f(a+h)-f(a)}}{{h}}\\)."},
                {"level": 2, "text": f"Compute \\(({a}+h)^2 - {a}^2\\), simplify, divide by \\(h\\), then let \\(h \\to 0\\)."},
                {"level": 3, "text": f"\\(({a}+h)^2 - {a**2} = 2 \\cdot {a} \\cdot h + h^2\\). Divide by \\(h\\): \\(2 \\cdot {a} + h \\to {deriv}\\)."},
            ],
        }
    elif variant == 1:
        # V2: f(x) = mx + c, find f'(0) = m (derivative of linear = slope)
        m = random.randint(2, 6)
        c = random.randint(1, 5)
        return {
            "problem_text": f"Using the limit definition, find \\(f'(0)\\) for \\(f(x) = {m}x + {c}\\). What is \\(f'(0)\\)?",
            "correct_answer": str(m), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Definition: \\(f'(0) = \\lim_{{h \\to 0}} \\frac{{f(h)-f(0)}}{{h}}\\)."},
                {"level": 2, "text": f"\\(f(h) = {m}h + {c}\\), \\(f(0) = {c}\\). So \\(\\frac{{f(h)-f(0)}}{{h}} = \\frac{{{m}h}}{{h}}\\)."},
                {"level": 3, "text": f"\\(\\frac{{{m}h}}{{h}} = {m}\\) for \\(h \\neq 0\\). As \\(h \\to 0\\), the limit is \\({m}\\)."},
            ],
        }
    else:
        # V3: f(x) = ax² + b, find f'(x0) = 2*a*x0
        a = random.randint(2, 4)
        b = random.randint(1, 5)
        x0 = random.randint(1, 3)
        deriv = 2 * a * x0
        return {
            "problem_text": f"Using the limit definition, find \\(f'({x0})\\) for \\(f(x) = {a}x^2 + {b}\\).",
            "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Definition: \\(f'(a) = \\lim_{{h \\to 0}} \\frac{{f(a+h)-f(a)}}{{h}}\\)."},
                {"level": 2, "text": f"\\(f({x0}+h) - f({x0}) = {a}({x0}+h)^2 + {b} - ({a*x0**2 + b}) = {2*a*x0}h + {a}h^2\\)."},
                {"level": 3, "text": f"Divide by \\(h\\): \\({2*a*x0} + {a}h \\to {deriv}\\) as \\(h \\to 0\\)."},
            ],
        }


# ── calc-deriv-power ──────────────────────────────────────────────────────────

def _gen_calc_deriv_power():
    n  = random.randint(2, 5)
    a  = random.randint(1, 4)
    b  = random.choice([-4,-3,-2,2,3,4])   # exclude 0, ±1 for x-term display
    x0 = random.randint(1, 3)
    deriv_at_x0 = a*n*x0**(n-1) + b
    return {
        "problem_text": f"Find \\(f'({x0})\\) for \\(f(x) = {_axn(a,n)} {_pm(b)}x\\).",
        "correct_answer": str(deriv_at_x0), "answer_type": "numeric", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": "Power rule: \\(\\frac{d}{dx} x^n = nx^{n-1}\\). Apply to each term."},
            {"level": 2, "text": f"\\(f'(x) = {a*n}{_xn(n-1)} {_pm(b)}\\). Substitute \\(x={x0}\\)."},
            {"level": 3, "text": f"\\(f'({x0}) = {a*n}({x0})^{{{n-1}}} + ({b}) = {a*n*x0**(n-1)} + ({b}) = {deriv_at_x0}\\)."},
        ],
    }


# ── calc-deriv-product ────────────────────────────────────────────────────────

def _gen_calc_deriv_product():
    a = random.randint(2, 4)
    b = random.choice([-3,-2,-1,1,2,3,4])
    c = random.randint(2, 4)
    d = random.choice([-3,-2,-1,1,2,3,4])
    deriv = a*(c+d) + (a+b)*c   # at x=1: f'g + fg' = a(c·1+d) + (a·1+b)c
    return {
        "problem_text": f"Let \\(h(x) = {_factor(a,b)} {_factor(c,d)}\\). Use the product rule to find \\(h'(1)\\).",
        "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Product rule: \\((fg)' = f'g + fg'\\)."},
            {"level": 2, "text": f"\\(f={_lin(a,b)}\\), \\(f'={a}\\). \\(g={_lin(c,d)}\\), \\(g'={c}\\). Evaluate at \\(x=1\\)."},
            {"level": 3, "text": f"\\(h'(1) = {a}({c}+{d}) + ({a}+{b})({c}) = {a*(c+d)} + {(a+b)*c} = {deriv}\\)."},
        ],
    }


# ── calc-deriv-chain ──────────────────────────────────────────────────────────

def _gen_calc_deriv_chain():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: f(x) = (ax + b)^n, find f'(0), b > 0
        n = random.randint(2, 4)
        a = random.randint(2, 4)
        b = random.choice([1, 2, 3])
        deriv = n * a * (b**(n-1))
        return {
            "problem_text": f"Find \\(f'(0)\\) for \\(f(x) = {_factor(a,b)}^{{{n}}}\\).",
            "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": f"Chain rule: \\(\\frac{{d}}{{dx}}[u^n] = nu^{{n-1}} \\cdot u'\\). Here \\(u = {_lin(a,b)}\\)."},
                {"level": 2, "text": f"\\(f'(x) = {n}{_factor(a,b)}^{{{n-1}}} \\cdot {a}\\). Evaluate at \\(x=0\\)."},
                {"level": 3, "text": f"\\(f'(0) = {n}({b})^{{{n-1}}} \\cdot {a} = {n*b**(n-1)} \\cdot {a} = {deriv}\\)."},
            ],
        }
    elif variant == 1:
        # V2: f(x) = (ax - b)^n, find f'(0), b > 0
        n = random.randint(2, 4)
        a = random.randint(2, 4)
        b = random.choice([1, 2, 3])
        deriv = n * a * ((-b)**(n-1))
        return {
            "problem_text": f"Find \\(f'(0)\\) for \\(f(x) = ({_lin(a,-b)})^{{{n}}}\\).",
            "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": f"Chain rule: \\(\\frac{{d}}{{dx}}[u^n] = nu^{{n-1}} \\cdot u'\\). Here \\(u = {_lin(a,-b)}\\)."},
                {"level": 2, "text": f"\\(f'(x) = {n}({_lin(a,-b)})^{{{n-1}}} \\cdot {a}\\). Evaluate at \\(x=0\\)."},
                {"level": 3, "text": f"\\(f'(0) = {n}({-b})^{{{n-1}}} \\cdot {a} = {deriv}\\)."},
            ],
        }
    else:
        # V3: f(x) = sqrt(ax + b), find f'(x0) = a/(2*sqrt(a*x0+b))
        a = random.choice([2, 4, 6, 8])
        b = random.choice([1, 4, 9, 16])
        x0 = 0
        k = int(b ** 0.5)   # sqrt(b) is integer since b in {1,4,9,16}
        frac = Fraction(a, 2 * k)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Find \\(f'({x0})\\) for \\(f(x) = \\sqrt{{{a}x + {b}}}\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Write \\(\\sqrt{u} = u^{1/2}\\) and apply the chain rule: \\(\\frac{1}{2}u^{-1/2} \\cdot u'\\)."},
                {"level": 2, "text": f"\\(f'(x) = \\frac{{{a}}}{{2\\sqrt{{{a}x+{b}}}}}\\). Evaluate at \\(x={x0}\\)."},
                {"level": 3, "text": f"\\(f'({x0}) = \\frac{{{a}}}{{2\\sqrt{{{b}}}}} = \\frac{{{a}}}{{2 \\cdot {k}}} = {ans}\\)."},
            ],
        }


# ── calc-deriv-exp-log ────────────────────────────────────────────────────────

def _gen_calc_deriv_exp_log():
    variant = random.choice([0, 1, 2])
    a = random.randint(2, 6)
    if variant == 0:
        # V1: f(x) = a*e^x, find f'(0) = a
        return {
            "problem_text": f"Find \\(f'(0)\\) for \\(f(x) = {a}e^x\\).",
            "correct_answer": str(a), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\frac{d}{dx}e^x = e^x\\). Constants factor out."},
                {"level": 2, "text": f"\\(f'(x) = {a}e^x\\). Evaluate at \\(x=0\\)."},
                {"level": 3, "text": f"\\(f'(0) = {a}e^0 = {a} \\cdot 1 = {a}\\)."},
            ],
        }
    elif variant == 1:
        # V2: f(x) = a*ln(x), find f'(1) = a
        return {
            "problem_text": f"Find \\(f'(1)\\) for \\(f(x) = {a}\\ln(x)\\).",
            "correct_answer": str(a), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\frac{d}{dx}\\ln(x) = \\frac{1}{x}\\). Constants factor out."},
                {"level": 2, "text": f"\\(f'(x) = \\frac{{{a}}}{{x}}\\). Evaluate at \\(x=1\\)."},
                {"level": 3, "text": f"\\(f'(1) = \\frac{{{a}}}{{1}} = {a}\\)."},
            ],
        }
    else:
        # V3: f(x) = a*e^(b*x), find f'(0) = a*b
        b = random.randint(2, 4)
        deriv = a * b
        return {
            "problem_text": f"Find \\(f'(0)\\) for \\(f(x) = {a}e^{{{b}x}}\\).",
            "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Chain rule: \\(\\frac{d}{dx}e^{u} = e^{u} \\cdot u'\\). Here \\(u = {b}x\\)."},
                {"level": 2, "text": f"\\(f'(x) = {a} \\cdot e^{{{b}x}} \\cdot {b}\\). Evaluate at \\(x=0\\)."},
                {"level": 3, "text": f"\\(f'(0) = {a} \\cdot e^0 \\cdot {b} = {a} \\cdot 1 \\cdot {b} = {deriv}\\)."},
            ],
        }


# ── calc-implicit ─────────────────────────────────────────────────────────────

def _gen_calc_implicit():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: circle x² + y² = r², dy/dx = -x/y
        triples = [(3,4,5),(5,12,13),(8,15,17),(6,8,10),(9,12,15)]
        x0, y0, r = random.choice(triples)
        frac = Fraction(-x0, y0)
        ans = f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator)
        return {
            "problem_text": f"For the circle \\(x^2 + y^2 = {r**2}\\), find \\(\\frac{{dy}}{{dx}}\\) at \\(({x0}, {y0})\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Differentiate both sides w.r.t. \\(x\\), treating \\(y\\) as a function of \\(x\\)."},
                {"level": 2, "text": "\\(2x + 2y\\frac{dy}{dx} = 0\\). Solve for \\(\\frac{dy}{dx}\\)."},
                {"level": 3, "text": f"\\(\\frac{{dy}}{{dx}} = -\\frac{{x}}{{y}}\\). At \\(({x0},{y0})\\): \\(-\\frac{{{x0}}}{{{y0}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: x² + 2y² = r², dy/dx = -x/(2y)
        # triples where x0²+2*y0² = r² (integer r²)
        ellipse_pts = [(1, 2, 9), (2, 2, 12), (4, 2, 24), (2, 1, 6)]
        x0, y0, r2 = random.choice(ellipse_pts)
        frac = Fraction(-x0, 2 * y0)
        ans = f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator)
        return {
            "problem_text": f"For the curve \\(x^2 + 2y^2 = {r2}\\), find \\(\\frac{{dy}}{{dx}}\\) at \\(({x0}, {y0})\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Differentiate both sides w.r.t. \\(x\\), treating \\(y\\) as a function of \\(x\\)."},
                {"level": 2, "text": "\\(2x + 4y\\frac{dy}{dx} = 0\\). Solve for \\(\\frac{dy}{dx}\\)."},
                {"level": 3, "text": f"\\(\\frac{{dy}}{{dx}} = -\\frac{{x}}{{2y}}\\). At \\(({x0},{y0})\\): \\(-\\frac{{{x0}}}{{2 \\cdot {y0}}} = {ans}\\)."},
            ],
        }
    else:
        # V3: xy = c, dy/dx = -y/x
        pairs = [(1, 2), (2, 3), (1, 4), (3, 2), (2, 4), (1, 6), (4, 3)]
        x0, y0 = random.choice(pairs)
        c = x0 * y0
        frac = Fraction(-y0, x0)
        ans = f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator)
        return {
            "problem_text": f"For the curve \\(xy = {c}\\), find \\(\\frac{{dy}}{{dx}}\\) at \\(({x0}, {y0})\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Differentiate both sides w.r.t. \\(x\\) using the product rule on the left."},
                {"level": 2, "text": "\\(y + x\\frac{dy}{dx} = 0\\). Solve for \\(\\frac{dy}{dx}\\)."},
                {"level": 3, "text": f"\\(\\frac{{dy}}{{dx}} = -\\frac{{y}}{{x}}\\). At \\(({x0},{y0})\\): \\(-\\frac{{{y0}}}{{{x0}}} = {ans}\\)."},
            ],
        }


# ── calc-optim ────────────────────────────────────────────────────────────────

def _gen_calc_optim():
    a  = random.randint(1, 3)
    h  = random.randint(-3, 4)
    k  = random.randint(1, 10)
    # f(x) = -a(x-h)^2 + k  →  expanded coefficients
    A  = -a
    B  = 2*a*h
    C  = k - a*h**2
    return {
        "problem_text": f"Find the \\(x\\)-value that maximizes \\(f(x) = {_Axn(A,2)} {_pm(B)}x {_pm(C)}\\).",
        "correct_answer": str(h), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "At a maximum, \\(f'(x) = 0\\). Differentiate and solve."},
            {"level": 2, "text": f"\\(f'(x) = {2*A}x {_pm(B)}\\). Set \\(= 0\\) and solve."},
            {"level": 3, "text": f"\\({2*A}x {_pm(B)} = 0 \\Rightarrow x = {h}\\)."},
        ],
    }


# ── calc-antideriv ────────────────────────────────────────────────────────────

def _gen_calc_antideriv():
    n  = random.randint(2, 5)     # avoid n=1 to dodge x^{1} display
    a  = random.randint(1, 5)
    frac = Fraction(a, n+1)
    coef_str = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    variant = random.choice([0, 1, 2])
    if variant in (0, 1):
        # V1/V2: indefinite integral — enter coefficient of x^(n+1)
        # (two structural variants naturally emerge from a=1 vs a>1 display)
        return {
            "problem_text": f"Find \\(\\int {_axn(a,n)}\\, dx\\). Enter the coefficient of \\({_xn(n+1)}\\).",
            "correct_answer": coef_str, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": f"Power rule: \\(\\int x^n\\,dx = \\frac{{x^{{n+1}}}}{{n+1}} + C\\)."},
                {"level": 2, "text": f"Raise the power: \\(n+1 = {n+1}\\). Divide coefficient \\({a}\\) by \\({n+1}\\)."},
                {"level": 3, "text": f"\\(\\int {_axn(a,n)}\\,dx = \\frac{{{a}}}{{{n+1}}}{_xn(n+1)} + C\\). Coefficient = \\({coef_str}\\)."},
            ],
        }
    else:
        # V3: definite integral from 0 to 1 — evaluate it
        def_frac = Fraction(a, n+1)
        def_ans = str(def_frac.numerator) if def_frac.denominator == 1 else f"{def_frac.numerator}/{def_frac.denominator}"
        return {
            "problem_text": f"Evaluate \\(\\int_{{0}}^{{1}} {_axn(a,n)}\\,dx\\).",
            "correct_answer": def_ans, "answer_type": "symbolic", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Find the antiderivative using the power rule, then apply the Fundamental Theorem of Calculus."},
                {"level": 2, "text": f"Antiderivative: \\(\\frac{{{a}}}{{{n+1}}}{_xn(n+1)}\\). Evaluate at \\(x=1\\) minus at \\(x=0\\)."},
                {"level": 3, "text": f"\\(\\frac{{{a}}}{{{n+1}}}(1)^{{{n+1}}} - 0 = \\frac{{{a}}}{{{n+1}}} = {def_ans}\\)."},
            ],
        }


# ── calc-riemann ──────────────────────────────────────────────────────────────

def _gen_calc_riemann():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: exact value of ∫_a^b c dx with n subintervals
        c = random.randint(2, 6)
        a = random.randint(0, 3)
        width = random.randint(2, 5)
        b = a + width
        n = random.randint(2, 5)
        total = c * width
        frac_dx = Fraction(width, n)
        dx_str = str(frac_dx) if frac_dx.denominator != 1 else str(frac_dx.numerator)
        return {
            "problem_text": (
                f"Approximate \\(\\int_{{{a}}}^{{{b}}} {c}\\,dx\\) using \\(n={n}\\) "
                f"equal subintervals. What is the exact value of the integral?"
            ),
            "correct_answer": str(total), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "Each rectangle has width \\(\\Delta x = (b-a)/n\\) and height given by the function."},
                {"level": 2, "text": f"\\(\\Delta x = ({b}-{a})/{n} = {dx_str}\\). The function \\(f(x)={c}\\) is constant, so every rectangle has height \\({c}\\)."},
                {"level": 3, "text": f"Sum \\(= {c} \\times {n} \\times {dx_str} = {c} \\times {width} = {total}\\)."},
            ],
        }
    elif variant == 1:
        # V2: find Δx for n subintervals on [a, b]
        a = random.randint(0, 3)
        width = random.randint(2, 6)
        b = a + width
        n = random.randint(2, 6)
        frac_dx = Fraction(width, n)
        dx_str = str(frac_dx) if frac_dx.denominator != 1 else str(frac_dx.numerator)
        return {
            "problem_text": f"What is \\(\\Delta x\\) for \\(n = {n}\\) equal subintervals on \\([{a}, {b}]\\)?",
            "correct_answer": dx_str, "answer_type": "symbolic", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\Delta x = \\frac{{b - a}}{{n}}\\)."},
                {"level": 2, "text": f"\\(b - a = {b} - {a} = {width}\\). Divide by \\(n = {n}\\)."},
                {"level": 3, "text": f"\\(\\Delta x = \\frac{{{width}}}{{{n}}} = {dx_str}\\)."},
            ],
        }
    else:
        # V3: single right-endpoint rectangle for ∫_0^b cx dx
        # area = c * b * b = c*b² (one rectangle: height = c*b, width = b)
        c = random.randint(2, 4)
        b = random.randint(2, 4)
        ans = c * b * b
        return {
            "problem_text": f"Using a single right-endpoint rectangle, approximate \\(\\int_{{0}}^{{{b}}} {c}x\\,dx\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.5,
            "hints": [
                {"level": 1, "text": "One rectangle: width \\(= b - 0 = b\\), height \\(= f(b)\\) (right endpoint)."},
                {"level": 2, "text": f"Width \\(= {b}\\). Height \\(= f({b}) = {c} \\cdot {b} = {c*b}\\)."},
                {"level": 3, "text": f"Area \\(= {c*b} \\times {b} = {ans}\\)."},
            ],
        }


# ── calc-ftc ──────────────────────────────────────────────────────────────────

def _gen_calc_ftc():
    n = random.randint(2, 4)      # avoid n=1 display issue
    c = random.randint(1, 4)
    b = random.randint(1, 4)
    frac = Fraction(c * b**(n+1), n+1)
    ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    variant = random.choice([0, 1, 2])
    if variant in (0, 1):
        # V1/V2: evaluate definite integral (two structural variants from c=1 vs c>1)
        return {
            "problem_text": f"Evaluate: \\(\\int_{{0}}^{{{b}}} {_axn(c,n)}\\,dx\\)",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "FTC: find the antiderivative \\(F(x)\\), then compute \\(F(b)-F(a)\\)."},
                {"level": 2, "text": f"\\(F(x) = \\frac{{{c}}}{{{n+1}}}{_xn(n+1)}\\). Evaluate at \\(x={b}\\) minus at \\(x=0\\)."},
                {"level": 3, "text": f"\\(F({b})-F(0) = \\frac{{{c}}}{{{n+1}}} \\cdot {b}^{{{n+1}}} = \\frac{{{c*b**(n+1)}}}{{{n+1}}} = {ans}\\)."},
            ],
        }
    else:
        # V3: area under the curve framing
        return {
            "problem_text": f"Find the area under \\(f(x) = {_axn(c,n)}\\) from \\(x = 0\\) to \\(x = {b}\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Area under a curve from \\(a\\) to \\(b\\) equals \\(\\int_a^b f(x)\\,dx\\)."},
                {"level": 2, "text": f"Compute \\(\\int_{{0}}^{{{b}}} {_axn(c,n)}\\,dx\\). Antiderivative: \\(\\frac{{{c}}}{{{n+1}}}{_xn(n+1)}\\)."},
                {"level": 3, "text": f"\\(\\frac{{{c}}}{{{n+1}}} \\cdot {b}^{{{n+1}}} - 0 = \\frac{{{c*b**(n+1)}}}{{{n+1}}} = {ans}\\)."},
            ],
        }


# ── calc-usub ─────────────────────────────────────────────────────────────────

def _gen_calc_usub():
    n = random.randint(2, 4)
    b = random.randint(1, 3)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: definite integral ∫_0^1 (x+b)^n dx
        numerator = (1+b)**(n+1) - b**(n+1)
        frac = Fraction(numerator, n+1)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Evaluate \\(\\int_{{0}}^{{1}} (x + {b})^{{{n}}}\\,dx\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": f"Let \\(u = x + {b}\\), so \\(du = dx\\). Change the bounds."},
                {"level": 2, "text": f"When \\(x=0\\), \\(u={b}\\). When \\(x=1\\), \\(u={1+b}\\). Integral: \\(\\int_{{{b}}}^{{{1+b}}} u^{{{n}}}\\,du\\)."},
                {"level": 3, "text": f"\\(\\left[\\frac{{u^{{{n+1}}}}}{{{n+1}}}\\right]_{{{b}}}^{{{1+b}}} = \\frac{{{(1+b)**(n+1)}-{b**(n+1)}}}{{{n+1}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: antiderivative of (x+b)^n — enter the coefficient of (x+b)^(n+1)
        frac = Fraction(1, n+1)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Find the antiderivative of \\((x + {b})^{{{n}}}\\). Enter the coefficient of \\((x+{b})^{{{n+1}}}\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": f"Let \\(u = x + {b}\\). Then \\(\\int u^{{{n}}}\\,du = \\frac{{u^{{{n+1}}}}}{{{n+1}}} + C\\)."},
                {"level": 2, "text": f"Substitute back: antiderivative is \\(\\frac{{(x+{b})^{{{n+1}}}}}{{{n+1}}} + C\\)."},
                {"level": 3, "text": f"The coefficient of \\((x+{b})^{{{n+1}}}\\) is \\(\\frac{{1}}{{{n+1}}} = {ans}\\)."},
            ],
        }
    else:
        # V3: definite integral ∫_0^1 a*(x+b)^n dx with coefficient a
        a = random.randint(2, 4)
        numerator = (1+b)**(n+1) - b**(n+1)
        frac = Fraction(a * numerator, n+1)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Evaluate \\(\\int_{{0}}^{{1}} {a}(x + {b})^{{{n}}}\\,dx\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": f"Let \\(u = x + {b}\\), \\(du = dx\\). Factor out the constant \\({a}\\)."},
                {"level": 2, "text": f"\\({a} \\int_{{{b}}}^{{{1+b}}} u^{{{n}}}\\,du = {a} \\cdot \\left[\\frac{{u^{{{n+1}}}}}{{{n+1}}}\\right]_{{{b}}}^{{{1+b}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{a}}}{{{n+1}}} \\left({(1+b)**(n+1)} - {b**(n+1)}\\right) = \\frac{{{a * numerator}}}{{{n+1}}} = {ans}\\)."},
            ],
        }


# ── calc-byparts ──────────────────────────────────────────────────────────────

def _gen_calc_byparts():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: ∫_0^b ax·x dx = a*b³/3
        a = random.randint(2, 4)
        b = random.randint(1, 3)
        frac = Fraction(a * b**3, 3)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Use integration by parts to evaluate \\(\\int_{{0}}^{{{b}}} {a}x \\cdot x\\,dx\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Integration by parts: \\(\\int u\\,dv = uv - \\int v\\,du\\)."},
                {"level": 2, "text": f"Let \\(u = {a}x\\), \\(dv = x\\,dx\\). Then \\(du = {a}\\,dx\\), \\(v = \\frac{{x^2}}{{2}}\\)."},
                {"level": 3, "text": f"\\(\\left[{a}x \\cdot \\frac{{x^2}}{{2}}\\right]_{{0}}^{{{b}}} - \\int_{{0}}^{{{b}}} \\frac{{{a}x^2}}{{2}}\\,dx = \\frac{{{a*b**3}}}{{2}} - \\frac{{{a*b**3}}}{{6}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: ∫_0^2 x·(ax+c) dx = a*8/3 + 2c  (b fixed at 2, a divisible by 3 for integer)
        a = random.choice([3, 6])
        c = random.randint(1, 4)
        b = 2
        # ∫_0^b x(ax+c)dx = ∫_0^b (ax²+cx) dx = a*b³/3 + c*b²/2
        ans_val = a * b**3 // 3 + c * b**2 // 2   # a divisible by 3, b=2 so b²/2=2 integer
        return {
            "problem_text": f"Use integration by parts to evaluate \\(\\int_{{0}}^{{{b}}} x \\cdot ({a}x + {c})\\,dx\\).",
            "correct_answer": str(ans_val), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Integration by parts: \\(\\int u\\,dv = uv - \\int v\\,du\\). Let \\(u=x\\), \\(dv=({a}x+{c})\\,dx\\)."},
                {"level": 2, "text": f"\\(du = dx\\), \\(v = \\frac{{{a}}}{{2}}x^2 + {c}x\\). Alternatively, expand and integrate directly: \\({a}x^2 + {c}x\\)."},
                {"level": 3, "text": f"\\(\\int_{{0}}^{{{b}}} ({a}x^2 + {c}x)\\,dx = \\left[\\frac{{{a}}}{{3}}x^3 + \\frac{{{c}}}{{2}}x^2\\right]_{{0}}^{{{b}}} = \\frac{{{a*b**3}}}{{3}} + \\frac{{{c*b**2}}}{{2}} = {ans_val}\\)."},
            ],
        }
    else:
        # V3: ∫_0^b x·(ax+c) dx — pick a not divisible by 3, use fractions
        # For variety pick a=2, b=3: answer = 2*27/3 + c*9/2 = 18 + 9c/2
        # Ensure integer: c must be even. Use c in {2,4}.
        a = 2
        b = 3
        c = random.choice([2, 4])
        frac = Fraction(a * b**3, 3) + Fraction(c * b**2, 2)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Find \\(\\int_{{0}}^{{{b}}} x({a}x + {c})\\,dx\\) using integration by parts.",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Let \\(u = x\\), \\(dv = ({a}x+{c})\\,dx\\). Or expand \\(x({a}x+{c}) = {a}x^2 + {c}x\\) and integrate term by term."},
                {"level": 2, "text": f"\\(\\int_{{0}}^{{{b}}} ({a}x^2 + {c}x)\\,dx = \\left[\\frac{{{a}}}{{3}}x^3 + \\frac{{{c}}}{{2}}x^2\\right]_{{0}}^{{{b}}}\\)."},
                {"level": 3, "text": f"\\(= \\frac{{{a * b**3}}}{{3}} + \\frac{{{c * b**2}}}{{2}} = {ans}\\)."},
            ],
        }


# ── calc-improper ─────────────────────────────────────────────────────────────

def _gen_calc_improper():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: ∫_1^∞ x^(-n) dx = 1/(n-1)
        n = random.randint(2, 4)
        frac = Fraction(1, n-1)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Evaluate: \\(\\int_{{1}}^{{\\infty}} x^{{-{n}}}\\,dx\\)",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Replace \\(\\infty\\) with \\(t\\) and take \\(\\lim_{{t \\to \\infty}}\\) after evaluating."},
                {"level": 2, "text": f"Antiderivative of \\(x^{{-{n}}}\\) is \\(\\frac{{x^{{{1-n}}}}}{{{1-n}}}\\). Evaluate from 1 to \\(t\\)."},
                {"level": 3, "text": f"\\(\\lim_{{t\\to\\infty}} \\left[\\frac{{x^{{{1-n}}}}}{{{1-n}}}\\right]_1^t = 0 - \\frac{{1}}{{{1-n}}} = \\frac{{1}}{{{n-1}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: ∫_0^∞ e^(-ax) dx = 1/a
        a = random.randint(2, 5)
        frac = Fraction(1, a)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Evaluate \\(\\int_{{0}}^{{\\infty}} e^{{-{a}x}}\\,dx\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Replace \\(\\infty\\) with \\(t\\) and take \\(\\lim_{{t \\to \\infty}}\\)."},
                {"level": 2, "text": f"Antiderivative of \\(e^{{-{a}x}}\\) is \\(-\\frac{{1}}{{{a}}}e^{{-{a}x}}\\). Evaluate from 0 to \\(t\\)."},
                {"level": 3, "text": f"\\(\\lim_{{t\\to\\infty}} \\left[-\\frac{{e^{{-{a}x}}}}{{{a}}}\\right]_0^t = 0 - \\left(-\\frac{{1}}{{{a}}}\\right) = \\frac{{1}}{{{a}}} = {ans}\\)."},
            ],
        }
    else:
        # V3: ∫_1^∞ c·x^(-n) dx = k → find c (= k*(n-1))
        n = random.randint(2, 4)
        k = random.randint(1, 4)
        c = k * (n - 1)
        return {
            "problem_text": f"If \\(\\int_{{1}}^{{\\infty}} c \\cdot x^{{-{n}}}\\,dx = {k}\\), find \\(c\\).",
            "correct_answer": str(c), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": f"First evaluate \\(\\int_{{1}}^{{\\infty}} x^{{-{n}}}\\,dx\\), then set \\(c\\) times that equal to \\({k}\\)."},
                {"level": 2, "text": f"\\(\\int_{{1}}^{{\\infty}} x^{{-{n}}}\\,dx = \\frac{{1}}{{{n-1}}}\\). So \\(c \\cdot \\frac{{1}}{{{n-1}}} = {k}\\)."},
                {"level": 3, "text": f"\\(c = {k} \\times {n-1} = {c}\\)."},
            ],
        }


# ── calc-series-conv ──────────────────────────────────────────────────────────

def _gen_calc_series_conv():
    a = random.randint(1, 4)
    r_num = random.randint(1, 3)
    r_den = random.choice([3, 4, 5])
    while r_num >= r_den: r_num = random.randint(1, 3)
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: ∑_{n=0}^∞ a*(r_num/r_den)^n = a*r_den/(r_den-r_num)
        frac = Fraction(a * r_den, r_den - r_num)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Find the sum: \\(\\sum_{{n=0}}^{{\\infty}} {a} \\left(\\frac{{{r_num}}}{{{r_den}}}\\right)^n\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Geometric series formula: \\(\\sum_{{n=0}}^{{\\infty}} ar^n = \\frac{{a}}{{1-r}}\\) when \\(|r|<1\\)."},
                {"level": 2, "text": f"\\(a={a}\\), \\(r=\\frac{{{r_num}}}{{{r_den}}}\\). Compute \\(1-r = \\frac{{{r_den-r_num}}}{{{r_den}}}\\)."},
                {"level": 3, "text": f"Sum \\(= \\frac{{{a}}}{{\\frac{{{r_den-r_num}}}{{{r_den}}}}} = \\frac{{{a*r_den}}}{{{r_den-r_num}}} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: geometric series framing — first term / (1-r)
        # Present as "first term a, ratio r, sum = a/(1-r)"
        first = a   # first term (n=0 gives a*r^0 = a)
        r_frac = Fraction(r_num, r_den)
        sum_frac = Fraction(a, 1) / (1 - r_frac)
        ans = str(sum_frac.numerator) if sum_frac.denominator == 1 else f"{sum_frac.numerator}/{sum_frac.denominator}"
        return {
            "problem_text": (
                f"A geometric series has first term \\({first}\\) and common ratio "
                f"\\(\\frac{{{r_num}}}{{{r_den}}}\\). What is its sum?"
            ),
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Geometric series sum formula: \\(S = \\frac{{a}}{{1-r}}\\) when \\(|r|<1\\)."},
                {"level": 2, "text": f"\\(a = {first}\\), \\(r = \\frac{{{r_num}}}{{{r_den}}}\\). Compute \\(1 - r = \\frac{{{r_den - r_num}}}{{{r_den}}}\\)."},
                {"level": 3, "text": f"\\(S = \\frac{{{first}}}{{\\frac{{{r_den - r_num}}}{{{r_den}}}}} = \\frac{{{first * r_den}}}{{{r_den - r_num}}} = {ans}\\)."},
            ],
        }
    else:
        # V3: alternating geometric ∑_{n=0}^∞ a*(-r_num/r_den)^n = a*r_den/(r_den+r_num)
        frac = Fraction(a * r_den, r_den + r_num)
        ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
        return {
            "problem_text": f"Find the sum: \\(\\sum_{{n=0}}^{{\\infty}} {a} \\left(-\\frac{{{r_num}}}{{{r_den}}}\\right)^n\\).",
            "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Geometric series formula: \\(\\sum ar^n = \\frac{{a}}{{1-r}}\\). Here \\(r = -\\frac{{{r_num}}}{{{r_den}}}\\)."},
                {"level": 2, "text": f"\\(1 - r = 1 + \\frac{{{r_num}}}{{{r_den}}} = \\frac{{{r_den+r_num}}}{{{r_den}}}\\)."},
                {"level": 3, "text": f"Sum \\(= \\frac{{{a}}}{{\\frac{{{r_den+r_num}}}{{{r_den}}}}} = \\frac{{{a*r_den}}}{{{r_den+r_num}}} = {ans}\\)."},
            ],
        }


# ── mv-partial ────────────────────────────────────────────────────────────────

def _gen_mv_partial():
    a = random.randint(1, 4)
    m = random.randint(2, 4)     # avoid ^{1} by keeping m,n ≥ 2
    n = random.randint(2, 4)
    a_str = str(a) if a != 1 else ""
    if random.randint(0,1) == 0:
        ans = a * m
        return {
            "problem_text": f"Let \\(f(x,y) = {a_str}x^{{{m}}}y^{{{n}}}\\). Find \\(\\frac{{\\partial f}}{{\\partial x}}(1,1)\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Treat \\(y\\) as a constant and differentiate w.r.t. \\(x\\)."},
                {"level": 2, "text": f"\\(\\frac{{\\partial f}}{{\\partial x}} = {a*m}x^{{{m-1}}}y^{{{n}}}\\). Evaluate at \\((1,1)\\)."},
                {"level": 3, "text": f"\\(\\frac{{\\partial f}}{{\\partial x}}(1,1) = {a*m}(1)(1) = {ans}\\)."},
            ],
        }
    else:
        ans = a * n
        return {
            "problem_text": f"Let \\(f(x,y) = {a_str}x^{{{m}}}y^{{{n}}}\\). Find \\(\\frac{{\\partial f}}{{\\partial y}}(1,1)\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Treat \\(x\\) as a constant and differentiate w.r.t. \\(y\\)."},
                {"level": 2, "text": f"\\(\\frac{{\\partial f}}{{\\partial y}} = {a*n}x^{{{m}}}y^{{{n-1}}}\\). Evaluate at \\((1,1)\\)."},
                {"level": 3, "text": f"\\(\\frac{{\\partial f}}{{\\partial y}}(1,1) = {a*n}(1)(1) = {ans}\\)."},
            ],
        }


# ── mv-double-integral ────────────────────────────────────────────────────────

def _gen_mv_double_integral():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: constant integrand ∫∫ c dx dy
        c = random.randint(1, 5)
        b = random.randint(1, 4)
        q = random.randint(1, 4)
        ans = c * b * q
        return {
            "problem_text": f"Evaluate \\(\\int_{{0}}^{{{q}}} \\int_{{0}}^{{{b}}} {c}\\,dx\\,dy\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Evaluate the inner integral first (treat \\(y\\) as constant), then the outer."},
                {"level": 2, "text": f"Inner: \\(\\int_{{0}}^{{{b}}} {c}\\,dx = {c*b}\\). Outer: \\(\\int_{{0}}^{{{q}}} {c*b}\\,dy\\)."},
                {"level": 3, "text": f"\\({c*b} \\times {q} = {ans}\\)."},
            ],
        }
    elif variant == 1:
        # V2: ∫_0^q ∫_0^p cx dx dy = c*p²*q/2 (p even, c>=2 to avoid '1x' artifact)
        c = random.randint(2, 4)
        p = random.choice([2, 4])   # even so cp²/2 is integer
        q = random.randint(1, 4)
        inner = c * p**2 // 2   # = c*p²/2, integer since p even
        ans = inner * q
        return {
            "problem_text": f"Evaluate \\(\\int_{{0}}^{{{q}}} \\int_{{0}}^{{{p}}} {c}x\\,dx\\,dy\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "Evaluate the inner integral first (treat \\(y\\) as constant), then the outer."},
                {"level": 2, "text": f"Inner: \\(\\int_{{0}}^{{{p}}} {c}x\\,dx = \\left[\\frac{{{c}}}{{2}}x^2\\right]_{{0}}^{{{p}}} = {inner}\\)."},
                {"level": 3, "text": f"Outer: \\(\\int_{{0}}^{{{q}}} {inner}\\,dy = {inner} \\times {q} = {ans}\\)."},
            ],
        }
    else:
        # V3: ∫_0^b ∫_0^2 (x+y) dx dy with fixed inner bound 2
        # inner = ∫_0^2 (x+y)dx = [x²/2+xy]_0^2 = 2+2y
        # outer = ∫_0^b (2+2y)dy = 2b + b²
        b = random.choice([2, 4, 6])
        inner_expr = "2 + 2y"
        ans = 2 * b + b**2
        return {
            "problem_text": f"Evaluate \\(\\int_{{0}}^{{{b}}} \\int_{{0}}^{{2}} (x + y)\\,dx\\,dy\\).",
            "correct_answer": str(ans), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Evaluate the inner integral (w.r.t. \\(x\\)) treating \\(y\\) as a constant."},
                {"level": 2, "text": f"Inner: \\(\\int_{{0}}^{{2}} (x+y)\\,dx = \\left[\\frac{{x^2}}{{2}} + xy\\right]_{{0}}^{{2}} = 2 + 2y\\)."},
                {"level": 3, "text": f"Outer: \\(\\int_{{0}}^{{{b}}} (2+2y)\\,dy = \\left[2y + y^2\\right]_{{0}}^{{{b}}} = {2*b} + {b**2} = {ans}\\)."},
            ],
        }


# ── mv-change-vars ────────────────────────────────────────────────────────────

def _gen_mv_change_vars():
    variant = random.choice([0, 1, 2])
    if variant == 0:
        # V1: u=ax, v=ay — area scales by a²
        a = random.randint(2, 5)
        region_area = random.randint(2, 8)
        transformed = region_area * a * a
        return {
            "problem_text": (
                f"The substitution \\(u = {a}x\\), \\(v = {a}y\\) maps a region with area \\({region_area}\\) "
                f"in \\((x,y)\\) coordinates. What is the area of the corresponding region in \\((u,v)\\) coordinates?"
            ),
            "correct_answer": str(transformed), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "Areas scale by the absolute value of the Jacobian determinant under a change of variables."},
                {"level": 2, "text": f"Jacobian \\(= \\left|\\det\\begin{{pmatrix}}{a}&0\\\\0&{a}\\end{{pmatrix}}\\right| = {a}^2 = {a**2}\\)."},
                {"level": 3, "text": f"New area \\(= {region_area} \\times {a**2} = {transformed}\\)."},
            ],
        }
    elif variant == 1:
        # V2: ask for the Jacobian determinant of u=ax, v=by (a≠b)
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        while b == a: b = random.randint(2, 5)
        jac = a * b
        return {
            "problem_text": f"What is the Jacobian determinant of the transformation \\(u = {a}x\\), \\(v = {b}y\\)?",
            "correct_answer": str(jac), "answer_type": "numeric", "difficulty": 0.6,
            "hints": [
                {"level": 1, "text": "The Jacobian matrix has partial derivatives \\(\\frac{{\\partial u}}{{\\partial x}}\\), \\(\\frac{{\\partial u}}{{\\partial y}}\\), \\(\\frac{{\\partial v}}{{\\partial x}}\\), \\(\\frac{{\\partial v}}{{\\partial y}}\\)."},
                {"level": 2, "text": f"Jacobian matrix \\(= \\begin{{pmatrix}}{a}&0\\\\0&{b}\\end{{pmatrix}}\\). Determinant = \\({a} \\times {b} - 0\\)."},
                {"level": 3, "text": f"\\(\\det = {a} \\times {b} = {jac}\\)."},
            ],
        }
    else:
        # V3: inverse map x=u/a, y=v/b — area in (x,y) given area in (u,v)
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        area_uv = random.randint(1, 6) * a * b   # ensure integer result
        area_xy = area_uv // (a * b)
        return {
            "problem_text": (
                f"The Jacobian of \\(x = u/{a}\\), \\(y = v/{b}\\) is \\(\\frac{{1}}{{{a*b}}}\\). "
                f"If a region in \\((u,v)\\) has area \\({area_uv}\\), what is the area in \\((x,y)\\)?"
            ),
            "correct_answer": str(area_xy), "answer_type": "numeric", "difficulty": 0.7,
            "hints": [
                {"level": 1, "text": "When mapping from \\((u,v)\\) to \\((x,y)\\), the area scales by the Jacobian \\(\\left|\\frac{{\\partial(x,y)}}{{\\partial(u,v)}}\\right|\\)."},
                {"level": 2, "text": f"Jacobian \\(= \\frac{{1}}{{{a}}} \\times \\frac{{1}}{{{b}}} = \\frac{{1}}{{{a*b}}}\\). Area in \\((x,y)\\) \\(= {area_uv} \\times \\frac{{1}}{{{a*b}}}\\)."},
                {"level": 3, "text": f"Area \\(= \\frac{{{area_uv}}}{{{a*b}}} = {area_xy}\\)."},
            ],
        }


# ── GENERATORS dict ───────────────────────────────────────────────────────────

GENERATORS = {
    "calc-limits":          _gen_calc_limits,
    "calc-limit-laws":      _gen_calc_limit_laws,
    "calc-continuity":      _gen_calc_continuity,
    "calc-deriv-def":       _gen_calc_deriv_def,
    "calc-deriv-power":     _gen_calc_deriv_power,
    "calc-deriv-product":   _gen_calc_deriv_product,
    "calc-deriv-chain":     _gen_calc_deriv_chain,
    "calc-deriv-exp-log":   _gen_calc_deriv_exp_log,
    "calc-implicit":        _gen_calc_implicit,
    "calc-optim":           _gen_calc_optim,
    "calc-antideriv":       _gen_calc_antideriv,
    "calc-riemann":         _gen_calc_riemann,
    "calc-ftc":             _gen_calc_ftc,
    "calc-usub":            _gen_calc_usub,
    "calc-byparts":         _gen_calc_byparts,
    "calc-improper":        _gen_calc_improper,
    "calc-series-conv":     _gen_calc_series_conv,
    "mv-partial":           _gen_mv_partial,
    "mv-double-integral":   _gen_mv_double_integral,
    "mv-change-vars":       _gen_mv_change_vars,
}
