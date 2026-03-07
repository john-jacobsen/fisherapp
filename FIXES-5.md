FISHER APP 3.0 — ROUND 5: FINAL MAJOR FIXES
=============================================

This is the final major fix round before moving to content development.
Read PROMPT.md, FIXES.md, FIXES-2.md, FIXES-3.md, and FIXES-4.md for
full context. This document builds on all of them.

Read this entire document before writing any code. Implement in the order
listed.

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
  git commit -m "FIXES-5 Item N: [brief description of what was done]"
  git push origin main


========================================================================
ITEM 1: FIX 400 BAD REQUEST ON 3RD PROBLEM (CRITICAL)
========================================================================

Priority: CRITICAL — practice sessions break after exactly 2 problems
every time, on every topic. This blocks all practice and testing.

SYMPTOMS:
- Problem 1: submit → 200 OK
- Problem 2: submit → 200 OK
- Problem 3: submit → 400 Bad Request
- Frontend shows "Connection error — your answer could not be submitted."
- Session is stuck — user cannot continue.

This pattern repeats across all topics (confirmed: fractions, exponents).

DIAGNOSIS STEPS:
1. First, add TEMPORARY detailed logging to find the exact cause.
   In the practice router's submit handler, BEFORE calling the service,
   log the full request body:

     logger.info("SUBMIT DEBUG: node=%s body=%r", node_id, req.dict())

2. In the practice_service.submit_practice_answer function, add logging
   at EVERY point where it could return a 400 or raise an HTTPException.
   The 400 means the backend is explicitly rejecting the request — find
   which line of code produces it.

3. Rebuild and reproduce the bug by submitting 3 answers in a row.
   Check docker compose logs backend for the exact error.

LIKELY CAUSES (investigate in order):

A) STALE PROBLEM_ID: The frontend sends a problem_id that the backend
   doesn't recognize. On-the-fly generated problems are ephemeral and
   stored in a session cache. If the cache has a size limit of 2, or
   if the "next problem" flow isn't storing the new problem_id in the
   cache, the 3rd submit will fail with "Problem not found."

   CHECK: In practice_service.py, find where ephemeral problems are
   stored (likely a dict keyed by session_id or problem_id). Check if
   there's a limit, if old problems are evicted, or if the problem_id
   from the /start response matches what the frontend sends back.

B) SESSION STATE CORRUPTION: The seen_problems tracking (from FIXES-2
   Item 10) might be breaking the session. If it's trying to find a
   new unseen problem and failing, or if it's corrupting the session
   state after 2 problems.

   CHECK: Look at how seen_problem_ids are tracked and whether the
   session becomes invalid after accumulating 2 entries.

C) PROBLEM GENERATION FAILURE: After 2 problems, the generator might
   fail to produce a 3rd, and the error isn't handled gracefully.

   CHECK: The /start endpoint is returning 200 OK for the 3rd problem
   (visible in the logs), so this is less likely — the problem is
   generated fine, but the SUBMIT for it fails.

D) MODE FIELD ISSUE: Check if the 3rd submit is missing the "mode"
   field or sending an unexpected value, causing validation to reject it.

FIX:
- Whatever the cause, fix it so that practice sessions can continue
  indefinitely (at least 20+ problems without error).
- After fixing, test by answering 10 problems in a row on exponents.
  All 10 must submit successfully with 200 OK.

IMPORTANT: Remove the temporary debug logging after finding and fixing
the cause.


========================================================================
ITEM 2: FIX MASTERY METER STUCK AT 20%
========================================================================

Priority: CRITICAL — mastery never advances, so students can never
master topics or unlock new ones.

SYMPTOMS:
- Mastery meter shows 20% and never changes, even after correct answers
  in Test Mode.
- This is partially caused by Item 1 (sessions break at problem 3),
  but may also have its own root cause.

