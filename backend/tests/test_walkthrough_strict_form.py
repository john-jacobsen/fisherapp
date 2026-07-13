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
from app.services.walkthrough_conditions import evaluate_condition, ConditionError
from app.services.walkthrough_generators.eq_one_step import generate as eq_generate
from app.services.walkthrough_generators.frac_simplify import generate as frac_generate
from app.services.walkthrough_generators.calc_deriv_power import generate as calc_deriv_power_generate
from app.services.walkthrough_generators.linalg_row_reduce import generate as rr_generate
from app.services.walkthrough_generators.prob_bayes import generate as bayes_generate
from app.services.walkthrough_generators.stat_ci_z import generate as stat_ci_z_generate
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

    # Non-fraction input — allowlist logic REJECTS anything that isn't a
    # fraction, so a decimal equal to the correct value can't bypass the form.
    ok, _ = sf("simplified_fraction", "0.75")
    check("0.75 (decimal) → reject (allowlist)", ok, False)

    ok, _ = sf("simplified_fraction", "3")
    check("plain integer 3 → reject (not a fraction)", ok, False)

    # Trailing garbage must not slip through the anchored pattern
    ok, _ = sf("simplified_fraction", "3/4 + 0")
    check("3/4 + 0 (trailing garbage) → reject", ok, False)

    # Verify rejection message is returned
    _, fb = sf("simplified_fraction", "6/8", rejection="Not simplified!")
    check("rejection_feedback is returned", fb, "Not simplified!")


def test_simplified_fraction_rejects_decimal():
    ok, _ = _check_strict_form("0.75", {"type": "simplified_fraction",
                                        "rejection_feedback": "r"})
    check("0.75 decimal rejected", ok, False)


def test_simplified_fraction_rejects_unparseable():
    for bad in ["3/4 + 0", "three fourths", "0.5", "1.0", ".5"]:
        ok, _ = _check_strict_form(bad, {"type": "simplified_fraction",
                                         "rejection_feedback": "r"})
        check(f"{bad!r} rejected", ok, False)


def test_simplified_fraction_accepts_valid():
    for good in ["3/4", "-3/4", r"\frac{3}{4}", r"\frac{-3}{4}"]:
        ok, _ = _check_strict_form(good, {"type": "simplified_fraction",
                                          "rejection_feedback": "r"})
        check(f"{good!r} accepted", ok, True)


def test_exact_form_rejects_scientific():
    for bad in ["1.5e3", "2E4", "3e-2", "1.0e10"]:
        ok, _ = _check_strict_form(bad, {"type": "exact_form",
                                         "rejection_feedback": "r"})
        check(f"{bad!r} (sci-notation/decimal) rejected", ok, False)
    for good in ["5", "-4", "1/2", r"\sqrt{2}", "42"]:
        ok, _ = _check_strict_form(good, {"type": "exact_form",
                                          "rejection_feedback": "r"})
        check(f"{good!r} accepted", ok, True)


def test_log_form_token_boundary():
    # log/ln must appear as a token, not buried in a variable name
    ok, _ = _check_strict_form("balloon", {"type": "log_form", "rejection_feedback": "r"})
    check("'balloon' (contains 'ln'? no) → reject", ok, False)
    ok, _ = _check_strict_form("salon + 3", {"type": "log_form", "rejection_feedback": "r"})
    check("'salon' (substring 'lo' not log) → reject", ok, False)
    for good in [r"\log_3(20)", "log(20)/log(3)", "ln(x)", r"\ln x"]:
        ok, _ = _check_strict_form(good, {"type": "log_form", "rejection_feedback": "r"})
        check(f"{good!r} accepted", ok, True)


def test_custom_regex_bad_pattern_no_500():
    # An invalid regex pattern must not raise — accept rather than crash
    ok, fb = _check_strict_form("anything", {"type": "custom_regex",
                                             "pattern": "([unbalanced",
                                             "rejection_feedback": "r"})
    check("bad regex pattern → accept (no exception)", ok, True)


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

    for node_id in ('frac-simplify', 'eq-one-step', 'calc-deriv-power', 'linalg-row-reduce', 'prob-bayes', 'stat-ci-z'):
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


