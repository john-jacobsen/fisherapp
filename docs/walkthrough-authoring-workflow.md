# Walkthrough Authoring Workflow

The reusable recipe for writing one interactive walkthrough, established during
the FIXES-16 pilot batch (8 walkthroughs) and the playbook for FIXES-17 mass
generation. Read `walkthrough-schema.md` first for the full schema and the
wrong-answer condition grammar; this doc is the *process* and the *gotchas*.

## What a walkthrough is

One node → two files:

1. **Template** — `backend/data/walkthroughs/{node_id}.json`
   A placeholder template: an intro, a `problem_generator` description block
   (documentation only), an ordered list of `steps`, and a `completion_message`.
2. **Generator** — `backend/app/services/walkthrough_generators/{node_id_with_underscores}.py`
   A module exposing `def generate() -> dict:` that returns a **flat dict** of
   variable values (ints and strings only). Hyphens in the node id become
   underscores in the module name (`frac-add-unlike` → `frac_add_unlike.py`).

**No central registration.** The loader (`walkthrough_generator._load_generator`)
imports the module by name and calls `generate()`. The validation harness and the
pytest wrapper auto-discover every `*.json` in the walkthroughs dir. Just create
the two files.

At request time, `generate_walkthrough(node_id)` calls `generate()`, substitutes
every `{key}` placeholder throughout the template with `str(value)`, shuffles the
multiple-choice options, and returns the hydrated dict. `GET /api/walkthrough/{node_id}`
serves it; `POST /api/walkthrough/{node_id}/check-step` grades one step.

## Steps to author one

1. **Pick the pedagogy.** 5–7 steps that build to the answer, ending with a
   conceptual `multiple_choice` "Check your understanding". Each numeric/algebra
   step should isolate ONE idea.
2. **Write the generator first.** Decide the variables, generate with a
   rejection loop that enforces every invariant (clean integers, positive
   results, non-integer fractions, distinct MC option values, small displayed
   numbers). Always include a deterministic fallback `return` after the loop.
3. **Write the template**, substituting `{var}` placeholders. Copy an existing
   gold standard of the same shape:
   - numeric/fraction → `frac-add-unlike.json`
   - equation, MC-then-numeric → `eq-one-step.json`, `eq-two-step.json`
   - exponent/derivative expression → `calc-deriv-power.json`, `exp-product.json`
   - `$…$` math + conceptual interpretation → `stat-ci-z.json`
   - strict-form finals → `log-definition` (log_form), `alg-factoring-quad`
     (factored_form), `frac-add-unlike` (simplified_fraction)
4. **Run the harness until PASS** (see below). Fix, repeat.
5. **Add test coverage** in `backend/tests/test_walkthrough_strict_form.py`
   (a `test_<node>_generator` that asserts the generator's invariants, mirroring
   the six originals). The auto-discovered `test_walkthrough_validation.py`
   already covers schema + hydration for every template.
6. **Verify the correct path end-to-end** via the API (register a user, GET the
   walkthrough, POST each step's `correct_answer`, expect `correct: true`).

## Harness command

```bash
# one node
docker compose exec -T backend python scripts/validate_walkthroughs.py 2>&1 | grep {node_id}
# everything (must end "All N templates passed.")
docker compose exec -T backend python scripts/validate_walkthroughs.py
# pytest wrappers (run in CI)
docker compose exec -T backend python -m pytest tests/test_walkthrough_validation.py tests/test_walkthrough_strict_form.py -q
```

The harness hydrates each template 25× and checks: no unresolved `{placeholder}`
remains; every numeric/expression `correct_answer` passes its own checker; every
`strict_form` correct answer passes AND a known-bad probe fails; all
`multiple_choice` options are unique and the correct index is in range.

## Common failure modes (seen during the pilot)

- **Brace nesting is literal, not `.format()`.** Hydration is
  `str.replace('{key}', value)`. To make a strict-form/expression
  `correct_answer` hydrate to a **single-brace** LaTeX group like `\frac{3}{4}`,
  write **double** braces: `\\frac{{simp_num}}{{simp_den}}`. For *display* math
  that should show a literal `{…}` (e.g. `\frac{{3}}{{4}}`, harmless in LaTeX),
  write **triple** braces: `\\frac{{{num}}}{{{den}}}`. Getting this wrong on a
  strict-form answer yields `\frac{{26}}{{21}}`, which the `simplified_fraction`
  regex rejects → harness FAIL. When unsure, copy `frac-add-unlike.json`.
- **Multiple-choice option collisions.** Options must be unique for *every*
  random draw, not just the common case. A symmetric draw can make two distractor
  strings hydrate identically (this bit `linalg-row-reduce`: for `a2==b1, b2==a1,
  c1==c2` the "rows swapped" and "columns swapped" options coincided). Add a
  rejection guard in the generator; brute-force a few hundred thousand draws to
  confirm 0 collisions.
- **strict-form probe.** `exact_form` rejects any `.`; `simplified_fraction`
  requires `gcd(num,den)==1` AND rejects a bare integer/decimal (so keep
  `denominator != 1`); `log_form` requires a `log`/`ln` token; `factored_form`
  needs a real `(…)(…)` product (a single group like `(x^2-9)` is rejected).
  Make the correct answer satisfy the form AND stay SymPy-equivalent to the value.
- **Math delimiters.** Intro `body`/`key_formula` render through KaTeX
  (remark-math): use `$…$` / `$$…$$`. Step prompts/options/hints/feedback render
  through MathJax (`MathDisplay`): use `$…$` or `\\(…\\)`. Don't mix a raw `\\`
  row-separator into a markdown-escaped context.
- **Display artifacts.** Avoid `^{1}`/`^{0}`, bare `1x`, and `+ -`/`- -`. Build
  sign-aware display strings in the generator (see `calc-deriv-power.py`).
- **MC correct_answer is the TEMPLATE index** (pre-shuffle), as a string (or a
  `{var}` that hydrates to an int index). Wrong-answer conditions also reference
  the template index (`answer == 1`); the backend translates the shuffled display
  index back before evaluating.
- **Conditions are a safe expression grammar** — names, `answer`/`answer_int`,
  comparisons, `and/or/not`, arithmetic. No function calls, attribute access, or
  subscripts. Always end a step's `wrong_answer_feedback` with `"default"`.

## Definition of done

- `[PASS]` in the harness for the node; `All N templates passed.` overall.
- `test_walkthrough_validation.py` + `test_walkthrough_strict_form.py` green.
- A generator invariant test added for the node.
- Correct-path API completion returns `correct: true` for every step.
- Optional `intro.video_id` left unset (populated in FIXES-17).
