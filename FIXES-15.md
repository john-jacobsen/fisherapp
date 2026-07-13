# FIXES-15: Code Review Remediation — Strict Form Hardening, Walkthrough Scaling Prep, Rendering Fixes

**Date:** 2026-07-13
**Scope:** Backend walkthrough system, problem generators, frontend lesson rendering, test infrastructure
**Source:** Full code review of repo at commit `907640d` — all findings verified by running the actual code

---

## READ THIS FIRST — ITEM 1 IS A SAFETY CHECK, DO IT BEFORE ANYTHING ELSE

---

## ITEM 1: Verify and commit uncommitted walkthrough work

**Problem:** The GitHub repo at `907640d` contains only TWO walkthroughs
(`frac-simplify`, `eq-one-step`). The gold-standard walkthroughs for
`calc-deriv-power`, `linalg-row-reduce`, and `prob-bayes` — and possibly
`stat-ci-z` if started — exist only as uncommitted local work.

**Task:**
1. Run `git status` and `git stash list` in the project root.
2. Note: a local FIXES-14.md (dated 2026-06-11) exists but is not on
   GitHub, along with any code changes it produced. Include FIXES-14.md
   and its associated changes in the rescue commit(s), and summarize in
   the final report what FIXES-14 covered and whether it was implemented.
3. If uncommitted walkthrough files exist (JSON templates in
   `backend/data/walkthroughs/`, generators in
   `backend/app/services/walkthrough_generators/`, or related frontend
   changes), commit them FIRST as their own commit with message
   "Add calc-deriv-power, linalg-row-reduce, prob-bayes walkthroughs"
   before making any FIXES-15 changes.
4. Push to main immediately.
5. Report in the final summary exactly which walkthrough files were found
   and committed. If none are found, say so explicitly — that means the
   work was lost and must be flagged to John.

Do NOT mix this commit with the FIXES-15 changes below.

---

## ITEM 2: Close the strict-form bypass (CRITICAL — flagship feature)

**Problem (verified by direct test):** In
`backend/app/routers/walkthrough.py`, `_check_strict_form()` is
permissive-by-default. For `simplified_fraction`:

- `6/8` → correctly rejected ✓
- `\frac{6}{8}` → correctly rejected ✓
- `0.75` → **ACCEPTED** ✗

The checker only rejects input it can parse as a fraction with GCD > 1.
Anything unparseable (decimals, mixed forms) passes. Since `0.75` equals
`3/4` symbolically, the math check passes too, so a student bypasses the
entire "express as a simplified fraction" requirement by typing a decimal.
This violates the core design requirement: mathematically equivalent but
wrong-form answers MUST be rejected with specific feedback.

**Fix — invert the logic to allowlist matching:**

In `_check_strict_form()`, rewrite `simplified_fraction`:

```python
if form_type == "simplified_fraction":
    # The answer MUST match a fraction pattern. Anything else (decimals,
    # bare integers when a fraction is expected, malformed input) is
    # rejected as wrong form. If it matches, GCD must be 1.
    m = re.match(r'^\\frac\{(-?\d+)\}\{(-?\d+)\}$', s)
    if not m:
        m = re.match(r'^(-?\d+)\s*/\s*(-?\d+)$', s)
    if not m:
        return False, rejection          # ← changed: no match = reject
    n, d = int(m.group(1)), int(m.group(2))
    g = gcd(abs(n), abs(d))
    if g > 1:
        return False, rejection
    return True, ""
```

Note the anchored patterns (`^...$`) so trailing garbage doesn't slip
through, and the fall-through now REJECTS instead of allowing.

**Also tighten the other form types:**

- `exact_form`: in addition to rejecting `.`, reject scientific notation
  (`e` or `E` between digits: `re.search(r'\d[eE][+-]?\d', s)`).
- `log_form`: require log/ln as a token, not a substring. Use
  `re.search(r'(\\?(log|ln))\b', s)` so a stray variable name containing
  those letters doesn't pass, and so `\log_3(20)` and `log(20)/log(3)`
  both pass.
