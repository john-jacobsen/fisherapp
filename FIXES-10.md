# FIXES-10: Problem Generator Diversity

**Date:** 2026-03-16
**Scope:** All 176 generators in `backend/app/services/problem_generator.py` and `backend/app/services/generators/*.py`

---

## Problem

148 of 176 generators produce only 1–2 unique problem structures. Only the random numbers change between calls — the form of the question never varies. Students quickly recognize the pattern and learn to solve the template rather than the concept.

## Goal

Every generator should produce at least 3 structurally distinct problem variants. "Structurally distinct" means the problem asks a different question or presents the math in a different arrangement — not just different numbers.

## General Pattern

Each generator function should use `random.choice()` to select from multiple templates. Example transformation:

**Before (single template):**
```python
def _gen_frac_multiply():
    a, b, c, d = ...
    return {
        "problem_text": f"Multiply: \\(\\frac{{{a}}}{{{b}}} \\times \\frac{{{c}}}{{{d}}}\\)",
        "correct_answer": ...,
    }
```

**After (3+ templates):**
```python
def _gen_frac_multiply():
    variant = random.choice(["standard", "whole_times_frac", "mixed_number"])
    if variant == "standard":
        # a/b × c/d
        ...
    elif variant == "whole_times_frac":
        # n × a/b (whole number times fraction)
        ...
    elif variant == "mixed_number":
        # "What is 2/3 of 12?" (fraction of a whole)
        ...
```

## Constraints

- All answers must remain scalar (numeric or symbolic). No intervals, sets, or matrices.
- All answers must pass through the existing answer checker unchanged.
- All hints must still follow the 3-level structure (conceptual → problem-specific → full solution).
- Difficulty values should vary by variant (easier variants get lower difficulty).
- Run `python tests/test_generators.py` after changes — all 176 must pass.
- Run each modified generator 30 times and verify at least 3 unique structures appear.

## Priority 1: Foundation generators (30 nodes)

These are what students encounter first. Fix all of these.

### eq-fractions (CRITICAL — currently broken)

Currently generates only `ax/a = c` where numerator and denominator are always the same number, making the fraction trivially cancel. Rewrite completely with these templates:

1. `x/a = b` → x = ab (simple fraction)
2. `ax/b = c` where a ≠ b → x = bc/a (non-trivial, ensure integer answer)
3. `(x + a)/b = c` → x = bc - a (fraction with sum in numerator)
4. `a/x = b` → x = a/b (variable in denominator, ensure integer answer)

### eq-one-step

Currently has 2 variants (add/subtract). Add:

3. `ax = b` (multiplication, solve by dividing)
4. `x/a = b` (division, solve by multiplying)

### eq-two-step

Currently single template. Add:

1. `ax + b = c` (standard)
2. `a(x + b) = c` (distribution first)
3. `(x + a)/b = c` (fraction form)
4. `ax - b = c` (subtraction variant)

### eq-distribution

Currently single template. Add:

1. `a(x + b) = c` (standard expand)
2. `a(x + b) + d = c` (expand then combine)
3. `a(x - b) = c(x + d)` (distribution on both sides, solve for x)

### frac-simplify, frac-multiply, frac-divide, frac-add-like, frac-add-unlike, frac-common-denom

Each of these currently has 1 template. For each, add at least 2 more variants:
- Vary whether the answer needs further simplification
- Include word problem variants ("What is 2/3 of 15?")
- Include "which is larger" comparison variants where appropriate

### exp-product, exp-power, exp-negative, exp-combined

Each has 1 template. Add:
- Forward direction (simplify the expression)
- Reverse direction ("what exponent makes this true?")
- Word-problem context where appropriate

### log-definition, log-rules, log-equations

Each has 1 template. Add:
- Multiple problem framings per topic (evaluate, solve, convert)
- `log-rules` should test all rules: product, quotient, power, change of base

### sum-arithmetic, sum-sigma, sum-nested

Each has 1 template. Add:
- Different series lengths
- "Find the sum" vs "find the nth term" vs "how many terms?"

### comb-counting, comb-permutations, comb-combinations

Each has 1 template. Add:
- Different real-world contexts (choosing from items, arranging people, forming committees)
- At least 3 word problem scenarios per generator

### geo-sequences, geo-finite, geo-infinite

Each has 1 template. Add:
- "Find the nth term" vs "find the common ratio" vs "find the sum"

### order-pemdas, order-nested

Add more expression structures — different combinations of operations, different nesting depths.

## Priority 2: Phase 3 generators (146 nodes)

For every Phase 3 generator that currently has ≤ 2 structures, add at least 1 more template so it reaches 3+. The approach for each subject:

### Algebra (12 nodes)
- `alg-factoring-gcf`: vary between `ax + ab`, `ax² + ax`, `abc + abd`
- `alg-rational-expr`: vary the question — "simplify" vs "find undefined values" vs "find the value of x that makes it zero"
- `alg-radical-simplify`: vary radicand complexity
- `alg-systems-elim`: add a variant where one variable already has matching coefficients

### Calculus (20 nodes)
- Derivative generators: vary the function type (polynomial, trig, exponential, composition)
- Integration generators: vary between definite and indefinite, different function families
- `calc-series-conv`: test different series types (geometric, p-series, ratio test)

### Linear Algebra (21 nodes)
- Matrix generators: vary dimensions (2×2, 3×3 where tractable)
- `linalg-eigenvalues`: vary between "find eigenvalues" and "verify this is an eigenvalue"
- `linalg-determinant`: vary between 2×2 and 3×3

### Probability (39 nodes)
- Distribution generators: vary what's being asked (P(X=k), E[X], Var(X), P(X>k))
- Bayes: vary the real-world context (medical test, manufacturing defect, weather)
- Conditional probability: vary between "find P(A|B)" and "are A and B independent?"

### Statistics (49 nodes)
- Hypothesis test generators: vary between "find the test statistic", "find the p-value", "reject or not?"
- CI generators: vary between "compute the interval", "find the margin of error", "what sample size?"
- Regression generators: vary between "find the slope", "predict y", "interpret the coefficient"

## Verification

After all changes, run:

```bash
docker compose exec backend python tests/test_generators.py
```

All 176 must pass all 3 tiers.

Then run this diversity check:

```bash
docker compose exec backend python -c "
import sys, re
sys.path.insert(0, '.')
from app.services.problem_generator import GENERATORS, generate_problem

low = []
for node in sorted(GENERATORS.keys()):
    structs = set()
    for _ in range(30):
        p = generate_problem(node)
        s = re.sub(r'-?\d+\.?\d*', 'N', p['problem_text'])
        structs.add(s)
    if len(structs) < 3:
        low.append((node, len(structs)))

if low:
    print(f'FAIL: {len(low)} generators still have < 3 structures')
    for n, c in low:
        print(f'  {n}: {c}')
else:
    print('PASS: All 176 generators have 3+ unique structures')
"
```

Every generator must produce at least 3 unique structures across 30 calls.
