# FIXES-7: Display Artifacts in Phase 3 Generators

**Date:** 2026-03-11
**Commit:** c59d0de (main)
**Scope:** Cosmetic display bugs in algebra.py and probability.py

---

## Summary

All 176 generators load, run without errors, and return correctly structured output (1,460 calls tested — 10 per new generator). Two classes of cosmetic artifact were found in 8 generators:

- **`+ 0` bug** — zero constant rendered explicitly instead of omitted (3 generators)
- **`1x` bug** — coefficient of 1 rendered as `1x` instead of `x` (6 generators)

No wrong answers. No crashes. No malformed hint structures.

---

## Bug 1: `+ 0` artifact (3 generators)

When a constant/intercept parameter is zero, the f-string renders `+ 0` instead of omitting the term entirely.

### alg-linear-graphs (algebra.py, L23)

**Line:** `b_str = f"+ {b}" if b >= 0 else f"- {abs(b)}"`
**Problem:** `b = random.randint(-5, 5)` — when `b=0`, renders `y = 2x + 0`.
**Fix:** Add a `b=0` branch: `b_str = "" if b == 0 else (f"+ {b}" if b > 0 else f"- {abs(b)}")`.

**Example:** `The line \(y = 2x + 0\) passes through the point...`
**Expected:** `The line \(y = 2x\) passes through the point...`

### alg-systems-sub (algebra.py, L95)

**Line:** `c1_str = f"+ {c1}" if c1 >= 0 else f"- {abs(c1)}"`
**Problem:** `c1 = y - a * x` can be 0. Renders `y = 3x + 0`.
**Fix:** Same pattern — add `c1 == 0` branch that returns `""`.

**Example:** `Solve the system by substitution: \(y = 3x + 0\) and...`
**Expected:** `Solve the system by substitution: \(y = 3x\) and...`

### prob-cdf-method (probability.py, L776–783)

**Line:** `b = random.randint(0, 3)` then f-string `Y = {a}X + {b}`
**Problem:** When `b=0`, renders `Y = 3X + 0`.
**Fix:** Either change range to `random.randint(1, 3)`, or use a conditional format string: `f"Y = {a}X + {b}"` → `f"Y = {a}X" if b == 0 else f"Y = {a}X + {b}"`.

**Example:** `Let \(X \sim \text{Uniform}(0, 1)\) and \(Y = 3X + 0\). Find...`
**Expected:** `Let \(X \sim \text{Uniform}(0, 1)\) and \(Y = 3X\). Find...`

---

## Bug 2: `1x` artifact (6 generators)

When a coefficient is 1, the f-string renders `1x` instead of `x`. The `alg-linear-graphs` generator already handles this correctly with its `m_str` logic — the same pattern should be applied everywhere.

**Shared helper suggestion:** Add to `algebra.py` top:

```python
def _coeff(n, var="x"):
    """Format coefficient for display: 1x→x, -1x→-x, 0x→''."""
    if n == 0:
        return ""
    if n == 1:
        return var
    if n == -1:
        return f"-{var}"
    return f"{n}{var}"
```

### alg-systems-elim (algebra.py, L137–139)

**Line:** `f"\\({a1}x + {b1}y = {c1}\\)"`
**Problem:** `a1, b1, a2, b2` all range 1–3. When any is 1, renders `1x` or `1y`.
**Fix:** Use `_coeff(a1, "x")` and `_coeff(b1, "y")` etc. Also need `+`/`-` handling between terms.

**Example:** `Solve by elimination: \(1x + 1y = 3\) and \(1x + 3y = 5\).`
**Expected:** `Solve by elimination: \(x + y = 3\) and \(x + 3y = 5\).`

### alg-systems-sub (algebra.py, L98)

**Line:** `f"\\({b}x + y = {c2}\\)"`
**Problem:** `b = random.randint(1, 3)`. When `b=1`, renders `1x + y`.
**Fix:** Use `_coeff(b, "x")` or conditional.

**Example:** `... and \(1x + y = 7\). Enter the value of \(x\).`
**Expected:** `... and \(x + y = 7\). Enter the value of \(x\).`

### alg-poly-ops (algebra.py, L201)

**Line:** `f"\\(({a1}x {b1_str}) {op} ({a2}x {b2_str})\\)"`
**Problem:** `a1, a2` range 1–6. When 1, renders `1x`.
**Fix:** Use `_coeff(a1, "x")` and `_coeff(a2, "x")`.

**Example:** `Simplify \((2x - 2) + (1x + 5)\).`
**Expected:** `Simplify \((2x - 2) + (x + 5)\).`

### alg-factoring-quad (algebra.py, L262)

**Line:** `b_str = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")`
**Problem:** When `b=1`, renders `+ 1x`. When `b=-1`, renders `- 1x`.
**Fix:** `b_str = f"+ x" if b == 1 else (f"- x" if b == -1 else ...)`.

**Example:** `Factor \(x^2 - 1x - 6\).`
**Expected:** `Factor \(x^2 - x - 6\).`

### alg-rational-expr (algebra.py, L308)

**Line:** `f"\\(\\frac{{(x - {r})({a}x + {b})}}{{(x - {r})({c}x + {d})}}\\)"`
**Problem:** `a` and `c` range 1–4. When 1, renders `1x`.
**Fix:** Use `_coeff()` for `a` and `c`.

**Example:** `...\(\frac{(x - 5)(3x + 1)}{(x - 5)(1x + 2)}\)...`
**Expected:** `...\(\frac{(x - 5)(3x + 1)}{(x - 5)(x + 2)}\)...`

