# Tonight's Claude Code Session — Ready-to-Paste Prompts

Run these in order from `C:\Users\jjcas\Desktop\Fisher App\Fisher App 3.0`.
After each backend change: `docker compose restart backend`, then test before moving on.

---

## PROMPT 1 — stat-ci-z walkthrough (last gold standard)

```
claude --dangerously-skip-permissions "Read the existing walkthrough implementations for context: all JSON files in backend/data/walkthroughs/ and their corresponding generators in backend/app/services/walkthrough_generators/. Also read backend/app/routers/walkthrough.py for strict_form and answer checking.

Create the stat-ci-z walkthrough:

1. Create backend/app/services/walkthrough_generators/stat_ci_z.py:
   - generate() returns variables for constructing a confidence interval for a population mean using a z-interval (known population standard deviation, large sample)
   - Generate a realistic scenario: sample mean (xbar) is an integer between 40 and 200, population standard deviation (sigma) is an integer between 5 and 30, sample size (n) is one of [36, 49, 64, 100, 144, 225, 400] (perfect squares so sqrt(n) is clean), confidence level is one of [90, 95, 99]
   - Look up the z-critical value: 90->1.645, 95->1.96, 99->2.576
   - Compute: sqrt_n = sqrt(n), standard_error = sigma / sqrt_n (must be a clean number — require sigma is divisible by sqrt_n), margin_of_error = z_star * standard_error (round to 2 decimal places), lower = xbar - margin_of_error, upper = xbar + margin_of_error
   - Constraints: standard_error must be a whole number or clean decimal (sigma % sqrt_n == 0), margin_of_error should round to at most 2 decimal places, lower > 0
   - Return: { xbar, sigma, n, sqrt_n, conf_level, z_star, standard_error, margin_of_error, lower, upper, alpha, alpha_half }
   - where alpha = 100 - conf_level, alpha_half = alpha/2 (as a number, not percentage)

2. Create backend/data/walkthroughs/stat-ci-z.json:

Intro:
- Title: 'Constructing a Z Confidence Interval'
- Body: Explain that a confidence interval gives a range of plausible values for a population parameter based on sample data. For the population mean with known sigma and large n, we use the z-interval. The interval is centered at the sample mean and extends by a margin of error in each direction. The margin of error depends on three things: how confident we want to be (higher confidence = wider interval), how variable the population is (larger sigma = wider interval), and how large the sample is (larger n = narrower interval). Walk through a concrete example with fixed numbers (xbar=100, sigma=15, n=25, 95% confidence) showing each computation step. Emphasize that the confidence level refers to the procedure, not the specific interval — if we repeated the sampling process many times, 95% of the resulting intervals would contain the true mean.
- Key formula: xbar ± z* × (sigma / sqrt(n))

Steps:

Step 1 (multiple_choice): 'You want a {conf_level}% confidence interval. What is the z-critical value z*?' Options: 1.645, 1.96, 2.576, and one wrong value like 1.28 or 2.326. Correct: {z_star}. Feedback should explain: z* comes from the standard normal distribution — it is the value where the central {conf_level}% of the area falls between -z* and z*.

Step 2 (numeric): 'Compute the standard error: sigma / sqrt(n) = {sigma} / sqrt({n}). What is sqrt({n})?' Correct: {sqrt_n}. Feedback for common square root errors.

Step 3 (numeric): 'Now compute the standard error: {sigma} / {sqrt_n} = ?' Correct: {standard_error}. Feedback for division errors.

Step 4 (numeric): 'Compute the margin of error: z* × standard error = {z_star} × {standard_error} = ?' Correct: {margin_of_error}. Feedback for multiplication errors. Accept answers within 0.01 of the correct value to handle rounding.

Step 5 (numeric): 'The lower bound of the interval is xbar - margin of error = {xbar} - {margin_of_error} = ?' Correct: {lower}.

Step 6 (numeric): 'The upper bound is xbar + margin of error = {xbar} + {margin_of_error} = ?' Correct: {upper}.

Step 7 (multiple_choice): Conceptual check — 'What does {conf_level}% confidence mean?' Best option: 'If we repeated this sampling procedure many times, {conf_level}% of the resulting intervals would contain the true population mean.' Wrong options: 'There is a {conf_level}% probability that the true mean is in this specific interval' (common misconception — the true mean is fixed, not random), 'The sample mean is within {conf_level}% of the true mean' (confuses confidence level with precision).

After creating both files, run tests to verify:
- The generator produces valid scenarios across 30 runs: standard_error is clean, margin_of_error has at most 2 decimal places, lower > 0, sqrt_n^2 == n, sigma % sqrt_n == 0
- The walkthrough hydrates with no remaining template placeholders
- The check-step endpoint works for all step types
- Numeric comparison for step 4 accepts answers within 0.01 tolerance"
```

