"""
Seed lesson content and worked examples for all knowledge nodes.
Run after seed_knowledge_graph.py.

Usage (from project root):
    docker compose run --rm backend python scripts/seed_lessons.py
"""
from app.database import SessionLocal
from app.models.content import Lesson, WorkedExample
from app.models.knowledge import KnowledgeNode
import app.models  # noqa

LESSONS = {
    "frac-simplify": {
        "video_url": "https://www.youtube.com/embed/MXRZ46YlFao",
        "content_markdown": """## Simplifying Fractions

A fraction is in **simplest form** (or lowest terms) when the numerator and denominator share no common factor other than 1.

### The Method

To simplify a fraction:
1. Find the **Greatest Common Divisor (GCD)** of the numerator and denominator
2. Divide both by the GCD

> **Key Formula:** \\(\\frac{a}{b} = \\frac{a \\div \\gcd(a,b)}{b \\div \\gcd(a,b)}\\)

### Example

Simplify \\(\\frac{12}{18}\\):
- Factors of 12: 1, 2, 3, **6**, 12
- Factors of 18: 1, 2, 3, **6**, 9, 18
- GCD = 6
- \\(\\frac{12 \\div 6}{18 \\div 6} = \\frac{2}{3}\\)

### Why This Matters for Statistics

In probability calculations, you'll constantly compute ratios like \\(\\frac{4}{16} = \\frac{1}{4}\\). Simplifying fractions makes these results easier to interpret.
""",
        "examples": [
            {
                "problem": "Simplify \\(\\frac{18}{24}\\)",
                "steps": [
                    {"step": 1, "text": "Find factors of both numbers", "result": "18: 1, 2, 3, **6**, 9, 18 — 24: 1, 2, 3, 4, **6**, 8, 12, 24"},
                    {"step": 2, "text": "Identify the GCD", "result": "GCD(18, 24) = 6"},
                    {"step": 3, "text": "Divide numerator and denominator by 6", "result": "\\(\\frac{18 \\div 6}{24 \\div 6} = \\frac{3}{4}\\)"},
                ]
            },
            {
                "problem": "Simplify \\(\\frac{35}{49}\\)",
                "steps": [
                    {"step": 1, "text": "Find GCD of 35 and 49", "result": "35 = 5 × 7, 49 = 7 × 7, so GCD = 7"},
                    {"step": 2, "text": "Divide both by 7", "result": "\\(\\frac{35 \\div 7}{49 \\div 7} = \\frac{5}{7}\\)"},
                ]
            }
        ]
    },
    "frac-add-like": {
        "video_url": "https://www.youtube.com/embed/52ZlXsFJULI",
        "content_markdown": """## Adding and Subtracting Fractions with Like Denominators

When fractions share the same denominator, adding or subtracting is straightforward.

> **Rule:** \\(\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}\\)

Simply add (or subtract) the numerators and keep the denominator the same.

### Example

\\(\\frac{3}{8} + \\frac{1}{8} = \\frac{3+1}{8} = \\frac{4}{8} = \\frac{1}{2}\\)

**Remember to simplify your answer!**
""",
        "examples": [
            {
                "problem": "Add: \\(\\frac{2}{9} + \\frac{4}{9}\\)",
                "steps": [
                    {"step": 1, "text": "Denominators are the same (9), so add numerators", "result": "2 + 4 = 6"},
                    {"step": 2, "text": "Write result over common denominator", "result": "\\(\\frac{6}{9}\\)"},
                    {"step": 3, "text": "Simplify: GCD(6,9) = 3", "result": "\\(\\frac{6 \\div 3}{9 \\div 3} = \\frac{2}{3}\\)"},
                ]
            },
            {
                "problem": "Subtract: \\(\\frac{7}{10} - \\frac{3}{10}\\)",
                "steps": [
                    {"step": 1, "text": "Same denominator — subtract numerators", "result": "7 − 3 = 4"},
                    {"step": 2, "text": "Result", "result": "\\(\\frac{4}{10} = \\frac{2}{5}\\)"},
                ]
            }
        ]
    },
    "frac-common-denom": {
        "video_url": "https://www.youtube.com/embed/pPCqwjxUbvk",
        "content_markdown": """## Finding Common Denominators

To add or subtract fractions with different denominators, we need a **common denominator** — a number that both denominators divide evenly into.

### Method 1: Least Common Multiple (LCM)

The **Least Common Denominator (LCD)** is the smallest number both denominators divide into.

**To find the LCD:**
1. List multiples of each denominator
2. Find the smallest multiple that appears in both lists

### Example

Find LCD of \\(\\frac{1}{4}\\) and \\(\\frac{1}{6}\\):
- Multiples of 4: 4, 8, **12**, 16…
- Multiples of 6: 6, **12**, 18…
- LCD = 12

### Method 2: Multiply the Denominators

If the denominators share no common factors, LCD = denominator₁ × denominator₂.

For \\(\\frac{1}{5}\\) and \\(\\frac{1}{7}\\): LCD = 5 × 7 = 35
""",
        "examples": [
            {
                "problem": "Find the LCD of \\(\\frac{2}{3}\\) and \\(\\frac{5}{8}\\)",
                "steps": [
                    {"step": 1, "text": "List multiples of 3", "result": "3, 6, 9, 12, 15, 18, 21, 24…"},
                    {"step": 2, "text": "List multiples of 8", "result": "8, 16, 24…"},
                    {"step": 3, "text": "First common multiple", "result": "LCD = 24"},
                ]
            }
        ]
    },
    "frac-add-unlike": {
        "video_url": "https://www.youtube.com/embed/DopFT7XbdYo",
        "content_markdown": """## Adding Fractions with Unlike Denominators

**Step-by-step process:**
1. Find the LCD (least common denominator)
2. Convert each fraction to an equivalent fraction with the LCD
3. Add the numerators
4. Simplify if possible

> **Converting:** Multiply top and bottom by whatever makes denominator = LCD
> \\(\\frac{1}{4} = \\frac{1 \\times 3}{4 \\times 3} = \\frac{3}{12}\\)
""",
        "examples": [
            {
                "problem": "Add: \\(\\frac{1}{3} + \\frac{1}{4}\\)",
                "steps": [
                    {"step": 1, "text": "LCD of 3 and 4", "result": "LCD = 12"},
                    {"step": 2, "text": "Convert fractions", "result": "\\(\\frac{1}{3} = \\frac{4}{12}\\), \\(\\frac{1}{4} = \\frac{3}{12}\\)"},
                    {"step": 3, "text": "Add", "result": "\\(\\frac{4}{12} + \\frac{3}{12} = \\frac{7}{12}\\)"},
                ]
            },
            {
                "problem": "Subtract: \\(\\frac{5}{6} - \\frac{1}{4}\\)",
                "steps": [
                    {"step": 1, "text": "LCD of 6 and 4 = 12", "result": ""},
                    {"step": 2, "text": "Convert", "result": "\\(\\frac{5}{6} = \\frac{10}{12}\\), \\(\\frac{1}{4} = \\frac{3}{12}\\)"},
                    {"step": 3, "text": "Subtract", "result": "\\(\\frac{10}{12} - \\frac{3}{12} = \\frac{7}{12}\\)"},
                ]
            }
        ]
    },
    "frac-multiply": {
        "video_url": "https://www.youtube.com/embed/EIdoKBGh5qs",
        "content_markdown": """## Multiplying Fractions

Multiplying fractions is simpler than adding — no common denominator needed!

> **Rule:** \\(\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}\\)

**Tip:** Cross-cancel before multiplying to keep numbers small.

### Example

\\(\\frac{3}{4} \\times \\frac{8}{9}\\):
- Cross-cancel: 3 and 9 share factor 3; 8 and 4 share factor 4
- \\(\\frac{\\cancel{3}^1}{\\cancel{4}_1} \\times \\frac{\\cancel{8}^2}{\\cancel{9}_3} = \\frac{1 \\times 2}{1 \\times 3} = \\frac{2}{3}\\)
""",
        "examples": [
            {
                "problem": "Multiply: \\(\\frac{4}{5} \\times \\frac{15}{16}\\)",
                "steps": [
                    {"step": 1, "text": "Multiply numerators and denominators", "result": "\\(\\frac{4 \\times 15}{5 \\times 16} = \\frac{60}{80}\\)"},
                    {"step": 2, "text": "Simplify: GCD(60, 80) = 20", "result": "\\(\\frac{60 \\div 20}{80 \\div 20} = \\frac{3}{4}\\)"},
                ]
            }
        ]
    },
    "frac-divide": {
        "video_url": "https://www.youtube.com/embed/VZzIJnICPtM",
        "content_markdown": """## Dividing Fractions

> **Rule:** To divide by a fraction, multiply by its **reciprocal**.

\\(\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\times \\frac{d}{c}\\)

**"Keep, Change, Flip"** — keep the first fraction, change ÷ to ×, flip the second fraction.
""",
        "examples": [
            {
                "problem": "Divide: \\(\\frac{5}{6} \\div \\frac{2}{3}\\)",
                "steps": [
                    {"step": 1, "text": "Keep, Change, Flip", "result": "\\(\\frac{5}{6} \\times \\frac{3}{2}\\)"},
                    {"step": 2, "text": "Multiply", "result": "\\(\\frac{15}{12}\\)"},
                    {"step": 3, "text": "Simplify", "result": "\\(\\frac{5}{4}\\)"},
                ]
            }
        ]
    },
    "order-pemdas": {
        "video_url": "https://www.youtube.com/embed/ClYdw4d4OmA",
        "content_markdown": """## Order of Operations (PEMDAS)

When an expression has multiple operations, the order in which you perform them matters.

> **PEMDAS:**
> - **P**arentheses
> - **E**xponents
> - **M**ultiplication and **D**ivision (left to right)
> - **A**ddition and **S**ubtraction (left to right)

### Example

\\(3 + 4 \\times 2^2 - (1 + 5)\\)

1. Parentheses: \\(3 + 4 \\times 2^2 - 6\\)
2. Exponents: \\(3 + 4 \\times 4 - 6\\)
3. Multiplication: \\(3 + 16 - 6\\)
4. Addition/Subtraction (left→right): \\(19 - 6 = 13\\)
""",
        "examples": [
            {
                "problem": "Evaluate: \\(2 + 3 \\times 4 - 1\\)",
                "steps": [
                    {"step": 1, "text": "Multiplication first: 3 × 4 = 12", "result": "\\(2 + 12 - 1\\)"},
                    {"step": 2, "text": "Left to right: 2 + 12 = 14", "result": "\\(14 - 1\\)"},
                    {"step": 3, "text": "Subtract", "result": "13"},
                ]
            }
        ]
    },
    "order-nested": {
        "video_url": "https://www.youtube.com/embed/5OdvA03UFFA",
        "content_markdown": """## Nested Expressions and Grouping

When parentheses are nested inside other grouping symbols, always work **from the innermost outward**.

**Grouping symbols** (all treated like parentheses):
- Parentheses ( )
- Brackets [ ]
- Braces { }
- Fraction bars (treat numerator/denominator separately)

### Example

\\(3 \\times [2 + (4 - 1)]\\)
1. Innermost: \\((4-1) = 3\\)
2. Next: \\([2+3] = 5\\)
3. Outer: \\(3 \\times 5 = 15\\)
""",
        "examples": [
            {
                "problem": "Evaluate: \\(\\{2 \\times [3 + (5-2)]\\} - 4\\)",
                "steps": [
                    {"step": 1, "text": "Innermost parentheses: (5−2) = 3", "result": "\\(\\{2 \\times [3+3]\\} - 4\\)"},
                    {"step": 2, "text": "Brackets: [3+3] = 6", "result": "\\(\\{2 \\times 6\\} - 4\\)"},
                    {"step": 3, "text": "Braces: 2×6 = 12", "result": "\\(12 - 4 = 8\\)"},
                ]
            }
        ]
    },
    "exp-product": {
        "video_url": "https://www.youtube.com/embed/X7pnJ4M_P3Q",
        "content_markdown": """## Product Rule for Exponents

When multiplying two powers with the **same base**, add the exponents.

> \\(x^a \\cdot x^b = x^{a+b}\\)

### Why?
\\(x^3 \\cdot x^4 = (x \\cdot x \\cdot x)(x \\cdot x \\cdot x \\cdot x) = x^7\\)

### Examples
- \\(2^3 \\cdot 2^5 = 2^8 = 256\\)
- \\(y^2 \\cdot y^7 = y^9\\)
- \\(3^1 \\cdot 3^4 = 3^5 = 243\\)

**Note:** This only works when the bases are identical!
""",
        "examples": [
            {
                "problem": "Simplify: \\(x^4 \\cdot x^3\\)",
                "steps": [
                    {"step": 1, "text": "Same base (x), so add exponents", "result": "4 + 3 = 7"},
                    {"step": 2, "text": "Write result", "result": "\\(x^7\\)"},
                ]
            }
        ]
    },
    "exp-power": {
        "video_url": "https://www.youtube.com/embed/Bsq8VRx5wF4",
        "content_markdown": """## Power Rule for Exponents

When raising a power to another power, **multiply** the exponents.

> \\((x^a)^b = x^{a \\cdot b}\\)

### Why?
\\((x^3)^4 = x^3 \\cdot x^3 \\cdot x^3 \\cdot x^3 = x^{3+3+3+3} = x^{12}\\)

### Examples
- \\((2^3)^2 = 2^6 = 64\\)
- \\((y^5)^3 = y^{15}\\)
- \\((a^2)^0 = a^0 = 1\\)
""",
        "examples": [
            {
                "problem": "Simplify: \\((x^3)^5\\)",
                "steps": [
                    {"step": 1, "text": "Power rule: multiply exponents", "result": "3 × 5 = 15"},
                    {"step": 2, "text": "Result", "result": "\\(x^{15}\\)"},
                ]
            }
        ]
    },
    "exp-negative": {
        "video_url": "https://www.youtube.com/embed/JnpqlXN9Whw",
        "content_markdown": """## Negative and Zero Exponents

> **Zero exponent:** \\(x^0 = 1\\) for any \\(x \\neq 0\\)

> **Negative exponent:** \\(x^{-n} = \\frac{1}{x^n}\\)

### Intuition

\\(x^3 = x \\cdot x \\cdot x\\), so dividing by \\(x\\) each time:
- \\(x^3 \\to x^2 \\to x^1 \\to x^0 = 1 \\to x^{-1} = \\frac{1}{x}\\)

### Examples
- \\(5^0 = 1\\)
- \\(2^{-4} = \\frac{1}{2^4} = \\frac{1}{16}\\)
- \\(x^{-2} = \\frac{1}{x^2}\\)
""",
        "examples": [
            {
                "problem": "Simplify: \\(3^{-2}\\)",
                "steps": [
                    {"step": 1, "text": "Negative exponent means reciprocal", "result": "\\(\\frac{1}{3^2}\\)"},
                    {"step": 2, "text": "Evaluate denominator", "result": "\\(\\frac{1}{9}\\)"},
                ]
            }
        ]
    },
    "exp-combined": {
        "video_url": "https://www.youtube.com/embed/hs_LBRPVTho",
        "content_markdown": """## Combining Exponent Rules

Real expressions often require multiple rules. The **quotient rule** is one more tool:

> **Quotient rule:** \\(\\frac{x^a}{x^b} = x^{a-b}\\)

### All Four Rules:
| Rule | Formula |
|------|---------|
| Product | \\(x^a \\cdot x^b = x^{a+b}\\) |
| Power | \\((x^a)^b = x^{ab}\\) |
| Negative | \\(x^{-n} = \\frac{1}{x^n}\\) |
| Quotient | \\(\\frac{x^a}{x^b} = x^{a-b}\\) |

### Strategy

Work through one rule at a time:
1. Handle parentheses first (power rule)
2. Apply product/quotient rules
3. Handle negatives last
""",
        "examples": [
            {
                "problem": "Simplify: \\(\\frac{x^6 \\cdot x^{-2}}{x^3}\\)",
                "steps": [
                    {"step": 1, "text": "Numerator: product rule", "result": "\\(x^{6+(-2)} = x^4\\)"},
                    {"step": 2, "text": "Quotient rule", "result": "\\(\\frac{x^4}{x^3} = x^{4-3} = x^1 = x\\)"},
                ]
            }
        ]
    },
    "eq-one-step": {
        "video_url": "https://www.youtube.com/embed/Js-cAn9DRDQ",
        "content_markdown": """## One-Step Linear Equations

A **linear equation** states that two expressions are equal. To solve it, isolate the variable on one side.

**Golden rule:** Whatever you do to one side, do to the other.

| Operation in equation | Undo it with |
|----------------------|--------------|
| Addition (+a) | Subtract (−a) |
| Subtraction (−a) | Add (+a) |
| Multiplication (×a) | Divide (÷a) |
| Division (÷a) | Multiply (×a) |
""",
        "examples": [
            {
                "problem": "Solve: \\(x + 9 = 15\\)",
                "steps": [
                    {"step": 1, "text": "Subtract 9 from both sides", "result": "\\(x + 9 - 9 = 15 - 9\\)"},
                    {"step": 2, "text": "Simplify", "result": "\\(x = 6\\)"},
                ]
            },
            {
                "problem": "Solve: \\(4x = 28\\)",
                "steps": [
                    {"step": 1, "text": "Divide both sides by 4", "result": "\\(\\frac{4x}{4} = \\frac{28}{4}\\)"},
                    {"step": 2, "text": "Simplify", "result": "\\(x = 7\\)"},
                ]
            }
        ]
    },
    "eq-two-step": {
        "video_url": "https://www.youtube.com/embed/tuVd355R-OQ",
        "content_markdown": """## Two-Step Linear Equations

Two-step equations require exactly two operations to isolate the variable.

**Order of operations (reversed!):** Undo addition/subtraction first, then multiplication/division.

### Example

Solve \\(2x + 5 = 13\\):
1. Subtract 5: \\(2x = 8\\)
2. Divide by 2: \\(x = 4\\)
""",
        "examples": [
            {
                "problem": "Solve: \\(3x - 7 = 14\\)",
                "steps": [
                    {"step": 1, "text": "Add 7 to both sides", "result": "\\(3x = 21\\)"},
                    {"step": 2, "text": "Divide by 3", "result": "\\(x = 7\\)"},
                ]
            }
        ]
    },
    "eq-fractions": {
        "video_url": "https://www.youtube.com/embed/kbqO0YTUyAY",
        "content_markdown": """## Equations with Fractions

**Elimination method:** Multiply both sides by the LCD to clear all fractions.

### Example

Solve \\(\\frac{x}{3} + \\frac{x}{6} = 5\\):
1. LCD = 6
2. Multiply through: \\(2x + x = 30\\)
3. \\(3x = 30 \\Rightarrow x = 10\\)
""",
        "examples": [
            {
                "problem": "Solve: \\(\\frac{x}{4} + \\frac{x}{8} = 3\\)",
                "steps": [
                    {"step": 1, "text": "LCD of 4 and 8 is 8. Multiply through by 8", "result": "\\(2x + x = 24\\)"},
                    {"step": 2, "text": "Combine like terms", "result": "\\(3x = 24\\)"},
                    {"step": 3, "text": "Divide by 3", "result": "\\(x = 8\\)"},
                ]
            }
        ]
    },
    "eq-distribution": {
        "video_url": "https://www.youtube.com/embed/q7uMHXNr4qA",
        "content_markdown": """## Equations with Distribution

The **Distributive Property:** \\(a(b + c) = ab + ac\\)

Use this to expand parentheses before solving.

### Example

Solve \\(5(x - 2) = 20\\):
1. Distribute: \\(5x - 10 = 20\\)
2. Add 10: \\(5x = 30\\)
3. Divide by 5: \\(x = 6\\)
""",
        "examples": [
            {
                "problem": "Solve: \\(2(3x + 4) = 26\\)",
                "steps": [
                    {"step": 1, "text": "Distribute the 2", "result": "\\(6x + 8 = 26\\)"},
                    {"step": 2, "text": "Subtract 8", "result": "\\(6x = 18\\)"},
                    {"step": 3, "text": "Divide by 6", "result": "\\(x = 3\\)"},
                ]
            }
        ]
    },
    "eq-quadratic": {
        "video_url": "https://www.youtube.com/embed/i7idZfS8t8w",
        "content_markdown": """## Quadratic Equations by Factoring

A **quadratic equation** has the form \\(ax^2 + bx + c = 0\\).

**Factoring method:** Find two numbers that multiply to \\(c\\) and add to \\(b\\).

### Example

Solve \\(x^2 - 7x + 12 = 0\\):
- Need two numbers: product = 12, sum = −7
- Those numbers are −3 and −4
- Factor: \\((x - 3)(x - 4) = 0\\)
- Solutions: \\(x = 3\\) or \\(x = 4\\)

> **Zero-Product Property:** If \\(AB = 0\\), then \\(A = 0\\) or \\(B = 0\\).
""",
        "examples": [
            {
                "problem": "Solve: \\(x^2 + 6x + 8 = 0\\)",
                "steps": [
                    {"step": 1, "text": "Find two numbers: product = 8, sum = 6", "result": "2 and 4"},
                    {"step": 2, "text": "Factor", "result": "\\((x+2)(x+4) = 0\\)"},
                    {"step": 3, "text": "Zero-product property", "result": "\\(x = -2\\) or \\(x = -4\\)"},
                ]
            }
        ]
    },
    "log-exponential": {
        "video_url": "https://www.youtube.com/embed/xILliUBvNyk",
        "content_markdown": """## Exponential Functions

An **exponential function** has the form \\(f(x) = a^x\\) where \\(a > 0, a \\neq 1\\).

### Key Properties

| Property | Value |
|----------|-------|
| \\(a^0\\) | 1 (always) |
| \\(a^1\\) | a |
| \\(a^{-x}\\) | \\(\\frac{1}{a^x}\\) |
| Growth (a > 1) | Increasing |
| Decay (0 < a < 1) | Decreasing |

### Why Important for Statistics?

Exponential growth/decay appears in population models, compound interest, and probability distributions (like the geometric distribution).
""",
        "examples": [
            {
                "problem": "Evaluate \\(f(3)\\) for \\(f(x) = 2^x\\)",
                "steps": [
                    {"step": 1, "text": "Substitute x = 3", "result": "\\(f(3) = 2^3\\)"},
                    {"step": 2, "text": "Evaluate", "result": "\\(2^3 = 8\\)"},
                ]
            }
        ]
    },
    "log-definition": {
        "video_url": "https://www.youtube.com/embed/Z5myJ8dg_rM",
        "content_markdown": """## Logarithm Definition

A **logarithm** is the inverse of exponentiation.

> \\(\\log_b(x) = y \\iff b^y = x\\)

Read \\(\\log_b(x)\\) as "log base b of x" = "what power must b be raised to in order to get x?"

### Common Bases
- **Base 10** (common log): \\(\\log_{10}(x) = \\log(x)\\)
- **Base e** (natural log): \\(\\log_e(x) = \\ln(x)\\)

### Examples
- \\(\\log_2(32) = 5\\) because \\(2^5 = 32\\)
- \\(\\log_{10}(100) = 2\\) because \\(10^2 = 100\\)
""",
        "examples": [
            {
                "problem": "Evaluate \\(\\log_3(81)\\)",
                "steps": [
                    {"step": 1, "text": "Ask: 3 to what power equals 81?", "result": "\\(3^? = 81\\)"},
                    {"step": 2, "text": "Try powers of 3: 3¹=3, 3²=9, 3³=27, 3⁴=81", "result": ""},
                    {"step": 3, "text": "Answer", "result": "\\(\\log_3(81) = 4\\)"},
                ]
            }
        ]
    },
    "log-rules": {
        "video_url": "https://www.youtube.com/embed/TMmxKZaCqe0",
        "content_markdown": """## Logarithm Rules

> **Product Rule:** \\(\\log_b(MN) = \\log_b(M) + \\log_b(N)\\)

> **Quotient Rule:** \\(\\log_b\\left(\\frac{M}{N}\\right) = \\log_b(M) - \\log_b(N)\\)

> **Power Rule:** \\(\\log_b(M^p) = p \\cdot \\log_b(M)\\)

### Examples
- \\(\\log_2(4 \\cdot 8) = \\log_2(4) + \\log_2(8) = 2 + 3 = 5\\)
- \\(\\log_3(27^2) = 2 \\log_3(27) = 2 \\times 3 = 6\\)
""",
        "examples": [
            {
                "problem": "Expand: \\(\\log_2(\\frac{x^3}{y})\\)",
                "steps": [
                    {"step": 1, "text": "Quotient rule", "result": "\\(\\log_2(x^3) - \\log_2(y)\\)"},
                    {"step": 2, "text": "Power rule on first term", "result": "\\(3\\log_2(x) - \\log_2(y)\\)"},
                ]
            }
        ]
    },
    "log-equations": {
        "video_url": "https://www.youtube.com/embed/sE5Cpxs1_8k",
        "content_markdown": """## Solving Logarithmic Equations

**Strategy 1:** Convert to exponential form.

\\(\\log_b(x) = c \\Rightarrow x = b^c\\)

**Strategy 2:** Use log rules to combine logs, then convert.

### Example

Solve \\(\\log_2(x+3) = 4\\):
1. Convert: \\(x + 3 = 2^4 = 16\\)
2. Solve: \\(x = 13\\)
""",
        "examples": [
            {
                "problem": "Solve: \\(\\log_5(2x+1) = 2\\)",
                "steps": [
                    {"step": 1, "text": "Convert to exponential form", "result": "\\(2x + 1 = 5^2 = 25\\)"},
                    {"step": 2, "text": "Subtract 1", "result": "\\(2x = 24\\)"},
                    {"step": 3, "text": "Divide by 2", "result": "\\(x = 12\\)"},
                ]
            }
        ]
    },
    "sum-sigma": {
        "video_url": "https://www.youtube.com/embed/5jwXThH6fg4",
        "content_markdown": """## Sigma Notation

**Sigma (Σ) notation** is a compact way to write sums.

> \\(\\sum_{i=1}^{n} a_i = a_1 + a_2 + a_3 + \\cdots + a_n\\)

**Parts:**
- \\(\\Sigma\\) — means "sum of"
- \\(i\\) — the **index** (counter)
- \\(1\\) (below) — **lower bound** (starting value)
- \\(n\\) (above) — **upper bound** (ending value)
- \\(a_i\\) — the **summand** (formula to evaluate at each i)

### Example

\\(\\sum_{i=1}^{4} i^2 = 1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30\\)
""",
        "examples": [
            {
                "problem": "Evaluate: \\(\\sum_{k=1}^{4} (2k+1)\\)",
                "steps": [
                    {"step": 1, "text": "Substitute k = 1, 2, 3, 4", "result": "(2·1+1) + (2·2+1) + (2·3+1) + (2·4+1)"},
                    {"step": 2, "text": "Simplify each term", "result": "3 + 5 + 7 + 9"},
                    {"step": 3, "text": "Sum", "result": "24"},
                ]
            }
        ]
    },
    "sum-arithmetic": {
        "video_url": "https://www.youtube.com/embed/XZJdyPkCxuE",
        "content_markdown": """## Arithmetic Sums

An **arithmetic sequence** has a constant difference between consecutive terms.

> **Sum formula:** \\(S_n = \\frac{n(a_1 + a_n)}{2} = \\frac{n(2a_1 + (n-1)d)}{2}\\)

Where:
- \\(n\\) = number of terms
- \\(a_1\\) = first term
- \\(a_n\\) = last term
- \\(d\\) = common difference

### Example

Sum of first 100 integers: \\(S_{100} = \\frac{100(1+100)}{2} = \\frac{100 \\times 101}{2} = 5050\\)

> **In statistics:** Used to compute expected values of discrete uniform distributions.
""",
        "examples": [
            {
                "problem": "Find \\(\\sum_{i=1}^{6} i = 1+2+3+4+5+6\\)",
                "steps": [
                    {"step": 1, "text": "Use formula: n(n+1)/2 with n=6", "result": "\\(\\frac{6 \\times 7}{2}\\)"},
                    {"step": 2, "text": "Compute", "result": "\\(\\frac{42}{2} = 21\\)"},
                ]
            }
        ]
    },
    "sum-nested": {
        "video_url": "https://www.youtube.com/embed/XOMJPQPG1Dc",
        "content_markdown": """## Nested (Double) Summations

A **double sum** has one sigma inside another.

> \\(\\sum_{i=1}^{m} \\sum_{j=1}^{n} a_{ij}\\)

**Evaluate the inner sum first (for each fixed value of i), then sum the results.**

### Example

\\(\\sum_{i=1}^{2} \\sum_{j=1}^{3} ij\\)

- i=1: \\(\\sum_{j=1}^{3} 1 \\cdot j = 1+2+3 = 6\\)
- i=2: \\(\\sum_{j=1}^{3} 2 \\cdot j = 2+4+6 = 12\\)
- Total: \\(6 + 12 = 18\\)

> **In statistics:** Variance formulas often involve double sums.
""",
        "examples": [
            {
                "problem": "Evaluate \\(\\sum_{i=1}^{2}\\sum_{j=1}^{2}(i+j)\\)",
                "steps": [
                    {"step": 1, "text": "Fix i=1, sum over j: (1+1)+(1+2) = 2+3 = 5", "result": ""},
                    {"step": 2, "text": "Fix i=2, sum over j: (2+1)+(2+2) = 3+4 = 7", "result": ""},
                    {"step": 3, "text": "Add outer results", "result": "5 + 7 = 12"},
                ]
            }
        ]
    },
    "comb-counting": {
        "video_url": "https://www.youtube.com/embed/XqQTXW7XfYA",
        "content_markdown": """## Counting Principles

**Fundamental Counting Principle:** If event A can occur in \\(m\\) ways and event B can occur in \\(n\\) ways, then both events together can occur in \\(m \\times n\\) ways.

### Addition Rule

If events are **mutually exclusive** (can't both happen), count their possibilities by adding.

### Multiplication Rule

If events are **sequential** (one after another), multiply.

### Example

A menu has 3 soups, 4 entrees, and 2 desserts. Number of 3-course meals = \\(3 \\times 4 \\times 2 = 24\\).

> **In statistics:** The foundation of probability — counting equally likely outcomes.
""",
        "examples": [
            {
                "problem": "How many 3-digit codes can be formed from digits 0–9 with no repetition?",
                "steps": [
                    {"step": 1, "text": "First digit: 10 choices (0–9)", "result": "10"},
                    {"step": 2, "text": "Second digit: 9 remaining choices", "result": "9"},
                    {"step": 3, "text": "Third digit: 8 remaining choices", "result": "\\(10 \\times 9 \\times 8 = 720\\)"},
                ]
            }
        ]
    },
    "comb-permutations": {
        "video_url": "https://www.youtube.com/embed/DROZVHObeko",
        "content_markdown": """## Permutations

A **permutation** is an **ordered** arrangement of objects.

> \\(P(n, r) = \\frac{n!}{(n-r)!}\\)

Where \\(n!\\) (n factorial) = \\(n \\times (n-1) \\times \\cdots \\times 2 \\times 1\\).

### Example

How many ways to arrange 3 books from a shelf of 7?

\\(P(7, 3) = \\frac{7!}{4!} = 7 \\times 6 \\times 5 = 210\\)

> **Key question:** Does order matter? If YES → permutations.
""",
        "examples": [
            {
                "problem": "In how many ways can 5 students be arranged in a line?",
                "steps": [
                    {"step": 1, "text": "This is P(5,5) = 5!", "result": ""},
                    {"step": 2, "text": "5! = 5 × 4 × 3 × 2 × 1", "result": "= 120"},
                ]
            }
        ]
    },
    "comb-combinations": {
        "video_url": "https://www.youtube.com/embed/iKy-d5_erhI",
        "content_markdown": """## Combinations

A **combination** is an **unordered** selection of objects.

> \\(C(n, r) = \\binom{n}{r} = \\frac{n!}{r!(n-r)!}\\)

### Permutations vs. Combinations

| | Permutations | Combinations |
|--|--|--|
| Order matters? | Yes | No |
| Formula | \\(P(n,r) = \\frac{n!}{(n-r)!}\\) | \\(C(n,r) = \\frac{n!}{r!(n-r)!}\\) |

### Example

Choose 3 students from 8 for a committee:
\\(C(8,3) = \\frac{8!}{3! \\cdot 5!} = \\frac{8 \\times 7 \\times 6}{3 \\times 2 \\times 1} = 56\\)

> **Binomial coefficients** \\(\\binom{n}{r}\\) appear throughout probability (binomial distribution, etc.).
""",
        "examples": [
            {
                "problem": "How many 2-card hands can be dealt from a 52-card deck?",
                "steps": [
                    {"step": 1, "text": "Order doesn't matter → combinations", "result": "\\(C(52, 2)\\)"},
                    {"step": 2, "text": "Apply formula", "result": "\\(\\frac{52!}{2! \\cdot 50!} = \\frac{52 \\times 51}{2} = 1326\\)"},
                ]
            }
        ]
    },
    "geo-sequences": {
        "video_url": "https://www.youtube.com/embed/pXo0bG4iAyg",
        "content_markdown": """## Geometric Sequences

A **geometric sequence** multiplies each term by a constant ratio \\(r\\).

> \\(a_n = a_1 \\cdot r^{n-1}\\)

### Identifying the Ratio

Divide any term by the previous term: \\(r = \\frac{a_{n+1}}{a_n}\\)

### Example

Sequence: 3, 6, 12, 24, …
- Common ratio: \\(r = 6/3 = 2\\)
- 5th term: \\(a_5 = 3 \\cdot 2^4 = 48\\)

### In Statistics

Geometric sequences model geometric distributions and waiting times.
""",
        "examples": [
            {
                "problem": "Find the 6th term of the sequence: 5, 15, 45, …",
                "steps": [
                    {"step": 1, "text": "Find r: 15/5 = 3", "result": "r = 3"},
                    {"step": 2, "text": "Apply formula: a₆ = 5 · 3⁵", "result": "5 · 243"},
                    {"step": 3, "text": "Compute", "result": "1215"},
                ]
            }
        ]
    },
    "geo-finite": {
        "video_url": "https://www.youtube.com/embed/27iSnzss2wM",
        "content_markdown": """## Finite Geometric Series

The sum of \\(n\\) terms of a geometric series:

> \\(S_n = a_1 \\cdot \\frac{1 - r^n}{1 - r}\\) for \\(r \\neq 1\\)

Where \\(a_1\\) is the first term and \\(r\\) is the common ratio.

### Example

Sum of first 5 terms of 2, 6, 18, 54, 162:
- \\(a_1 = 2\\), \\(r = 3\\), \\(n = 5\\)
- \\(S_5 = 2 \\cdot \\frac{1 - 3^5}{1 - 3} = 2 \\cdot \\frac{-242}{-2} = 242\\)
""",
        "examples": [
            {
                "problem": "Find the sum of 4 terms: 1 + 2 + 4 + 8",
                "steps": [
                    {"step": 1, "text": "a₁ = 1, r = 2, n = 4", "result": ""},
                    {"step": 2, "text": "Apply formula: S₄ = 1·(1-2⁴)/(1-2)", "result": "= (1-16)/(−1)"},
                    {"step": 3, "text": "Simplify", "result": "= (−15)/(−1) = 15"},
                ]
            }
        ]
    },
    "geo-infinite": {
        "video_url": "https://www.youtube.com/embed/b-7kCymoUpg",
        "content_markdown": """## Infinite Geometric Series

When \\(|r| < 1\\), the infinite geometric series **converges** to a finite sum:

> \\(S = \\frac{a_1}{1 - r}\\) (only when \\(|r| < 1\\))

When \\(|r| \\geq 1\\), the series **diverges** (no finite sum).

### Example

\\(1 + \\frac{1}{3} + \\frac{1}{9} + \\frac{1}{27} + \\cdots\\)

- \\(a_1 = 1\\), \\(r = \\frac{1}{3}\\)
- \\(S = \\frac{1}{1 - \\frac{1}{3}} = \\frac{1}{\\frac{2}{3}} = \\frac{3}{2}\\)

### In Statistics

Appears in geometric distribution expected values and moment-generating functions.
""",
        "examples": [
            {
                "problem": "Find the sum: \\(4 + 2 + 1 + \\frac{1}{2} + \\cdots\\)",
                "steps": [
                    {"step": 1, "text": "Identify: a₁ = 4, r = 1/2, |r| < 1 ✓", "result": "Converges"},
                    {"step": 2, "text": "Apply formula: S = 4 / (1 - 1/2)", "result": "= 4 / (1/2)"},
                    {"step": 3, "text": "Simplify", "result": "= 8"},
                ]
            }
        ]
    },
}


