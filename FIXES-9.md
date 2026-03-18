# FIXES-9: Manual Testing Bug Report

**Date:** 2026-03-16
**Commit:** 3037586 (main)
**Source:** Manual testing of live app

---

## Item 1: Answer checker rejects valid formats like "x=2"

### Symptom

For "Solve for x: 2x + 8 = 12", entering `x=2` is graded incorrect. Only `2` is accepted. Same for "Solve for x: x + 5 = 12" — `x=7` is rejected, only `7` works.

### Fix

In `backend/app/services/answer_checker.py`, add a preprocessing step before comparison. If the student answer contains `=`, extract the right-hand side. Also handle `x =` with spaces.

```python
def _normalize_student_answer(raw_answer: str, correct_answer: str) -> str:
    """Strip variable assignment prefix if present."""
    cleaned = raw_answer.strip()
    # Handle "x = 2", "x=2", "y = 3", etc.
    if '=' in cleaned:
        parts = cleaned.split('=', 1)
        rhs = parts[1].strip()
        if rhs:  # only strip if there's something after the =
            cleaned = rhs
    return cleaned
```

Call this at the top of `check_answer()` before any comparison logic. This way `x=2`, `x = 2`, and `2` all resolve to `2` before hitting the SymPy comparison.

### Testing

After fixing, verify these all return correct:
- `check_answer("x=2", "2", "numeric")` → True
- `check_answer("x = 2", "2", "numeric")` → True  
- `check_answer("x=3/4", "3/4", "symbolic")` → True
- `check_answer("2", "2", "numeric")` → True (no regression)

---

## Item 2: Placement test question counter overshoots

### Symptom

During the placement test, the counter reads "Question 19 of ~18" and then "Question 20 of ~19". The counter should never exceed its own estimate, and the estimate shouldn't change mid-test.

### Fix

Find the placement test logic (likely in a placement-specific page or in the practice service). Two issues:

1. The `~N` estimate should be computed once at the start and not updated during the test.
2. The test should terminate when it hits the estimated cap OR when the adaptive algorithm has enough confidence — whichever comes first. If the algorithm needs more questions than estimated, either raise the initial estimate or hard-cap at the estimate.

Search the frontend for where the placement question counter is rendered. It probably reads something like `Question ${current} of ~${total}`. Make `total` a fixed value set on mount, not a reactive value that changes as the session progresses.

---

## Item 3: Lesson videos not loading

### Symptom

Videos on lesson pages direct the user to a YouTube search instead of embedding a playable video. Students should see an embedded, ready-to-play video.

### Fix

Check `backend/data/lesson_videos.json` (referenced in FIXES-6). This file should map node IDs to actual YouTube video URLs (not search queries). 

For each node, the video should be a specific YouTube video ID embedded via iframe:

```html
<iframe src="https://www.youtube.com/embed/{VIDEO_ID}" ...></iframe>
```

The current implementation probably constructs a search URL like `https://www.youtube.com/results?search_query=...` as a fallback when no specific video ID exists. This fallback needs to be replaced with actual curated video IDs.

**Approach:** For each of the 176 nodes (or at least the ones with lesson content), find a high-quality YouTube video and store its video ID in `lesson_videos.json`. Khan Academy and 3Blue1Brown videos are good sources for most topics. The frontend should embed these directly, not link to search.

If curating 176 videos is too much for this round, at minimum:
1. Fix the embedding so that when a video ID IS present, it embeds properly
2. When no video ID exists, show "No video available for this topic yet" instead of a broken YouTube search link

---

## Item 4: Lesson notes markdown/LaTeX rendering is broken

### Symptom

Multiple lesson pages show raw markdown or broken LaTeX:
- "One-Step Linear Equations" — markdown table shows as raw pipe characters: `| Operation in equation | Undo it with | |---|---| ...`
- Exponents lesson — "Intuition" section has text running together: `sodividingby(x)eachtime` instead of "so dividing by x each time"
- Exponents "All Four Rules" — table not rendering, raw markdown pipes visible
- Logarithm lesson — text runs together: `as"logbaseofx" ="whatpowermustbberaisedtoinordertogetx?"` instead of properly spaced text with quotes

### Diagnosis

The lesson content is stored as markdown (or markdown-like text) but the frontend is rendering it as raw text, not parsing it. The LaTeX is being rendered by MathLive/KaTeX, but the surrounding markdown (tables, emphasis, spacing) is not being parsed.

### Fix

1. Find where lesson content is rendered in the frontend. It's probably in a lesson/notes component that receives markdown text and puts it in a div.

