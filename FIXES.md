FISHER APP 3.0 — BUG FIXES AND FEATURE ADDITIONS
===================================================

This document describes 8 fixes/features to implement in Fisher App 3.0.

Read PROMPT.md first — it is the original architecture spec (1,079 lines)
containing database schemas, API endpoint definitions, KST engine details,
and the full implementation plan. This document (FIXES.md) builds on top of
that spec. Do not modify PROMPT.md.

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
  git commit -m "Item N: [brief description of what was done]"
  git push origin main

Push to: https://github.com/john-jacobsen/fisherapp
Branch: main (or whatever the current default branch is — check with
git branch)

This ensures every working state is backed up to GitHub. If something
breaks in a later item, we can always roll back to the last good commit.


========================================================================
ITEM 1: FIX MATH RENDERING AND MATH INPUT
========================================================================

Priority: HIGHEST — almost every other bug appears worse than it is because
raw LaTeX is being displayed as plain text.

PROBLEM:
- Math content (problem prompts, hints, lesson text, worked examples, feedback)
  is stored as LaTeX strings but displayed as raw text in the browser.
  Examples of what users currently see:
    "Evaluate: \sum_{i=1}^{4} i"
    "Simplify: \log_2(4) + \log_2(8)"
    "Multiply: \frac{2}{3} \times \frac{3}{4}"
- The MathLive input component was specified in PROMPT.md (Section 2, and
  frontend/src/components/MathInput.jsx) but never properly integrated.
  The practice screen shows a plain HTML text input ("Enter your answer...")
  instead of a MathLive math editor.

TWO SUB-TASKS:

1a. MATHJAX FOR DISPLAY RENDERING
- Install MathJax (not KaTeX). The developer chose MathJax because it has
  broader LaTeX notation support, which matters for future topic additions
  (calculus, linear algebra, etc.).
- Create a reusable React component (e.g., <MathDisplay>) that takes a string
  containing LaTeX and renders it via MathJax.
- The component must handle mixed content: strings that contain both plain text
  and LaTeX fragments. For example: "Evaluate: \sum_{i=1}^{4} i" should render
  "Evaluate:" as plain text and the summation as formatted math.
- IMPORTANT: MathJax does not automatically re-typeset when React components
  update. The <MathDisplay> component must call MathJax.typesetPromise() (or
  equivalent) in a useEffect hook whenever its content prop changes. Without
  this, dynamically loaded content (e.g., fetching a new practice problem)
  will show raw LaTeX even though the initial page load worked fine.
- Apply this component EVERYWHERE math appears in the app:
    * Problem prompts on the practice screen
    * Hint text (all 3 levels)
    * Lesson notes / written explanations
    * Worked example steps
    * Placement test questions
    * Answer feedback messages ("Correct! The answer is ...")
    * Knowledge map node names (if any contain notation)

1b. MATHLIVE FOR STUDENT INPUT
- MathLive is already in the project spec (PROMPT.md Section 2) and the
  component file MathInput.jsx should exist. Check the frontend dependencies
  (package.json) and the component file.
- Replace the plain text input on the practice screen with a properly
  configured MathLive <math-field> web component.
- Enable the MathLive virtual keyboard with notation tabs for:
    * Basic arithmetic and fractions
    * Exponents and roots
    * Logarithms
    * Summation / sigma notation
    * Greek letters
    * Combinatorics (factorial, binomial coefficient)
  These tabs should be visible and accessible on both desktop and mobile.
- MathLive outputs LaTeX strings. Ensure the submit flow sends the LaTeX
  string to the backend answer-checking endpoint.
- Also apply MathLive input to the placement test answer input, not just
  the practice screen.

REFERENCE: Fisher App 1.0 at C:\Users\jjcas\Desktop\Fisher App\Fisher App 1.0
has a working MathLive + React integration. Use it as reference if helpful.


========================================================================
ITEM 2: ROBUST ANSWER CHECKER
========================================================================

Priority: HIGH — unreliable answer checking makes all testing unreliable.
This must be solid before fixing the practice screen.

CURRENT STATE:
The backend uses SymPy for symbolic equivalence checking (see PROMPT.md
Section 10.3 and backend/app/services/answer_checker.py). MathLive on the
frontend produces LaTeX strings. There is a LaTeX → SymPy conversion step
that has known edge cases.

FIRST: Check how correct answers are stored in the database (the problems
table — see PROMPT.md Section 5.4 for schema). They may be stored as LaTeX,
plain math strings, or SymPy-ready expressions. The parser pipeline depends
on knowing this. Examine:
  - backend/app/models/content.py (the Problem model)
  - backend/app/services/answer_checker.py
  - backend/scripts/seed_problems.py (to see the format of seeded answers)