def seed():
    db = SessionLocal()
    try:
        nodes = {n.id: n for n in db.query(KnowledgeNode).all()}
        if not nodes:
            print("No nodes found. Run seed_knowledge_graph.py first.")
            return

        lesson_count = 0
        example_count = 0

        for node_id, data in LESSONS.items():
            if node_id not in nodes:
                print(f"Warning: node {node_id} not in DB, skipping.")
                continue

            # Upsert lesson
            existing = db.query(Lesson).filter(Lesson.node_id == node_id).first()
            if existing:
                existing.video_url = data["video_url"]
                existing.content_markdown = data["content_markdown"]
            else:
                lesson = Lesson(
                    node_id=node_id,
                    video_url=data["video_url"],
                    content_markdown=data["content_markdown"],
                )
                db.add(lesson)
            lesson_count += 1

            # Remove existing worked examples
            db.query(WorkedExample).filter(WorkedExample.node_id == node_id).delete()

            # Add worked examples
            for i, ex in enumerate(data.get("examples", [])):
                we = WorkedExample(
                    node_id=node_id,
                    problem_text=ex["problem"],
                    steps=ex["steps"],
                    display_order=i,
                )
                db.add(we)
                example_count += 1

        db.commit()
        print(f"Seeded {lesson_count} lessons and {example_count} worked examples.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