DIAGNOSIS:
After fixing Item 1 (so sessions don't break), test in TEST MODE:

1. Switch to Test Mode on a topic
2. Answer 5 problems correctly in a row
3. After each correct answer, check the submit response payload —
   does it include an updated mastery value?

If the mastery value in the response never changes:

CHECK the BLIM posterior update logic in practice_service.py:
- Is the BLIM update code actually being reached when mode="test"?
- Is the posterior being calculated correctly?
- Is it being saved back to the StudentState record?
- Is the response including the new mastery value?

CHECK the initial mastery value:
- When a new StudentState is created, what's the initial posterior?
  If it's 0.2 (20%), that explains the starting value.
- The BLIM update formula should increase the posterior toward 1.0
  after each correct answer. If the formula is wrong or the update
  isn't being persisted, it'll stay at 0.2 forever.

Also check the frontend:
- Does PracticePage.jsx read the mastery value from the submit response?
- Does it update the mastery meter state variable?
- Is the meter re-rendering with the new value?

FIX:
- Ensure the BLIM posterior updates after each correct Test Mode answer
- Ensure the frontend reads and displays the updated mastery value
- Test: after 5 correct answers in Test Mode, mastery should be
  visibly higher than 20%
- Test: after enough correct answers (typically 5-7), mastery should
  cross the 0.85 threshold and trigger the mastery celebration


========================================================================
ITEM 3: FIX MATHLIVE CURSOR ESCAPING SUPERSCRIPT
========================================================================

Priority: HIGH — students cannot type multi-digit exponents like x^12.

PROBLEM:
When typing an exponent in MathLive, the cursor exits the superscript
position after the first character. Typing "x^12" produces "(x^1)2"
because after typing "1", MathLive drops the cursor back to the base
level and "2" is entered as a coefficient.

This is a MathLive configuration issue, not a bug in our code.

FIX:
In frontend/src/components/MathInput.jsx, when initializing the
MathField, configure it to keep the cursor in superscript:

Option A (preferred): Set the MathField's smartSuperscript option to
false (or equivalent). Check MathLive's documentation for the exact
property name. It may be called:
  - smartSuperscript: false
  - removeExtraneousParentheses: false
  - Or it may need a custom keybinding configuration

Option B: If there's no simple config option, add a helper that
automatically wraps content in braces. When the user types "^", insert
"^{}" and place the cursor between the braces. This way all superscript
content is grouped.

Option C: If neither A nor B works cleanly, add a visible instruction
below the MathLive input: "Tip: For multi-digit exponents, use the
arrow keys (→) to exit the exponent." This is the least preferred option
but better than a broken input.

TESTING:
- Type x^12 — should produce x^{12}, NOT (x^1)2
- Type x^2 — should still work as before (single digit)
- Type 2^{10} — should produce 2^{10}
- Type \frac{1}{2} — should still work (fractions unaffected)


========================================================================
ITEM 4: FIX ANSWER CHECKER FALSE MULTI-VALUE DETECTION
========================================================================

Priority: HIGH — the checker incorrectly treats x^{11} as a solution set.

PROBLEM:
From the logs:
  check_answer | student='x^{11}' | correct='x**11'
  solution set mode: student_multi=True, correct_multi=False
  solution set: student multi (1 val) == correct single

The answer checker sees {11} in x^{11} and thinks it's set notation
{11}, triggering the multi-value comparison path. It currently gets the
right answer by accident, but this is fragile.

FIX:
In answer_checker.py, the multi-value detection logic needs to be
smarter. Currently it probably checks for curly braces {} to detect
sets. Fix it to NOT treat LaTeX grouping braces as set notation:

1. Before checking for multi-value/set answers, FIRST preprocess the
   student answer to normalize LaTeX:
   - Run the \frac, \sqrt, etc. normalization (from FIXES-4)
   - REMOVE all LaTeX grouping braces that are part of LaTeX commands:
     \frac{a}{b}, x^{n}, \sqrt{n}, \log_{b}, etc.
   - Only THEN check for set-like patterns: {a, b} or {a, b, c}

2. A set/multi-value answer should only be detected if:
   - The answer contains a comma OUTSIDE of LaTeX command braces
   - OR the answer is wrapped in set braces with commas: {2, 3}
   - OR the answer contains "and" as a word separator: "x=2 and x=3"

3. Do NOT detect multi-value if:
   - The braces are part of LaTeX commands (x^{11}, \frac{1}{2})
   - There are no commas in the answer
   - The braces contain a single number with no comma ({11} means
     LaTeX group, not a set with one element)

TESTING:
  student="x^{11}",  correct="x**11" → CORRECT (not via set path)
  student="x^{12}",  correct="x^12"  → CORRECT (not via set path)
  student="{2, 3}",  correct="2, 3"  → CORRECT (set path, correct)
  student="2, 3",    correct="2, 3"  → CORRECT (set path, correct)
  student="3, 2",    correct="2, 3"  → CORRECT (set path, order)

Add these to test_answer_checker.py and run them.


========================================================================
ITEM 5: AI BACKEND PROXY ENDPOINT
========================================================================

Priority: HIGH — enables AI tutoring feature.

ARCHITECTURE:
The user's Anthropic API key is stored in localStorage in the browser.
When the user requests AI help, the frontend sends the key + message
to our backend, which proxies the request to api.anthropic.com. This
avoids CORS issues.

IMPLEMENTATION:

1. Create a new router: backend/app/routers/ai_chat.py

2. Define the endpoint:

   POST /api/ai/chat
   Request body:
   {
     "api_key": "sk-ant-...",
     "messages": [
       {"role": "user", "content": "Help me solve x^2 - 5x + 6 = 0"}
     ],
     "context": {
       "topic": "Quadratic Equations",
       "problem_text": "Solve: x^2 - 5x + 6 = 0",
       "hints": ["Factor the quadratic...", "Find two numbers..."]
     }
   }

3. The backend handler:
   - Validates the API key format (starts with "sk-ant-")
   - Constructs the Anthropic API request with a system prompt:

     SYSTEM PROMPT:
     "You are a math tutor helping a student with {topic}. The student
     is working on this problem: {problem_text}. Available hints for
     this problem: {hints}.

     Guide the student toward the answer without giving it away directly.
     Ask leading questions. Use LaTeX notation for math (wrap in \\( \\)
     for inline or \\[ \\] for display). Keep responses concise — 2-3
     sentences max unless the student asks for more detail."

   - Sends the request to https://api.anthropic.com/v1/messages
     using the httpx library (add to requirements.txt if not present)
   - Model: claude-sonnet-4-20250514 (or claude-haiku-4-5-20251001
     for faster/cheaper responses — use haiku)
   - max_tokens: 300
   - Returns the assistant's response text to the frontend

4. Error handling:
   - Invalid API key → 401 with message "Invalid API key"
   - Anthropic rate limit → 429 with message "Rate limited, try again"
   - Anthropic error → 502 with message "AI service unavailable"
   - Network error → 502 with message "Could not reach AI service"

5. IMPORTANT: Do NOT store the API key anywhere on the backend. It
   arrives in the request, gets used for the Anthropic call, then is
   discarded. It never touches the database.

6. Add httpx to requirements.txt if not already present.

7. Register the router in main.py.


========================================================================
ITEM 6: AI CHAT PANEL IN PRACTICE
========================================================================

Priority: HIGH — the user-facing AI feature.

DESIGN:
On the practice screen (PracticePage.jsx), in LEARNING MODE only:

1. Show two side-by-side buttons below the answer submission area:
   - "💡 Hints" button (existing)
   - "🤖 AI Help" button (new)

2. When "Hints" is clicked, the hints panel opens below (existing
   behavior, just needs to be in the right position).

3. When "AI Help" is clicked:
   - If no API key is configured (check localStorage), show a message:
     "To use AI help, add your API key in Settings → AI Hints."
     with a link to /ai-setup
   - If API key exists, open a chat panel below the problem area

4. The chat panel UI:
   - Shows conversation history (scrollable)
   - Has a text input field at the bottom with a "Send" button
   - Messages are displayed as chat bubbles (user on right, AI on left)
   - AI responses render LaTeX via the MathDisplay component
   - Shows a loading indicator while waiting for the AI response
   - An "×" close button to collapse the panel

5. When the user sends a message:
   - POST to /api/ai/chat with:
     - api_key from localStorage
     - The full conversation history (all previous messages)
     - Context: current topic name, problem_text, and hints
   - Display the AI response in the chat
   - Maintain conversation history in React state so follow-up
     questions have context

6. When the user moves to the next problem:
   - Clear the chat history (start fresh for the new problem)
   - Keep the panel open/closed state

7. In TEST MODE: both the Hints button and AI Help button are HIDDEN.

STYLING:
- Keep it simple and consistent with the existing theme
- Chat panel max-height: 400px with scroll
- User messages: right-aligned, primary color background, white text
- AI messages: left-aligned, light gray background, dark text
- Input field: full width with send button on the right


========================================================================
ITEM 7: AI SETUP PAGE IMPROVEMENTS
========================================================================

Priority: MEDIUM — user guidance for API key setup.

CURRENT STATE:
The AI setup page (/ai-setup) exists but lacks explanation of what an
API key is and how to get one. Users see "Connection failed" errors.

FIX:

1. Add clear explainer text at the top of the AI setup page:

   Title: "Set Up AI Tutoring"

   Body:
   "Fisher App can connect to an AI tutor that gives you personalized
   help when you're stuck on a problem. The AI tutor is powered by
   Claude, made by Anthropic.

   To use this feature, you'll need an Anthropic API key:

   1. Go to console.anthropic.com and create a free account
   2. Navigate to 'API Keys' in your dashboard
   3. Click 'Create Key' and copy the key
   4. Paste it below

   Your API key is stored only in your browser — it is never sent to
   or stored on our servers. You can remove it at any time in Settings."

2. Add a prominent link:
   <a href="https://console.anthropic.com" target="_blank">
     Get your API key at console.anthropic.com →
   </a>

3. Fix the connection test: the "Test Connection" button currently
   fails because it tries to call Anthropic directly from the browser
   (CORS). Update it to call the new /api/ai/chat endpoint with a
   simple test message like "Say hello" to verify the key works
   through the backend proxy.

4. On success, show: "✓ Connected! AI tutoring is ready to use."
   On failure, show the specific error from the backend proxy (invalid
   key, network error, etc.)


========================================================================
ITEM 8: LATEX CLEANUP IN HINT TEMPLATES
========================================================================

Priority: MEDIUM — hint text has formatting issues.

PROBLEM:
From the screenshot, hint text shows issues like:
- "x^(a+b). Addtheexponents." — missing space, exponent not in LaTeX
- Plain text math expressions instead of LaTeX-rendered ones

FIX:

1. Open backend/app/services/problem_generator.py

2. Audit EVERY hint template across all 30 generators. Fix these
   common issues:

   a) Wrap all math expressions in LaTeX delimiters \\( ... \\):
      WRONG: "Product rule: x^a · x^b = x^(a+b). Add the exponents."
      RIGHT: "Product rule: \\(x^a \\cdot x^b = x^{a+b}\\). Add the exponents."

   b) Ensure spaces between sentences:
      WRONG: "x^(a+b).Addtheexponents."
      RIGHT: "\\(x^{a+b}\\). Add the exponents."

   c) Use proper LaTeX operators:
      · should be \\cdot
      * should be \\times
      / in fractions should be \\frac{}{}
      >= should be \\geq
      <= should be \\leq

   d) Ensure Hint 3 (bottom-out hint) uses the actual computed values
      from the generated problem, not placeholders.

