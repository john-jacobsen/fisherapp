"""
Tests for the walkthrough system added in the strict_form + generator refactor.

Run from the backend/ directory:
    python tests/test_walkthrough_strict_form.py

Covers:
  - _check_strict_form for all six types (including edge cases)
  - _check_answer expression normalization ("x = N" accepted)
  - eq-one-step generator contract
  - generate_walkthrough hydration (frac-simplify and eq-one-step)
  - No unsubstituted {placeholders} in hydrated output
"""
import sys
import os

_here = os.path.dirname(os.path.abspath(__file__))
_backend = os.path.join(_here, "..")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

from app.routers.walkthrough import _check_strict_form, _check_answer, _eval_condition
from app.services.walkthrough_generators.eq_one_step import generate as eq_generate
from app.services.walkthrough_generators.frac_simplify import generate as frac_generate
from app.services.walkthrough_generator import generate_walkthrough

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"

_failures = []


def check(description: str, result, expected):
    ok = result == expected
    status = PASS if ok else FAIL
    print(f"  [{status}] {description}")
    if not ok:
        print(f"         got={result!r}, expected={expected!r}")
        _failures.append(description)


def sf(form_type, answer, rejection="REJECTED", pattern=None):
    """Build a strict_form dict and call _check_strict_form."""
    d = {"type": form_type, "rejection_feedback": rejection}
    if pattern is not None:
        d["pattern"] = pattern
    return _check_strict_form(answer, d)


# ── simplified_fraction ────────────────────────────────────────────────────────

def test_simplified_fraction():
    print("\n[simplified_fraction]")

    # GCD > 1 → reject
    ok, _ = sf("simplified_fraction", r"\frac{6}{8}")
    check(r"\frac{6}{8} GCD=2 → reject", ok, False)

    ok, _ = sf("simplified_fraction", r"\frac{18}{24}")
    check(r"\frac{18}{24} GCD=6 → reject", ok, False)

    ok, _ = sf("simplified_fraction", "6/8")
    check("6/8 GCD=2 → reject", ok, False)

    ok, _ = sf("simplified_fraction", "18 / 24")
    check("18 / 24 with spaces → reject", ok, False)

    # GCD == 1 → accept
    ok, _ = sf("simplified_fraction", r"\frac{3}{4}")
    check(r"\frac{3}{4} GCD=1 → accept", ok, True)

    ok, _ = sf("simplified_fraction", "3/4")
    check("3/4 GCD=1 → accept", ok, True)

    ok, _ = sf("simplified_fraction", r"\frac{5}{7}")
    check(r"\frac{5}{7} GCD=1 → accept", ok, True)

    # Negative numerators
    ok, _ = sf("simplified_fraction", r"\frac{-3}{4}")
    check(r"\frac{-3}{4} GCD=1 → accept", ok, True)

    ok, _ = sf("simplified_fraction", r"\frac{-6}{8}")
    check(r"\frac{-6}{8} GCD=2 → reject", ok, False)

    # Non-fraction input — no regex match, so form passes through
    ok, _ = sf("simplified_fraction", "0.75")
    check("0.75 no fraction structure → accept (math check guards this)", ok, True)

    ok, _ = sf("simplified_fraction", "3")
    check("plain integer 3 → accept (math check guards this)", ok, True)

    # Verify rejection message is returned
    _, fb = sf("simplified_fraction", "6/8", rejection="Not simplified!")
    check("rejection_feedback is returned", fb, "Not simplified!")


# ── log_form ──────────────────────────────────────────────────────────────────

def test_log_form():
    print("\n[log_form]")

    ok, _ = sf("log_form", "4")
    check("plain number 4 → reject", ok, False)

    ok, _ = sf("log_form", "16")
    check("plain number 16 → reject", ok, False)

    ok, _ = sf("log_form", "log2(16)")
    check("log2(16) → accept", ok, True)

    ok, _ = sf("log_form", r"\log_2 16")
    check(r"\log_2 16 → accept", ok, True)

    ok, _ = sf("log_form", r"\log_{2}(16)")
    check(r"\log_{2}(16) → accept", ok, True)

    ok, _ = sf("log_form", "ln(x)")
    check("ln(x) → accept", ok, True)

    ok, _ = sf("log_form", r"\ln x")
    check(r"\ln x → accept", ok, True)

    ok, _ = sf("log_form", "2.something_else")
    check("string with no log → reject", ok, False)


# ── factored_form ─────────────────────────────────────────────────────────────

