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
- \binom{n}{k}  → binomial(n,k)
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

    # Remove surrounding \( \) delimiters if present
    s = re.sub(r'^\\\(', '', s).strip()
    s = re.sub(r'\\\)$', '', s).strip()

    # Remove surrounding \[ \] delimiters if present
    s = re.sub(r'^\\\[', '', s).strip()
    s = re.sub(r'\\\]$', '', s).strip()

    # Remove surrounding $ $ delimiters if present
    s = re.sub(r'^\$+|\$+$', '', s).strip()

    # \frac{a}{b} → (a)/(b) — handle nested (apply multiple times)
    def replace_frac(m):
        return f'({m.group(1)})/({m.group(2)})'
    for _ in range(5):
        prev = s
        s = re.sub(
            r'\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
            replace_frac, s
        )
        if s == prev:
            break

    # \sqrt[n]{x} → x**(1/n), \sqrt{x} → sqrt(x)
    s = re.sub(r'\\sqrt\[([^\]]+)\]\{([^}]+)\}', r'((\2)**(1/(\1)))', s)
    s = re.sub(r'\\sqrt\{([^}]+)\}', r'sqrt(\1)', s)

    # x^{n} → x**(n), x^n → x**n
    s = re.sub(r'\^\{([^}]+)\}', r'**(\1)', s)
    s = re.sub(r'\^([a-zA-Z0-9])', r'**\1', s)

    # Subscripts (indices) — remove for simple cases
    s = re.sub(r'_\{[^}]+\}', '', s)
    s = re.sub(r'_[a-zA-Z0-9]', '', s)

    # \log_{b}(x) → log(x, b); various forms
    s = re.sub(r'\\log_\{([^}]+)\}\s*\(([^)]+)\)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_\{([^}]+)\}\s*([a-zA-Z0-9]+)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_([0-9]+)\s*\(([^)]+)\)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_([0-9]+)\s+([a-zA-Z0-9]+)', r'log(\2, \1)', s)
    s = re.sub(r'\\log\s*\(([^)]+)\)', r'log(\1, 10)', s)
    s = re.sub(r'\\log\s+([a-zA-Z0-9]+)', r'log(\1, 10)', s)
    s = re.sub(r'\\ln\s*\(([^)]+)\)', r'log(\1)', s)
    s = re.sub(r'\\ln\s+([a-zA-Z0-9]+)', r'log(\1)', s)

    # \binom{n}{k} → binomial(n, k)
    s = re.sub(r'\\binom\{([^}]+)\}\{([^}]+)\}', r'binomial(\1, \2)', s)

    # n! → factorial(n)
    s = re.sub(r'([a-zA-Z0-9]+)!', r'factorial(\1)', s)

    # Operators
    s = s.replace('\\cdot', '*').replace('\\times', '*')
    s = s.replace('\\div', '/')
    s = s.replace('÷', '/').replace('×', '*')

    # Remove grouping helpers
    s = s.replace('\\left', '').replace('\\right', '')
    s = s.replace('\\!', '').replace('\\ ', ' ')

    # Remove any remaining unknown backslash-letter commands
    s = re.sub(r'\\[a-zA-Z]+\*?', '', s)

    # Clean up extra spaces and stray braces
    s = s.replace('{', '(').replace('}', ')')
    s = re.sub(r'\s+', ' ', s).strip()

    return s


def _try_parse(expr_str: str):
    """Try multiple parsing strategies. Returns SymPy expr or None."""
    if not SYMPY_AVAILABLE:
        return None

    # Strategy 1: parse_expr with implicit multiplication
    try:
        return parse_expr(expr_str, transformations=TRANSFORMATIONS)
    except Exception:
        pass

    # Strategy 2: sympify directly
    try:
        return sympify(expr_str)
    except Exception:
        pass

    return None


def _to_sympy(raw: str):
    """
    Convert a raw answer string (LaTeX or plain text) to a SymPy expression.
    Tries LaTeX conversion first, then plain-text parsing.
    Returns the SymPy expression or None on failure.
    """
    # Try LaTeX conversion first
    converted = latex_to_sympy_str(raw)
    logger.debug(f"  latex_to_sympy_str({raw!r}) → {converted!r}")

    expr = _try_parse(converted)
    if expr is not None:
        logger.debug(f"  parsed({converted!r}) → {expr}")
        return expr

    # If LaTeX conversion changed the string, also try the original plain text
    if converted != raw:
        expr = _try_parse(raw)
        if expr is not None:
            logger.debug(f"  parsed plain({raw!r}) → {expr}")
            return expr

    logger.debug(f"  could not parse {raw!r}")
    return None


