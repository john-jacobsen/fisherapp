# FIXES-16: Walkthrough Rendering & UX, Open FIXES-14 Backlog, Authoring Pilot Batch

**Date:** 2026-07-27
**Scope:** WalkthroughPage math rendering, topic access policy, mastery persistence, MathLive keyboard, video slots, stat-ci-z quality, log-rules generator, knowledge graph colors, review enforcement, walkthrough authoring pilot
**Base:** repo at `97e379e` (all FIXES-15 work merged, CI green)

---

## CONTEXT

FIXES-15 hardened the walkthrough backend (strict form allowlist, MC shuffle,
safe condition evaluator, validation harness) and fixed matrix rendering in
LESSONS via remark-math + rehype-katex. Six walkthrough templates exist and
pass the harness: frac-simplify, eq-one-step, calc-deriv-power,
linalg-row-reduce, prob-bayes, stat-ci-z.

This round: fix the walkthrough-side rendering gap, clear the open FIXES-14
backlog, and run a pilot authoring batch to establish the scaling workflow
before mass generation in FIXES-17.

---

## ITEM 1: Fix math rendering in WalkthroughPage (14-1 — STILL LIVE)

**Problem (verified):** FIXES-15 Item 6 fixed LessonPage.jsx only.
`WalkthroughPage.jsx` still renders `walkthrough.intro.body` through
ReactMarkdown with only `remarkGfm`, plus the MathDisplay child-wrapping
helper. Markdown escaping collapses `\\` to `\` before any math engine sees
it, so the `linalg-row-reduce` intro's `\begin{cases}` and
`\left[\begin{array}{cc|c}...\right]` blocks lose their row separators and
render flat — the exact bug FIXES-14 Item 14-1 described.

**Fix:** Apply the proven LessonPage recipe to WalkthroughPage's intro
rendering (and the completion screen if it also renders markdown):

1. Import `remarkMath`, `rehypeKatex`, and `'katex/dist/katex.min.css'`
   (deps already installed in FIXES-15).
2. On the intro's ReactMarkdown:
   `remarkPlugins={[remarkGfm, remarkMath]}`,
   `rehypePlugins={[[rehypeKatex, { throwOnError: false, strict: false }]]}`.
3. Remove the MathDisplay child-wrapping helper FROM THE INTRO PATH ONLY.
   Step prompts, options, hints, and feedback are NOT markdown — they're
   plain strings with `\( \)` delimiters rendered via MathDisplay/MathJax.
   Leave that path alone; it works.
4. Check the six templates for intro math using `$...$` vs `\( \)`
   delimiters. remark-math only recognizes `$`/`$$`. If any intro uses
   `\( \)` inline math inside the markdown body, either convert those
   intros to `$` delimiters (preferred — matches lesson convention) or add
   a preprocessing replace. Grep all six intros and report which needed
   conversion.

**Verify:** render the `linalg-row-reduce` intro through the real pipeline
(same node-based DOM check used in R15: ReactMarkdown + remark-math +
rehype-katex over the actual intro body) and confirm the augmented matrix
produces stacked rows (both `\\`-separated values present as separate MathML
rows). Also render the other five intros and confirm no KaTeX parse errors.

---

## ITEM 2: Free topic access (14-7)

**Problem:** The backend raises PermissionError when a student opens a topic
whose prerequisites aren't all mastered. Prerequisite structure should be
advisory, not enforced.

**Fix:**
1. Locate the gate (grep PermissionError in `backend/app/routers/practice.py`
   and any service it delegates to) and remove it, for practice, lessons, and
   walkthroughs alike.
2. Keep the dashboard/graph visual distinction (locked/gray styling for
   unmet-prereq topics) but make those nodes clickable. If the frontend
   blocks navigation for "locked" nodes, change to allow navigation; show a
   small non-blocking notice on the target page ("Heads up: this topic
   builds on X and Y, which you haven't mastered yet") — reuse the existing
   above-fringe warning pattern if one exists.
3. Do not change placement, BLIM updates, or fringe computation — this is
   access policy only.

**Verify:** with a fresh test user (no mastery), GET/POST the practice start
endpoint for a deep node (e.g. `stat-ci-z`) → 200, problem returned. Confirm
the dashboard still visually distinguishes ready vs not-ready.

---

## ITEM 3: Mastery persistence to dashboard (14-6)

**Problem:** The frontend never calls the completion endpoint when a student
reaches mastery in practice, so mastery resets on reload.

**Fix:** In PracticePage.jsx, on reaching the mastery threshold, POST to the
appropriate complete/mastery endpoint (find the exact route in
`backend/app/routers/practice.py`; if none exists, add one that sets the
node's mastery state and triggers the KST fringe recompute the same way the
existing mastery path does). Ensure idempotency (double-submit safe).

**Verify:** via the API — start practice on frac-simplify with a test user,
submit correct answers to threshold, call the completion flow, then GET the
dashboard and confirm the node reports mastered. Re-fetch after a fresh
login to confirm persistence.

---

## ITEM 4: MathLive virtual keyboard (14-4)

**Problem:** No toolbar/virtual keyboard on math inputs. Students can't
enter matrices, integrals, summations, trig, or Greek letters — increasingly
painful now that the curriculum spans calc/linalg/prob/stat.

**Fix:** Configure MathLive's virtual keyboard on the MathInput component
(used by WalkthroughPage and PracticePage):
1. Read the installed MathLive version from package.json and use the
   matching API (virtual keyboard config changed across versions — check
   the version's docs, don't guess).
2. Enable a keyboard with layers/tabs covering: numeric/basic, algebra
   (frac, sqrt, exponents), calculus (int, sum, lim, d/dx), trig + Greek,
   and comparison operators. A matrix layer is nice-to-have; skip if the
   installed version makes it painful (answers are scalars/fractions
   anyway).
3. Trigger: keyboard appears on focus for touch devices; on desktop show a
   small toggle button. Do not force the keyboard open on desktop.
4. Keep the existing keyboard shortcuts (`/` for fractions etc.) working.

**Verify:** frontend compiles; MathInput mounts with keyboard config without
console errors (check Vite/browser console via the dev server logs). Flag
for John's manual mobile check (see checklist).

---

## ITEM 5: Video slot in walkthrough intros (14-5)

**Fix:**
1. Add optional `video_id` (YouTube ID string) to the walkthrough schema —
   document in walkthrough-schema.md; update the validation harness to
   accept (and type-check) the optional field.
2. In WalkthroughPage intro screen: if `video_id` present, render the same
   YouTube iframe embed pattern LessonPage uses, above the intro body.
3. Leave `video_id` unset in all six templates. Populating videos is
   FIXES-17 (14-12).

**Verify:** harness passes with and without the field (add a temporary
in-test template dict with a video_id, or unit-test the schema check
directly). Frontend renders a walkthrough with a hand-injected video_id in
a quick DOM check, then remove the injection.

---

## ITEM 6: stat-ci-z quality review + row-reduce phrasing check (14-2)

**stat-ci-z** was rescued in FIXES-15 and passes the harness, but has not
had the gold-standard quality pass. Review against the other five:

1. **Numeric tolerance vs rounding:** steps 3–6 (standard error, margin of
   error, bounds) produce decimals checked with tolerance ±0.01. Verify the
   generator only produces values where the prompt's rounding instruction
   (add one if missing: "round to 2 decimal places") is coherent with the
   tolerance — no cases where correct rounding falls outside ±0.01 of the
   stored answer, and no cases where two plausible roundings both pass or
   both fail. If sigma/sqrt_n produces long decimals, prefer generator
   parameters where sqrt_n is exact (n a perfect square — verify it already
   does this) and values round cleanly.
2. **Hint quality:** every step needs level-appropriate hint(s) per the
   house style (conceptual → this-problem-specific → worked). Fill gaps.
3. **Wrong-answer feedback:** each numeric step should catch the canonical
   mistakes (using sigma instead of SE, forgetting sqrt, swapping bounds,
   using z for the wrong confidence level) with expression conditions in
   the new grammar. Add where missing.
4. **Interpretation step (7):** confirm the distractors are the classic
   misinterpretations ("95% of data falls in the interval", "95% chance mu
   is in this interval" vs the correct long-run coverage statement) and
   wrong choices get targeted feedback.
5. **14-2 check:** confirm the rescued linalg-row-reduce.json includes the
   negative-multiplier phrasing fix ("add {abs_multiplier} times Row 1"
   when multiplier < 0). If not, implement it per FIXES-14 Item 14-2.

**Verify:** harness passes; run the full stat-ci-z walkthrough end-to-end
via the API (as in R15) with both correct answers and each targeted wrong
answer, confirming the intended feedback fires.

---

## ITEM 7: log-rules generator rewrite (14-8)

**Problem:** `log-rules` expects computed numeric answers (log₂16 → "4");
answers must stay in log form. Change-of-base variants were wrongly added in
FIXES-10 and belong in a separate node.

**Fix:** rewrite the generator variants so answers are log expressions
(e.g. combine log(a) + log(b) → "log(ab)"); set answer_type appropriately
for the checker (symbolic with SymPy log handling — verify the checker
accepts equivalent log forms and REJECTS the evaluated number; if the
symbolic path auto-evaluates, compare on canonical string forms instead and
document the choice). Remove change-of-base variants from this node (leave
the change-of-base NODE, if one exists in the graph, untouched).

**Verify:** 200-run generator scan: no numeric-only answers; checker accepts
the log-form answer and rejects its decimal evaluation for at least 20
sampled problems. Existing tier tests still pass.

---

## ITEM 8: Knowledge graph "ready to learn" color propagation (14-9)

**Problem:** some nodes with all prerequisites mastered still show
locked/gray instead of ready/amber on KnowledgeGraph.

**Fix:** audit the status derivation in KnowledgeGraph.jsx (and the
dashboard API payload it consumes). Likely causes: status computed from a
stale field, OR ready-state computed only over direct prereqs vs the API's
notion, OR a mismatch between node id formats. Reproduce with the 14-9 test
case: master `frac-simplify` and `frac-add-sub-like` (whichever ids
`frac-mult` actually depends on — read the graph JSON), then fetch the
dashboard and confirm `frac-mult` reports ready; fix until the frontend
renders it amber.

**Verify:** API-level: dashboard payload marks the test node ready after
prereq mastery. Add a small backend test if the ready-computation lives
server-side.

---

## ITEM 9: Review enforcement — escalating soft gate (14-10)

Implement the autonomy-supportive enforcement ladder on top of the existing
SM-2 review system:

- 1–2 days overdue: dismissible banner on dashboard (exists? verify — the
  ReviewBanner component may already cover this tier).
- 3–5 days overdue: persistent (non-dismissible) banner + a "Review now"
  interstitial prompt before starting any practice session (skippable, one
  click).
- 6+ days overdue: limit NEW practice to 3 sessions/day until overdue
  reviews are cleared; reviews themselves always available. Enforce
  server-side (count practice session starts per UTC day for the user);
  return a structured 409/limit response the frontend renders with a clear
  explanation and a "Do reviews" CTA.
- Failed review drops the topic mastered → ready (verify this already
  happens; implement if not).
- Update SM-2 intervals to: 7d → 14d → 30d → 90d (per 14-10; the current
  code uses 1/3/7/14/30 — migrate the schedule constants; existing due
  dates keep their stored values, only future scheduling changes).

Keep all copy transparent and non-punitive, consistent with the two-step
reminder philosophy.

**Verify:** backend tests for the day-limit and the interval constants;
API-level walk of each tier by back-dating review due dates on a test user.

---

## ITEM 10: Walkthrough authoring pilot batch (prep for 14-11)

Write the NEXT EIGHT walkthroughs by hand-quality standards, using the six
gold standards as style reference and the harness as the gate. Choose nodes
that (a) students hit early on common paths and (b) cover distinct step
patterns:

- `frac-add-sub-unlike` (fractions, multi-step numeric)
- `eq-two-step` (equations, builds on eq-one-step's MC-then-numeric pattern)
- `exp-product` (exponent rules, exact_form)
- `log-definition` (log_form strict checking — coordinates with Item 7's
  checker verification)
- `alg-factoring-quad` (factored_form strict checking)
- `calc-deriv-chain` (calculus, expression answers)
- `prob-conditional` (probability, fraction answers)
- `stat-hyp-setup` (statistics, MC-heavy conceptual pattern)

For each: JSON template + Python generator + registration, following the
schema doc (expression-grammar conditions only, strict_form where the form
matters pedagogically, conceptual MC close, hints in house style). Run the
harness after each; all must PASS. Add each to the strict-form test file's
walkthrough coverage the way the six existing ones are covered.

Then write `docs/walkthrough-authoring-workflow.md`: the exact reusable
recipe (files to create, harness command, test registration, common
failure modes seen during this batch) — this becomes the playbook for
FIXES-17 mass generation.

---

## OUT OF SCOPE (do not do this round)

- Mass AI generation of remaining ~160 walkthroughs (FIXES-17, uses Item 10's playbook)
- Video population in lesson_videos.json / walkthrough video_ids (FIXES-17)
- Placement engine, BLIM, BKT changes
- Any UI restyling beyond what the items above require

---

## COMMIT PLAN

- Commit A: Item 1 (walkthrough math rendering)
- Commit B: Items 2 + 3 (free access + mastery persistence)
- Commit C: Item 4 (MathLive keyboard)
- Commit D: Item 5 (video slot)
- Commit E: Item 6 (stat-ci-z quality + 14-2 check)
- Commit F: Items 7 + 8 (log-rules + graph colors)
- Commit G: Item 9 (review enforcement)
- Commits H1–H8: Item 10, one commit per walkthrough, then H9 for the workflow doc
- CI must be green after every push.

---

## MANDATORY TESTING CHECKLIST

Write results to `backend/tests/TESTING-RESULTS-R16.txt`:

1. Item 1: DOM-level render of linalg-row-reduce intro through the real
   pipeline shows stacked matrix rows; all six intros render without KaTeX
   errors; list any intros converted from `\( \)` to `$` delimiters.
2. Item 2: fresh user can start practice on `stat-ci-z` (200 + problem);
   dashboard still shows the visual ready/not-ready distinction.
3. Item 3: mastery persists across re-login (API evidence).
4. Item 4: frontend compiles; MathInput mounts with keyboard config, no
   console errors in Vite logs.
5. Item 5: harness green with optional video_id; DOM check of injected
   video renders iframe.
6. Item 6: full stat-ci-z API walk — correct path + each targeted wrong
   answer with its feedback; rounding-coherence scan over 200 generator
   runs (no tolerance ambiguity); 14-2 phrasing confirmed or fixed.
7. Item 7: log-rules 200-run scan + accept/reject evidence for log form vs
   decimal.
8. Item 8: dashboard payload marks the 14-9 test node ready after prereq
   mastery.
9. Item 9: each enforcement tier demonstrated via back-dated reviews;
   day-limit test; new interval constants tested.
10. Item 10: harness table showing all 14 templates PASS; per-walkthrough
    end-to-end API completion (correct path) for the 8 new ones.
11. Full pytest suite green locally AND on GitHub Actions after final push.

## FLAG FOR JOHN'S MANUAL BROWSER PASS (Claude Code: list these at the end of your summary)

- Walkthrough intros with matrices (linalg-row-reduce) look right on screen
- MathLive keyboard usability, especially on a phone
- The review-enforcement banners/interstitial feel right (tone + friction)
- Spot-check 2–3 of the 8 new walkthroughs end-to-end as a student would
