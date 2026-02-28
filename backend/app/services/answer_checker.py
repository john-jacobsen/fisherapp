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

Solution set handling:
- "2, 3" or "3, 2" or "x=2, x=3" or "{2, 3}" or "\{2, 3\}" all treated as sets
- Compared as sets (order-independent), partial answers marked INCORRECT
"""
import re
import logging
from typing import Literal, Optional

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

    # Handle LaTeX set braces \{ ... \} — strip them to expose the contents
    # e.g. \{2, 3\} → 2, 3
    s = re.sub(r'\\\{', '{', s)
    s = re.sub(r'\\\}', '}', s)

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

    # \log_{b}(x) → log(x, b); various forms
    # IMPORTANT: these must run BEFORE the general subscript-removal step so
    # that the base (e.g. the "2" in \log_{2}) is not stripped prematurely.
    s = re.sub(r'\\log_\{([^}]+)\}\s*\(([^)]+)\)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_\{([^}]+)\}\s*([a-zA-Z0-9]+)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_([0-9]+)\s*\(([^)]+)\)', r'log(\2, \1)', s)
    s = re.sub(r'\\log_([0-9]+)\s+([a-zA-Z0-9]+)', r'log(\2, \1)', s)
    s = re.sub(r'\\log\s*\(([^)]+)\)', r'log(\1, 10)', s)
    s = re.sub(r'\\log\s+([a-zA-Z0-9]+)', r'log(\1, 10)', s)
    s = re.sub(r'\\ln\s*\(([^)]+)\)', r'log(\1)', s)
    s = re.sub(r'\\ln\s+([a-zA-Z0-9]+)', r'log(\1)', s)

    # x^{n} → x**(n), x^n → x**n
    s = re.sub(r'\^\{([^}]+)\}', r'**(\1)', s)
    s = re.sub(r'\^([a-zA-Z0-9])', r'**\1', s)

    # Subscripts (indices) — remove for simple cases
    # (log subscripts have already been handled above)
    s = re.sub(r'_\{[^}]+\}', '', s)
    s = re.sub(r'_[a-zA-Z0-9]', '', s)

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


# ── Solution-set helpers ─────────────────────────────────────────────────────

def _is_multi_value(s: str) -> bool:
    """
    Return True if the string looks like a multi-value answer (solution set).

    A string is multi-value if it contains:
      - a comma not inside parentheses, or
      - the word "and" (as a separator), or
      - set-brace notation { ... }

    We deliberately exclude single expressions like "2x + 3" which contain
    no comma and no "and" as a separator between values.
    """
    stripped = s.strip()

    # Check for LaTeX set braces \{ \} or plain { }
    if re.search(r'[\{\}]', stripped):
        return True

    # Check for "and" used as a value separator (standalone word)
    # e.g. "x=2 and x=3"  but NOT "sin and cos" (but that won't appear here)
    if re.search(r'\band\b', stripped, re.IGNORECASE):
        return True

    # Check for a comma that is not inside parentheses
    # We scan character by character tracking parenthesis depth
    depth = 0
    for ch in stripped:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch == ',' and depth == 0:
            return True

    return False


def _strip_variable_prefix(token: str) -> str:
    """
    Remove leading variable assignment like "x = " or "x=" from a token.
    Examples:
      "x = 2"  → "2"
      "x=3"    → "3"
      "y = -1" → "-1"
      "2"      → "2"
    """
    # Match patterns like: letter(s) optional-spaces = optional-spaces
    m = re.match(r'^[a-zA-Z]\s*=\s*(.*)', token.strip())
    if m:
        return m.group(1).strip()
    return token.strip()


def _split_multi_value(s: str) -> list:
    """
    Split a multi-value answer string into individual value tokens.

    Handles:
      "2, 3"           → ["2", "3"]
      "x = 2, x = 3"  → ["2", "3"]
      "x=2 and x=3"   → ["2", "3"]
      "{2, 3}"         → ["2", "3"]
      "\{2, 3\}"       → ["2", "3"]
      "x = 2, 3"       → ["2", "3"]
    """
    stripped = s.strip()

    # Remove outer set braces (both LaTeX \{ \} and plain { })
    # LaTeX style: \{...\}
    stripped = re.sub(r'^\\\{(.*)\\\}$', r'\1', stripped).strip()
    # Plain style: {...}
    stripped = re.sub(r'^\{(.*)\}$', r'\1', stripped).strip()

    # Split on "and" or commas
    parts = re.split(r'\s+and\s+|,', stripped, flags=re.IGNORECASE)

    # Strip variable prefixes and whitespace from each part
    tokens = [_strip_variable_prefix(p) for p in parts]

    # Filter out empty tokens
    tokens = [t for t in tokens if t]

    return tokens


def _parse_value_set(s: str):
    """
    Parse a multi-value answer string into a frozenset of SymPy expressions.
    Returns None if any value cannot be parsed.
    """
    tokens = _split_multi_value(s)
    sympy_values = []
    for token in tokens:
        expr = _to_sympy(token)
        if expr is None:
            logger.debug(f"  _parse_value_set: could not parse token {token!r}")
            return None
        sympy_values.append(expr)
    return sympy_values  # list (will be compared as a set)


def _sympy_values_equal(a, b) -> bool:
    """
    Return True if two SymPy expressions are mathematically equal.
    Uses simplify(a - b) == 0 with numeric fallback.
    """
    try:
        diff = simplify(a - b)
        if diff == 0:
            return True
    except Exception:
        pass

    try:
        va = complex(N(a))
        vb = complex(N(b))
        if abs(va - vb) < 1e-6:
            return True
    except Exception:
        pass

    return False


def _compare_solution_sets(student_values: list, correct_values: list) -> bool:
    """
    Compare two lists of SymPy expressions as sets.
    Returns True only if the student set exactly matches the correct set
    (same cardinality, each correct value matched by exactly one student value).
    """
    if len(student_values) != len(correct_values):
        logger.info(
            f"  solution set size mismatch: "
            f"student={len(student_values)} correct={len(correct_values)}"
        )
        return False

    # Check that every correct value has a matching student value (and vice versa,
    # implied by equal size + injection).
    correct_unmatched = list(correct_values)
    for sv in student_values:
        matched = False
        for i, cv in enumerate(correct_unmatched):
            if _sympy_values_equal(sv, cv):
                correct_unmatched.pop(i)
                matched = True
                break
        if not matched:
            logger.info(f"  solution set: student value {sv} not in correct set")
            return False

    return True


# ── Main entry point ─────────────────────────────────────────────────────────

def check_answer(student_answer: str, correct_answer: str, answer_type: AnswerType = "symbolic") -> bool:
    """
    Check if a student's answer matches the correct answer.

    Detailed logging is included to help diagnose format mismatches.

    For multiple_choice: case-insensitive string match.
    For numeric: float comparison with tolerance.
    For symbolic: SymPy symbolic equivalence, with LaTeX parsing for MathLive output.
                  Also handles solution sets (multiple comma-separated values).
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

    # ── Solution-set detection ───────────────────────────────────────────────
    # If either the student answer or the correct answer looks like a multi-value
    # solution set (contains commas, "and", or set braces), handle as a set
    # comparison.  A single value against a multi-value correct answer is INCORRECT
    # (partial answers not accepted).

    student_is_multi = _is_multi_value(student)
    correct_is_multi = _is_multi_value(correct)

    if correct_is_multi or student_is_multi:
        logger.info(
            f"  solution set mode: student_multi={student_is_multi}, "
            f"correct_multi={correct_is_multi}"
        )

        # Parse both sides as value sets
        # If correct is multi but student is single, treat student as a 1-element set
        if correct_is_multi and not student_is_multi:
            # Partial answer — student only gave one value
            correct_values = _parse_value_set(correct)
            if correct_values is not None and len(correct_values) > 1:
                # More than one correct value required; single answer is wrong
                logger.info(
                    f"  solution set: student gave single value but "
                    f"{len(correct_values)} required → INCORRECT"
                )
                return False
            # Correct set has only 1 value; fall through to single comparison below

        student_values = _parse_value_set(student) if student_is_multi else None
        correct_values = _parse_value_set(correct) if correct_is_multi else None

        # If student is multi-value
        if student_values is not None:
            if correct_values is not None:
                result = _compare_solution_sets(student_values, correct_values)
                logger.info(f"  solution set comparison: {result}")
                return result
            else:
                # correct is single value; student gave multiple — need exact match of sets
                c_expr = _to_sympy(correct)
                if c_expr is not None:
                    # Student must have given exactly one value equal to correct
                    if len(student_values) == 1 and _sympy_values_equal(student_values[0], c_expr):
                        logger.info("  solution set: student multi (1 val) == correct single")
                        return True
                logger.info("  solution set: student multi != correct single")
                return False

        # correct_is_multi but student is single — we already handled the >1 case above
        # Here correct_values has exactly 1 element
        if correct_values is not None:
            s_expr = _to_sympy(student)
            if s_expr is not None and len(correct_values) == 1:
                result = _sympy_values_equal(s_expr, correct_values[0])
                logger.info(f"  solution set (single correct): {result}")
                return result

        # Fallback: normalized string comparison for sets
        ns = normalize_string(student)
        nc = normalize_string(correct)
        result = ns == nc
        logger.info(f"  solution set string fallback: {ns!r} vs {nc!r} → {result}")
        return result

    # ── Standard single-value symbolic comparison ────────────────────────────
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