REQUIREMENTS — the answer checker must handle at minimum:
- Equivalent fractions: 2/4 = 1/2
- Exponent notation variants: x^2 = x**2
- Commutativity: 2+3 = 3+2, a*b = b*a
- Associativity: (2+3)+4 = 2+(3+4)
- Simplified vs unsimplified: 6/8 = 3/4
- Logarithmic equivalences: log_2(8) = 3
- Summation evaluation: sum_{i=1}^{3} i = 6
- Factorial expressions: 5! = 120, n!/(n-k)! = P(n,k)
- Combination/permutation notation: C(5,2) = 10, \binom{5}{2} = 10
- Decimal vs fraction: 0.5 = 1/2
- Negative exponents: x^{-1} = 1/x

IMPLEMENTATION APPROACH:
- First, check how correct answers are stored in the database (the problems
  table). They may be stored as LaTeX, plain math strings, or SymPy-ready
  expressions. The parser pipeline depends on knowing this.
- Parse MathLive LaTeX output into SymPy expressions
- Use SymPy's simplify() and equals() for symbolic comparison
- Build a LaTeX-to-SymPy parser that handles common MathLive output patterns
- Include a fallback: if symbolic parsing fails, try numeric evaluation at
  random test points (for expressions with variables)
- If all parsing fails, fall back to normalized string comparison as last resort
- Log all answer-check failures for debugging (student answer, expected answer,
  why it failed) so edge cases can be identified and fixed over time


========================================================================
ITEM 3: FIX PRACTICE SCREEN — PROBLEM DISPLAY, NaN%, INLINE HINTS
========================================================================

Priority: HIGH — core functionality is non-functional.

PROBLEM:
The practice screen has three distinct bugs:

3a. NO PROBLEM TEXT DISPLAYED
- The backend API call POST /api/practice/{node_id}/start returns 200 OK
  (confirmed from server logs), meaning it IS sending problem data.
- The frontend is not rendering the problem text it receives.
- Debug the React component (frontend/src/pages/PracticePage.jsx) that
  handles the practice/start response. Ensure the problem text is passed
  to the MathDisplay component from Item 1.
- ALSO: The generate_problems.py script produced 0 problems because node IDs
  in the database (e.g., "frac-simplify") don't match the generator's internal
  keys (e.g., "frac_basic"). Fix the ID mapping in generate_problems.py and
  re-run it. The original 65 seeded problems should work, but the generator
  should also work for expanding content later.

3b. MASTERY RING SHOWS "NaN%"
- The circular mastery meter (frontend/src/components/MasteryMeter.jsx)
  displays "NaN%" instead of a number.
- This is a frontend JavaScript issue: the component receives null or undefined
  mastery data from the API and performs arithmetic on it.
- Fix: default to 0% when mastery data is null/undefined/NaN.
- Also verify the backend /api/dashboard endpoint is returning mastery values
  in the expected format.

3c. HINTS PANEL — NAVIGATES TO BLANK PAGE INSTEAD OF EXPANDING INLINE
- Clicking the "Hints" accordion/tab on the practice screen navigates to a
  separate blank page instead of expanding an inline panel.
- This is likely a React Router <Link> where there should be an onClick toggle.
- The component should be frontend/src/components/HintPanel.jsx (see PROMPT.md
  Section 3 directory structure).
- Correct behavior: clicking "Hints" expands a collapsible panel ON the practice
  page (no navigation). The panel reveals hints progressively:
    * First click: show Hint 1
    * Second click: show Hint 2 (Hint 1 remains visible)
    * Third click: show Hint 3 (all visible)
  Each hint should render math via the MathDisplay component.
- Below the hints, show a button: "Ask AI for help" which opens the AI chat
  (see PROMPT.md Phase 5, and frontend/src/components/AIChat.jsx). This is a
  FRONTEND-ONLY feature. The AI chat widget makes direct API calls from the
  browser to the student's chosen AI provider using the student's own API key
  stored in localStorage. It NEVER touches the Fisher App backend. It NEVER
  has access to the app's code, database, or API endpoints. It is a sandboxed
  chat window.
- When the AI chat opens, pre-load a system prompt:
    "The student is working on this problem: [full problem text].
     They have seen the following hints: [list hints revealed so far].
     Help them think through the problem without giving the answer directly.
     Use clear mathematical reasoning and guide them step by step."


========================================================================
ITEM 4: FIX LESSON PAGE — RENDER CONTENT IN CORRECT LAYOUT
========================================================================

Priority: HIGH — lessons are the primary learning content.

PROBLEM:
- The lesson page (frontend/src/pages/LessonPage.jsx) shows an empty
  "Lesson Notes" box despite the backend returning 200 OK for
  GET /api/lessons/{node_id}.
- The frontend component is not rendering the content from the API response.