**Test after:** restart backend, walk through stat-ci-z. Try the misconception answer on Step 7 (the "95% probability the true mean is in this interval" option) and check the feedback explains why it's wrong.

---

## PROMPT 2 — Commit the walkthroughs

```
claude --dangerously-skip-permissions "Stage and commit all changes with the message 'Add gold-standard walkthroughs: linalg-row-reduce, prob-bayes, stat-ci-z

- linalg-row-reduce: 7-step Gaussian elimination walkthrough with augmented matrix MC, integer-multiplier elimination, back-substitution
- prob-bayes: 7-step natural frequency Bayes walkthrough (medical screening scenario, base rate fallacy conceptual check)
- stat-ci-z: 7-step z confidence interval walkthrough with z-critical lookup, standard error, margin of error, and the confidence-level-interpretation misconception check
- calc-deriv-power: MC option collision fix (a != n constraint, all 4 option values distinct)
- Test suite expanded to cover all 6 gold-standard generators and hydration

All 6 gold-standard walkthroughs complete: frac-simplify, eq-one-step, calc-deriv-power, linalg-row-reduce, prob-bayes, stat-ci-z'. Then push to origin main. Do NOT stage __pycache__ or frontend/dist files."
```

---

## PROMPT 3 — FIXES-14 Priority 1: Walkthrough UI bugs

First copy FIXES-14.md into the repo root, then:

```
claude --dangerously-skip-permissions "Read FIXES-14.md in the repo root. Implement items 14-1 through 14-5 (Priority 1 — Walkthrough Bugs):

14-1: Fix matrix LaTeX rendering in WalkthroughPage.jsx. The \begin{array} environment displays as flat text. Check what KaTeX version is in use and whether the array environment with column separators ({cc|c}) is supported. If KaTeX supports it but it's failing, the issue is likely in how the markdown pipeline parses the LaTeX before KaTeX sees it (e.g., newlines \\\\ being eaten by JSON or markdown). Debug with the linalg-row-reduce intro. If the markdown pipeline is mangling multi-line LaTeX, consider rendering display math blocks directly with katex.render() instead of going through ReactMarkdown.

14-2: Fix the row-reduce multiplier phrasing for negative multipliers. In linalg-row-reduce.json, the generator should provide an additional variable 'operation_phrase' computed in linalg_row_reduce.py: if multiplier > 0, operation_phrase = 'subtract {multiplier} times Row 1 from Row 2'; if multiplier == -1, operation_phrase = 'add Row 1 to Row 2'; if multiplier < -1, operation_phrase = 'add {abs_multiplier} times Row 1 to Row 2'. Update Step 2 and Step 3/4 prompts to use natural phrasing.

14-3: Verify completed walkthrough steps show full content (prompt text + the student's correct answer), not just a collapsed title with 'Done'. If they're collapsing, fix WalkthroughPage.jsx so completed steps remain expanded.

14-4: Add the MathLive virtual keyboard to the math input component used in WalkthroughPage.jsx and PracticePage.jsx. Configure mathVirtualKeyboard with layouts covering: numeric, symbols, alphabetic, and greek. Ensure the keyboard appears when the math field is focused (virtualKeyboardMode or the appropriate MathLive 0.9x+ API). Test that a student can enter: fractions, exponents, square roots, integrals, summation, sin/cos/tan, Greek letters, and matrices. Check the MathLive version in package.json first and use the API matching that version.

14-5: Add optional video support to walkthroughs. Add an optional 'video_id' field to the walkthrough JSON schema (top level, next to 'title'). In WalkthroughPage.jsx, if video_id is present and non-empty, render a YouTube iframe embed at the top of the intro screen before the body text, using the same pattern as LessonPage.jsx. Leave video_id absent from all existing templates.

After implementing, rebuild the frontend (docker compose exec frontend npx vite build --mode development) to verify no errors, and run the backend test suite to confirm nothing broke."
```

**Test after:** restart backend, hard-refresh browser. Check: linalg-row-reduce intro matrices render stacked, multiplier phrasing reads naturally, completed steps stay visible, MathLive keyboard appears with full notation, no video shows (since video_id is empty everywhere).

---

## PROMPT 4 — FIXES-14 Priority 2: Mastery persistence + free access