2. Install a markdown renderer. Add `react-markdown` to the frontend:
```bash
npm install react-markdown remark-math rehype-katex
```

3. Replace the raw text rendering with:
```jsx
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'

<ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
  {lessonContent}
</ReactMarkdown>
```

4. Also check the lesson content itself. The "sodividingby(x)eachtime" issue suggests the source markdown may have missing spaces or the LaTeX delimiters are eating surrounding text. The content might use `$...$` for inline math but the spaces around the `$` signs are missing, so when LaTeX renders, it swallows adjacent words.

Fix both the renderer AND audit the lesson content for these spacing issues. The lesson content is likely generated — check where it comes from (probably a `lessons` table in the DB or static files) and fix the source text.

---

## Item 5: No "next topic" prompt after mastering a topic

### Symptom

After mastering a topic in test mode, the session ends but there's no prompt to continue to the next recommended topic. The student has to manually navigate back to the dashboard and find what to do next.

### Fix

In `frontend/src/pages/PracticePage.jsx` (or the score/results page that appears after mastery), add a "Continue to next topic" button.

When mastery is achieved:
1. Call the dashboard API or a dedicated endpoint to get `recommended_next`
2. Show the mastery celebration screen with two buttons:
   - "Continue to [Next Topic Name] →" (primary, navigates to `/lesson/{next_node_id}`)
   - "Back to Dashboard" (secondary)

If there's already a score page at `/score/{nodeId}`, add this there. The recommended next topic should come from the same logic the dashboard uses (`compute_node_fringes` → outer fringe → first recommended node).

Consider adding a backend endpoint if one doesn't exist:
```
GET /api/recommended-next/{node_id}
```
Returns the next recommended node after mastering `node_id`, based on the updated fringe.

---

## Item 6: Dashboard stops recommending topics after mastery

### Symptom

After mastering a topic, the dashboard's "recommended next" section stops showing recommendations. There should ALWAYS be a recommendation — either the next unmastered topic in the prerequisite path, or review of previously mastered topics.

### Fix

In the backend dashboard endpoint (likely `backend/app/routers/dashboard.py` or the service it calls), find where `recommended_next` is computed. The logic probably uses the outer fringe from KST. When the outer fringe is empty (rare — means everything is mastered or the fringe computation failed), it should fall back to:

1. First: any unmastered nodes that have all prereqs met
2. Second: nodes currently in progress (started but not mastered)
3. Third: previously mastered nodes due for review (from `ReviewSchedule`)
4. Fourth: the earliest unmastered node in the curriculum order

The `recommended_next` list should never be empty. Add a fallback chain:

```python
recommended = get_outer_fringe_nodes(...)
if not recommended:
    recommended = get_unmastered_with_prereqs_met(...)
if not recommended:
    recommended = get_review_due_nodes(...)
if not recommended:
    recommended = get_first_unmastered_nodes(...)
```

---

## Item 7: "Ready to learn" color coding not working at all navigation levels

### Symptom

In the knowledge graph drill-down, "Ready to Learn" (yellow/amber) color coding doesn't appear consistently. Screenshot shows the Exponents topic view where some nodes that should show as "Ready to Learn" may not be colored correctly.

### Fix

In `frontend/src/components/KnowledgeGraph.jsx`, find where node status colors are assigned. The status is probably determined by checking:
- Is the node in `mastered_nodes`? → green/mastered
- Are all prereqs mastered? → yellow/ready
- Otherwise → gray/locked

The bug is likely in how this propagates through the three drill-down levels (subject → topic → skill). The topic-level aggregate may not correctly reflect that some child nodes are "ready." 

Check: when computing topic stats in the `topicStats` useMemo, does it count "ready" nodes? It currently counts `mastered` and `total`, but may be missing the `ready` count or not passing it down to the color logic.

Also verify that the `knowledge_map` data from the dashboard API includes prerequisite information for each node, not just mastery status. The frontend needs to know each node's prereqs to compute "ready" status client-side, OR the backend needs to send the computed status for each node.

---

## Item 8: Switching from learning to test mode must generate a new problem

### Symptom

A student can read hints in learning mode, then switch to test mode and submit the answer to the same problem. This defeats the purpose of test mode.

### Fix

In `frontend/src/pages/PracticePage.jsx`, find the `switchToTest` function. Currently it just does:

```javascript
const switchToTest = () => { setMode('test'); setFeedback(null); };
```

Change it to also request a new problem:

```javascript
const switchToTest = async () => {
  setMode('test');
  setFeedback(null);
  setAnswer('');
  // Request a new problem from the backend
  try {
    const r = await api.post(`/practice/${nodeId}/submit`, {
      session_id: sessionId,
      problem_id: problem.id,
      answer: '__SKIP__',  // or add a dedicated endpoint
      mode: 'learning',    // don't count the skip in test stats
    });
    if (r.data.next_problem) {
      setProblem(r.data.next_problem);
    }
  } catch (e) {
    // If skip fails, at minimum clear hints
    console.error('Failed to get new problem on mode switch', e);
  }
};
```

Alternatively (and cleaner), add a dedicated backend endpoint:

```
POST /practice/{node_id}/new-problem
Body: { session_id }
Returns: { problem: { id, problem_text, answer_type } }
```

This generates and returns a fresh problem without submitting an answer.

---

## Item 9: Answer format guidance for students

### Symptom

Students don't know what format to enter answers in. If the app expects `2` but the student types `x=2`, they get marked wrong (see Item 1). Even after fixing Item 1, there are many potential format issues (fractions, decimals, expressions).

### Fix

Add a small line of text below the MathLive input that describes the expected format, based on the problem's `answer_type`:

```javascript
const formatHint = {
  numeric: "Enter a number (e.g., 7, -3, 0.5)",
  symbolic: "Enter an expression (e.g., 3/4, x+1, -2/3)",
};
```

Display this in small gray text below the input field:

```jsx
<p style={{ fontSize: 12, color: '#888' }}>
  {formatHint[problem.answer_type] || "Enter your answer"}
</p>
```

For specific problem types, make the hint more specific. The generator already knows what format the answer is in — pass a `format_hint` field from the generator:

```python
# In each generator, add an optional format_hint:
"format_hint": "Enter the value of x as a number"
# or
"format_hint": "Enter your answer as a fraction (e.g., 3/4)"
```

The frontend displays this if present, otherwise falls back to the generic hint.

---

## Item 10: "Exponential Form ↔ Log Form" problems are just exponents

### Symptom

The problems for the "Exponential Form ↔ Log Form" topic are all just exponent calculations like "5^3" or "4^3". There's no conversion between exponential and logarithmic form, which is what the topic name promises.

### Fix

Find the generator for this node (likely `log-exp-form` or similar in `backend/app/services/problem_generator.py`). Rewrite it to actually test conversion between forms.

The generator should produce problems like:
- "Convert to logarithmic form: 2^5 = 32" → answer: "log_2(32) = 5" or just "5" with the problem asking "What is the exponent?"
- "Convert to exponential form: log_3(81) = 4" → answer: "3^4 = 81" or just "81"

Since the answer checker can't easily handle full log expressions, the simplest approach is to keep numeric answers but change the problem framing:

```python
def _gen_log_exp_form():
    base = random.choice([2, 3, 4, 5, 10])
    exp = random.randint(2, 4)
    result = base ** exp
    
    variant = random.choice(["to_log", "find_base", "find_exp"])
    
    if variant == "to_log":
        return {
            "problem_text": f"If \\({base}^{exp} = {result}\\), what is \\(\\log_{{{base}}}({result})\\)?",
            "correct_answer": str(exp),
            "answer_type": "numeric",
            ...
        }
    elif variant == "find_base":
        return {
            "problem_text": f"\\(\\log_b({result}) = {exp}\\). What is \\(b\\)?",
            "correct_answer": str(base),
            "answer_type": "numeric",
            ...
        }
    elif variant == "find_exp":
        return {
            "problem_text": f"\\(\\log_{{{base}}}({result}) = x\\). What is \\(x\\)?",
            "correct_answer": str(exp),
            "answer_type": "numeric",
            ...
        }
```

Also consider renaming the topic to just "Logarithms — Exponential Conversion" or similar if the node label is misleading.

---

## Item 11: Problem diversity — same form repeated with different numbers

### Symptom

When practicing "equations with fractions", the student kept getting the same form: `2x/2 = 4`, `5x/5 = 3`, etc. Only the numbers changed, not the structure. Also, the numerator and denominator were always the same number (e.g., 2x/2, 5x/5), which makes the fraction trivial.

### Fix

Find the generator for the fraction equations node (likely `eq-frac` or similar in `problem_generator.py`). The generator needs:

1. **Multiple problem templates.** Not just `ax/a = c`. Include:
   - `x/a = b` (simple fraction)
   - `ax/b = c` where a ≠ b (non-trivial fraction)
   - `(x + a)/b = c` (fraction with addition in numerator)
   - `a/x = b` (variable in denominator)
   - `a/(x + b) = c` (variable expression in denominator)