CORRECT LAYOUT (top to bottom):
1. Topic title at the top (e.g., "Simplifying Fractions")
2. Mastery ring (current, already present but may need the NaN fix from Item 3b)
3. Embedded video (YouTube embed) — this goes ABOVE the written explanation.
   The VideoEmbed component is specified in PROMPT.md Section 3.
4. Written explanation with rendered math (use MathDisplay component from Item 1)
5. Worked examples with step-by-step solutions (also math-rendered). See
   WorkedExamplesPage.jsx in PROMPT.md Section 3.
6. "Start Practice →" button at the bottom (already exists)

DEBUG STEPS:
- Check what the /api/lessons/{node_id} endpoint actually returns (see
  backend/app/routers/lessons.py). The seed script claims 30 lessons with
  markdown content and video URLs.
- Check the React Lesson page component to find where it drops the response data.
- Render markdown content properly (consider react-markdown or similar).
- Embed YouTube videos using standard iframe embed. Video URLs are stored in
  the lesson records from the seed script.


========================================================================
ITEM 5: FIX PROBLEM GENERATOR ID MISMATCH
========================================================================

Priority: MEDIUM — needed for content expansion.

PROBLEM:
The generate_problems.py script (see PROMPT.md Section 14.4) ran without
errors but produced 0 problems. The cause is that node IDs in the database
use the format "frac-simplify" but the generator script uses internal keys
like "frac_basic". The mapping between them is broken.

FIX:
- Open backend/scripts/generate_problems.py
- Fix the mapping between generator keys and database node IDs
- Verify the generator produces valid problems with correct LaTeX formatting
- Re-run the script and confirm problems are inserted into the database
- Test that generated problems display correctly on the practice screen
  (with MathJax rendering from Item 1)


========================================================================
ITEM 6: FIX 404 ROUTES — REVIEW SYSTEM AND SETTINGS PROFILE
========================================================================

Priority: MEDIUM — these are partially unbuilt features.

PROBLEM:
Server logs show these endpoints returning 404 Not Found:
- GET /api/review/due
- GET /api/review/upcoming
- GET /api/settings/profile

These routes were specified in PROMPT.md (Phase 6 for review, Phase 7 for
settings) but were either never implemented or never registered with the
FastAPI app.

FIX:
- Check if the router files exist in backend/app/routers/ (review.py and
  settings.py per PROMPT.md Section 3). If they exist but aren't registered,
  add them to main.py. If they don't exist, implement them per the spec.
- /api/review/due: Return list of knowledge nodes due for spaced repetition
  review. See PROMPT.md Section 12 for SM-2 algorithm details (intervals:
  1, 3, 7, 14, 30 days).
- /api/review/upcoming: Return list of nodes with upcoming review dates.
- /api/settings/profile: GET returns user profile info, PUT updates it.
- Ensure the corresponding frontend pages (ReviewQueue.jsx, SettingsPage.jsx
  per PROMPT.md Section 3) are making correct API calls and rendering responses.


========================================================================
ITEM 7: KNOWLEDGE MAP — SEMANTIC ZOOM WITH HIERARCHICAL NAVIGATION
========================================================================

Priority: MEDIUM — significant new feature, not a bug fix.

CURRENT STATE:
- The knowledge map (frontend/src/components/KnowledgeGraph.jsx) shows all
  30 nodes in a flat graph. It works but is dense and hard to navigate.

DESIRED BEHAVIOR:
Build a multi-level semantic zoom for the knowledge map:

LEVEL 1 — SUBJECT VIEW (fully zoomed out):
- Show high-level subject areas as nodes: "Algebra" (and in the future:
  "Calculus I", "Calculus II", "Linear Algebra", "Probability",
  "Mathematical Statistics", etc.)
- Show arrows between subjects representing prerequisite relationships
  (e.g., Algebra → Calculus I).
- FOR NOW: Only "Algebra" has content. Other subjects are placeholders for
  future expansion. The system should make it trivial to add new subjects later.

LEVEL 2 — TOPIC VIEW (click into a subject):
- Clicking on "Algebra" (or zooming in) reveals the 8 topic clusters:
  Fraction Arithmetic, Exponent Rules, Order of Operations, Solving Equations,
  Logarithms & Exponentials, Summation Notation, Combinatorics, Geometric Series.
- Show prerequisite arrows between topic clusters. These arrows should be
  DERIVED AUTOMATICALLY from the sub-skill prerequisite edges: if any sub-skill
  in Topic A is a prerequisite for any sub-skill in Topic B, draw A → B.

LEVEL 3 — SUB-SKILL VIEW (click into a topic):
- Clicking on "Fraction Arithmetic" reveals the 6 sub-skills (simplify,
  add like denom, find common denom, add unlike denom, multiply, divide)
  with their internal prerequisite edges.
- This is essentially the current graph view, but scoped to one topic.