def test_factored_form():
    print("\n[factored_form]")

    ok, _ = sf("factored_form", "(x-3)(x+3)")
    check("(x-3)(x+3) → accept", ok, True)

    ok, _ = sf("factored_form", "2(x-3)(x+3)")
    check("2(x-3)(x+3) → accept", ok, True)

    ok, _ = sf("factored_form", "(x-3) (x+3)")
    check("(x-3) (x+3) with space → accept", ok, True)

    ok, _ = sf("factored_form", "x^2-9")
    check("x^2-9 expanded → reject", ok, False)

    ok, _ = sf("factored_form", "x^2 - 9")
    check("x^2 - 9 with spaces → reject", ok, False)

    ok, _ = sf("factored_form", "x-3")
    check("x-3 (no parens) → reject", ok, False)

    # Single group in parens is not a product of factors
    ok, _ = sf("factored_form", "(x^2-9)")
    check("(x^2-9) single group → reject (no factor structure)", ok, False)


# ── expanded_form ─────────────────────────────────────────────────────────────

def test_expanded_form():
    print("\n[expanded_form]")

    ok, _ = sf("expanded_form", "x^2-9")
    check("x^2-9 → accept", ok, True)

    ok, _ = sf("expanded_form", "x^2 - 9")
    check("x^2 - 9 → accept", ok, True)

    ok, _ = sf("expanded_form", "(x-3)(x+3)")
    check("(x-3)(x+3) factored → reject", ok, False)

    ok, _ = sf("expanded_form", "2(x-3)(x+3)")
    check("2(x-3)(x+3) → reject", ok, False)

    # Single paren group without factor multiplication structure — allowed
    ok, _ = sf("expanded_form", "(x^2-9)")
    check("(x^2-9) single group → accept", ok, True)


# ── exact_form ────────────────────────────────────────────────────────────────

def test_exact_form():
    print("\n[exact_form]")

    ok, _ = sf("exact_form", "5")
    check("integer 5 → accept", ok, True)

    ok, _ = sf("exact_form", "-4")
    check("-4 → accept", ok, True)

    ok, _ = sf("exact_form", "5.0")
    check("5.0 decimal → reject", ok, False)

    ok, _ = sf("exact_form", "3.14")
    check("3.14 decimal → reject", ok, False)

    ok, _ = sf("exact_form", "1/2")
    check("1/2 fraction → accept", ok, True)

    ok, _ = sf("exact_form", r"\sqrt{2}")
    check(r"\sqrt{2} → accept", ok, True)

    ok, _ = sf("exact_form", "1.414")
    check("1.414 decimal approximation → reject", ok, False)

    ok, _ = sf("exact_form", "x = 4")
    check("x = 4 → accept", ok, True)

    ok, _ = sf("exact_form", "x = 4.0")
    check("x = 4.0 → reject", ok, False)


# ── custom_regex ──────────────────────────────────────────────────────────────

def test_custom_regex():
    print("\n[custom_regex]")

    ok, _ = sf("custom_regex", "x = 5", pattern=r"x\s*=\s*-?\d+")
    check("x = 5 matches pattern → accept", ok, True)

    ok, _ = sf("custom_regex", "x=-3", pattern=r"x\s*=\s*-?\d+")
    check("x=-3 matches pattern → accept", ok, True)

    ok, _ = sf("custom_regex", "5", pattern=r"x\s*=\s*-?\d+")
    check("bare 5 doesn't match x=N pattern → reject", ok, False)

    ok, _ = sf("custom_regex", "hello", pattern=r"^\d+$")
    check("'hello' doesn't match digits-only → reject", ok, False)

    ok, _ = sf("custom_regex", "42", pattern=r"^\d+$")
    check("'42' matches digits-only → accept", ok, True)


# ── _check_answer expression normalization ────────────────────────────────────

def test_expression_normalization():
    print("\n[_check_answer expression normalization]")

    # "x = 4" should be accepted when correct answer is "4"
    ok = _check_answer("x = 4", "4", "expression")
    check("'x = 4' accepted when correct='4'", ok, True)

    ok = _check_answer("x=4", "4", "expression")
    check("'x=4' (no spaces) accepted when correct='4'", ok, True)

    ok = _check_answer("x = -5", "-5", "expression")
    check("'x = -5' accepted when correct='-5'", ok, True)

    ok = _check_answer("4", "4", "expression")
    check("bare '4' still accepted", ok, True)

    ok = _check_answer("x = 5", "4", "expression")
    check("'x = 5' rejected when correct='4'", ok, False)


# ── eq-one-step generator ─────────────────────────────────────────────────────

