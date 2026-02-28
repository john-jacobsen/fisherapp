FISHER APP 3.0 — ROUND 3 BUG FIXES AND FEATURES
=================================================

This document describes 11 fixes for Fisher App 3.0, Round 3.

Read PROMPT.md, FIXES.md, and FIXES-2.md first — they are the architecture
spec and the Round 1 and Round 2 implementation specs. This document builds
on all of them. Do not modify those files.

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
  git commit -m "FIXES-3 Item N: [brief description of what was done]"
  git push origin main


========================================================================
ITEM 1: OVERHAUL ANSWER CHECKER — THIS IS THE #1 PRIORITY
========================================================================

Priority: CRITICAL — the single most important fix in this round. Every
other feature is degraded if the answer checker marks correct answers wrong.

THE CORE PROBLEM:
The answer checker fails in two categories:
  A) FORMAT MISMATCH: MathLive sends LaTeX (e.g., \frac{5}{6}) but the
     database stores plain text (e.g., 5/6). The checker does not normalize
     both inputs to a common representation before comparing.
  B) MULTI-VALUE ANSWERS: Problems with multiple solutions (quadratics,
     absolute value) expect a single expression, but students naturally
     write things like "x = 2, 3" or "2, 3" or "{2, 3}".

FIX PART A — FORMAT NORMALIZATION:

The answer checker (backend/app/services/answer_checker.py) must normalize
ALL inputs through a unified pipeline before comparison:

1. Detect if input is LaTeX or plain text:
   - Contains \frac, \sqrt, \log, \sum, \binom, or other LaTeX commands
     → treat as LaTeX
   - Otherwise → treat as plain text

2. Parse to SymPy regardless of input format:
   - LaTeX input: use latex2sympy or a custom parser to convert to SymPy
   - Plain text input: use sympify() with appropriate transformations
     (e.g., "5/6" → Rational(5,6), "x^2" → x**2)

3. Compare the two SymPy expressions using:
   - simplify(student - correct) == 0
   - If that fails: student.equals(correct)
   - If that fails: numeric evaluation at random test points
   - If that fails: normalized string comparison as last resort

4. IMPORTANT — handle these specific plain text formats that students
   commonly type:
   - "5/6" → Rational(5, 6)
   - "x^2" → x**2
   - "2x" → 2*x (implicit multiplication)
   - "log2(8)" or "log_2(8)" → log(8, 2)
   - "sqrt(4)" → sqrt(4)
   - Plain integers: "3", "42", "-7"
   - Decimals: "0.5", "3.14"

FIX PART B — MULTI-VALUE ANSWERS (SOLUTION SETS):

For problems that have multiple solutions (e.g., "Solve x² - 5x + 6 = 0"):

1. The correct_answer in the database should store multi-value answers
   in a consistent format. Check what's currently stored and decide on a
   canonical format. Recommended: store as a comma-separated string of
   values, e.g., "2, 3" or as a set notation "{2, 3}".