CROSS-SUBJECT PREREQUISITE HANDLING:
- When a student is zoomed into a subject (e.g., future Calculus) and a
  sub-skill is locked because of an unmet prerequisite from another subject
  (e.g., Algebra), show a clear message: "Requires: Simplifying Fractions
  (Algebra)" with a clickable link that navigates to that topic in the
  Algebra section.
- The KST engine operates on the FULL flat graph across all subjects.
  The semantic zoom is purely a navigation/display layer. It does not change
  how the engine computes knowledge states or fringes.

ARCHITECTURE — EXTENSIBILITY IS CRITICAL:
- Topic groupings and subject groupings must be DATA-DRIVEN, not hardcoded.
  They should be defined in the knowledge_graph.json (or a similar config file)
  and read by the frontend.
- Adding a new subject should require only:
    1. Adding nodes and edges to the knowledge graph JSON
    2. Specifying which topic group and subject each node belongs to
    3. Re-running the seed script
  No frontend code changes should be needed to add new subjects or topics.
- The JSON structure should support arbitrary nesting depth (subject → topic →
  sub-skill) even if we only use 3 levels for now.
- EXAMPLE of the target JSON structure for knowledge_graph.json:

  {
    "subjects": [
      {
        "id": "algebra",
        "name": "Algebra",
        "prerequisites": [],
        "topics": [
          {
            "id": "fraction-arithmetic",
            "name": "Fraction Arithmetic",
            "nodes": [
              {
                "id": "frac-simplify",
                "name": "Simplifying Fractions",
                "prerequisites": []
              },
              {
                "id": "frac-add-like",
                "name": "Adding Fractions (Like Denominators)",
                "prerequisites": ["frac-simplify"]
              }
            ]
          }
        ]
      },
      {
        "id": "calculus-1",
        "name": "Calculus I",
        "prerequisites": ["algebra"],
        "topics": []
      }
    ]
  }

  This is illustrative — adapt as needed, but preserve the principle that
  subjects contain topics, topics contain nodes, and prerequisites can
  reference nodes across topics and subjects. The existing knowledge_graph.json
  (see PROMPT.md Section 7 for the current graph definition) will need to be
  restructured into this hierarchical format. Ensure the seed script and the
  KST engine still work correctly after the restructure — the engine needs
  the flat list of all nodes and edges regardless of how they're grouped.

ZOOM INTERACTION:
- Support both click-to-drill-down and scroll/pinch-to-zoom.
- Provide a breadcrumb or back button: "All Subjects > Algebra > Fractions"
- Smooth animated transitions between zoom levels.


========================================================================
ITEM 8: DOCKER-COMPOSE.YML CLEANUP
========================================================================

Priority: LOW — cosmetic but noted in build output.

The docker-compose.yml contains a `version` attribute that Docker now considers
obsolete. The build output shows:
  level=warning msg="the attribute `version` is obsolete, it will be ignored,
  please remove it to avoid potential confusion"

Remove the `version` key from docker-compose.yml.


========================================================================
IMPLEMENTATION ORDER
========================================================================

1. Item 1  — MathJax rendering + MathLive input (foundation for everything)
2. Item 2  — Robust answer checker (needed to test practice correctly)
3. Item 3  — Practice screen fixes (problem display, NaN%, inline hints + AI chat)
4. Item 4  — Lesson page rendering (video, text, worked examples)
5. Item 5  — Fix problem generator ID mismatch
6. Item 6  — Fix 404 routes (review system, settings profile)
7. Item 7  — Semantic zoom knowledge map (largest feature, builds on working base)
8. Item 8  — Docker cleanup

After each item:
  1. Rebuild: docker compose up --build
  2. Test in browser: http://localhost:5173
  3. Commit and push:
       git add -A
       git commit -m "Item N: [brief description]"
       git push origin main

If seed scripts need re-running:
  docker compose run --rm backend alembic upgrade head
  docker compose run --rm backend python scripts/seed_knowledge_graph.py
  docker compose run --rm backend python scripts/seed_problems.py
  docker compose run --rm backend python scripts/seed_lessons.py
  docker compose run --rm backend python scripts/generate_problems.py


========================================================================
DESIGN PRINCIPLES
========================================================================

- The knowledge graph structure (nodes, edges, topic groupings, subject
  groupings) must be entirely data-driven from JSON config files. Adding new
  subjects, topics, or sub-skills should never require frontend code changes.
- MathJax for display, MathLive for input — everywhere, consistently.
- The BYOK AI chat is frontend-only and sandboxed. It never contacts the
  Fisher App backend. It never has access to app code or data beyond the
  specific problem context passed in the system prompt.
- The KST engine operates on the full flat graph. Visual hierarchy (semantic
  zoom) is a display layer only.
- All LaTeX content must render correctly. If you store math as LaTeX, it
  must go through MathJax for display. No raw LaTeX should ever be visible
  to the student.