### alg-radical-equations (algebra.py, L349)

**Line:** `inner = f"{a}x {b_str}"`
**Problem:** `a = random.randint(1, 4)`. When 1, renders `1x`.
**Fix:** Use `_coeff(a, "x")`.

**Example:** `Solve: \(\sqrt{1x - 4} = 2\)`
**Expected:** `Solve: \(\sqrt{x - 4} = 2\)`

---

## Testing protocol

Run after fixes to confirm:

```bash
docker compose exec backend python -c "
from app.services.problem_generator import generate_problem
import re

bug_nodes = [
    'alg-linear-graphs', 'alg-systems-sub', 'alg-systems-elim',
    'alg-poly-ops', 'alg-factoring-quad', 'alg-rational-expr',
    'alg-radical-equations', 'prob-cdf-method',
]

for node in bug_nodes:
    issues = 0
    for _ in range(100):
        p = generate_problem(node)
        text = p['problem_text']
        if '+ 0' in text or '- 0' in text:
            issues += 1
        if re.search(r'(?<![0-9])1x(?![0-9])', text) or '1y' in text:
            issues += 1
    status = 'PASS' if issues == 0 else f'FAIL ({issues}/100)'
    print(f'{node}: {status}')
"
```

Also re-run the full 176-generator smoke test (10 calls each) to confirm no regressions.

---

## Item 2: Write and run `test_generators.py`

After applying the cosmetic fixes above, write `backend/tests/test_generators.py` — a comprehensive automated test suite for all 176 generators. Run it against the live Docker backend. The script should cover three tiers of testing, described below.

### Tier 1: Structural smoke test (all 176 nodes, 10 iterations each)

For every generator, call it 10 times and assert:

1. **Required keys present:** `problem_text`, `correct_answer`, `answer_type`, `difficulty`, `hints`
2. **`answer_type`** is `"numeric"` or `"symbolic"`
3. **`difficulty`** is a float in `[0.0, 1.0]`
4. **`hints`** is a list of exactly 3 dicts, each with `"level"` (1/2/3) and `"text"` (non-empty string)
5. **`correct_answer`** is a non-empty string (and not literally `"None"`)
6. **`problem_text`** is a non-empty string containing at least one `\(` (inline math delimiter)
7. **No display artifacts:** text does not contain `+ 0`, `- 0`, or `1x`/`1y` as bare coefficients. Use this regex for the coefficient check: `re.search(r'(?<![0-9\\])1[xy](?![0-9])', text)`

### Tier 2: Answer checker round-trip (all 176 nodes, 10 iterations each)

This is the highest-value automated test. For each generator call:

1. Generate a problem
2. Feed the generator's own `correct_answer` back into the answer checker (`check_answer` from `app.services.answer_checker`)
3. Assert the checker returns `True` (i.e., the generator's stated answer is accepted by the checker)

This catches format mismatches between generators and the checker — e.g., a generator emitting `"3/4"` when the checker expects `"0.75"`, or a symbolic answer the checker can't parse.

**Expected exceptions:** Some node IDs may use answer formats the checker doesn't fully support (e.g., comma-separated roots like `"-2, 3"` from `alg-factoring-quad`, or dimension strings like `"10x2"` from `stat-slr-matrix`). If a node consistently fails round-trip despite having a correct answer, log it as a known exception rather than a test failure. Collect these into a printed summary at the end.

The call signature for the answer checker should be something like:

```python
from app.services.answer_checker import check_answer
result = check_answer(
    user_answer=p["correct_answer"],
    correct_answer=p["correct_answer"],
    answer_type=p["answer_type"]
)
```

Confirm the actual function signature by reading `answer_checker.py` before writing the test.

### Tier 3: Hint fidelity spot-check (all 176 nodes, 3 iterations each)

For each generator call, check that the hints reference the specific problem instance:

1. **Level 1 hint** should NOT contain any of the specific numeric values from `correct_answer` (it's supposed to be conceptual, no numbers from this problem). This is a soft check — flag but don't fail, since some conceptual hints legitimately mention small integers.
2. **Level 2 and 3 hints** should contain at least one numeric value that also appears in either `problem_text` or `correct_answer`. This confirms the hint was templated with this problem's specific parameters, not a generic static string.

This tier is informational — print a summary of nodes where hints look suspicious, but don't treat them as hard failures.

### Output format

Print a summary like:

```
=== TIER 1: STRUCTURAL (176 nodes × 10) ===
PASS: 176/176
FAIL: 0

=== TIER 2: ANSWER CHECKER ROUND-TRIP (176 nodes × 10) ===
PASS: 174/176
KNOWN EXCEPTIONS: alg-factoring-quad (comma-separated roots), stat-slr-matrix (dimension string)
UNEXPECTED FAILURES: 0

=== TIER 3: HINT FIDELITY (176 nodes × 3) ===
Suspicious nodes (level 1 contains answer values): [list]
Suspicious nodes (level 2-3 missing problem values): [list]

=== OVERALL: PASS ===
```

### Placement and running

Save the test file at `backend/tests/test_generators.py`. Run it inside Docker:

```bash
docker compose exec backend python -m pytest backend/tests/test_generators.py -v --tb=short
```

Or if pytest isn't wired up for this path, just run it directly:

```bash
docker compose exec backend python backend/tests/test_generators.py
```

Write it as a standalone script (with `if __name__ == "__main__"`) so it works either way. Don't add any new dependencies — only use stdlib, sympy (already installed), and the app's own modules.