- `factored_form` / `expanded_form`: exclude function-call notation from
  the factor heuristic. Before applying `factor_pattern`, strip common
  function heads: `re.sub(r'\\?(sin|cos|tan|log|ln|exp|sqrt|frac)\s*', '', s)`
  so `f(x)`-style or `\sin(x)` input isn't misclassified as a product of
  factors.
- `custom_regex`: wrap `re.search(pattern, s)` in try/except
  `re.error` → on a bad (possibly hydrated) pattern, log a warning and
  return `(True, "")` rather than 500ing the endpoint.

**Add tests** to `backend/tests/test_walkthrough_strict_form.py`:

```python
def test_simplified_fraction_rejects_decimal():
    ok, _ = _check_strict_form("0.75", {"type": "simplified_fraction",
                                        "rejection_feedback": "r"})
    assert ok is False

def test_simplified_fraction_rejects_unparseable():
    for bad in ["3/4 + 0", "three fourths", "0.5", "1.0", ".5"]:
        ok, _ = _check_strict_form(bad, {"type": "simplified_fraction",
                                         "rejection_feedback": "r"})
        assert ok is False, bad

def test_simplified_fraction_accepts_valid():
    for good in ["3/4", "-3/4", r"\frac{3}{4}", r"\frac{-3}{4}"]:
        ok, _ = _check_strict_form(good, {"type": "simplified_fraction",
                                          "rejection_feedback": "r"})
        assert ok is True, good
```

Plus equivalent reject/accept cases for the other tightened types.

**Design note:** rejection feedback for a decimal should be specific.
Where templates supply `rejection_feedback`, review the two pilot
templates and make the message cover the decimal case, e.g. "Your value
is right, but write it as a simplified fraction (like 3/4), not a
decimal."

---

## ITEM 3: Shuffle multiple-choice options during hydration

**Problem (verified):** Option order is fixed in the JSON templates and
neither the backend hydration nor `WalkthroughPage.jsx` shuffles it. In
both pilot walkthroughs the closing conceptual question's correct answer
is index 0 — the first option, every visit. Numbers regenerate each
visit but the click pattern never changes, so students can pass the
conceptual step by position memory.

**Fix — shuffle server-side in `generate_walkthrough()`:**

In `backend/app/services/walkthrough_generator.py`, after hydration and
before returning, for every step with `input_type == "multiple_choice"`:

1. Build `order = list(range(len(options)))`, `random.shuffle(order)`.
2. Reorder `step["options"]` accordingly.
3. Remap `step["correct_answer"]` to the new index of the old correct
   index. Store as string (templates store it as a string like `"0"`).
4. Do NOT expose the original order to the client.

**Problem this creates:** `check_step` re-loads the RAW template, so the
raw `correct_answer` index no longer matches what the client displays.
Solve it statelessly, consistent with the existing variables-passback
design: include the shuffle in the returned payload as
`variables["_mc_order_{step_number}"] = order` (a list of ints). In
`check_step`, when the step is multiple_choice and that key is present
in `body.variables`, translate the student's submitted display-index
back to the template index before comparing:

```python
order = body.variables.get(f"_mc_order_{body.step_number}")
if input_type == "multiple_choice" and order:
    submitted = int(body.answer)
    template_index = order[submitted]
    is_correct = (template_index == int(step["correct_answer"]))
```

Yes, a student could tamper with this via devtools — walkthroughs don't
affect mastery, so stateless is an acceptable tradeoff, same as the
existing variables passback. Add a code comment saying exactly that, so
if walkthrough completion ever gates anything, the comment flags the
need to move state server-side.

**Frontend:** verify `WalkthroughPage.jsx` sends back the full
`variables` object it received (it should already — confirm, don't
assume). Verify the completed-step answer display
(`renderCompletedAnswer`) shows the correct option text after
shuffling.

**Test:** add a test that hydrates `frac-simplify` 20 times and asserts
the conceptual step's correct answer appears at more than one position
across runs, and that check-step returns correct=True when the
translated index is submitted.

---

## ITEM 4: Generalize the wrong-answer feedback condition system

**Problem:** `_eval_condition()` in `walkthrough.py` hardcodes
frac-simplify-specific conditions as literal string matches — e.g.
`"answer divides numerator but not denominator"` is an if-branch in the
router. With 174 walkthroughs to go, every new topic means editing the
router. This must be generalized BEFORE more walkthroughs are written.

