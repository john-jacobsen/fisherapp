# FIXES-12: Lesson Content Generation

**Date:** 2026-03-16
**Scope:** Generate markdown lesson content for all 176 knowledge nodes

---

## Problem

The current lesson content has rendering issues (broken tables, run-together text) and many nodes have no lesson content at all. The existing content was likely generated without consistent formatting standards.

## Goal

Produce a markdown lesson file for every one of the 176 nodes, following a consistent structure, with correct LaTeX math notation and proper markdown formatting. Store them as static files that the backend serves to the frontend.

## Lesson Structure

Every lesson file must follow this exact template:

```markdown
# [Topic Title]

## Overview

[1-2 sentences defining the concept. Bold the key term on first use.]

## Key Idea

[The central rule, formula, or principle. Use display math ($$...$$) for important formulas. Keep this to 2-3 sentences max.]

## Worked Examples

**Example 1: [Brief description]**

[Problem statement]

[Step-by-step solution with inline math ($...$) and display math ($$...$$)]

---

**Example 2: [Brief description]**

[Problem statement]

[Step-by-step solution]

---

**Example 3: [Brief description]**

[Problem statement]

[Step-by-step solution]

## Common Mistakes

- **[Mistake 1].** [Why it's wrong and how to avoid it.]
- **[Mistake 2].** [Why it's wrong and how to avoid it.]
- **[Mistake 3].** [Why it's wrong and how to avoid it.]

## Quick Check

Try these before using hints:

1. [Problem 1]
2. [Problem 2]
3. [Problem 3]

*(Answers: [answer1], [answer2], [answer3])*
```

## Formatting Rules

1. **Inline math:** Use `$...$` for expressions within text (e.g., "the slope $m = 3$")
2. **Display math:** Use `$$...$$` for standalone equations on their own line
3. **Tables:** Use proper markdown tables with `|` delimiters and `---` separator rows
4. **No HTML tags.** Pure markdown only.
5. **No raw LaTeX commands** outside of math delimiters. Don't use `\textbf{}` for bold — use `**bold**`.
6. **Spacing:** Always leave a blank line before and after display math `$$` blocks
7. **Fractions:** Use `\frac{a}{b}` in display math, `a/b` in inline text
8. **Worked examples:** Always show the original problem, then step-by-step work, then final answer. Use "→" or "therefore" to connect steps, not just bare equations.

## Content Guidelines

- **Difficulty level:** Assume the student has mastered all prerequisites but is seeing this topic for the first time. Don't explain prereqs in depth — just reference them.
- **Length:** 300–500 words per lesson. Concise, not verbose.
- **Tone:** Direct, clear, second-person ("you"). Not overly formal, not condescending.
- **Examples:** 3 worked examples per lesson, progressing from easy to medium. Use concrete numbers, not abstract variables, for at least the first example.
- **Common mistakes:** 2–3 per lesson. These should be mistakes a real student would make, not trivial errors.
- **Quick check:** 3 problems the student can try mentally or on paper before doing the interactive practice. Include answers at the bottom.

## Implementation

### Step 1: Generate lesson files

Create a Python script `backend/scripts/generate_lessons.py` that generates all 176 lessons. The script should:

1. Read the list of all 176 node IDs from `backend/data/knowledge_graph.json`
2. For each node, use the node ID and label to determine the topic
3. Generate the lesson content following the template above
4. Save each lesson as `backend/data/lessons/{node_id}.md`

The content for each lesson must be written directly in the script (or generated programmatically for simple topics). Here's how to organize by subject:

**Foundations (30 nodes):** These are the most important to get right — students spend the most time here. Each lesson should be thorough with clear, simple language.

**Algebra through Statistics (146 nodes):** These can be more concise since the students are more advanced. Still follow the template but the explanation can assume more mathematical maturity.

For each node, the script should contain the lesson markdown as a string constant or generate it from a template. The key is that EVERY node gets a lesson — no gaps.

### Step 2: Backend serving

Check how the backend currently serves lesson content. If it reads from a database, add a fallback that reads from the markdown files in `backend/data/lessons/`. If it already reads from files, just ensure the path is correct.

The backend endpoint (likely `GET /lessons/{node_id}`) should:
1. Look for `backend/data/lessons/{node_id}.md`
2. If found, return its contents as the `content` field in the response
3. If not found, return a generic "Lesson content coming soon" message

### Step 3: Frontend rendering

This was already addressed in FIXES-9 Item 4 — `LessonPage.jsx` now uses `react-markdown` with `remark-gfm` for tables. Verify that the new lesson content renders correctly with the existing renderer.

The one thing to check: the renderer must handle `$...$` and `$$...$$` math delimiters. If the current MathDisplay component is being used for inline code blocks, the lessons should use backtick-delimited math to match. Check what delimiter convention the renderer expects and match it in the lesson content.

Look at how the existing lesson content uses math delimiters and match that convention. If the renderer expects `\(...\)` and `\[...\]`, use those instead of `$` and `$$`.

### Step 4: Verification

After generating all lessons:

```bash
# Check all 176 files exist
ls backend/data/lessons/*.md | wc -l
# Should output 176

# Check each file has the required sections
for f in backend/data/lessons/*.md; do
    node=$(basename "$f" .md)
    has_overview=$(grep -c "## Overview" "$f")
    has_examples=$(grep -c "## Worked Examples" "$f")
    has_mistakes=$(grep -c "## Common Mistakes" "$f")
    if [ "$has_overview" -eq 0 ] || [ "$has_examples" -eq 0 ] || [ "$has_mistakes" -eq 0 ]; then
        echo "MISSING SECTIONS: $node"
    fi
done

# Check no file is suspiciously short
find backend/data/lessons/ -name "*.md" -size -500c
# Should output nothing (all files should be > 500 bytes)
```

Then load the app, navigate to a lesson page for each subject, and verify:
- Tables render as tables (not pipe characters)
- Math renders as formatted equations (not raw LaTeX)
- Text is properly spaced (no "run together" words)
- All 3 worked examples are present
- Common mistakes section is present

## Content for specific tricky nodes

Some nodes need special attention because the content is non-obvious:

- **stat-confounding, stat-causal-intro:** These are conceptual, not computational. The "worked examples" should be scenario analysis, not math problems.
- **stat-neyman-pearson, stat-ump:** These are theoretical. Examples should walk through the logic of the lemma with a simple distribution.
- **prob-memoryless:** Explain the memoryless property of exponential/geometric distributions. Examples should demonstrate it with conditional probability calculations.
- **linalg-svd:** Keep it simple — 2×2 example, interpret the components geometrically.
- **calc-improper:** Show both Type I (infinite limit) and Type II (integrand blows up) examples.