2. The answer checker must detect when a problem expects multiple values
   and compare as SETS, not strings. All of these student inputs should
   be marked correct for the solution {2, 3}:
   - "2, 3"
   - "3, 2"  (order doesn't matter)
   - "x = 2, 3"
   - "x = 2, x = 3"
   - "x=2 and x=3"
   - "{2, 3}"
   - "\{2, 3\}" (LaTeX set notation)

3. Implementation approach:
   - Check if student answer contains commas, "and", or set braces
   - If yes: split into individual values, parse each to SymPy, compare
     as a set against the parsed correct answer set
   - If no: compare as a single value against each element of the correct
     set (in case the problem accepts partial answers — but prefer full set)

4. For the seed data and problem generators, ensure problems with multiple
   solutions store their answers in the canonical multi-value format.

TESTING — MANDATORY BEFORE MOVING TO ITEM 2:

After implementing the fix, write and run an automated test script that
verifies ALL of these cases pass:

  # Fractions
  student="\frac{5}{6}", correct="5/6"         → CORRECT
  student="5/6",          correct="\frac{5}{6}" → CORRECT
  student="\frac{1}{2}",  correct="1/2"         → CORRECT
  student="1/2",          correct="0.5"         → CORRECT

  # Exponents
  student="x^{12}",       correct="x^12"        → CORRECT
  student="x^12",         correct="x^{12}"      → CORRECT

  # Integers
  student="20",           correct="20"           → CORRECT
  student="21",           correct="20"           → INCORRECT
  student="-7",           correct="-7"           → CORRECT

  # Logarithms
  student="3",            correct="3"            → CORRECT
  student="\log_{2}(8)",  correct="3"            → CORRECT

  # Solution sets (quadratics)
  student="2, 3",         correct="2, 3"         → CORRECT
  student="3, 2",         correct="2, 3"         → CORRECT
  student="x = 2, 3",     correct="2, 3"         → CORRECT
  student="x=2, x=3",     correct="2, 3"         → CORRECT
  student="{2, 3}",       correct="2, 3"         → CORRECT
  student="2",            correct="2, 3"         → INCORRECT (partial)
  student="2, 4",         correct="2, 3"         → INCORRECT

  # Expressions
  student="2x + 3",       correct="3 + 2x"       → CORRECT (commutativity)
  student="\frac{x}{2}",  correct="x/2"          → CORRECT

Log the result of EVERY test case to the console. If any fail, fix the
checker before proceeding. Save this test script as:
  backend/tests/test_answer_checker.py

So it can be re-run after future changes.


========================================================================
ITEM 2: FIX SUBMISSION ERRORS (500 ERRORS ON SOME TOPICS)
========================================================================

Priority: CRITICAL — some topics are completely unusable.

PROBLEM:
Submitting answers for certain topics (confirmed: Product Rule for
Exponents, Sigma Notation) shows "Submission error. Please try again."
This is almost certainly a 500 error from the backend — the answer checker
is crashing instead of returning a result.

DIAGNOSIS:
1. Check the backend logs (docker compose logs backend) for tracebacks
   when submitting answers for these topics.

2. The most likely cause: the answer checker's LaTeX parser encounters
   an expression format it can't handle and throws an unhandled exception
   instead of gracefully falling back.

FIX:
1. Wrap the entire answer checking pipeline in a try/except. If ANY step
   throws an exception, catch it, log the full traceback with the student
   answer and correct answer, and return a structured error response:
   {
     "is_correct": false,
     "error": true,
     "message": "Could not evaluate your answer. Please try a different format.",
     "correct_answer": "[the correct answer from the DB]"
   }

2. The frontend should handle this error response gracefully:
   - Show the message to the student
   - Show the correct answer
   - Allow them to proceed to the next problem
   - Do NOT count this as an incorrect answer for mastery purposes

3. After adding the error handling, test submissions for EVERY topic:
   - Fraction simplification
   - Fraction addition (like and unlike denominators)
   - Fraction multiplication and division
   - Exponent rules (product, power, negative/zero, combining)
   - Order of operations (PEMDAS, nested)
   - Solving equations (one-step through quadratics)
   - Logarithms (definition, rules, solving)
   - Summation notation (basic, arithmetic, nested)
   - Combinatorics (counting, permutations, combinations)
   - Geometric series (sequences, finite, infinite)

   Log which topics still produce errors even with the fallback, so they
   can be investigated further.


========================================================================
ITEM 3: PLACEMENT TEST — STOP AUTO-ADVANCING
========================================================================

Priority: HIGH — placement test moves too fast for students to read feedback.

PROBLEM:
After answering a placement question, the test immediately advances to
the next question. Students can't see whether they were right or wrong.

FIX:
In the placement question page (frontend/src/pages/PlacementQuestion.jsx
or equivalent):

1. After the student submits an answer and feedback is received:
   - Show "✓ Correct" or "✗ Incorrect" (do NOT show the correct answer
     for placement — we don't want students memorizing answers)
   - Disable the MathLive input and submit button
   - Show a "Next Question →" button

2. Only advance to the next question when the student clicks
   "Next Question →"

3. Do NOT auto-advance under any circumstances.

4. The placement completion screen (results) should still work as before
   after the last question.


========================================================================
ITEM 4: PLACEMENT TEST — RANDOMIZE PROBLEM NUMBERS
========================================================================

Priority: HIGH — every student sees identical placement problems.

PROBLEM:
The placement test presents the same problems with the same numbers every
time, even across different accounts. The KST adaptive algorithm correctly
selects WHICH topics to test, but the specific problem instances are
always the same because they're pulled from a fixed pool in the database.

FIX:
Use the same on-the-fly problem generation approach from FIXES-2 Item 4,
but apply it to placement as well:

1. When the placement service selects a node to test, instead of picking
   a stored problem from the database, call the problem generator to
   create a fresh problem with randomized numbers.

2. The FORM of the problem stays the same (e.g., "Solve for x: x + a = b"
   for one-step equations), but the specific numbers (a and b) are
   randomly generated each time.

3. Fall back to database problems if no generator exists for that node.

4. Ensure the generated problem's correct_answer is computed correctly
   by the generator (using SymPy or direct calculation).

5. The placement service should pass the generated problem to the same
   answer checking pipeline, so format consistency matters.

IMPORTANT: Do NOT change how the KST algorithm selects which nodes to
test. Only change how the specific problem instance is generated for the
selected node.


========================================================================
ITEM 5: LOGIN ERROR — STOP PAGE REFRESH ON WRONG PASSWORD
========================================================================

Priority: MEDIUM — usability issue.

PROBLEM:
When a user enters a wrong password, an error message briefly flashes
but then the page refreshes, clearing the message and the email field.
The user doesn't have time to read the error.

FIX:
In the login page (frontend/src/pages/LoginPage.jsx):

1. The form submit handler is likely not calling event.preventDefault(),
   causing the browser's default form submission (which triggers a page
   reload).

2. Ensure the login handler:
   - Calls e.preventDefault() on form submission
   - Makes the API call (POST /api/auth/login)
   - On failure: sets an error state that displays a persistent error
     message (e.g., "Incorrect email or password. Please try again.")
   - The error message stays visible until the user tries again
   - The email field should remain populated (don't clear it)
   - Only the password field should be cleared

3. Test: enter wrong password 3 times in a row. The error message should
   appear each time, the email should stay filled, and the page should
   never refresh.


========================================================================
ITEM 6: HINTS FOR ON-THE-FLY GENERATED PROBLEMS
========================================================================

Priority: MEDIUM — hints show "No hints available" for generated problems.

PROBLEM:
On-the-fly generated problems (from FIXES-2 Item 4) have no associated
hints in the database, so the hints panel shows "No hints available for
this problem." This defeats the purpose of Learning Mode.

FIX:
When generating a problem on-the-fly, also generate hints:

1. Each problem generator should return not just the problem_text and
   correct_answer, but also 3 hint levels:
   - Hint 1 (conceptual): e.g., "To simplify a fraction, find a number
     that divides both the numerator and denominator."
   - Hint 2 (strategic): e.g., "Find the GCD of [numerator] and
     [denominator]."
   - Hint 3 (procedural/bottom-out): e.g., "The GCD of 20 and 24 is 4.
     Divide both by 4: \frac{20 \div 4}{24 \div 4} = \frac{5}{6}"

2. Hint 3 should use the ACTUAL numbers from the generated problem, not
   generic placeholders. Hints 1 and 2 can be more generic per-topic
   templates.

3. The practice endpoint should return these hints alongside the problem
   data, in the same format the frontend expects.

4. The frontend hint panel should work identically whether the hints
   came from the database or were generated on-the-fly.

5. If hint generation fails or a generator doesn't support hints, fall
   back to topic-level generic hints (one set per node_id, stored as
   templates). Example for frac-simplify:
   - "What number divides both the numerator and denominator?"
   - "Try finding the greatest common factor."
   - "Divide numerator and denominator by their GCF to get the answer."


========================================================================
ITEM 7: FIX VIDEO EMBED FALLBACK
========================================================================

Priority: MEDIUM — broken video embeds on lesson pages.

PROBLEM:
Many lesson pages show broken or blank video embeds because the YouTube
URLs in the seed data are dead or placeholder links. The YouTube search
fallback from FIXES-2 Item 8 is either not implemented or not detecting
the broken embeds.

FIX:
1. In the video embed component (frontend/src/components/VideoEmbed.jsx
   or wherever the YouTube iframe is rendered):

   - Check if the video_url is null, empty, undefined, or a known
     placeholder string (like "https://youtube.com" with no video ID)
   - If the URL looks valid (contains a YouTube video ID), attempt to
     render the iframe
   - Add an onError handler to the iframe to catch load failures

2. When video is unavailable (bad URL, null, or load error), show:
   - A clean placeholder box (light gray background, same dimensions
     as a video would be)
   - Text: "No video available for this topic."
   - A button styled as a link: "Search YouTube for this topic →"
   - The button opens a NEW browser tab (target="_blank") with URL:
     https://www.youtube.com/results?search_query=[topic+name]+algebra+tutorial
   - URL-encode the topic name. Example for "Simplifying Fractions":
     https://www.youtube.com/results?search_query=simplifying+fractions+algebra+tutorial

3. Do NOT use YouTube API. This is purely a link to YouTube search.


========================================================================
ITEM 8: PRACTICE PROBLEM GENERATION — ENSURE ALL TOPICS COVERED
========================================================================

Priority: MEDIUM — some topics may have no working problem generator.

PROBLEM:
On-the-fly generation was added in FIXES-2, but it may not cover all 30
nodes. Topics without a generator fall back to database problems, which
are limited.

FIX:
1. Audit which nodes have working on-the-fly generators by checking
   backend/app/services/problem_generator.py (or wherever generators
   were placed).

2. For each of the 30 knowledge nodes, ensure there is a generator that:
   - Produces a valid problem_text with proper LaTeX formatting
   - Computes a correct_answer that the answer checker can verify
   - Randomizes the numbers in the problem each time
   - Generates 3 hints (per Item 6 above)

3. The generators should produce problems of VARYING DIFFICULTY within
   each topic. For example, fraction simplification:
   - Easy: \frac{4}{8} (GCD is obvious)
   - Medium: \frac{15}{25} (requires finding GCD = 5)
   - Hard: \frac{48}{72} (GCD = 24, less obvious)
   Use random ranges for the numbers that produce this natural variation.

4. For topics where writing a generator is complex (e.g., solving
   quadratics), the generator can use SymPy:
   - Pick random integer roots (e.g., r1=2, r2=3)
   - Construct the equation: (x - r1)(x - r2) = 0 → expand to standard form
   - The correct_answer is already known: "{r1}, {r2}"
   - This guarantees nice integer answers

5. Print a summary at the end: "Generators available for N/30 nodes.
   Missing: [list of node_ids without generators]."


========================================================================
ITEM 9: MASTERY AND SCORE FLOW AFTER PRACTICE
========================================================================

Priority: MEDIUM — verify the full learning loop works end-to-end.

CHECK AND FIX:
1. In Test Mode, does the mastery meter actually update after each
   correct answer? The BLIM posterior should be updating. Verify by:
   - Start Test Mode on a topic
   - Answer 5 questions correctly in a row
   - The mastery meter should visibly increase
   - If it doesn't, debug the submit endpoint to ensure BLIM updates
     are being applied when mode is "test"

2. When mastery reaches the threshold (0.85), what happens?
   - The app should show a success/celebration message
   - Then navigate to a score report or back to the dashboard
   - If nothing happens, add this logic to PracticePage.jsx:
     check the mastery value in the submit response, and when it
     crosses 0.85, show a modal or message and offer navigation
     to the dashboard

3. Does the dashboard knowledge map update after mastering a topic?
   - The node should change color/status from "in progress" to "mastered"
   - Newly unlocked topics (outer fringe) should become accessible
   - If the map doesn't update, the issue is in the dashboard API
     not reflecting the updated BLIM state

4. Does "Finish Session" on the practice page lead to a score report?
   - If there's no score report page, ensure it navigates back to
     the dashboard with updated mastery shown

5. After mastering a topic, does it appear in the Reviews page with
   a scheduled review date?


========================================================================
ITEM 10: REVIEW SYSTEM — VERIFY FUNCTIONALITY
========================================================================

Priority: LOW — verify existing implementation works.

CHECK AND FIX:
1. Navigate to the Reviews page. Does it load without errors?

2. If a topic has been mastered, does it show in the review queue with
   a scheduled date?

3. Can the student start a review session? Does it pull up practice
   problems for the mastered topic?

4. If the Reviews page is blank or errors out, check:
   - Is the /api/review/due endpoint working? (Test with curl or
     browser dev tools)
   - Is the ReviewSchedule being created when a topic is mastered?
   - Is the frontend making the correct API call?

5. If reviews are fundamentally broken, implement the minimum viable
   version:
   - When a node reaches mastery, create a ReviewSchedule record with
     next_review_date = now + 1 day
   - /api/review/due returns nodes where next_review_date <= now
   - Review page shows these nodes with a "Review" button
   - Review practice works exactly like Test Mode practice
   - After a successful review (3 correct in a row), update
     next_review_date using SM-2 intervals: 1 → 3 → 7 → 14 → 30 days


========================================================================
ITEM 11: SETTINGS PAGE — VERIFY AND FIX
========================================================================

Priority: LOW — verify existing implementation works.

CHECK AND FIX:
1. Does the Settings page load?
2. Does it show user profile information (name, email)?
3. Can the user update their name?
4. Is the AI API key setup interface present?
   - Can the user enter an API key?
   - Does it save to localStorage (NOT to the backend)?
   - Does the AI chat button in Learning Mode practice use this key?
5. If the Settings page is broken, fix the minimum: display name and
   email, allow name update, show AI key input that saves to localStorage.


========================================================================
IMPLEMENTATION ORDER
========================================================================

1. Item 1  — Overhaul answer checker (CRITICAL, blocks everything)
2. Item 2  — Fix submission errors / 500s (CRITICAL)
3. Item 3  — Placement test: stop auto-advancing
4. Item 4  — Placement test: randomize problem numbers
5. Item 5  — Login: fix page refresh on wrong password
6. Item 6  — Generate hints for on-the-fly problems
7. Item 7  — Fix video embed fallback
8. Item 8  — Ensure all 30 nodes have problem generators
9. Item 9  — Verify mastery/score flow end-to-end
10. Item 10 — Verify review system
11. Item 11 — Verify settings page

After each item:
  1. Rebuild: docker compose up --build
  2. Test in browser: http://localhost:5173
  3. Commit and push:
       git add -A
       git commit -m "FIXES-3 Item N: [brief description]"
       git push origin main

If seed scripts need re-running:
  docker compose run --rm backend python scripts/seed_lessons.py
  docker compose run --rm backend python scripts/seed_problems.py
  docker compose run --rm backend python scripts/generate_problems.py


========================================================================
MANDATORY TESTING AFTER ALL ITEMS COMPLETE
========================================================================

Before committing the final state, run through this checklist and log
results to a file (backend/tests/TESTING-RESULTS.txt):

ANSWER CHECKER:
  [ ] Run backend/tests/test_answer_checker.py — all cases pass
  [ ] Fractions: submit \frac{5}{6} for correct answer 5/6 → Correct
  [ ] Integers: submit 20 for correct answer 20 → Correct
  [ ] Exponents: submit x^{12} for correct answer x^12 → Correct
  [ ] Solution sets: submit "2, 3" for correct answer "2, 3" → Correct
  [ ] Solution sets: submit "3, 2" for correct answer "2, 3" → Correct
  [ ] No submission errors (500s) on any topic

PLACEMENT TEST:
  [ ] Does not auto-advance — "Next Question →" button required
  [ ] Two different accounts see different numbers in problems
  [ ] Shows Correct/Incorrect without revealing the answer
  [ ] Completes and shows results page

PRACTICE — LEARNING MODE:
  [ ] Banner shows "Learning Mode"
  [ ] Hints load (not "No hints available") for at least 3 topics
  [ ] AI chat button visible
  [ ] Answers do not affect mastery meter
  [ ] "Ready to Test" switches to Test Mode

PRACTICE — TEST MODE:
  [ ] Banner shows "Test Mode"
  [ ] Hints and AI hidden
  [ ] Correct answers increase mastery meter
  [ ] Mastery threshold triggers success message

LOGIN:
  [ ] Wrong password shows persistent error, no page refresh
  [ ] Email field stays populated after failed attempt

LESSONS:
  [ ] Video loads or fallback "Search YouTube" button appears
  [ ] Lesson text renders LaTeX correctly
  [ ] Worked examples render with LaTeX

DASHBOARD:
  [ ] Knowledge map loads and shows mastery colors
  [ ] Mastered topics reflected after practice

Log any remaining issues to the TESTING-RESULTS.txt file.


========================================================================
DESIGN PRINCIPLES
========================================================================

- The answer checker is the foundation. It must be robust, well-tested,
  and gracefully handle any input without crashing.
- Never crash on bad input. Always catch exceptions, log them, show the
  student the correct answer, and let them continue.
- Generators should produce problems with random numbers but predictable
  structure. Use SymPy to compute correct answers so they're always right.
- Hints should be available for every problem, generated or stored.
- Keep the UI simple. Correct/Incorrect feedback, Next button, clear
  mode indicators. No complex state machines.
