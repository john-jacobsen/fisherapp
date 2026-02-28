FISHER APP 3.0 — ROUND 2 BUG FIXES AND FEATURES
=================================================

This document describes 10 fixes/features for Fisher App 3.0, Round 2.

Read PROMPT.md and FIXES.md first — they are the architecture spec and the
Round 1 implementation spec respectively. This document builds on top of
both. Do not modify PROMPT.md or FIXES.md.

Read this entire document before writing any code. Implement in the order
listed — the sequence matters because later items depend on earlier ones.

Project location: C:\Users\jjcas\Desktop\Fisher App\Fisher App 3.0\
GitHub repo: https://github.com/john-jacobsen/fisherapp

The app runs via Docker Compose (3 services: backend, frontend, db).
  Frontend: React 18+ / Vite at localhost:5173
  Backend: Python 3.11+ / FastAPI at localhost:8000
  Database: PostgreSQL 15 / SQLAlchemy ORM / Alembic migrations


========================================================================
VERSION CONTROL — COMMIT AND PUSH AFTER EACH ITEM
========================================================================

After completing each item, rebuild, test, then commit and push:

  docker compose up --build
  (test in browser at http://localhost:5173)

  git add -A
  git commit -m "FIXES-2 Item N: [brief description of what was done]"
  git push origin main


========================================================================
ITEM 1: FIX ANSWER CHECKER — CORRECT ANSWERS MARKED WRONG
========================================================================

Priority: CRITICAL — this is the highest-priority bug. Practice is unusable
until this is fixed.

PROBLEM:
When a student enters a correct answer (e.g., "5/9" for "Simplify 10/18"),
the app marks it incorrect. This happens for ALL fraction simplification
problems and likely other topics too. The answer checker from FIXES.md
Item 2 is not working correctly in production.

DIAGNOSIS STEPS:
1. Add detailed logging to the answer checking pipeline. For every answer
   submission, log:
   - The raw student_answer string received from the frontend
   - The raw correct_answer string from the database
   - The format of each (is it LaTeX? Plain text? MathLive output?)
   - Each comparison step attempted (symbolic, numeric, string)
   - The result of each comparison step
   - The final is_correct decision and why

2. Check the full pipeline end-to-end:
   - What does MathLive actually send when the student types "5/9"?
     It likely sends LaTeX like "\frac{5}{9}" — verify this.
   - What is stored in the problems table correct_answer column?
     Check seed_problems.py to see the format. It might be "5/9" as
     plain text, or "\frac{5}{9}" as LaTeX, or something else.
   - Does the practice router (backend/app/routers/practice.py) pass
     both values correctly to the answer checker service?
   - Does the answer checker parse both formats into SymPy correctly?

3. The most likely cause is a FORMAT MISMATCH:
   - Student sends LaTeX (\frac{5}{9}) but DB stores plain text (5/9)
   - Or the LaTeX-to-SymPy parser fails on one of the formats
   - Or the practice router is passing the wrong field name

FIX:
- Ensure the answer checker normalizes BOTH inputs (student answer AND
  correct answer) through the same LaTeX-to-SymPy parsing pipeline
- Add a plain-text parser as fallback: if the input doesn't look like
  LaTeX, try parsing it directly (e.g., "5/9" → Rational(5,9))
- Test EVERY topic after fixing:
    * Fraction simplification: "5/9" for "Simplify 10/18"
    * Fraction addition: "7/6" for "1/2 + 2/3"
    * Exponents: "x^5" for "x^2 · x^3"
    * Logarithms: "3" for "log_2(8)"
    * Solving equations: "5" for "2x + 3 = 13"
    * Summation: "10" for "sum_{i=1}^{4} i"
    * Combinatorics: "10" for "C(5,2)"
- Run these as automated tests in a test script, not just manual testing


========================================================================
ITEM 2: STOP AUTO-ADVANCING AFTER ANSWER SUBMISSION
========================================================================

Priority: HIGH — students can't review feedback before the next problem.

PROBLEM:
After submitting an answer, the practice screen immediately advances to
the next problem. Students need time to see whether they were right or
wrong, review the correct answer, and read the feedback.

FIX:
In PracticePage.jsx, after the answer is submitted and feedback is
received from the backend:

1. Show the feedback (correct/incorrect) with the correct answer displayed
   via MathDisplay. If the student was wrong, show both their answer and
   the correct answer side by side.

2. Show a brief one-line explanation if one exists in the problem data.
   If no explanation field exists, just show the correct answer.

3. Disable the MathLive input field and submit button (greyed out).

4. Show a "Next Problem →" button. The student stays on the current
   problem until they click this button.

5. Only when "Next Problem →" is clicked does the app fetch and display
   the next problem.

Do NOT auto-advance under any circumstances.


========================================================================
ITEM 3: TWO-MODE PRACTICE SYSTEM (LEARNING MODE + TEST MODE)
========================================================================

Priority: HIGH — core pedagogical feature, changes how practice works.

CURRENT STATE:
Practice mode is a single undifferentiated stream of problems. Hints and
AI are theoretically available but the system doesn't distinguish between
"learning" and "demonstrating mastery."

NEW DESIGN — TWO MODES:

The practice screen now has two distinct modes for each topic:

MODE 1: LEARNING MODE (default when entering practice)
- Full support available: all 3 hint levels accessible on demand, AI chat
  accessible on demand. No restrictions on when hints or AI can be used.
- Problems do NOT count toward mastery. The mastery meter does not change.
- The purpose is learning and exploration. Students can use as much help
  as they want.
- The UI should clearly indicate this is Learning Mode (e.g., a banner
  or label at the top: "Learning Mode — hints and AI available. Problems
  do not count toward mastery.")
- A prominent button: "Ready to Test →" that switches to Test Mode.
- Students can also go directly to Test Mode without doing any Learning
  Mode problems (via a "Skip to Test" option).

MODE 2: TEST MODE
- NO support available: hints panel is hidden, AI chat button is hidden.
  The student works independently.
- Problems DO count toward mastery. The mastery meter updates after each
  answer.
- The UI should clearly indicate this is Test Mode (e.g., "Test Mode —
  answer without help to demonstrate mastery.")
- To master a topic, the student must answer N questions correctly in
  Test Mode. Use the existing mastery threshold from the KST/BLIM engine
  (currently 0.85 in .env as BLIM_MASTERY_THRESHOLD). The backend already
  tracks this — the change is that ONLY Test Mode answers feed into it.
- A "Back to Learning" button lets the student return to Learning Mode
  at any time if they realize they need more practice. This does NOT
  reset their Test Mode progress.
- When mastery is achieved, show a celebration/success message and
  navigate to the score report or dashboard.

IMPLEMENTATION:

Backend changes:
- The POST /api/practice/{node_id}/submit endpoint needs a new field in
  the request body: "mode": "learning" | "test"
- When mode is "learning": record the response in response_logs (for
  analytics) but do NOT update the BLIM posterior or BKT mastery estimate.
  Return feedback (correct/incorrect + correct answer) as normal.
- When mode is "test": process exactly as currently implemented — update
  BLIM posterior, BKT mastery, check mastery threshold, update fringe.

Frontend changes:
- PracticePage.jsx: Add state for current mode ("learning" or "test").
  Default to "learning" when first entering practice for a topic.
- Conditionally render hints panel and AI chat button based on mode.
- Conditionally show/hide the mastery meter (show in both modes, but
  only animate changes in Test Mode).
- Add "Ready to Test →" and "Back to Learning" toggle buttons.
- Add "Skip to Test" link/button visible in Learning Mode.
- Send the mode field in the submit request body.
- Update the mode indicator banner based on current mode.

This is deliberately simple. No progressive scaffolding, no hint fading,
no tracking of what level of help the student needs. Just an on/off
switch between "learning with support" and "testing without support."


========================================================================
ITEM 4: ON-THE-FLY PROBLEM GENERATION
========================================================================

Priority: HIGH — needed for adequate problem variety.

PROBLEM:
Problems are generated once at seed time and stored in the database.
The same 10 problems per node cycle repeatedly. Students quickly memorize
the answers rather than learning the skill.

FIX:
Move problem generation from seed-time to request-time:

1. The problem generators already exist in generate_problems.py. Refactor
   them into a service module (e.g., backend/app/services/problem_generator.py)
   that can be called at runtime.

2. When POST /api/practice/{node_id}/start is called:
   - First, try to generate a fresh problem on-the-fly using the generator
     for that node_id.
   - If the generator succeeds, return the generated problem. Do NOT store
     it in the database (it's ephemeral).
   - If the generator fails or no generator exists for that node_id, fall
     back to selecting a random problem from the database (existing behavior).
   - Ensure the generated problem includes the correct_answer in the same
     format the answer checker expects.

3. The response format to the frontend must remain the same regardless of
   whether the problem was generated on-the-fly or pulled from the database.
   The frontend should not need to know the difference.

4. Keep the seeded problems in the database as fallback. Don't delete them.

5. Ensure each generator produces problems with correct LaTeX formatting
   in the problem_text and correct_answer fields.


========================================================================
ITEM 5: FIX BROKEN LATEX RENDERING IN PRACTICE
========================================================================

Priority: HIGH — math displays as garbled text.

PROBLEM:
The practice screen shows broken LaTeX like:
  "Simplify: x²\( · x³\)"
with raw \( and \) delimiters visible instead of being rendered.

The MathDisplay component from FIXES.md Item 1 is not handling all
LaTeX delimiter formats correctly.

FIX:
1. Open frontend/src/components/MathDisplay.jsx

2. The component's regex or parsing logic needs to handle ALL of these
   delimiter formats that may appear in problem text:
   - \( ... \)  (inline math delimiters)
   - \[ ... \]  (display math delimiters)
   - $ ... $    (single dollar inline)
   - $$ ... $$  (double dollar display)
   - Raw LaTeX commands with no delimiters (e.g., \frac{2}{3})

3. The component should:
   - Strip existing delimiters before passing to MathJax
   - OR ensure MathJax is configured to recognize all delimiter types
   - Treat the ENTIRE math portion of the string as a single MathJax
     expression rather than trying to render fragments separately

4. Test with these exact strings from the database:
   - "Simplify: x²\( · x³\)"
   - "Evaluate: \sum_{i=1}^{4} i"
   - "Simplify: \log_2(4) + \log_2(8)"
   - "Multiply: \frac{2}{3} \times \frac{3}{4}"
   - Mixed content with both plain text and LaTeX

5. Also check that MathJax.typesetPromise() is being called after
   dynamic content updates (switching problems, loading hints, etc.)
   as specified in FIXES.md Item 1.


========================================================================
ITEM 6: FIX HINTS NOT LOADING
========================================================================

Priority: HIGH — hints show "Loading hints..." indefinitely.

PROBLEM:
The practice page hints panel shows "Loading hints..." and never
resolves. This means either:
- The hints API endpoint is failing
- The hints aren't seeded for the relevant problems
- The frontend is requesting hints with wrong parameters

DIAGNOSIS:
1. Check the backend logs when hints are requested. Is the endpoint
   being called? What's the response?

2. Check the hints table in the database:
   docker compose exec db psql -U fisher -d fisherapp -c \
     "SELECT h.id, h.problem_id, h.level, LEFT(h.content, 50) FROM hints h LIMIT 20;"
   
   Are there hints? Are they associated with the right problem IDs?

3. Check the frontend request: what URL is it calling? What parameters?
   Compare with what the backend expects.

FIX:
- Fix whatever is broken in the pipeline (endpoint, data, or request)
- Add error handling: if hints fail to load after 5 seconds, show
  "No hints available for this problem" instead of infinite loading
- Ensure hints render through MathDisplay for proper LaTeX formatting
- Verify hints work in Learning Mode (visible) and are hidden in Test Mode


========================================================================
ITEM 7: FIX LESSON TEXT AND WORKED EXAMPLE FORMATTING
========================================================================

Priority: MEDIUM — lessons are readable but ugly.

PROBLEM:
Lesson text and worked examples lack proper LaTeX formatting. Math
expressions appear as plain text (e.g., "a/b" instead of rendered
fractions). The worked example steps are also not fully fleshed out.

FIX:
1. Update seed_lessons.py to use proper LaTeX notation in all lesson
   content. Every mathematical expression should be wrapped in LaTeX:
   - Fractions: \frac{a}{b} not a/b
   - Exponents: x^{2} not x^2 or x²
   - Operations: \times not *, \div not /, \cdot not ·
   - Special functions: \log, \sum, \binom, etc.

2. Update seed_problems.py worked examples similarly — all math in
   LaTeX notation.

3. Ensure the lesson page (LessonPage.jsx) renders all text content
   through the MathDisplay component, not just plain HTML/markdown.

4. Ensure worked example steps are rendered through MathDisplay.

5. Re-run seed scripts after updating:
   docker compose run --rm backend python scripts/seed_lessons.py
   docker compose run --rm backend python scripts/seed_problems.py


========================================================================
ITEM 8: YOUTUBE SEARCH FALLBACK FOR MISSING VIDEOS
========================================================================

Priority: MEDIUM — some lesson videos don't load.

PROBLEM:
Some lesson pages have dead or placeholder YouTube links. The video
embed shows a broken/blank player.

FIX:
1. In the lesson page video section, detect when a YouTube embed fails
   to load (onerror on iframe, or check if the video_url is null/empty
   or a known placeholder).

2. When video is unavailable, instead of showing a broken player, show:
   - A clean placeholder box with a message: "No video available for
     this topic yet."
   - A button: "Search YouTube →" that opens a new browser tab with a
     YouTube search URL pre-filled with the topic name. The URL format:
     https://www.youtube.com/results?search_query=how+to+[topic+name]+algebra
   - Example: for "Simplifying Fractions", the button opens:
     https://www.youtube.com/results?search_query=how+to+simplify+fractions+algebra

3. This requires NO API key and NO backend changes. It's purely a
   frontend fallback in the VideoEmbed component.


========================================================================
ITEM 9: SHOW CORRECT ANSWER AFTER INCORRECT SUBMISSION
========================================================================

Priority: MEDIUM — students need to see what the right answer was.

PROBLEM:
When a student submits a wrong answer, the feedback just says "Incorrect"
but doesn't show the correct answer. Students can't learn from mistakes
if they don't see the right answer.

NOTE: This overlaps with Item 2 (stop auto-advancing). Implement them
together. After an incorrect submission:

1. Show "Incorrect" feedback clearly (red text or indicator)
2. Show the student's submitted answer (rendered via MathDisplay)
3. Show the correct answer (rendered via MathDisplay): "The correct
   answer is: [correct_answer]"
4. The backend already returns the correct answer in the submit response
   (check the response payload). If it doesn't, add it.
5. In Learning Mode, also show a "Review Hint" button that expands the
   hint panel so the student can understand why.
6. In Test Mode, just show the correct answer with no hints.
7. The "Next Problem →" button (from Item 2) appears below all of this.


========================================================================
ITEM 10: PROBLEM RANDOMIZATION — DON'T REPEAT UNTIL POOL EXHAUSTED
========================================================================

Priority: LOW — nice to have, improves experience.

PROBLEM:
When falling back to database problems (before on-the-fly generation is
working for all topics), students may see the same problem twice in a
row.

FIX:
For database-sourced problems only (not on-the-fly generated ones):
1. Track which problem IDs the student has seen in the current practice
   session (store in session state or response_logs).
2. When selecting the next problem, exclude already-seen IDs.
3. When all problems in the pool have been seen, reset the seen list
   and start over (shuffle order).
4. This is a backend change in the problem selection logic of the
   practice service.


========================================================================
IMPLEMENTATION ORDER
========================================================================

1. Item 1  — Fix answer checker (CRITICAL, everything else is pointless
             without correct answer checking)
2. Item 5  — Fix broken LaTeX rendering (needed to see problems properly)
3. Item 6  — Fix hints loading (needed before building two-mode system)
4. Item 2  — Stop auto-advancing + show feedback (Items 2 and 9 together)
   Item 9  — Show correct answer after wrong submission (implement with 2)
5. Item 3  — Two-mode practice system (Learning + Test)
6. Item 4  — On-the-fly problem generation
7. Item 7  — Fix lesson/worked example formatting (re-run seeds)
8. Item 8  — YouTube search fallback
9. Item 10 — Problem randomization (no repeats)

After each item:
  1. Rebuild: docker compose up --build
  2. Test in browser: http://localhost:5173
  3. Commit and push:
       git add -A
       git commit -m "FIXES-2 Item N: [brief description]"
       git push origin main

If seed scripts need re-running:
  docker compose run --rm backend python scripts/seed_lessons.py
  docker compose run --rm backend python scripts/seed_problems.py
  docker compose run --rm backend python scripts/generate_problems.py


========================================================================
DESIGN PRINCIPLES
========================================================================

- Two practice modes: Learning (full support, no mastery credit) and
  Test (no support, mastery credit). Simple on/off, no progressive
  scaffolding complexity.
- Students always have the option to skip Learning Mode and go straight
  to Test Mode if they're confident.
- The answer checker must be reliable above all else. Log everything.
  When in doubt, show the student the correct answer so they can
  self-assess even if the checker fails.
- On-the-fly problem generation provides variety without bloating the
  database. Fall back to stored problems when generators don't exist.
- All math content must render correctly via MathJax. No raw LaTeX
  visible to students anywhere.
- Keep the frontend simple. No complex state tracking for hint levels
  or scaffolding progression.
