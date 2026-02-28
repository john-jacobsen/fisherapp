"""
Robust answer checker using SymPy for symbolic math verification.
Handles LaTeX input from MathLive as well as plain expressions.

LaTeX conversion handles:
- \frac{a}{b}   → a/b
- x^{n}         → x**n
- \sqrt{x}      → sqrt(x)
- \log_b(x)     → log(x, b)
- \ln(x)        → log(x)
- \cdot, \times → *
- \div          → /
- \binom{n}{k}  → factorial(n)/(factorial(k)*factorial(n-k))
- n!            → factorial(n)
"""
import re
import logging
from typing import Literal

logger = logging.getLogger(__name__)

try:
    from sympy import (
        simplify, sympify, SympifyError, N, Symbol,
        factorial, log, sqrt, Rational, binomial,
        oo, zoo, nan
    )
    from sympy.parsing.sympy_parser import (
        parse_expr, standard_transformations, implicit_multiplication_application
    )
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False


AnswerType = Literal["symbolic", "numeric", "multiple_choice"]

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application,)


def latex_to_sympy_str(latex: str) -> str:
    """
    Convert a LaTeX string (as output by MathLive) to a SymPy-parseable string.
    Handles common patterns found in this app's content.
    """
    s = latex.strip()

    # Remove surrounding \( \) or $ $ delimiters if present
    s = re.sub(r'^\\\(|\\\)$', '', s).strip()
    s = re.sub(r'^\$|\$$', '', s).strip()

    # \frac{a}{b} → (a)/(b)
    def replace_frac(m):
        return f'({m.group(1)})/({m.group(2)})'
    # Handle nested fracs - apply multiple times
    for _ in range(5):
        prev = s
        s = re.sub(r'\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', replace_frac, s)
        if s == prev:
            break

    # \sqrt{x} → sqrt(x), \sqrt[n]{x} → x**(1/n)
    s = re.sub(r'\\sqrt\[([^\]]+)\]\{([^}]+)\}', r'((\2)**(1/(\1)))', s)
    s = re.sub(r'\\sqrt\{([^}]+)\}', r'sqrt(\1)', s)

    # x^{n} or x^n → x**n (but keep multi-char exponents in parens)
    s = re.sub(r'\^\{([^}]+)\}', r'**(\1)', s)
    s = re.sub(r'\^([a-zA-Z0-9])', r'**\1', s)

    # Subscripts like x_{n} or x_n (usually in indices) — just remove them for simple cases
    s = re.sub(r'_\{[^}]+\}', '', s)
    s = re.sub(r'_[a-zA-Z0-9]', '', s)

    # \log_{b}(x) → log(x, b) ; \log_b x → log(x, b)
    s = re.sub(r'\\log_\{([^}]+)\}\s*\(([^)]+)\)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_\{([^}]+)\}\s*([a-zA-Z0-9]+)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_([0-9]+)\s*\(([^)]+)\)', r'log(\2, \1)', s)
    s = re.sub(r'\\log\s*\(([^)]+)\)', r'log(\1, 10)', s)  # log without base = log10
    s = re.sub(r'\\log\s+([a-zA-Z0-9]+)', r'log(\1, 10)', s)
    s = re.sub(r'\\ln\s*\(([^)]+)\)', r'log(\1)', s)
    s = re.sub(r'\\ln\s+([a-zA-Z0-9]+)', r'log(\1)', s)

    # \binom{n}{k} → binomial(n, k)
    s = re.sub(r'\\binom\{([^}]+)\}\{([^}]+)\}', r'binomial(\1, \2)', s)

    # n! → factorial(n)  — handle carefully to avoid double-replacement
    s = re.sub(r'([a-zA-Z0-9]+)!', r'factorial(\1)', s)

    # \cdot, \times → *
    s = s.replace('\\cdot', '*').replace('\\times', '*')

    # \div → /
    s = s.replace('\\div', '/')

    # ÷ → /  (unicode division)
    s = s.replace('÷', '/').replace('×', '*')

    # Remove remaining LaTeX commands that don't affect value
    s = s.replace('\\left', '').replace('\\right', '')
    s = s.replace('\\!', '').replace('\\ ', ' ')

    # Remove any remaining backslash-letter sequences (unknown commands)
    s = re.sub(r'\\[a-zA-Z]+', '', s)

    # Clean up extra spaces
    s = re.sub(r'\s+', ' ', s).strip()

    return s


def normalize_string(s: str) -> str:
    """Basic string normalization for fallback comparison."""
    s = s.strip().lower()
    s = s.replace(' ', '').replace('×', '*').replace('÷', '/').replace('−', '-')
    return s


def check_answer(student_answer: str, correct_answer: str, answer_type: AnswerType = "symbolic") -> bool:
    """
    Check if a student's answer matches the correct answer.

    For multiple_choice: case-insensitive string match.
    For numeric: float comparison with tolerance.
    For symbolic: SymPy symbolic equivalence, with LaTeX parsing for MathLive output.
    """
    student = student_answer.strip()
    correct = correct_answer.strip()

    if answer_type == "multiple_choice":
        return student.lower() == correct.lower()

    if answer_type == "numeric":
        # Try direct float comparison first
        try:
            sv = float(student)
            cv = float(correct)
            return abs(sv - cv) <= 0.01
        except ValueError:
            pass
        # Try LaTeX conversion then float
        try:
            sv = float(N(sympify(latex_to_sympy_str(student))))
            cv = float(N(sympify(latex_to_sympy_str(correct))))
            return abs(sv - cv) <= 0.01
        except Exception:
            pass
        return normalize_string(student) == normalize_string(correct)

    # Symbolic (default) — also used for numeric-like answers expressed as fractions
    if not SYMPY_AVAILABLE:
        return normalize_string(student) == normalize_string(correct)

    # Try symbolic comparison with SymPy
    try:
        s_str = latex_to_sympy_str(student)
        c_str = latex_to_sympy_str(correct)

        s_expr = parse_expr(s_str, transformations=TRANSFORMATIONS)
        c_expr = parse_expr(c_str, transformations=TRANSFORMATIONS)

        diff = simplify(s_expr - c_expr)
        if diff == 0:
            return True

        # Numeric evaluation as backup (catches cases simplify misses)
        try:
            s_val = complex(N(s_expr))
            c_val = complex(N(c_expr))
            if abs(s_val - c_val) < 1e-6:
                return True
        except Exception:
            pass

        return False

    except Exception as e:
        logger.debug(f"Symbolic check failed: student={student!r}, correct={correct!r}, error={e}")

    # Fallback: try direct sympify without transformation
    try:
        s_expr = sympify(latex_to_sympy_str(student))
        c_expr = sympify(latex_to_sympy_str(correct))
        diff = simplify(s_expr - c_expr)
        if diff == 0:
            return True
    except Exception:
        pass

    # Last resort: normalized string comparison
    return normalize_string(student) == normalize_string(correct)