**Fix — safe expression evaluation over the variables dict.** Replace
the named-condition branches with a restricted AST evaluator. Create
`backend/app/services/walkthrough_conditions.py`:

```python
"""
Safe evaluation of walkthrough feedback conditions.

Conditions are small Python-like boolean expressions evaluated against:
  answer       — student's answer as float (None if non-numeric)
  answer_int   — as int (None if not a whole number)
  answer_str   — raw stripped string
  plus every key in the walkthrough's variables dict (numeric values).

Examples of valid conditions:
  "answer == 1"
  "answer == numerator"
  "answer_int is not None and numerator % answer_int == 0 and denominator % answer_int != 0"
  "answer_int is not None and answer_int < gcf and numerator % answer_int == 0 and denominator % answer_int == 0"

NEVER use eval()/exec(). Parse with ast.parse(mode='eval') and walk the
tree, allowing ONLY: BoolOp, UnaryOp (Not, USub), Compare (all ops),
BinOp (+ - * / % **), Name, Constant, and the `is`/`is not` comparisons
against None. Reject everything else (calls, attributes, subscripts,
comprehensions, lambdas) by raising ValueError.
"""
```

Implement `evaluate_condition(condition: str, answer: str, variables: dict) -> bool`:
- Build the namespace: parse `answer` to float/int as the current code
  does; merge `variables` (numeric values coerced to int/float).
- Parse with `ast.parse(condition, mode="eval")`, validate every node
  against the allowlist, then evaluate by walking the tree (or compile
  the validated tree — validation makes this safe).