# ── calc-deriv-power generator ────────────────────────────────────────────────

def test_calc_deriv_power_generator():
    print("\n[calc-deriv-power generator]")

    required_keys = {'a', 'n', 'new_coeff', 'new_exp', 'abs_a', 'abs_new_coeff',
                     'display_original', 'display_derivative'}
    valid_a = set(range(-8, 9)) - {0, 1, -1}

    for i in range(20):
        v = calc_deriv_power_generate()
        missing = required_keys - set(v.keys())
        check(f"Run {i+1}: all required keys present", missing, set())

        a, n = v['a'], v['n']
        check(f"Run {i+1}: a in valid range (not 0, ±1)", a in valid_a, True)
        check(f"Run {i+1}: n in [2, 7]", 2 <= n <= 7, True)
        check(f"Run {i+1}: new_coeff = a * n", v['new_coeff'], a * n)
        check(f"Run {i+1}: new_exp = n - 1", v['new_exp'], n - 1)
        check(f"Run {i+1}: abs_a = abs(a)", v['abs_a'], abs(a))
        check(f"Run {i+1}: abs_new_coeff = abs(new_coeff)", v['abs_new_coeff'], abs(a * n))

        # display_derivative must not contain '^1' (new_exp==1 case uses plain 'x')
        deriv = v['display_derivative']
        if v['new_exp'] == 1:
            check(f"Run {i+1}: display_derivative has no ^1 when new_exp==1",
                  '^1' not in deriv, True)
            check(f"Run {i+1}: display_derivative ends with 'x' when new_exp==1",
                  deriv.endswith('x'), True)
        else:
            check(f"Run {i+1}: display_derivative contains 'x^' when new_exp>1",
                  'x^' in deriv, True)

        # display_original must always show the coefficient (a is never ±1)
        orig = v['display_original']
        check(f"Run {i+1}: display_original contains str(a)",
              str(a) in orig, True)


# ── calc-deriv-power MC distinctness (100 runs) ────────────────────────────────

def test_calc_deriv_power_mc_distinctness():
    print("\n[calc-deriv-power MC distinctness — 100 runs]")

    for i in range(100):
        v = calc_deriv_power_generate()
        a, n, new_coeff, new_exp = v['a'], v['n'], v['new_coeff'], v['new_exp']

        # Primary guard: a != n prevents the most common Step 1 duplicate
        check(f"Run {i+1}: a != n ({a} != {n})", a != n, True)

        # Full guard: all four MC option values must be distinct
        four = {n, a, new_coeff, new_exp}
        check(f"Run {i+1}: all four MC values distinct (n={n}, a={a}, new_coeff={new_coeff}, new_exp={new_exp})",
              len(four), 4)


# ── calc-deriv-power step-4 strict_form rejects decimals ──────────────────────

def test_calc_deriv_power_exact_form():
    print("\n[calc-deriv-power step 4 exact_form rejects decimals]")

    ok, _ = sf("exact_form", "15x^{2}")
    check("15x^{2} (integer coeff) → accept", ok, True)

    ok, _ = sf("exact_form", "-12x^{3}")
    check("-12x^{3} → accept", ok, True)

    ok, _ = sf("exact_form", "4x")
    check("4x (new_exp==1) → accept", ok, True)

    ok, fb = sf("exact_form", "15.0x^{2}", rejection="No decimals allowed.")
    check("15.0x^{2} (decimal) → reject", ok, False)
    check("rejection feedback returned", fb, "No decimals allowed.")

    ok, _ = sf("exact_form", "14.999x^{2}")
    check("14.999x^{2} (decimal) → reject", ok, False)


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


# ── linalg-row-reduce generator (50 runs) ────────────────────────────────────

