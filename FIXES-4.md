FISHER APP 3.0 — ROUND 4: MATHLIVE FRACTION FORMAT FIX
======================================================

Priority: CRITICAL — this is the root cause of the fraction bug that has
persisted through Rounds 1-3.

Read this entire document before writing any code.

Project location: C:\Users\jjcas\Desktop\Fisher App\Fisher App 3.0\


========================================================================
ROOT CAUSE (CONFIRMED BY DIAGNOSTIC LOGS)
========================================================================

MathLive's .value property returns LaTeX fractions in TWO formats:

  FORMAT 1 (single-digit): \frac12      (no curly braces)
  FORMAT 2 (multi-digit):  \frac{15}{24} (with curly braces)

Both are valid LaTeX, but the answer checker's LaTeX parser ONLY handles
Format 2. When a student enters a single-digit fraction like 1/2, 5/6,
2/3, etc., MathLive sends \frac12 and the parser can't extract the
numerator and denominator, so it fails and returns is_correct: false.

Proof from backend diagnostic logs (real browser submissions):

  student='\\frac12'     correct='1/2'   → INCORRECT (bug)
  student='\\frac{3}{5}' correct='3/5'   → CORRECT  (works)
  student='5/8'          correct='5/8'   → CORRECT  (plain text works)

The \x0crac entries in the logs are from flawed curl tests (shell
escaping issue), not from the browser. Ignore them.


========================================================================
ITEM 1: FIX THE ANSWER CHECKER'S LATEX PREPROCESSING
========================================================================

In backend/app/services/answer_checker.py, add a preprocessing step
that normalizes MathLive's shorthand LaTeX BEFORE any parsing occurs.

The fix is a single regex substitution at the top of the check_answer
function (or in a normalize/preprocess function if one exists):

  import re

  # Normalize \fracAB → \frac{A}{B} for single-character arguments
  # MathLive sends \frac12 instead of \frac{1}{2} for single digits
  text = re.sub(r'\\frac([^{])([^{])', r'\\frac{\1}{\2}', text)

Apply this normalization to the student_answer string BEFORE it enters
the LaTeX-to-SymPy parsing pipeline. Apply it to BOTH the student answer
AND the correct answer, since either could be in either format.

IMPORTANT: This regex handles the case where MathLive omits braces for
single-character arguments. It should NOT break the already-working
\frac{15}{24} format because the { character won't match [^{].

Also check for these additional MathLive shorthand patterns while you're
at it:
  - \sqrt followed by single char without braces: \sqrt2 → \sqrt{2}
  - \log_ followed by single char: \log_2 → \log_{2}

Use the same [^{] pattern for these.

TESTING:

After implementing, run the existing test suite:
  docker compose run --rm backend python tests/test_answer_checker.py

Then add these NEW test cases to test_answer_checker.py and verify they
ALL pass:

  # MathLive shorthand (no braces)
  student="\\frac12",      correct="1/2"        → CORRECT
  student="\\frac56",      correct="5/6"        → CORRECT
  student="\\frac23",      correct="2/3"        → CORRECT

  # MathLive with braces (should still work)
  student="\\frac{1}{2}",  correct="1/2"        → CORRECT
  student="\\frac{5}{6}",  correct="5/6"        → CORRECT

  # Mixed: student shorthand, correct with braces (or vice versa)
  student="\\frac12",      correct="\\frac{1}{2}" → CORRECT
  student="\\frac{1}{2}",  correct="\\frac12"     → CORRECT

  # Plain text still works
  student="1/2",           correct="1/2"        → CORRECT
  student="5/6",           correct="\\frac{5}{6}" → CORRECT

  # Multi-digit fractions (already working, don't break them)
  student="\\frac{15}{24}", correct="5/8"       → CORRECT
  student="\\frac{10}{18}", correct="5/9"       → CORRECT

All existing tests must continue to pass.


========================================================================
ITEM 2: VERIFY END-TO-END VIA SIMULATED BROWSER SUBMISSION
========================================================================

After fixing the answer checker, simulate an actual browser submission
using Python inside the Docker container (NOT curl, which has escaping
issues):

  docker compose exec backend python3 -c "
  import json, urllib.request, sys
  sys.path.insert(0, '/app')

  # Register or login to get a token
  # ... (use existing test user or register new one)

  # Start a practice session for frac-simplify
  # Submit with MathLive shorthand format: \\frac12
  # Verify is_correct == true
  "

Also test with \\frac56, \\frac23, and \\frac{5}{6} formats.

If ANY of these return is_correct: false, the fix is incomplete.


========================================================================
ITEM 3: REMOVE DIAGNOSTIC LOGGING
========================================================================

After confirming the fix works, remove the temporary DIAG logging that
was added during the diagnostic phase:

1. backend/app/routers/practice.py — remove the DIAG log lines
2. backend/app/services/practice_service.py — remove the DIAG log lines
3. backend/app/main.py — revert the DEBUG log level overrides back to
   INFO (or whatever they were before)

Keep the answer checker's own internal logging at a reasonable level.


========================================================================
COMMIT AND PUSH
========================================================================

  docker compose up --build
  (test in browser — enter fraction answers using MathLive's fraction
   button, verify they are marked correct)

  git add -A
  git commit -m "FIXES-4: Fix MathLive fraction shorthand parsing (\\frac12 → \\frac{1}{2})"
  git push origin main
