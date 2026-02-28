"""
Standalone test script for answer_checker.py

Run with: cd backend && python tests/test_answer_checker.py

Tests ALL cases required by FIXES-3 Item 1.
"""
import sys
import os

# Make sure the backend/app package is importable when run from the backend/ dir
# or from the project root.
_here = os.path.dirname(os.path.abspath(__file__))
_backend = os.path.join(_here, "..")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

from app.services.answer_checker import check_answer

# ---------------------------------------------------------------------------
# Test case definition
# Each entry: (description, student, correct, expected_result)
# ---------------------------------------------------------------------------
TEST_CASES = [
    # ── Fractions ────────────────────────────────────────────────────────────
    (r'Fraction: student="\frac{5}{6}", correct="5/6"',
     r'\frac{5}{6}', '5/6', True),

    (r'Fraction: student="5/6", correct="\frac{5}{6}"',
     '5/6', r'\frac{5}{6}', True),

    (r'Fraction: student="\frac{1}{2}", correct="1/2"',
     r'\frac{1}{2}', '1/2', True),

    ('Fraction: student="1/2", correct="0.5"',
     '1/2', '0.5', True),

    # ── Exponents ────────────────────────────────────────────────────────────
    ('Exponent: student="x^{12}", correct="x^12"',
     'x^{12}', 'x^12', True),

    ('Exponent: student="x^12", correct="x^{12}"',
     'x^12', 'x^{12}', True),

    # ── Integers ─────────────────────────────────────────────────────────────
    ('Integer: student="20", correct="20"',
     '20', '20', True),

    ('Integer (wrong): student="21", correct="20"',
     '21', '20', False),

    ('Integer (negative): student="-7", correct="-7"',
     '-7', '-7', True),

    # ── Logarithms ───────────────────────────────────────────────────────────
    ('Log: student="3", correct="3"',
     '3', '3', True),

    (r'Log: student="\log_{2}(8)", correct="3"',
     r'\log_{2}(8)', '3', True),

    # ── Solution sets (quadratics) ───────────────────────────────────────────
    ('SolSet: student="2, 3", correct="2, 3"',
     '2, 3', '2, 3', True),

    ('SolSet (order): student="3, 2", correct="2, 3"',
     '3, 2', '2, 3', True),

    ('SolSet (x= prefix): student="x = 2, 3", correct="2, 3"',
     'x = 2, 3', '2, 3', True),

    ('SolSet (x=each): student="x=2, x=3", correct="2, 3"',
     'x=2, x=3', '2, 3', True),

    ('SolSet (braces): student="{2, 3}", correct="2, 3"',
     '{2, 3}', '2, 3', True),

    (r'SolSet (LaTeX braces): student="\{2, 3\}", correct="2, 3"',
     r'\{2, 3\}', '2, 3', True),

    ('SolSet (and separator): student="x=2 and x=3", correct="2, 3"',
     'x=2 and x=3', '2, 3', True),

    ('SolSet (partial - INCORRECT): student="2", correct="2, 3"',
     '2', '2, 3', False),

    ('SolSet (wrong values): student="2, 4", correct="2, 3"',
     '2, 4', '2, 3', False),

    # ── Expressions ──────────────────────────────────────────────────────────
    ('Expr (commutativity): student="2x + 3", correct="3 + 2x"',
     '2x + 3', '3 + 2x', True),

    (r'Expr (frac/var): student="\frac{x}{2}", correct="x/2"',
     r'\frac{x}{2}', 'x/2', True),

    # ── Plain-text sqrt / log ─────────────────────────────────────────────────
    ('Sqrt: student="sqrt(4)", correct="2"',
     'sqrt(4)', '2', True),

    ('Log2: student="log2(8)", correct="3"',
     'log2(8)', '3', True),
]


def run_tests():
    passed = 0
    failed = 0
    failures = []

    print("=" * 70)
    print("Answer Checker Test Suite")
    print("=" * 70)

    for desc, student, correct, expected in TEST_CASES:
        result = check_answer(student, correct, "symbolic")
        ok = (result == expected)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {desc}")
        if not ok:
            print(f"       student={student!r}  correct={correct!r}")
            print(f"       expected={expected}  got={result}")
            failures.append(desc)
            failed += 1
        else:
            passed += 1

    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)} total")
    if failures:
        print("\nFAILED cases:")
        for f in failures:
            print(f"  - {f}")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
