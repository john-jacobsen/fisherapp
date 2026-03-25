# Interactive Walkthrough — JSON Schema & Pilot Example

## Design Decisions (from interview)

- Walkthrough **replaces** the static lesson page
- One template per topic, **regenerated with different numbers** each visit
- Recommended but **skippable** (Skip to Practice always visible)
- Input types: multiple choice, numeric, MathLive expression, dropdown
- Wrong answers: specific feedback, retry with no limit
- Hints/feedback: inline below the active step
- Conceptual intro: present, prioritizing understanding over brevity
- Pilot topic: `frac-simplify`

---

## Schema: `walkthrough_template.json`

Each node gets one file: `backend/data/walkthroughs/{node_id}.json`

```json
{
  "node_id": "frac-simplify",
  "title": "Simplifying Fractions",

  "intro": {
    "body": "Markdown string — conceptual overview with LaTeX math. As long as needed for genuine understanding, but every sentence must earn its place.",
    "key_formula": "LaTeX string — the central formula or rule, displayed prominently"
  },

  "problem_generator": {
    "description": "How to generate fresh numbers for this walkthrough each time",
    "params": {
      "numerator": { "type": "random_int", "min": 4, "max": 48, "constraint": "must share a common factor > 1 with denominator" },
      "denominator": { "type": "random_int", "min": 4, "max": 48, "constraint": "must share a common factor > 1 with numerator" }
    },
    "derived": {
      "gcf": "gcd(numerator, denominator)",
      "simplified_num": "numerator / gcf",
      "simplified_den": "denominator / gcf"
    },
    "display_problem": "Simplify $\\frac{{{numerator}}}{{{denominator}}}$"
  },

  "steps": [
    {
      "step_number": 1,
      "title": "Identify common factors",
      "prompt": "Look at the numerator {numerator} and denominator {denominator}. What is the greatest common factor (GCF) of these two numbers?",
      "input_type": "numeric",
      "correct_answer": "{gcf}",
      "hint": "List the factors of {numerator} and the factors of {denominator}. The GCF is the largest number that appears in both lists.",
      "wrong_answer_feedback": [
        {
          "condition": "answer == 1",
          "feedback": "A GCF of 1 would mean the fraction is already simplified. But both {numerator} and {denominator} are divisible by {smallest_common_factor} — try finding their largest shared factor."
        },
        {
          "condition": "answer divides numerator but not denominator",
          "feedback": "{answer} is a factor of {numerator}, but it doesn't divide evenly into {denominator}. The GCF must divide both numbers."
        },
        {
          "condition": "answer divides denominator but not numerator",
          "feedback": "{answer} is a factor of {denominator}, but it doesn't divide evenly into {numerator}. The GCF must divide both numbers."
        },
        {
          "condition": "answer divides both but is not the greatest",
          "feedback": "{answer} is a common factor, but it's not the greatest one. Keep looking — is there a larger number that divides both {numerator} and {denominator}?"
        }
      ]
    },
    {
      "step_number": 2,
      "title": "Divide the numerator",
      "prompt": "Divide the numerator {numerator} by the GCF ({gcf}). What do you get?",
      "input_type": "numeric",
      "correct_answer": "{simplified_num}",
      "hint": "Compute {numerator} ÷ {gcf}.",
      "wrong_answer_feedback": [
        {
          "condition": "answer == numerator",
          "feedback": "That's the original numerator. You need to divide it by the GCF ({gcf}): {numerator} ÷ {gcf} = ?"
        },
        {
          "condition": "default",
          "feedback": "Not quite. {numerator} ÷ {gcf} = {simplified_num}. Try again."
        }
      ]
    },
    {
      "step_number": 3,
      "title": "Divide the denominator",
      "prompt": "Now divide the denominator {denominator} by the same GCF ({gcf}). What do you get?",
      "input_type": "numeric",
      "correct_answer": "{simplified_den}",
      "hint": "Compute {denominator} ÷ {gcf}.",
      "wrong_answer_feedback": [
        {
          "condition": "answer == denominator",
          "feedback": "That's the original denominator. You need to divide it by the GCF ({gcf}): {denominator} ÷ {gcf} = ?"
        },
        {
          "condition": "default",
          "feedback": "Not quite. {denominator} ÷ {gcf} = {simplified_den}. Try again."
        }
      ]
    },
    {
      "step_number": 4,
      "title": "Write the simplified fraction",
      "prompt": "You divided both the numerator and denominator by {gcf}. Write the simplified fraction.",
      "input_type": "expression",
      "correct_answer": "\\frac{{{simplified_num}}}{{{simplified_den}}}",
      "hint": "Put your new numerator ({simplified_num}) over your new denominator ({simplified_den}).",
      "wrong_answer_feedback": [
        {
          "condition": "answer == original fraction",
          "feedback": "That's the original fraction, not the simplified one. Use the results from steps 2 and 3."
        },
        {
          "condition": "answer is equivalent but not fully simplified",
          "feedback": "That fraction is equivalent to the original, but it can be simplified further. Did you divide by the GCF, or by a smaller common factor?"
        },
        {
          "condition": "default",
          "feedback": "The simplified fraction is {simplified_num}/{simplified_den}. Try entering it as a fraction."
        }
      ]
    },
    {
      "step_number": 5,
      "title": "Check your understanding",
      "prompt": "Why does dividing both the numerator and denominator by the same number give an equivalent fraction?",
      "input_type": "multiple_choice",
      "options": [
        "Dividing by {gcf}/{gcf} is the same as dividing by 1, which doesn't change the value",
        "The numerator and denominator get smaller, so the fraction gets smaller",
        "It only works for certain numbers"
      ],
      "correct_answer": 0,
      "hint": "Think about what {gcf}/{gcf} equals. What happens when you divide any number by 1?",
      "wrong_answer_feedback": [
        {
          "condition": "answer == 1",
          "feedback": "The numbers do get smaller, but the fraction's value stays the same. We're dividing top and bottom by the same number — that's like dividing by {gcf}/{gcf} = 1."
        },
        {
          "condition": "answer == 2",
          "feedback": "This works for any common factor, not just certain numbers. The key insight is that dividing top and bottom by the same number is equivalent to dividing the whole fraction by 1."
        }
      ]
    }
  ],

  "completion_message": "You simplified $\\frac{{{numerator}}}{{{denominator}}}$ to $\\frac{{{simplified_num}}}{{{simplified_den}}}$ by dividing both parts by their GCF of {gcf}. Ready to practice on your own?",

  "transition": {
    "button_text": "Start Practice →",
    "target": "practice"
  }
}
```