3. The hints for ALL 30 generators should be audited. Focus especially
   on:
   - exp-product, exp-power, exp-negative, exp-combining (exponent rules)
   - log-definition, log-rules, log-equations (logarithm rules)
   - sum-sigma, sum-arithmetic, sum-nested (summation notation)
   - comb-counting, comb-permutations, comb-combinations
   - eq-quadratic (solution sets)

4. After fixing, verify hints render correctly by checking the Hints
   panel in the browser for at least 5 different topics.

IMPORTANT: Make sure hint text passes through the MathDisplay component
on the frontend. If hints are being rendered as raw HTML/text instead
of through MathDisplay, fix the hint rendering in PracticePage.jsx.


========================================================================
ITEM 9: END-TO-END MASTERY FLOW VERIFICATION
========================================================================

Priority: MEDIUM — verify the complete learning loop works.

After Items 1 and 2 are fixed, verify this full flow:

1. Start as a new user (register fresh account)
2. Complete placement test
3. Dashboard shows knowledge map with some ready/locked nodes
4. Open a "ready" topic (e.g., frac-simplify)
5. View lesson, see worked examples
6. Enter practice in Learning Mode
7. Answer a few problems with hints available
8. Switch to Test Mode
9. Answer enough problems correctly to reach mastery (0.85)
10. Mastery celebration appears
11. Navigate to dashboard — the mastered node changes color
12. A new topic is unlocked (outer fringe updated)
13. The mastered topic appears in the Reviews page with a scheduled date