```
claude --dangerously-skip-permissions "Read FIXES-14.md in the repo root. Implement items 14-6 and 14-7 (Priority 2):

14-6: Mastery persistence. Find where PracticePage.jsx determines the student has achieved mastery on a topic. Verify whether it calls a backend endpoint to persist this. If not, find the appropriate endpoint (check backend/app/routers/practice.py for a /complete or mastery endpoint) and wire it up: when mastery is achieved, POST to persist it, and ensure the dashboard reflects the updated status after navigating back. If no backend endpoint exists, create one that updates the student's mastery record in the database.

14-7: Free topic access. Find the PermissionError gate in the backend that blocks access to topics with unmet prerequisites (check practice.py, lessons.py, and walkthrough.py routers). Remove the gate so any topic can be accessed regardless of prerequisite status. Keep the visual locked/gray styling on the dashboard, but make locked nodes clickable — they should navigate to the walkthrough/lesson like any other node. Update KnowledgeList.jsx and KnowledgeGraph.jsx click handlers to allow navigation for all node statuses.

After implementing, test: 1) achieve mastery on a topic in practice mode, navigate to dashboard, verify it shows as mastered, refresh the page, verify it still shows as mastered. 2) click a locked/gray topic and verify it opens the walkthrough."
```

**Test after:** restart backend. Master a topic, refresh, confirm it persists. Click a gray node, confirm it opens.

---

## PROMPT 5 — FIXES-14 Priority 3: log-rules generator + color coding

```
claude --dangerously-skip-permissions "Read FIXES-14.md in the repo root. Implement items 14-8 and 14-9 (Priority 3, first two items):

14-8: log-rules generator rewrite. Read backend/app/services/generators/ to find the log-rules generator. Rewrite it so all variants produce problems whose answers are LOG EXPRESSIONS, not computed numbers. Example: 'Combine: log2(2) + log2(8)' should have answer 'log2(16)', NOT '4'. Remove any change-of-base variants from this generator (change-of-base is taught in a different node). The answer checker needs to accept log expressions — check how answer_checker.py handles log notation and ensure SymPy comparison works for expressions like log2(16) vs log(16)/log(2). Add a strict-form-like check in the practice answer flow OR ensure the correct answers are stored in log form so SymPy equivalence with a plain number still requires... actually, NOTE: SymPy will treat log2(16) and 4 as equal. The practice problem flow needs the same form checking as walkthroughs. Check how practice answers are validated in practice.py and add a form check: if the expected answer contains log notation, the student's answer must also contain log notation. Apply the same rejection feedback pattern used in the walkthrough strict_form system.

14-9: Knowledge graph color coding. In KnowledgeGraph.jsx, find the logic that assigns node status colors. Debug why some nodes with all prerequisites mastered still show as locked/gray instead of amber 'ready to learn'. Likely causes: the status computation uses the wrong key for prerequisites (check whether it reads 'surmise_relations' — the correct key in knowledge_graph.json — or the wrong key 'edges'), or the mastered-set lookup has an ID mismatch. Write the fix and explain what the bug was.

After implementing, run the generator test suite (tests/test_generators.py) to verify log-rules still passes all 3 tiers, and manually verify: master frac-simplify's prerequisites and check that frac-simplify turns amber on the graph."
```

**Test after:** restart backend. Practice log-rules — answers in log form should be accepted, plain numbers rejected with feedback. Check graph colors update.

---

## PROMPT 6 — Commit FIXES-14 work

```
claude --dangerously-skip-permissions "Stage and commit all changes with the message 'FIXES-14: Walkthrough UI polish, mastery persistence, log-rules form checking

- Matrix LaTeX rendering fixed in walkthroughs (array environments)
- Row-reduce multiplier phrasing natural for negative multipliers
- Completed walkthrough steps remain fully visible
- MathLive virtual keyboard with full notation (integrals, trig, Greek, matrices)
- Optional video_id slot in walkthrough schema
- Mastery persists to database and dashboard (FIXES-8 item 1)
- Free topic access — prerequisite gate removed, all topics clickable (FIXES-8 item 2)
- log-rules generator rewritten: answers stay in log form, change-of-base removed, form checking added to practice flow
- Knowledge graph ready-to-learn color propagation fixed'. Then push to origin main. Do NOT stage __pycache__ or frontend/dist files."
```

---

## DEFERRED to next session (don't run tonight)

- **14-10 Review enforcement** — bigger feature, deserves its own session
- **14-11 AI-generate ~170 walkthroughs** — wait until all 6 gold standards are tested and the UI bugs (especially matrix rendering and MathLive keyboard) are fixed, since the generated templates will inherit any format problems
- **14-12 Video population** — separate content session

---

## Quick reference

| After changing | Do this |
|---|---|
| JSX/CSS only | refresh browser |
| Python or JSON | `docker compose restart backend` |
| package.json / Dockerfile | `docker compose up --build -d` |
| Containers missing | `docker compose up -d` |

Check containers: `docker compose ps` (should show backend AND frontend)
Backend logs: `docker compose logs backend --tail 50`
