Read FIXES-3.md for context. Do NOT implement any fixes yet. Diagnostic only.

TASK 1: Add temporary detailed logging to the submit endpoint.
In the practice router's submit handler, add logging that prints:
- The raw request body (the entire JSON payload)
- The raw student_answer string, repr() format (shows exact bytes/escapes)  
- The raw correct_answer string from the DB, repr() format
- The result of each comparison step in the answer checker

Rebuild with docker compose up --build.

TASK 2: Simulate MathLive submissions via curl.
Use curl to POST to the submit endpoint for a fraction problem, trying these exact student_answer values:
- "\\frac{5}{9}"
- "\frac{5}{9}"  
- "5/9"
- "\\frac{5}{6}"
You'll need a valid auth token — register a test user via the API first.

Log all results. Which formats return is_correct: true? Which return false? What do the backend logs show for each?

TASK 3: Check what MathLive actually outputs.
Read frontend/src/pages/PracticePage.jsx and find where the MathLive value is extracted and sent to the API. What field/method is used — .value? .getValue('latex')? .getValue('ascii-math')? Print the exact code path.

Write all findings to backend/tests/DIAGNOSTIC-FRACTION-BUG.txt. Do not fix anything yet.