---

## Concrete Example: frac-simplify with numbers filled in

If the generator produces numerator=18, denominator=24:

### Intro screen

**Simplifying Fractions**

> A fraction is simplified (or "in lowest terms") when the numerator and denominator share no common factor other than 1. For example, $\frac{6}{8}$ and $\frac{3}{4}$ represent the same quantity — three-quarters — but $\frac{3}{4}$ is simplified because 3 and 4 share no factor besides 1.
>
> The method is straightforward: find the **greatest common factor (GCF)** of the numerator and denominator, then divide both by it. This works because dividing the top and bottom of a fraction by the same number is equivalent to dividing by $\frac{\text{GCF}}{\text{GCF}} = 1$, which doesn't change the fraction's value.
>
> $$\frac{a}{b} = \frac{a \div \gcd(a,b)}{b \div \gcd(a,b)}$$

### Step 1: Identify common factors

**Prompt:** Look at the numerator 18 and denominator 24. What is the greatest common factor (GCF) of these two numbers?

**Input:** `[numeric field]`

- Student types `3` → "3 is a common factor, but it's not the greatest one. Keep looking — is there a larger number that divides both 18 and 24?"
- Student types `6` → ✅ Correct! Advance to step 2.

### Step 2: Divide the numerator

**Prompt:** Divide the numerator 18 by the GCF (6). What do you get?

**Input:** `[numeric field]`

- Student types `3` → ✅ Correct!

### Step 3: Divide the denominator

**Prompt:** Now divide the denominator 24 by the same GCF (6). What do you get?

**Input:** `[numeric field]`

- Student types `4` → ✅ Correct!

### Step 4: Write the simplified fraction

**Prompt:** You divided both the numerator and denominator by 6. Write the simplified fraction.

**Input:** `[MathLive expression field]`

- Student enters `3/4` → ✅ Correct!

### Step 5: Check your understanding

**Prompt:** Why does dividing both the numerator and denominator by the same number give an equivalent fraction?

**Options:**
- (A) Dividing by 6/6 is the same as dividing by 1, which doesn't change the value ✅
- (B) The numerator and denominator get smaller, so the fraction gets smaller
- (C) It only works for certain numbers

### Completion

"You simplified $\frac{18}{24}$ to $\frac{3}{4}$ by dividing both parts by their GCF of 6. Ready to practice on your own?"

**[Start Practice →]**  **[Try Another Example]**

---

## Implementation Notes

### Number regeneration
The `problem_generator` section defines how to pick fresh numbers. The backend generates a concrete instance by:
1. Sampling params within the specified ranges and constraints
2. Computing derived values
3. Substituting `{variable}` placeholders throughout all steps

This means the JSON template is a **template with placeholders**, and the backend has a small `walkthrough_generator.py` that hydrates it into a concrete walkthrough instance for each session.

### Architecture
- **Template storage:** `backend/data/walkthroughs/{node_id}.json` — one per node
- **Runtime hydration:** `backend/app/services/walkthrough_generator.py` — reads template, generates numbers, substitutes placeholders, returns concrete JSON to frontend
- **API endpoint:** `GET /api/walkthrough/{node_id}` — returns a hydrated walkthrough instance
- **Frontend component:** `frontend/src/pages/WalkthroughPage.jsx` — renders the intro, steps, and completion screen
- **Answer validation:** Can reuse `answer_checker.py` for expression steps; numeric and MC steps are trivial to validate

### What changes from current flow
- `LessonPage.jsx` is replaced by `WalkthroughPage.jsx` for any node that has a walkthrough template
- Nodes without a walkthrough template fall back to the static lesson (graceful degradation during rollout)
- The "Skip to Practice" button is always visible (links to PracticePage)
- Dashboard topic cards link to walkthrough instead of lesson

### Scaling to 176 nodes
After the pilot is working:
1. Write 4-5 more walkthroughs by hand across different subjects (one calc, one linalg, one prob, one stat) to establish quality patterns
2. AI-generate the remaining ~170 templates using the hand-written ones as few-shot examples
3. Review and iterate