2. **Independent random generation.** The coefficient in the numerator and the denominator should be generated independently, with a check that they don't simplify to 1.

Example rewrite:

```python
def _gen_eq_frac():
    template = random.choice(["simple", "coeff", "sum_numer", "var_denom"])
    
    if template == "simple":
        # x/a = b → x = ab
        a = random.randint(2, 8)
        b = random.randint(1, 6)
        x = a * b
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{x}}{{{a}}} = {b}\\)",
            "correct_answer": str(x), ...
        }
    elif template == "coeff":
        # ax/b = c → x = bc/a (ensure integer solution)
        a = random.randint(2, 5)
        b = random.randint(2, 6)
        while gcd(a, b) == a:  # avoid trivial cancellation
            b = random.randint(2, 6)
        x = random.randint(1, 8)
        c_num = a * x
        # ensure c_num / b is integer for clean problem
        # adjust: pick x such that ax is divisible by b
        x = b * random.randint(1, 4)
        c = (a * x) // b
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{{a}x}}{{{b}}} = {c}\\)",
            "correct_answer": str(x), ...
        }
    elif template == "sum_numer":
        # (x + a)/b = c → x = bc - a
        a = random.randint(1, 6)
        b = random.randint(2, 5)
        c = random.randint(2, 6)
        x = b * c - a
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{x + {a}}}{{{b}}} = {c}\\)",
            "correct_answer": str(x), ...
        }
    elif template == "var_denom":
        # a/x = b → x = a/b (ensure integer)
        b = random.randint(2, 6)
        x = random.randint(1, 6)
        a = b * x
        return {
            "problem_text": f"Solve for \\(x\\): \\(\\frac{{{a}}}{{x}} = {b}\\)",
            "correct_answer": str(x), ...
        }
```

Apply the same diversity principle to ALL generators that currently use a single template. Each generator should have at least 2–3 structural variants, not just different numbers.

---

## Item 12: MathLive keyboard missing log base button

### Symptom

The MathLive virtual keyboard (shown in screenshot) has buttons for sin, cos, tan, ln, log, exp, etc., but no button for entering logarithm bases (e.g., log_2, log_3). Students need this for logarithm problems.

### Fix

MathLive keyboards are configurable. In the frontend where MathLive is initialized, add a custom keyboard button or modify the keyboard layout.

Find where MathLive is configured (likely in a MathInput component). Add a custom key:

```javascript
// When initializing MathLive, configure custom virtual keyboard
mathfield.setOptions({
  virtualKeyboards: 'numeric functions symbols',
  customVirtualKeyboardLayers: {
    'log-base': {
      rows: [
        [
          { latex: '\\log_{\\placeholder{}}(\\placeholder{})', label: 'log_b' },
        ]
      ]
    }
  }
});
```

Alternatively, if MathLive supports it natively, check if there's a subscript button that works after typing `log`. The student should be able to type `log`, then subscript to enter the base.

Check the MathLive documentation at https://cortexjs.io/mathlive/ for the correct API for custom virtual keyboard keys. The exact config format may differ from the above.

At minimum, add instructions below the input: "For log bases, type 'log' then use the subscript button (the _ key) to enter the base."

---

## Item 13: Placement test question count display

### Related to Item 2

The placement test question counter should display a fixed estimate (set once when the test starts) and should never show the current question exceeding that estimate. If the adaptive algorithm needs more questions, the display should either:

- Show "Question 19 of ~20" (round up the estimate)  
- Or just show "Question 19" without a total

The `~` prefix on the total is fine but the total must be >= the current question number at all times.

---

## Priority order

1. **Item 1** (answer checker) — directly causes wrong grading, highest impact
2. **Item 8** (mode switch new problem) — testing integrity issue
3. **Item 4** (lesson rendering) — large visual breakage across many pages
4. **Item 11** (problem diversity) — educational quality
5. **Item 10** (log form problems) — wrong content for the topic
6. **Item 12** (MathLive log base) — blocks students from answering log problems
7. **Item 5** (next topic prompt) — UX flow
8. **Item 6** (always recommend) — UX flow
9. **Item 9** (format hints) — reduces student frustration
10. **Item 7** (ready status colors) — visual bug
11. **Item 2** (question counter) — cosmetic
12. **Item 3** (videos) — requires manual curation, lower priority
13. **Item 13** (question count display) — cosmetic