def test_linalg_row_reduce_generator():
    print("\n[linalg-row-reduce generator — 50 runs]")

    required_keys = {
        'a1', 'b1', 'c1', 'a2', 'b2', 'c2',
        'multiplier', 'new_b2', 'new_c2', 'x_sol', 'y_sol', 'abs_multiplier',
    }

    for i in range(50):
        v = rr_generate()

        missing = required_keys - set(v.keys())
        check(f"Run {i+1}: all required keys present", missing, set())

        a1, b1, c1 = v['a1'], v['b1'], v['c1']
        a2, b2, c2 = v['a2'], v['b2'], v['c2']
        multiplier = v['multiplier']
        new_b2, new_c2 = v['new_b2'], v['new_c2']
        x_sol, y_sol = v['x_sol'], v['y_sol']

        # a1 divides a2 (multiplier is an integer)
        check(f"Run {i+1}: a1 divides a2", a2 % a1, 0)
        check(f"Run {i+1}: multiplier == a2/a1", multiplier, a2 // a1)

        # All main coefficients nonzero and in range
        for name, val in [('a1', a1), ('b1', b1), ('a2', a2), ('b2', b2)]:
            check(f"Run {i+1}: {name} != 0", val != 0, True)
            check(f"Run {i+1}: {name} in [-6,6]", -6 <= val <= 6, True)

        # Derived values correct
        check(f"Run {i+1}: new_b2 == b2 - mult*b1", new_b2, b2 - multiplier * b1)
        check(f"Run {i+1}: new_c2 == c2 - mult*c1", new_c2, c2 - multiplier * c1)

        # new_b2 != 0 (unique solution guarantee)
        check(f"Run {i+1}: new_b2 != 0", new_b2 != 0, True)

        # Arithmetic consistency: new_c2 == new_b2 * y_sol
        check(f"Run {i+1}: new_c2 == new_b2 * y_sol", new_c2, new_b2 * y_sol)

        # Back-substitution works
        check(f"Run {i+1}: y_sol == new_c2 / new_b2", y_sol, new_c2 // new_b2)
        check(f"Run {i+1}: x_sol back-sub", x_sol, (c1 - b1 * y_sol) // a1)

        # Solutions in range
        check(f"Run {i+1}: x_sol in [-5,5]", -5 <= x_sol <= 5, True)
        check(f"Run {i+1}: y_sol in [-5,5]", -5 <= y_sol <= 5, True)

        # Unique solution: det = a1*(b2 - mult*b1) = a1*new_b2 != 0
        det = a1 * b2 - a2 * b1
        check(f"Run {i+1}: determinant != 0", det != 0, True)

        # Step 2 MC options distinct: {multiplier, a2, a1} all different
        check(f"Run {i+1}: MC option values distinct",
              len({multiplier, a2, a1}), 3)

        # abs_multiplier correct
        check(f"Run {i+1}: abs_multiplier == abs(multiplier)",
              v['abs_multiplier'], abs(multiplier))


# ── linalg-row-reduce check-step (numeric + MC) ───────────────────────────────

def test_linalg_row_reduce_check_steps():
    print("\n[linalg-row-reduce check-step — numeric and MC correctness]")

    # Use the fallback problem: 2x+3y=8, 4x+y=6
    v = rr_generate.__wrapped__() if hasattr(rr_generate, '__wrapped__') else None

    # Generate until we get the fallback-like values or just use a fresh sample
    v = rr_generate()

    mult = v['multiplier']
    new_b2, new_c2 = v['new_b2'], v['new_c2']
    x_sol, y_sol = v['x_sol'], v['y_sol']
    a1, a2 = v['a1'], v['a2']

    # Step 2 — multiple_choice: correct answer is index 0 (multiplier)
    ok = _check_answer("0", "0", "multiple_choice")
    check("Step 2 MC: answer index 0 == correct 0", ok, True)

    ok = _check_answer("1", "0", "multiple_choice")
    check("Step 2 MC: answer index 1 != correct 0", ok, False)

    # Step 3 — numeric: new_b2
    ok = _check_answer(str(new_b2), str(new_b2), "numeric")
    check("Step 3 numeric: correct new_b2 accepted", ok, True)

    ok = _check_answer(str(new_b2 + 1), str(new_b2), "numeric")
    check("Step 3 numeric: wrong value rejected", ok, False)

    # Step 4 — numeric: new_c2
    ok = _check_answer(str(new_c2), str(new_c2), "numeric")
    check("Step 4 numeric: correct new_c2 accepted", ok, True)

    # Step 5 — numeric: y_sol
    ok = _check_answer(str(y_sol), str(y_sol), "numeric")
    check("Step 5 numeric: correct y_sol accepted", ok, True)

    ok = _check_answer(str(y_sol + 1 if y_sol != 5 else y_sol - 1), str(y_sol), "numeric")
    check("Step 5 numeric: wrong y rejected", ok, False)

    # Step 6 — numeric: x_sol
    ok = _check_answer(str(x_sol), str(x_sol), "numeric")
    check("Step 6 numeric: correct x_sol accepted", ok, True)

    # Step 7 — multiple_choice: correct is index 0
    ok = _check_answer("0", "0", "multiple_choice")
    check("Step 7 MC: answer 0 == correct 0", ok, True)

    ok = _check_answer("2", "0", "multiple_choice")
    check("Step 7 MC: answer 2 != correct 0", ok, False)


# ── prob-bayes generator (30 runs) ────────────────────────────────────────────

def test_prob_bayes_generator():
    print("\n[prob-bayes generator — 30 runs]")

    required_keys = {
        'prev_num', 'prev_den', 'sensitivity', 'specificity', 'false_pos_rate',
        'population', 'num_diseased', 'num_healthy', 'true_positives',
        'false_positives', 'total_positives', 'ppv_percent',
        'ppv_fraction_num', 'ppv_fraction_den',
    }

    for i in range(30):
        v = bayes_generate()

        missing = required_keys - set(v.keys())
        check(f"Run {i+1}: all required keys present", missing, set())

        pop = v['population']
        nd = v['num_diseased']
        nh = v['num_healthy']
        tp = v['true_positives']
        fp = v['false_positives']
        tot = v['total_positives']
        sens = v['sensitivity']
        fpr = v['false_pos_rate']
        ppv = v['ppv_percent']
        pn = v['ppv_fraction_num']
        pd_ = v['ppv_fraction_den']

        # Whole-number counts
        check(f"Run {i+1}: num_diseased is int", nd, int(nd))
        check(f"Run {i+1}: num_healthy is int", nh, int(nh))
        check(f"Run {i+1}: true_positives is int", tp, int(tp))
        check(f"Run {i+1}: false_positives is int", fp, int(fp))
        check(f"Run {i+1}: total_positives is int", tot, int(tot))

        # Partition consistency
        check(f"Run {i+1}: num_diseased + num_healthy == population", nd + nh, pop)
        check(f"Run {i+1}: true_positives + false_positives == total_positives", tp + fp, tot)

        # Derivation consistency
        check(f"Run {i+1}: false_pos_rate == 100 - specificity",
              fpr, 100 - v['specificity'])
        check(f"Run {i+1}: true_positives == num_diseased * sensitivity / 100",
              tp, nd * sens // 100)
        check(f"Run {i+1}: false_positives == num_healthy * fpr / 100",
              fp, nh * fpr // 100)

        # PPV bounds: strictly between 0 and 100
        check(f"Run {i+1}: ppv_percent > 0", ppv > 0, True)
        check(f"Run {i+1}: ppv_percent < 100", ppv < 100, True)

        # PPV fraction is in lowest terms (GCD == 1)
        from math import gcd as _gcd2
        check(f"Run {i+1}: ppv fraction in lowest terms", _gcd2(pn, pd_), 1)

        # PPV fraction matches ppv_percent (within 0.05 of a percentage point)
        ppv_from_frac = round(pn * 100 / pd_, 1)
        check(f"Run {i+1}: ppv_fraction consistent with ppv_percent",
              abs(ppv_from_frac - ppv) <= 0.05, True)


# ── prob-bayes check-step (numeric + MC) ──────────────────────────────────────

def test_prob_bayes_check_steps():
    print("\n[prob-bayes check-step — numeric and MC correctness]")

    v = bayes_generate()

    nd = v['num_diseased']
    nh = v['num_healthy']
    tp = v['true_positives']
    fp = v['false_positives']
    tot = v['total_positives']
    ppv = v['ppv_percent']

    # Steps 1-5: numeric
    ok = _check_answer(str(nd), str(nd), "numeric")
    check("Step 1 numeric: correct num_diseased accepted", ok, True)

    ok = _check_answer(str(nd + 1), str(nd), "numeric")
    check("Step 1 numeric: wrong value rejected", ok, False)

    ok = _check_answer(str(nh), str(nh), "numeric")
    check("Step 2 numeric: correct num_healthy accepted", ok, True)

    ok = _check_answer(str(tp), str(tp), "numeric")
    check("Step 3 numeric: correct true_positives accepted", ok, True)

    ok = _check_answer(str(fp), str(fp), "numeric")
    check("Step 4 numeric: correct false_positives accepted", ok, True)

    ok = _check_answer(str(tot), str(tot), "numeric")
    check("Step 5 numeric: correct total_positives accepted", ok, True)

    # Step 6: numeric with 1 decimal — ppv_percent
    ok = _check_answer(str(ppv), str(ppv), "numeric")
    check("Step 6 numeric: correct ppv_percent accepted", ok, True)

    # A clearly wrong percentage (0%) is rejected
    ok = _check_answer("0", str(ppv), "numeric")
    check("Step 6 numeric: 0 rejected when ppv != 0", ok, ppv <= 0.01)

    # Step 7: multiple_choice
    ok = _check_answer("0", "0", "multiple_choice")
    check("Step 7 MC: answer 0 == correct 0", ok, True)

    ok = _check_answer("1", "0", "multiple_choice")
    check("Step 7 MC: answer 1 != correct 0", ok, False)

    ok = _check_answer("2", "0", "multiple_choice")
    check("Step 7 MC: answer 2 != correct 0", ok, False)


# ── stat-ci-z generator (30 runs) ────────────────────────────────────────────

def test_stat_ci_z_generator():
    print("\n[stat-ci-z generator — 30 runs]")

    required_keys = {
        'xbar', 'sigma', 'n', 'sqrt_n', 'conf_level', 'z_star', 'z_star_index',
        'standard_error', 'margin_of_error', 'lower', 'upper', 'alpha', 'alpha_half',
    }
    z_stars = {90: 1.645, 95: 1.96, 99: 2.576}
    z_star_indices = {90: 0, 95: 1, 99: 2}
    valid_n = {36, 49, 64, 100, 144, 225, 400}

    for i in range(30):
        v = stat_ci_z_generate()

        missing = required_keys - set(v.keys())
        check(f"Run {i+1}: all required keys present", missing, set())

        xbar = v['xbar']
        sigma = v['sigma']
        n = v['n']
        sqrt_n = v['sqrt_n']
        conf_level = v['conf_level']
        z_star = v['z_star']
        z_star_index = v['z_star_index']
        se = v['standard_error']
        moe = v['margin_of_error']
        lower = v['lower']
        upper = v['upper']
        alpha = v['alpha']
        alpha_half = v['alpha_half']

        check(f"Run {i+1}: n in valid set", n in valid_n, True)
        check(f"Run {i+1}: sqrt_n² == n", sqrt_n * sqrt_n, n)
        check(f"Run {i+1}: sigma % sqrt_n == 0", sigma % sqrt_n, 0)
        check(f"Run {i+1}: standard_error == sigma // sqrt_n", se, sigma // sqrt_n)
        check(f"Run {i+1}: conf_level in {{90, 95, 99}}", conf_level in {90, 95, 99}, True)
        check(f"Run {i+1}: z_star matches conf_level", z_star, z_stars[conf_level])
        check(f"Run {i+1}: z_star_index matches conf_level", z_star_index, z_star_indices[conf_level])

        expected_moe = round(z_star * se, 2)
        check(f"Run {i+1}: margin_of_error within 0.01 of z_star*se",
              abs(moe - expected_moe) <= 0.01, True)

        moe_str = str(moe)
        dp = len(moe_str.split('.')[-1]) if '.' in moe_str else 0
        check(f"Run {i+1}: margin_of_error has at most 2 decimal places", dp <= 2, True)

        check(f"Run {i+1}: lower > 0", lower > 0, True)
        check(f"Run {i+1}: lower == xbar - moe",
              abs(lower - (xbar - moe)) <= 0.001, True)
        check(f"Run {i+1}: upper == xbar + moe",
              abs(upper - (xbar + moe)) <= 0.001, True)

        check(f"Run {i+1}: alpha == 100 - conf_level", alpha, 100 - conf_level)
        check(f"Run {i+1}: alpha_half == alpha / 2", alpha_half, alpha / 2)


# ── stat-ci-z check-step (numeric + MC) ──────────────────────────────────────

def test_stat_ci_z_check_steps():
    print("\n[stat-ci-z check-step — numeric and MC correctness]")

    v = stat_ci_z_generate()
    z_star_index = v['z_star_index']
    sqrt_n = v['sqrt_n']
    se = v['standard_error']
    moe = v['margin_of_error']
    lower = v['lower']
    upper = v['upper']

    # Step 1 — multiple_choice: correct is z_star_index
    ok = _check_answer(str(z_star_index), str(z_star_index), "multiple_choice")
    check("Step 1 MC: correct z_star_index accepted", ok, True)

    wrong_idx = (z_star_index + 1) % 3
    ok = _check_answer(str(wrong_idx), str(z_star_index), "multiple_choice")
    check("Step 1 MC: wrong index rejected", ok, False)

    # Step 2 — numeric: sqrt_n
    ok = _check_answer(str(sqrt_n), str(sqrt_n), "numeric")
    check("Step 2 numeric: correct sqrt_n accepted", ok, True)

    ok = _check_answer(str(sqrt_n + 1), str(sqrt_n), "numeric")
    check("Step 2 numeric: wrong value rejected", ok, False)

    # Step 3 — numeric: standard_error
    ok = _check_answer(str(se), str(se), "numeric")
    check("Step 3 numeric: correct standard_error accepted", ok, True)

    ok = _check_answer(str(se + 1), str(se), "numeric")
    check("Step 3 numeric: wrong value rejected", ok, False)

    # Step 4 — numeric: margin_of_error with 0.01 tolerance
    ok = _check_answer(str(moe), str(moe), "numeric")
    check("Step 4 numeric: exact moe accepted", ok, True)

    within = str(round(moe + 0.005, 3))
    ok = _check_answer(within, str(moe), "numeric")
    check("Step 4 numeric: answer within 0.01 accepted (moe+0.005)", ok, True)

    outside = str(round(moe + 0.02, 3))
    ok = _check_answer(outside, str(moe), "numeric")
    check("Step 4 numeric: answer outside 0.01 rejected (moe+0.02)", ok, False)

    # Step 5 — numeric: lower (upper is always far outside 0.01 tolerance)
    ok = _check_answer(str(lower), str(lower), "numeric")
    check("Step 5 numeric: correct lower accepted", ok, True)

    ok = _check_answer(str(upper), str(lower), "numeric")
    check("Step 5 numeric: upper rejected as lower bound", ok, False)

    # Step 6 — numeric: upper
    ok = _check_answer(str(upper), str(upper), "numeric")
    check("Step 6 numeric: correct upper accepted", ok, True)

    ok = _check_answer(str(lower), str(upper), "numeric")
    check("Step 6 numeric: lower rejected as upper bound", ok, False)

    # Step 7 — multiple_choice: correct is always 0
    ok = _check_answer("0", "0", "multiple_choice")
    check("Step 7 MC: answer 0 == correct 0", ok, True)

    ok = _check_answer("1", "0", "multiple_choice")
    check("Step 7 MC: answer 1 != correct 0", ok, False)

    ok = _check_answer("2", "0", "multiple_choice")
    check("Step 7 MC: answer 2 != correct 0", ok, False)


# ── Condition evaluator security (Item 4) ─────────────────────────────────────

def test_condition_evaluator_rejects_malicious():
    print("\n[condition evaluator — malicious input rejected, no execution]")

    import os as _os
    sentinel = os.path.join(_here, "_condition_pwned.txt")
    if os.path.exists(sentinel):
        os.remove(sentinel)

    malicious = [
        "__import__('os').system('ls')",
        "open('/etc/passwd')",
        "answer.__class__",
        "[x for x in range(9**9)]",
        f"__import__('os').system('echo x > {sentinel}')",
        "(1).__class__.__bases__",
        "answer if answer else 0",
    ]
    for expr in malicious:
        # evaluate_condition must raise ConditionError (never execute)
        raised = False
        try:
            evaluate_condition(expr, "6", {"numerator": 12, "denominator": 18})
        except ConditionError:
            raised = True
        check(f"evaluate_condition rejects {expr!r}", raised, True)

        # _eval_condition must return False (safe fallback), not blow up
        result = _eval_condition(expr, "6", {"numerator": 12, "denominator": 18})
        check(f"_eval_condition({expr!r}) → False", result, False)

    check("no side-effect file was created", os.path.exists(sentinel), False)


def test_condition_evaluator_valid_expressions():
    print("\n[condition evaluator — valid expressions]")

    v = {"numerator": 12, "denominator": 18, "gcf": 6}
    check("answer == 1 with answer=1", evaluate_condition("answer == 1", "1", v), True)
    check("answer == 1 with answer=2", evaluate_condition("answer == 1", "2", v), False)
    check("answer == numerator", evaluate_condition("answer == numerator", "12", v), True)
    check("divides num not den (answer=4)",
          evaluate_condition("answer_int is not None and answer_int > 1 and numerator % answer_int == 0 and denominator % answer_int != 0", "4", v),
          True)
    check("divides both not greatest (answer=2 < gcf 6)",
          evaluate_condition("answer_int is not None and answer_int > 1 and numerator % answer_int == 0 and denominator % answer_int == 0 and answer_int < gcf", "2", v),
          True)
    check("divides both not greatest (answer=6 == gcf, not <)",
          evaluate_condition("answer_int is not None and answer_int > 1 and numerator % answer_int == 0 and denominator % answer_int == 0 and answer_int < gcf", "6", v),
          False)
    # Non-numeric answer → answer_int is None → guarded expression is False
    check("non-numeric answer guarded",
          evaluate_condition("answer_int is not None and numerator % answer_int == 0", "abc", v),
          False)


def test_condition_migration_equivalence():
    print("\n[condition migration — new expressions match legacy behavior]")

    # Legacy reference implementation of the three frac-simplify "divides" rules
    def legacy(cond_kind, ans, num, den, gcf):
        try:
            f = float(ans); ai = int(f) if f == int(f) else None
        except ValueError:
            ai = None
        if cond_kind == "num_not_den":
            return bool(ai and ai > 1 and num % ai == 0 and den % ai != 0)
        if cond_kind == "den_not_num":
            return bool(ai and ai > 1 and den % ai == 0 and num % ai != 0)
        if cond_kind == "both_not_greatest":
            return bool(ai and ai > 1 and num % ai == 0 and den % ai == 0 and ai < gcf)
        return False

    exprs = {
        "num_not_den": "answer_int is not None and answer_int > 1 and numerator % answer_int == 0 and denominator % answer_int != 0",
        "den_not_num": "answer_int is not None and answer_int > 1 and denominator % answer_int == 0 and numerator % answer_int != 0",
        "both_not_greatest": "answer_int is not None and answer_int > 1 and numerator % answer_int == 0 and denominator % answer_int == 0 and answer_int < gcf",
    }

    num, den, gcf = 12, 18, 6
    v = {"numerator": num, "denominator": den, "gcf": gcf}
    for ans in ["1", "2", "3", "4", "6", "9", "0", "-2", "abc", "12", "18"]:
        for kind, expr in exprs.items():
            new = evaluate_condition(expr, ans, v)
            old = legacy(kind, ans, num, den, gcf)
            check(f"{kind} @ answer={ans!r}: new==legacy ({new})", new, old)


# ── MC option shuffling (Item 3) ──────────────────────────────────────────────

def test_mc_shuffle_varies_position():
    print("\n[MC shuffle — correct conceptual option varies position]")

    positions = []
    translate_ok = True
    for _ in range(20):
        result = generate_walkthrough('frac-simplify')
        # Step 5 is the conceptual multiple_choice step; template correct == 0
        step5 = next(s for s in result['steps'] if s['step_number'] == 5)
        check_type = step5['input_type'] == 'multiple_choice'
        if not check_type:
            continue
        display_correct = int(step5['correct_answer'])
        positions.append(display_correct)

        order = result['variables'].get('_mc_order_5')
        # The order list must translate the displayed-correct index back to the
        # template index 0 (mirrors check_step's translation).
        if not order or order[display_correct] != 0:
            translate_ok = False

    check("correct option appears at >1 distinct position across 20 runs",
          len(set(positions)) > 1, True)
    check("check-step translation maps displayed-correct -> template index 0",
          translate_ok, True)


def test_mc_shuffle_reorders_options_consistently():
    print("\n[MC shuffle — options reordered to match order list]")

    from app.services.walkthrough_generators.frac_simplify import generate as _frac
    # Compare a raw template's option set to the hydrated (shuffled) one: same
    # multiset of options, order key present, and displayed correct option text
    # is the known correct concept.
    result = generate_walkthrough('frac-simplify')
    step5 = next(s for s in result['steps'] if s['step_number'] == 5)
    order = result['variables'].get('_mc_order_5')
    check("order list present for step 5", order is not None, True)
    check("order is a permutation of range(len(options))",
          sorted(order), list(range(len(step5['options']))))
    # Displayed correct option must be the "dividing by 1" concept (contains "1")
    displayed_correct = step5['options'][int(step5['correct_answer'])]
    check("displayed correct option is the equivalence concept",
          'dividing by 1' in displayed_correct or "doesn't change the value" in displayed_correct,
          True)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_simplified_fraction()
    test_simplified_fraction_rejects_decimal()
    test_simplified_fraction_rejects_unparseable()
    test_simplified_fraction_accepts_valid()
    test_exact_form_rejects_scientific()
    test_log_form_token_boundary()
    test_custom_regex_bad_pattern_no_500()
    test_log_form()
    test_factored_form()
    test_expanded_form()
    test_exact_form()
    test_custom_regex()
    test_mc_shuffle_varies_position()
    test_mc_shuffle_reorders_options_consistently()
    test_expression_normalization()
    test_eq_generator()
    test_frac_generator()
    test_calc_deriv_power_generator()
    test_calc_deriv_power_mc_distinctness()
    test_calc_deriv_power_exact_form()
    test_hydration()
    test_eval_condition_variable_lookup()
    test_condition_evaluator_rejects_malicious()
    test_condition_evaluator_valid_expressions()
    test_condition_migration_equivalence()
    test_linalg_row_reduce_generator()
    test_linalg_row_reduce_check_steps()
    test_prob_bayes_generator()
    test_prob_bayes_check_steps()
    test_stat_ci_z_generator()
    test_stat_ci_z_check_steps()

    print()
    if _failures:
        print(f"\033[91m{len(_failures)} FAILURE(S):\033[0m")
        for f in _failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("\033[92mAll tests passed.\033[0m")