def normalize_string(s: str) -> str:
    """Basic string normalization for last-resort fallback comparison."""
    s = s.strip().lower()
    # Remove LaTeX-specific formatting
    s = re.sub(r'\\[a-zA-Z]+', '', s)
    s = s.replace('{', '').replace('}', '')
    s = s.replace(' ', '').replace('×', '*').replace('÷', '/').replace('−', '-')
    # Normalize fraction notation
    s = re.sub(r'\((\d+)\)/\((\d+)\)', r'\1/\2', s)
    return s


def check_answer(student_answer: str, correct_answer: str, answer_type: AnswerType = "symbolic") -> bool:
    """
    Check if a student's answer matches the correct answer.

    Detailed logging is included to help diagnose format mismatches.

    For multiple_choice: case-insensitive string match.
    For numeric: float comparison with tolerance.
    For symbolic: SymPy symbolic equivalence, with LaTeX parsing for MathLive output.
    """
    student = student_answer.strip()
    correct = correct_answer.strip()

    logger.info(
        f"check_answer | type={answer_type!r} | "
        f"student={student!r} | correct={correct!r}"
    )

    # ── Multiple choice ──────────────────────────────────────────────────────
    if answer_type == "multiple_choice":
        result = student.lower() == correct.lower()
        logger.info(f"  multiple_choice match: {result}")
        return result

    # ── Numeric ─────────────────────────────────────────────────────────────
    if answer_type == "numeric":
        # Direct float comparison
        try:
            sv = float(student)
            cv = float(correct)
            result = abs(sv - cv) <= 0.01
            logger.info(f"  numeric float: {sv} vs {cv} → {result}")
            return result
        except ValueError:
            pass

        # SymPy numeric evaluation
        if SYMPY_AVAILABLE:
            s_expr = _to_sympy(student)
            c_expr = _to_sympy(correct)
            if s_expr is not None and c_expr is not None:
                try:
                    sv = float(N(s_expr))
                    cv = float(N(c_expr))
                    result = abs(sv - cv) <= 0.01
                    logger.info(f"  numeric sympy: {sv} vs {cv} → {result}")
                    return result
                except Exception as e:
                    logger.debug(f"  numeric sympy N() failed: {e}")

        # Normalized string fallback
        ns = normalize_string(student)
        nc = normalize_string(correct)
        result = ns == nc
        logger.info(f"  numeric string fallback: {ns!r} vs {nc!r} → {result}")
        return result

    # ── Symbolic (default) ───────────────────────────────────────────────────
    if not SYMPY_AVAILABLE:
        ns = normalize_string(student)
        nc = normalize_string(correct)
        result = ns == nc
        logger.info(f"  symbolic (no sympy) string: {result}")
        return result

    s_expr = _to_sympy(student)
    c_expr = _to_sympy(correct)

    if s_expr is not None and c_expr is not None:
        # Symbolic simplification
        try:
            diff = simplify(s_expr - c_expr)
            if diff == 0:
                logger.info("  symbolic simplify: match (diff=0)")
                return True
        except Exception as e:
            logger.debug(f"  simplify failed: {e}")

        # Numeric evaluation backup
        try:
            sv = complex(N(s_expr))
            cv = complex(N(c_expr))
            if abs(sv - cv) < 1e-6:
                logger.info(f"  symbolic numeric eval: match ({sv} ≈ {cv})")
                return True
        except Exception as e:
            logger.debug(f"  numeric eval failed: {e}")

        logger.info(f"  symbolic: no match ({s_expr!r} vs {c_expr!r})")
    else:
        logger.info(f"  symbolic: parse failed (s={s_expr}, c={c_expr})")

    # Normalized string fallback
    ns = normalize_string(student)
    nc = normalize_string(correct)
    result = ns == nc
    logger.info(f"  symbolic string fallback: {ns!r} vs {nc!r} → {result}")
    return result