- Any parse/validation/evaluation error → return False (a broken
  condition should never 500 a student's submission; log a warning).

**Migration:**
- Keep `"default"` → True.
- Rewrite the named conditions in the two pilot JSON templates into the
  expression form (e.g. `"answer divides numerator but not denominator"`
  becomes
  `"answer_int is not None and answer_int > 1 and numerator % answer_int == 0 and denominator % answer_int != 0"`).
- For backwards compatibility during migration, `_eval_condition` may
  first try the new evaluator, then fall back to the legacy named
  branches; but the two pilot templates must be fully migrated so new
  walkthroughs never use named conditions.
- The special condition `"answer == original fraction"` (symbolic check)
  becomes a reserved helper: support a `symbolic_equals(latex_string)`
  pseudo-condition OR keep it as one remaining named condition —
  implementer's choice, but document it in walkthrough-schema.md.

**Tests:** malicious inputs must be rejected or return False, never
execute: `"__import__('os').system('ls')"`, `"open('/etc/passwd')"`,
`"answer.__class__"`, `"[x for x in range(9**9)]"`. Add all four as
tests asserting False without side effects.

**Update `walkthrough-schema.md`** to document the condition grammar
with examples, so future walkthrough authoring (human or Claude) uses it.

---

## ITEM 5: Walkthrough validation harness

**Problem:** `_substitute()` silently leaves unresolved `{placeholders}`
if a generator doesn't supply a variable. There is no automated check
that templates and generators agree, that correct answers pass the
checker, or that MC options are unique (duplicate options from parameter
coincidences have happened before). This harness must exist BEFORE
scaling to 174 more walkthroughs.

**Create `backend/scripts/validate_walkthroughs.py`:**

For every `backend/data/walkthroughs/*.json`:

1. **Schema check:** required keys present (`node_id`, `title`, `intro`,
   `steps`; each step has `step_number`, `prompt`, `input_type`,
   `correct_answer`); `step_number`s are sequential from 1;
   `input_type` is one of the four supported values; multiple_choice
   steps have ≥ 2 options and a valid integer `correct_answer` index;
   any `strict_form.type` is one of the six supported types.
2. **Generator exists** in `walkthrough_generators/` and returns a dict.
3. **Hydrate 25 times.** After each hydration:
   - Assert NO unresolved placeholders remain anywhere:
     `re.search(r'\{[a-z_][a-z0-9_]*\}', json.dumps(hydrated))` must be
     None (this pattern avoids false positives on LaTeX braces like
     `\frac{3}{4}` because those contain digits/backslashes, but verify
     against the real templates and tune if needed — the goal is zero
     false negatives on snake_case variable names).
   - For numeric/expression steps: assert the hydrated `correct_answer`
     passes `_check_answer(correct_answer, correct_answer, input_type)`.
   - For steps with `strict_form`: assert the hydrated correct answer
     PASSES its own form check, and assert a known-bad probe FAILS it
     (for simplified_fraction probe with a decimal string of the correct
     value; for exact_form probe with the decimal; for log_form probe
     with a plain number; skip probes for custom_regex).
   - For multiple_choice steps: assert all hydrated option strings are
     unique.
4. Print a per-node PASS/FAIL table and exit nonzero on any failure.

**Also fix the silent-failure root cause:** in
`walkthrough_generator.py`, after substitution, run the same unresolved-
placeholder scan and `raise ValueError(f"Unresolved placeholders in
{node_id}: {found}")`. Better to 500 loudly in dev than serve a student
a prompt containing `{gcf}`.

**Wire into pytest:** add
`backend/tests/test_walkthrough_validation.py` that imports the harness
and runs it over all templates, so it runs with the rest of the suite.

---

## ITEM 6: Fix matrix rendering in lessons (root cause identified)

**Problem:** Matrix rows don't stack in lesson pages. Root cause:
`LessonPage.jsx` renders lessons through `react-markdown` + `remark-gfm`
with math left inline as `$$...$$` text. Markdown escape processing
collapses `\\` to `\` BEFORE any math renderer sees the content, so
`\begin{pmatrix}1&2\\3&4\end{pmatrix}` loses its row separator and
renders as a single row. Ten linalg lessons contain matrix LaTeX
affected by this.

**Fix — use remark-math + rehype-katex:**

```
cd frontend
npm install remark-math rehype-katex katex
```

In `LessonPage.jsx`:
- `import remarkMath from 'remark-math'`
- `import rehypeKatex from 'rehype-katex'`
- `import 'katex/dist/katex.min.css'`
- `remarkPlugins={[remarkGfm, remarkMath]}`,
  `rehypePlugins={[rehypeKatex]}`.
- remark-math extracts `$...$` / `$$...$$` spans BEFORE markdown escape
  processing, which is exactly what fixes the `\\` corruption.
- Remove the custom string-sniffing MathDisplay wrapping inside the
  ReactMarkdown component map for lesson content (the helpers around
  lines 251–260) — KaTeX now handles it. Do NOT touch MathDisplay usage
  elsewhere (practice, placement, walkthrough) in this item.

**Verify:** load `linalg-row-reduce`, `linalg-determinant`,
`linalg-matrix-ops` lesson pages. Matrices must render as proper stacked
rows. Also spot-check 3 non-linalg lessons (one Foundations, one calc,
one stat) to confirm inline math, display math, and tables still render.
KaTeX doesn't support `\xrightarrow{...}` over-arrow text as fully as
MathJax in some versions — if the row-reduce lesson's arrows break,
either load the katex `mhchem`/extension needed, or replace
`\xrightarrow{R_2 \leftarrow ...}` with `\to` plus a text annotation in
those lesson files. Check and report which route was taken.

---

## ITEM 7: Fix `eq-fractions` "+ -" display artifact

**Problem (verified):** `eq-fractions` can generate
`Solve for x: \frac{x + -2}{2} = 3`.

**Fix:** in `backend/app/services/problem_generator.py` (or wherever the
eq-fractions generator formats its expression), format the constant term
with sign-aware rendering: if the constant is negative, emit `x - 2`,
if positive `x + 2`, if zero omit the term. Grep the generator modules
for other raw `+ {b}` interpolations with signed variables and apply the
same guard — check at minimum `eq-two-step`, `eq-distribution`, and the
algebra module's linear-expression formatting. A shared helper
`fmt_signed(coef_or_const)` is preferred over copy-paste.

**Test:** run `eq-fractions` 500 times, assert `'+ -'` and `'- -'`
never appear in `problem_text` or any hint text.

---

## ITEM 8: Fix `exp-combined` exponent-of-1 artifact

**Problem (verified):** `exp-combined` can generate
`Simplify: \frac{x^{4}}{x^{1}}` and `\frac{4^{5}}{4^{1}}`. An exponent
of 1 is visually wrong for an exponent-rules topic.

**Fix:** constrain all randomly chosen exponents in `exp-combined` (and
audit `exp-product`, `exp-power`, `exp-negative` for the same) to ≥ 2.
Where a difference of exponents is displayed (quotient rule
intermediates in hints), also ensure no `^{1}` or `^{0}` appears in
DISPLAYED problem text — those values may legitimately appear in hint
step math (e.g., "= x^{1} = x") only if pedagogically intentional;
default to avoiding them.

**Test:** run each exp-* generator 500 times, assert `'^{1}'` and
`'^{0}'` never appear in `problem_text`.

---

## ITEM 9: CI — run the test suite on every push

**Problem:** 41 answer-checker tests + strict-form tests exist and pass,
but nothing runs them automatically. Also `tests/test_generators.py` is
not pytest-collectable ("no tests ran") and `test_answer_checker.py` is
script-style (`python tests/test_answer_checker.py`).

**Tasks:**
1. Convert `test_answer_checker.py` to be BOTH pytest-collectable and
   runnable as a script: wrap the TEST_CASES loop in a
   `@pytest.mark.parametrize` function, keep the `__main__` block.
2. Do the same for `test_generators.py`, or fold its checks into the
   Item 5 harness and delete it.
3. Create `.github/workflows/tests.yml`: on push and PR to main, set up
   Python 3.11, `pip install -r backend/requirements.txt pytest`, run
   `python -m pytest backend/tests/ --ignore=backend/tests/test_e2e_submission.py -q`
   (the e2e test needs a live DB; excluded in CI for now).
4. Confirm the workflow passes on GitHub after pushing.

---

## COMMIT PLAN

- Commit A (Item 1 alone): rescue uncommitted walkthroughs. PUSH IMMEDIATELY.
- Commit B: Items 2 + 3 (strict form + MC shuffle) with tests.
- Commit C: Item 4 (condition system) with tests + schema doc update.
- Commit D: Item 5 (validation harness).
- Commit E: Item 6 (matrix rendering).
- Commit F: Items 7 + 8 (generator artifacts) with tests.
- Commit G: Item 9 (CI).

---

## MANDATORY TESTING CHECKLIST

Write results to `backend/tests/TESTING-RESULTS-R15.txt`:

1. `git status` output from Item 1 and list of rescued files (or "none found").
2. Strict form: `0.75` rejected on frac-simplify step 4 via a real
   POST to `/api/walkthrough/frac-simplify/check-step` (curl with auth
   token, same approach as Diagnos.md). Include the response JSON.
3. `3/4` accepted, `6/8` rejected, `\frac{6}{8}` rejected — same endpoint.
4. MC shuffle: GET `/api/walkthrough/frac-simplify` 10 times, record the
   position of the correct conceptual option each time; must vary.
   Submitting the correct displayed option returns correct=True.
5. Condition evaluator: all four malicious-input tests pass; both pilot
   templates produce the SAME feedback text for the same wrong answers
   as before migration (spot-check 3 wrong answers per template).
6. Validation harness output table: all templates PASS.
7. Browser check: `linalg-row-reduce` lesson shows stacked matrix rows.
   Screenshot or DOM-text confirmation.
8. `eq-fractions` and `exp-*` 500-run artifact scans: zero hits.
9. Full pytest suite green locally; GitHub Actions run green after push.
10. Regression: complete one full frac-simplify walkthrough and one
    eq-one-step walkthrough end-to-end in the browser (register test
    user if needed) — intro renders, steps advance, completed steps stay
    visible, completion screen appears, Skip to Practice works.

## OUT OF SCOPE FOR THIS ROUND (do not do)

- stat-ci-z gold-standard walkthrough (next round, after harness exists)
- MathLive virtual keyboard / toolbar expansion
- Video slots in walkthroughs
- Medieval cartographic rebrand
- Any changes to placement engine, BKT, review system, or AI chat