If ANY step fails, fix it. Document what was broken and what was fixed.

Test this flow for at least 2 different topics.

Write results to backend/tests/MASTERY-FLOW-RESULTS.txt


========================================================================
IMPLEMENTATION ORDER
========================================================================

1. Item 1  — Fix 400 Bad Request on 3rd problem (CRITICAL)
2. Item 2  — Fix mastery meter stuck at 20% (CRITICAL)
3. Item 3  — Fix MathLive cursor in superscript (HIGH)
4. Item 4  — Fix answer checker false multi-value detection (HIGH)
5. Item 5  — AI backend proxy endpoint (HIGH)
6. Item 6  — AI chat panel in practice (HIGH)
7. Item 7  — AI setup page improvements (MEDIUM)
8. Item 8  — LaTeX cleanup in hint templates (MEDIUM)
9. Item 9  — End-to-end mastery flow verification (MEDIUM)

After each item:
  1. Rebuild: docker compose up --build
  2. Test in browser: http://localhost:5173
  3. Commit and push:
       git add -A
       git commit -m "FIXES-5 Item N: [brief description]"
       git push origin main


========================================================================
MANDATORY TESTING AFTER ALL ITEMS COMPLETE
========================================================================

Run through this checklist and log results to
backend/tests/TESTING-RESULTS-R5.txt:

