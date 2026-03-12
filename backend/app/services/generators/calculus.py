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
    a = random.randint(1, 5)
    deriv = 2*a
    return {
        "problem_text": f"Using the limit definition, find \\(f'({a})\\) for \\(f(x) = x^2\\).",
        "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Definition: \\(f'(a) = \\lim_{{h \\to 0}} \\frac{{f(a+h)-f(a)}}{{h}}\\)."},
            {"level": 2, "text": f"Compute \\(({a}+h)^2 - {a}^2\\), simplify, divide by \\(h\\), then let \\(h \\to 0\\)."},
            {"level": 3, "text": f"\\(({a}+h)^2 - {a**2} = 2 \\cdot {a} \\cdot h + h^2\\). Divide by \\(h\\): \\(2 \\cdot {a} + h \\to {deriv}\\)."},
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
    n = random.randint(2, 4)
    a = random.randint(2, 4)
    b = random.choice([-3,-2,-1,1,2,3])   # exclude 0
    # f'(0) = n*a*(a*0+b)^(n-1) = n*a*b^(n-1)
    deriv = n * a * (b**(n-1))
    return {
        "problem_text": f"Find \\(f'(0)\\) for \\(f(x) = {_factor(a,b)}^{{{n}}}\\).",
        "correct_answer": str(deriv), "answer_type": "numeric", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Chain rule: \\(\\frac{d}{dx}[u^n] = nu^{n-1} \\cdot u'\\). Here \\(u = {_lin(a,b)}\\)."},
            {"level": 2, "text": f"\\(f'(x) = {n}{_factor(a,b)}^{{{n-1}}} \\cdot {a}\\). Evaluate at \\(x=0\\)."},
            {"level": 3, "text": f"\\(f'(0) = {n}({b})^{{{n-1}}} \\cdot {a} = {n*b**(n-1)} \\cdot {a} = {deriv}\\)."},
        ],
    }


# ── calc-deriv-exp-log ────────────────────────────────────────────────────────

def _gen_calc_deriv_exp_log():
    a = random.randint(2, 6)
    if random.randint(0,1) == 0:
        return {
            "problem_text": f"Find \\(f'(0)\\) for \\(f(x) = {a}e^x\\).",
            "correct_answer": str(a), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\frac{d}{dx}e^x = e^x\\). Constants factor out."},
                {"level": 2, "text": f"\\(f'(x) = {a}e^x\\). Evaluate at \\(x=0\\)."},
                {"level": 3, "text": f"\\(f'(0) = {a}e^0 = {a} \\cdot 1 = {a}\\)."},
            ],
        }
    else:
        return {
            "problem_text": f"Find \\(f'(1)\\) for \\(f(x) = {a}\\ln(x)\\).",
            "correct_answer": str(a), "answer_type": "numeric", "difficulty": 0.4,
            "hints": [
                {"level": 1, "text": "\\(\\frac{d}{dx}\\ln(x) = \\frac{1}{x}\\). Constants factor out."},
                {"level": 2, "text": f"\\(f'(x) = \\frac{{{a}}}{{x}}\\). Evaluate at \\(x=1\\)."},
                {"level": 3, "text": f"\\(f'(1) = \\frac{{{a}}}{{1}} = {a}\\)."},
            ],
        }


# ── calc-implicit ─────────────────────────────────────────────────────────────

def _gen_calc_implicit():
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
    return {
        "problem_text": f"Find \\(\\int {_axn(a,n)}\\, dx\\). Enter the coefficient of \\({_xn(n+1)}\\).",
        "correct_answer": coef_str, "answer_type": "symbolic", "difficulty": 0.5,
        "hints": [
            {"level": 1, "text": f"Power rule: \\(\\int x^n\\,dx = \\frac{{x^{{n+1}}}}{{n+1}} + C\\)."},
            {"level": 2, "text": f"Raise the power: \\(n+1 = {n+1}\\). Divide coefficient \\({a}\\) by \\({n+1}\\)."},
            {"level": 3, "text": f"\\(\\int {_axn(a,n)}\\,dx = \\frac{{{a}}}{{{n+1}}}{_xn(n+1)} + C\\). Coefficient = \\({coef_str}\\)."},
        ],
    }


# ── calc-riemann ──────────────────────────────────────────────────────────────

def _gen_calc_riemann():
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


# ── calc-ftc ──────────────────────────────────────────────────────────────────

def _gen_calc_ftc():
    n = random.randint(2, 4)      # avoid n=1 display issue
    c = random.randint(1, 4)
    b = random.randint(1, 4)
    frac = Fraction(c * b**(n+1), n+1)
    ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    return {
        "problem_text": f"Evaluate: \\(\\int_{{0}}^{{{b}}} {_axn(c,n)}\\,dx\\)",
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "FTC: find the antiderivative \\(F(x)\\), then compute \\(F(b)-F(a)\\)."},
            {"level": 2, "text": f"\\(F(x) = \\frac{{{c}}}{{{n+1}}}{_xn(n+1)}\\). Evaluate at \\(x={b}\\) minus at \\(x=0\\)."},
            {"level": 3, "text": f"\\(F({b})-F(0) = \\frac{{{c}}}{{{n+1}}} \\cdot {b}^{{{n+1}}} = \\frac{{{c*b**(n+1)}}}{{{n+1}}} = {ans}\\)."},
        ],
    }


# ── calc-usub ─────────────────────────────────────────────────────────────────

def _gen_calc_usub():
    n = random.randint(2, 4)
    b = random.randint(1, 3)
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


# ── calc-byparts ──────────────────────────────────────────────────────────────

def _gen_calc_byparts():
    # ∫_0^b a*x^2 dx = a*b^3/3  (show as u=ax, dv=x dx)
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


# ── calc-improper ─────────────────────────────────────────────────────────────

def _gen_calc_improper():
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


# ── calc-series-conv ──────────────────────────────────────────────────────────

def _gen_calc_series_conv():
    a = random.randint(1, 4)
    r_num = random.randint(1, 3)
    r_den = random.choice([3, 4, 5])
    while r_num >= r_den: r_num = random.randint(1, 3)
    frac = Fraction(a * r_den, r_den - r_num)
    ans = str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"
    return {
        "problem_text": f"Find the sum: \\(\\sum_{{n=0}}^{{\\infty}} {a} \\left(\\frac{{{r_num}}}{{{r_den}}}\\right)^n\\).",
        "correct_answer": ans, "answer_type": "symbolic", "difficulty": 0.6,
        "hints": [
            {"level": 1, "text": "Geometric series formula: \\(\\sum ar^n = \\frac{a}{1-r}\\) when \\(|r|<1\\)."},
            {"level": 2, "text": f"\\(a={a}\\), \\(r=\\frac{{{r_num}}}{{{r_den}}}\\). Compute \\(1-r = \\frac{{{r_den-r_num}}}{{{r_den}}}\\)."},
            {"level": 3, "text": f"Sum \\(= \\frac{{{a}}}{{\\frac{{{r_den-r_num}}}{{{r_den}}}}} = \\frac{{{a*r_den}}}{{{r_den-r_num}}} = {ans}\\)."},
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
    c = random.randint(1, 5)
    b = random.randint(1, 4)
    q = random.randint(1, 4)   # both bounds start at 0, keep ≥1
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


# ── mv-change-vars ────────────────────────────────────────────────────────────

def _gen_mv_change_vars():
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