def test_eq_generator():
    print("\n[eq-one-step generator]")

    required_keys = {'a', 'b', 'solution', 'abs_a', 'operation_name', 'operation_inverse'}

    for i in range(20):
        v = eq_generate()
        missing = required_keys - set(v.keys())
        check(f"Run {i+1}: all required keys present", missing, set())

        a, b, sol = v['a'], v['b'], v['solution']
        check(f"Run {i+1}: a in valid range", a in range(-12, 13) and a not in (0, 1, -1), True)
        check(f"Run {i+1}: solution non-zero", sol != 0, True)
        check(f"Run {i+1}: b = a * solution", b, a * sol)
        check(f"Run {i+1}: solution in [-10, 10]", -10 <= sol <= 10, True)
        check(f"Run {i+1}: abs_a = abs(a)", v['abs_a'], abs(a))
        check(f"Run {i+1}: operation_name", v['operation_name'], 'multiplication')
        check(f"Run {i+1}: operation_inverse", v['operation_inverse'], 'division')


# ── frac-simplify generator ───────────────────────────────────────────────────

def test_frac_generator():
    print("\n[frac-simplify generator]")
    from math import gcd as _gcd

    for i in range(10):
        v = frac_generate()
        g = _gcd(v['numerator'], v['denominator'])
        check(f"Run {i+1}: gcf matches gcd", v['gcf'], g)
        check(f"Run {i+1}: gcf > 1", g > 1, True)
        check(f"Run {i+1}: simplified_num = num/gcf", v['simplified_num'], v['numerator'] // g)
        check(f"Run {i+1}: simplified_den = den/gcf", v['simplified_den'], v['denominator'] // g)
        check(f"Run {i+1}: simplified_den != 1", v['simplified_den'] != 1, True)


# ── hydration (no remaining placeholders) ─────────────────────────────────────

import re as _re

def _find_placeholders(obj, variable_keys: set) -> list:
    """
    Return list of {key} occurrences where key is a known template variable
    that should have been substituted.  This intentionally ignores LaTeX
    brace groups like \\text{then} or \\frac{x}{...} and runtime-only tokens
    like {answer}.
    """
    found = []
    if isinstance(obj, str):
        for match in _re.finditer(r'\{([a-zA-Z_]\w*)\}', obj):
            if match.group(1) in variable_keys:
                found.append(match.group(0))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(_find_placeholders(item, variable_keys))
    elif isinstance(obj, dict):
        for v in obj.values():
            found.extend(_find_placeholders(v, variable_keys))
    return found


def test_hydration():
    print("\n[hydration — no remaining placeholders]")

    for node_id in ('frac-simplify', 'eq-one-step'):
        result = generate_walkthrough(node_id)
        check(f"{node_id}: generate_walkthrough returns non-None", result is not None, True)
        if result is None:
            continue

        # Only check that template variables (from the generator) were all substituted.
        # LaTeX braces (\\text{GCF}, \\frac{x}{...}) and runtime tokens ({answer})
        # are allowed to remain in the hydrated output.
        variable_keys = set(result.get('variables', {}).keys())
        payload = {k: v for k, v in result.items() if k != 'variables'}
        leftovers = _find_placeholders(payload, variable_keys)
        check(f"{node_id}: no unsubstituted placeholders", leftovers, [])

        check(f"{node_id}: 'variables' key present", 'variables' in result, True)
        check(f"{node_id}: 'steps' key present", 'steps' in result, True)


# ── _eval_condition generic variable lookup ───────────────────────────────────

def test_eval_condition_variable_lookup():
    print("\n[_eval_condition generic variable lookup]")

    variables = {'a': -5, 'solution': -4, 'abs_a': 5}

    ok = _eval_condition("answer == abs_a", "5", variables)
    check("answer == abs_a: '5' matches abs_a=5", ok, True)

    ok = _eval_condition("answer == abs_a", "-4", variables)
    check("answer == abs_a: '-4' doesn't match abs_a=5", ok, False)

    ok = _eval_condition("answer == solution", "-4", variables)
    check("answer == solution: '-4' matches solution=-4", ok, True)

    ok = _eval_condition("answer == -4", "-4", {})
    check("answer == -4 (literal negative): '-4' matches", ok, True)

    ok = _eval_condition("answer == -4", "4", {})
    check("answer == -4 (literal negative): '4' doesn't match", ok, False)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_simplified_fraction()
    test_log_form()
    test_factored_form()
    test_expanded_form()
    test_exact_form()
    test_custom_regex()
    test_expression_normalization()
    test_eq_generator()
    test_frac_generator()
    test_hydration()
    test_eval_condition_variable_lookup()

    print()
    if _failures:
        print(f"\033[91m{len(_failures)} FAILURE(S):\033[0m")
        for f in _failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("\033[92mAll tests passed.\033[0m")