PRACTICE SESSIONS:
  [ ] Answer 10+ problems in a row on frac-simplify — no 400 errors
  [ ] Answer 10+ problems in a row on exp-product — no 400 errors
  [ ] Answer 10+ problems in a row on eq-quadratic — no 400 errors

MASTERY:
  [ ] In Test Mode, mastery meter increases after correct answers
  [ ] Mastery reaches 0.85+ after enough correct answers
  [ ] Mastery celebration/message appears
  [ ] Dashboard updates after mastering a topic

MATHLIVE:
  [ ] Type x^12 — produces x^{12}, not (x^1)2
  [ ] Type x^2 — still works
  [ ] Type \frac{1}{2} — still works
  [ ] Fraction answers marked correct

ANSWER CHECKER:
  [ ] x^{11} NOT detected as multi-value set
  [ ] Run test_answer_checker.py — all tests pass

AI CHAT:
  [ ] API key entry on setup page with explainer text
  [ ] Test connection works through backend proxy
  [ ] AI Help button visible in Learning Mode practice
  [ ] AI Help button hidden in Test Mode
  [ ] Can send message and receive AI response
  [ ] AI responses render LaTeX correctly
  [ ] Chat clears when moving to next problem

HINTS:
  [ ] LaTeX renders correctly in hints for exp-product
  [ ] Hints have proper spacing between sentences
  [ ] Hint 3 shows actual values from the problem

MASTERY FLOW:
  [ ] Full flow documented in MASTERY-FLOW-RESULTS.txt


========================================================================
DESIGN PRINCIPLES
========================================================================

- This is the last major fix round. Everything should work end-to-end
  after this.
- The AI feature uses a backend proxy so users never encounter CORS.
  The API key stays in localStorage and is never persisted server-side.
- MathLive input must handle all common math entry patterns without
  surprising cursor behavior.
- The answer checker must not have false positives from LaTeX syntax.
- Every practice session must support 20+ problems without errors.
