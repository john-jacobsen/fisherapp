#!/usr/bin/env python3
"""Generate lesson markdown files for all 176 knowledge-graph nodes.

Usage:
    python backend/scripts/generate_lessons.py
"""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "lessons")

LESSONS = {

# ── Fractions ──────────────────────────────────────────────────────────────────
"frac-simplify": """\
# Simplifying Fractions

## Overview

A **fraction** $a/b$ is in simplest form when the numerator and denominator share no common factor other than 1. You simplify by dividing both parts by their greatest common factor (GCF).

## Key Idea

Find GCF$(a, b)$, then divide both top and bottom:

$$\\frac{a}{b} = \\frac{a \\div \\text{GCF}}{b \\div \\text{GCF}}$$

Simplifying never changes the value of the fraction — it only changes how it looks.

## Worked Examples

**Example 1: Simplify $\\frac{12}{18}$**

GCF(12, 18) = 6.

$$\\frac{12}{18} = \\frac{12 \\div 6}{18 \\div 6} = \\frac{2}{3}$$

---

**Example 2: Simplify $\\frac{24}{36}$**

GCF(24, 36) = 12. Therefore $\\frac{24}{36} = \\frac{2}{3}$.

---

**Example 3: Simplify $\\frac{45}{60}$**

GCF(45, 60) = 15.

$$\\frac{45}{60} = \\frac{3}{4}$$

## Common Mistakes

- **Dividing only the numerator or only the denominator.** You must apply the same operation to both parts.
- **Stopping too early.** If you divide by a factor that is not the GCF, the result is still not fully simplified — keep going.
- **Assuming a fraction with small numbers is already simplified.** Check: GCF(4, 6) = 2, so $\\frac{4}{6}$ is not simplified.

## Quick Check

Try these before using hints:

1. Simplify $\\frac{8}{12}$
2. Simplify $\\frac{15}{25}$
3. Simplify $\\frac{30}{45}$

*(Answers: $\\frac{2}{3}$, $\\frac{3}{5}$, $\\frac{2}{3}$)*
""",

"frac-add-like": """\
# Adding Fractions (Like Denominators)

## Overview

When two fractions share the **same denominator**, you add them by adding the numerators and keeping the denominator unchanged. This works because both fractions already use the same-size pieces.

## Key Idea

$$\\frac{a}{c} + \\frac{b}{c} = \\frac{a + b}{c}$$

Always simplify the result if possible.

## Worked Examples

**Example 1: $\\frac{2}{7} + \\frac{3}{7}$**

Same denominator (7), so add numerators:

$$\\frac{2}{7} + \\frac{3}{7} = \\frac{2 + 3}{7} = \\frac{5}{7}$$

---

**Example 2: $\\frac{3}{8} + \\frac{5}{8}$**

$$\\frac{3}{8} + \\frac{5}{8} = \\frac{8}{8} = 1$$

---

**Example 3: $\\frac{4}{9} + \\frac{7}{9}$**

$$\\frac{4}{9} + \\frac{7}{9} = \\frac{11}{9}$$

This is an improper fraction; as a mixed number it equals $1\\frac{2}{9}$.

## Common Mistakes

- **Adding the denominators.** The denominator stays the same — only the numerators are added.
- **Forgetting to simplify.** $\\frac{6}{8} = \\frac{3}{4}$; always check at the end.

## Quick Check

1. $\\frac{1}{5} + \\frac{3}{5}$
2. $\\frac{5}{12} + \\frac{7}{12}$
3. $\\frac{2}{9} + \\frac{4}{9}$

*(Answers: $\\frac{4}{5}$, $1$, $\\frac{6}{9} = \\frac{2}{3}$)*
""",

"frac-common-denom": """\
# Common Denominators

## Overview

A **common denominator** is a shared multiple of two or more denominators. You need one before adding or subtracting fractions with different denominators. The **least common denominator** (LCD) is the smallest such multiple.

## Key Idea

To find the LCD of $\\frac{a}{b}$ and $\\frac{c}{d}$, compute LCM$(b, d)$. Then rewrite each fraction with that denominator:

$$\\frac{a}{b} = \\frac{a \\cdot (\\text{LCD}/b)}{\\text{LCD}}$$

## Worked Examples

**Example 1: Find the LCD of $\\frac{1}{4}$ and $\\frac{1}{6}$**

Multiples of 4: 4, 8, **12**, ... Multiples of 6: 6, **12**, ... LCD = 12.

$$\\frac{1}{4} = \\frac{3}{12}, \\quad \\frac{1}{6} = \\frac{2}{12}$$

---

**Example 2: Rewrite $\\frac{2}{3}$ and $\\frac{3}{4}$ with a common denominator**

LCD(3, 4) = 12.

$$\\frac{2}{3} = \\frac{8}{12}, \\quad \\frac{3}{4} = \\frac{9}{12}$$

---

**Example 3: Find the LCD of $\\frac{5}{6}$ and $\\frac{7}{9}$**

LCM(6, 9) = 18. So $\\frac{5}{6} = \\frac{15}{18}$ and $\\frac{7}{9} = \\frac{14}{18}$.

## Common Mistakes

- **Using the product $b \\cdot d$ when a smaller LCD exists.** This works but creates larger numbers to simplify later.
- **Multiplying only the denominator, not the numerator.** You must multiply both by the same factor to keep the fraction's value.

## Quick Check

1. What is the LCD of $\\frac{1}{3}$ and $\\frac{1}{4}$?
2. Rewrite $\\frac{2}{5}$ with denominator 20.
3. What is the LCD of $\\frac{3}{8}$ and $\\frac{5}{12}$?

*(Answers: 12, $\\frac{8}{20}$, 24)*
""",

"frac-add-unlike": """\
# Adding Fractions (Unlike Denominators)

## Overview

Adding fractions with **different denominators** requires a two-step process: first rewrite both fractions with a common denominator, then add the numerators.

## Key Idea

$$\\frac{a}{b} + \\frac{c}{d} = \\frac{a \\cdot d}{b \\cdot d} + \\frac{c \\cdot b}{b \\cdot d} = \\frac{ad + cb}{bd}$$

Using the LCD instead of $b \\cdot d$ keeps numbers smaller and reduces simplification work.

## Worked Examples

**Example 1: $\\frac{1}{3} + \\frac{1}{4}$**

LCD = 12.

$$\\frac{1}{3} + \\frac{1}{4} = \\frac{4}{12} + \\frac{3}{12} = \\frac{7}{12}$$

---

**Example 2: $\\frac{2}{5} + \\frac{3}{4}$**

LCD = 20.

$$\\frac{2}{5} + \\frac{3}{4} = \\frac{8}{20} + \\frac{15}{20} = \\frac{23}{20}$$

---

**Example 3: $\\frac{5}{6} + \\frac{7}{9}$**

LCD = 18.

$$\\frac{5}{6} + \\frac{7}{9} = \\frac{15}{18} + \\frac{14}{18} = \\frac{29}{18}$$

## Common Mistakes

- **Adding numerators and adding denominators separately.** $\\frac{1}{2} + \\frac{1}{3} \\ne \\frac{2}{5}$.
- **Forgetting to adjust the numerator when changing the denominator.**

## Quick Check

1. $\\frac{1}{2} + \\frac{1}{3}$
2. $\\frac{3}{4} + \\frac{1}{6}$
3. $\\frac{2}{3} + \\frac{3}{5}$

*(Answers: $\\frac{5}{6}$, $\\frac{11}{12}$, $\\frac{19}{15}$)*
""",

"frac-multiply": """\
# Multiplying Fractions

## Overview

**Multiplying fractions** is simpler than adding them: multiply the numerators together and the denominators together. No common denominator is needed.

## Key Idea

$$\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$$

Simplify before multiplying when possible (cross-cancel) to keep numbers small.

## Worked Examples

**Example 1: $\\frac{2}{3} \\cdot \\frac{4}{5}$**

$$\\frac{2}{3} \\cdot \\frac{4}{5} = \\frac{8}{15}$$

---

**Example 2: $\\frac{3}{4} \\cdot \\frac{8}{9}$ (cross-cancel first)**

GCF(3, 9) = 3 and GCF(8, 4) = 4. Cancel before multiplying:

$$\\frac{\\cancel{3}^1}{\\cancel{4}_1} \\cdot \\frac{\\cancel{8}^2}{\\cancel{9}_3} = \\frac{1 \\cdot 2}{1 \\cdot 3} = \\frac{2}{3}$$

---

**Example 3: $\\frac{5}{6} \\cdot \\frac{3}{10}$**

Cancel 5 and 10 (factor of 5), cancel 3 and 6 (factor of 3):

$$\\frac{5}{6} \\cdot \\frac{3}{10} = \\frac{1}{2} \\cdot \\frac{1}{2} = \\frac{1}{4}$$

## Common Mistakes

- **Finding a common denominator before multiplying.** That step is only needed for addition and subtraction.
- **Forgetting to simplify the final answer.**

## Quick Check

1. $\\frac{1}{2} \\cdot \\frac{3}{5}$
2. $\\frac{4}{7} \\cdot \\frac{7}{8}$
3. $\\frac{2}{9} \\cdot \\frac{3}{4}$

*(Answers: $\\frac{3}{10}$, $\\frac{1}{2}$, $\\frac{1}{6}$)*
""",

"frac-divide": """\
# Dividing Fractions

## Overview

**Dividing by a fraction** is equivalent to multiplying by its reciprocal. The reciprocal of $\\frac{a}{b}$ is $\\frac{b}{a}$.

## Key Idea

$$\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\cdot \\frac{d}{c} = \\frac{ad}{bc}$$

The phrase "Keep, Change, Flip" captures the steps: keep the first fraction, change ÷ to ×, flip the second fraction.

## Worked Examples

**Example 1: $\\frac{3}{4} \\div \\frac{2}{5}$**

$$\\frac{3}{4} \\div \\frac{2}{5} = \\frac{3}{4} \\cdot \\frac{5}{2} = \\frac{15}{8}$$

---

**Example 2: $\\frac{2}{3} \\div \\frac{4}{9}$**

$$\\frac{2}{3} \\cdot \\frac{9}{4} = \\frac{18}{12} = \\frac{3}{2}$$

---

**Example 3: $\\frac{5}{6} \\div \\frac{5}{12}$**

$$\\frac{5}{6} \\cdot \\frac{12}{5} = \\frac{60}{30} = 2$$

## Common Mistakes

- **Flipping the first fraction instead of the second.** Always flip the divisor (the fraction you're dividing by).
- **Forgetting to flip at all and just multiplying straight across.**

## Quick Check

1. $\\frac{1}{2} \\div \\frac{1}{4}$
2. $\\frac{3}{5} \\div \\frac{6}{7}$
3. $\\frac{4}{9} \\div \\frac{2}{3}$

*(Answers: 2, $\\frac{7}{10}$, $\\frac{2}{3}$)*
""",

# ── Order of Operations ────────────────────────────────────────────────────────
"order-pemdas": """\
# Order of Operations (PEMDAS)

## Overview

**PEMDAS** (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction) is the agreed-upon order for evaluating mathematical expressions so everyone gets the same answer. Without it, $2 + 3 \\times 4$ would be ambiguous.

## Key Idea

Evaluate in this order:
1. **P**arentheses — innermost first
2. **E**xponents
3. **M**ultiplication and **D**ivision — left to right
4. **A**ddition and **S**ubtraction — left to right

Multiplication and division have equal priority (same for addition and subtraction) — evaluate left to right within each level.

## Worked Examples

**Example 1: $2 + 3 \\times 4$**

Multiplication before addition: $3 \\times 4 = 12$, then $2 + 12 = 14$.

---

**Example 2: $(5 + 3)^2 \\div 4 - 1$**

Parentheses first: $5 + 3 = 8$. Exponent: $8^2 = 64$. Division: $64 \\div 4 = 16$. Subtraction: $16 - 1 = 15$.

---

**Example 3: $3 \\times 2^3 - 12 \\div (4 - 2)$**

Parentheses: $4 - 2 = 2$. Exponent: $2^3 = 8$. Now left to right (mult/div): $3 \\times 8 = 24$, $12 \\div 2 = 6$. Subtraction: $24 - 6 = 18$.

## Common Mistakes

- **Treating $M/D$ and $A/S$ as having strict ordering within the pair.** $8 \\div 2 \\times 4 = (8 \\div 2) \\times 4 = 16$, not $8 \\div 8 = 1$.
- **Ignoring implied groupings.** The fraction bar in $\\frac{6+2}{4}$ means the entire numerator is grouped.

## Quick Check

1. $10 - 2 \\times 3$
2. $(10 - 2) \\times 3$
3. $2^3 + 4 \\div 2$

*(Answers: 4, 24, 10)*
""",

"order-nested": """\
# Nested Expressions

## Overview

A **nested expression** contains parentheses within parentheses (or brackets within brackets). You evaluate from the **innermost** grouping outward.

## Key Idea

Work from the inside out:

$$\\bigl[\\,(a + b) \\cdot c\\,\\bigr] + d$$

Evaluate $(a + b)$ first, multiply by $c$, then add $d$.

## Worked Examples

**Example 1: $2 \\times [3 + (4 - 1)]$**

Innermost: $4 - 1 = 3$. Brackets: $3 + 3 = 6$. Multiply: $2 \\times 6 = 12$.

---

**Example 2: $\\{[(2 + 3) \\times 2] - 4\\} \\div 2$**

Step 1 (innermost): $2 + 3 = 5$. Step 2: $5 \\times 2 = 10$. Step 3: $10 - 4 = 6$. Step 4: $6 \\div 2 = 3$.

---

**Example 3: $4 + 2 \\times [5 - (1 + 2)]$**

Innermost: $1 + 2 = 3$. Brackets: $5 - 3 = 2$. Multiply: $2 \\times 2 = 4$. Add: $4 + 4 = 8$.

## Common Mistakes

- **Starting with the outer grouping.** Always work from the innermost group.
- **Losing track of which closing bracket matches which opening bracket.** Count carefully — every opener has exactly one closer.

## Quick Check

1. $3 \\times [2 + (5 - 3)]$
2. $[(4 + 2) \\times 3] - 8$
3. $10 - [2 \\times (3 + 1)]$

*(Answers: 12, 10, 2)*
""",

# ── Exponents ──────────────────────────────────────────────────────────────────
"exp-product": """\
# Product Rule for Exponents

## Overview

The **product rule** tells you how to multiply two powers that share the same base: add their exponents. This shortcut comes directly from the definition of exponentiation as repeated multiplication.

## Key Idea

$$a^m \\cdot a^n = a^{m+n}$$

The base must be the same. You cannot combine $a^2 \\cdot b^3$ with this rule.

## Worked Examples

**Example 1: $x^3 \\cdot x^4$**

$$x^3 \\cdot x^4 = x^{3+4} = x^7$$

---

**Example 2: $2^5 \\cdot 2^3$**

$$2^5 \\cdot 2^3 = 2^{5+3} = 2^8 = 256$$

---

**Example 3: $3x^2 \\cdot 5x^4$**

Multiply coefficients and apply product rule to the $x$ terms:

$$3x^2 \\cdot 5x^4 = (3 \\cdot 5) \\cdot x^{2+4} = 15x^6$$

## Common Mistakes

- **Multiplying the exponents instead of adding them.** $x^3 \\cdot x^4 = x^7$, not $x^{12}$.
- **Applying the rule when bases differ.** $x^3 \\cdot y^4$ cannot be simplified with this rule.

## Quick Check

1. $x^2 \\cdot x^5$
2. $3^2 \\cdot 3^4$
3. $4y^3 \\cdot 2y$

*(Answers: $x^7$, $3^6 = 729$, $8y^4$)*
""",

"exp-power": """\
# Power Rule for Exponents

## Overview

The **power rule** handles an exponent raised to another exponent: multiply the two exponents. It also extends to products and quotients inside parentheses.

## Key Idea

$$\\left(a^m\\right)^n = a^{m \\cdot n}$$

Extended form for products: $(ab)^n = a^n b^n$, and for quotients: $(a/b)^n = a^n / b^n$.

## Worked Examples

**Example 1: $(x^3)^4$**

$$\\left(x^3\\right)^4 = x^{3 \\cdot 4} = x^{12}$$

---

**Example 2: $(2x^2)^3$**

Apply to each factor: $2^3 \\cdot (x^2)^3 = 8x^6$.

---

**Example 3: $\\left(\\frac{3y^2}{z}\\right)^2$**

$$\\frac{3^2 \\cdot (y^2)^2}{z^2} = \\frac{9y^4}{z^2}$$

## Common Mistakes

- **Adding instead of multiplying the exponents.** $(x^3)^4 = x^{12}$, not $x^7$.
- **Forgetting to raise the coefficient to the power.** $(2x)^3 = 8x^3$, not $2x^3$.

## Quick Check

1. $(y^4)^3$
2. $(3x)^2$
3. $\\left(\\frac{x^2}{y}\\right)^3$

*(Answers: $y^{12}$, $9x^2$, $\\frac{x^6}{y^3}$)*
""",

"exp-negative": """\
# Negative Exponents

## Overview

A **negative exponent** does not make the result negative. It indicates a reciprocal: $a^{-n}$ means $1/a^n$. Negative exponents are a compact way to write fractions with powers in the denominator.

## Key Idea

$$a^{-n} = \\frac{1}{a^n} \\quad (a \\ne 0)$$

Moving a factor from numerator to denominator (or vice versa) flips the sign of its exponent.

## Worked Examples

**Example 1: $3^{-2}$**

$$3^{-2} = \\frac{1}{3^2} = \\frac{1}{9}$$

---

**Example 2: $x^{-4}$**

$$x^{-4} = \\frac{1}{x^4}$$

---

**Example 3: $\\frac{5x^{-2}}{y^{-3}}$**

Move $x^{-2}$ to denominator and $y^{-3}$ to numerator:

$$\\frac{5x^{-2}}{y^{-3}} = \\frac{5y^3}{x^2}$$

## Common Mistakes

- **Thinking $a^{-n}$ is negative.** $2^{-3} = \\frac{1}{8}$, which is positive.
- **Only applying the negative exponent to part of the expression.** $(-2)^{-2} = \\frac{1}{(-2)^2} = \\frac{1}{4}$.

## Quick Check

1. $4^{-1}$
2. $x^{-3} \\cdot x^5$
3. $\\frac{1}{a^{-2}}$

*(Answers: $\\frac{1}{4}$, $x^2$, $a^2$)*
""",

"exp-combined": """\
# Combined Exponent Rules

## Overview

Most exponent problems require applying several rules in sequence. **Combining exponent rules** means recognizing which rule applies at each step: product, power, negative, or zero exponent.

## Key Idea

All rules at a glance:

$$a^m \\cdot a^n = a^{m+n}, \\quad \\frac{a^m}{a^n} = a^{m-n}, \\quad (a^m)^n = a^{mn}, \\quad a^{-n} = \\frac{1}{a^n}, \\quad a^0 = 1$$

Simplify in any order, but power rule first on grouped expressions.

## Worked Examples

**Example 1: $\\frac{x^5 \\cdot x^{-2}}{x^3}$**

Numerator: $x^{5+(-2)} = x^3$. Then: $\\frac{x^3}{x^3} = x^0 = 1$.

---

**Example 2: $(2x^3 y^{-1})^2$**

$$4x^6 y^{-2} = \\frac{4x^6}{y^2}$$

---

**Example 3: $\\frac{(3a^2)^3}{9a^4}$**

Numerator: $27a^6$. Then: $\\frac{27a^6}{9a^4} = 3a^2$.

## Common Mistakes

- **Applying rules in the wrong order.** Handle parentheses/powers before product/quotient rules.
- **Dropping negative signs on coefficients when raising to even powers.** $(-2)^2 = 4$.

## Quick Check

1. $\\frac{a^7}{a^3}$
2. $(x^2)^3 \\cdot x^{-4}$
3. $\\frac{(2y)^3}{4y^2}$

*(Answers: $a^4$, $x^2$, $2y$)*
""",

# ── Equations ──────────────────────────────────────────────────────────────────
"eq-one-step": """\
# One-Step Equations

## Overview

A **one-step equation** is solved with a single inverse operation — one addition, subtraction, multiplication, or division applied to both sides.

## Key Idea

Whatever you do to one side, do to the other. The goal is to isolate the variable:

- If the equation has $x + a = b$, subtract $a$ from both sides.
- If it has $ax = b$, divide both sides by $a$.

## Worked Examples

**Example 1: $x + 7 = 12$**

Subtract 7 from both sides: $x = 12 - 7 = 5$.

---

**Example 2: $3x = 18$**

Divide both sides by 3: $x = 18/3 = 6$.

---

**Example 3: $x - 4 = -1$**

Add 4 to both sides: $x = -1 + 4 = 3$.

## Common Mistakes

- **Applying the operation to only one side.** Balance is everything.
- **Using the wrong inverse.** The inverse of $+7$ is $-7$, not $\\times 7$.

## Quick Check

1. $x + 9 = 15$
2. $5x = 35$
3. $x - 6 = -2$

*(Answers: 6, 7, 4)*
""",

"eq-two-step": """\
# Two-Step Equations

## Overview

A **two-step equation** requires exactly two inverse operations to isolate the variable. The standard order is: undo addition/subtraction first, then undo multiplication/division.

## Key Idea

For $ax + b = c$:

1. Subtract $b$ from both sides: $ax = c - b$
2. Divide both sides by $a$: $x = (c - b)/a$

## Worked Examples

**Example 1: $2x + 3 = 11$**

Subtract 3: $2x = 8$. Divide by 2: $x = 4$.

---

**Example 2: $3x - 5 = 10$**

Add 5: $3x = 15$. Divide by 3: $x = 5$.

---

**Example 3: $\\frac{x}{4} - 2 = 3$**

Add 2: $\\frac{x}{4} = 5$. Multiply by 4: $x = 20$.

## Common Mistakes

- **Dividing before adding/subtracting.** While algebraically valid, it usually creates fractions unnecessarily.
- **Sign errors when adding/subtracting a negative.** If $2x - 5 = 9$, add 5 (not subtract).

## Quick Check

1. $4x + 1 = 13$
2. $\\frac{x}{3} + 2 = 7$
3. $5x - 8 = 12$

*(Answers: 3, 15, 4)*
""",

"eq-fractions": """\
# Equations with Fractions

## Overview

Equations containing fractions are solved most cleanly by **multiplying through by the LCD** to eliminate all denominators at once, then solving the resulting integer equation.

## Key Idea

Multiply every term by the LCD. For $\\frac{x}{a} + \\frac{b}{c} = d$, multiply both sides by LCD$(a, c)$ to clear fractions, then solve.

## Worked Examples

**Example 1: $\\frac{x}{3} + \\frac{1}{2} = \\frac{5}{6}$**

LCD = 6. Multiply through: $2x + 3 = 5$. Solve: $2x = 2 \\Rightarrow x = 1$.

---

**Example 2: $\\frac{2x}{5} - \\frac{1}{3} = 1$**

LCD = 15. Multiply: $6x - 5 = 15$. Solve: $6x = 20 \\Rightarrow x = 10/3$.

---

**Example 3: $\\frac{x+1}{4} = \\frac{x-1}{2}$**

LCD = 4. Multiply: $x + 1 = 2(x - 1) = 2x - 2$. Rearrange: $3 = x$.

## Common Mistakes

- **Multiplying only some terms by the LCD, not all.** Every term on both sides must be multiplied.
- **Forgetting to distribute the LCD over sums in numerators.**

## Quick Check

1. $\\frac{x}{4} = \\frac{3}{8}$
2. $\\frac{2x}{3} + 1 = 3$
3. $\\frac{x+2}{5} = \\frac{x-1}{3}$

*(Answers: $3/2$, 3, 11/2)*
""",

"eq-distribution": """\
# Distributive Property in Equations

## Overview

When an equation contains an expression like $a(x + b)$, you must **distribute** before combining like terms or isolating the variable. The distributive property states $a(b + c) = ab + ac$.

## Key Idea

$$a(b + c) = ab + ac$$

Distribute, collect like terms on each side, then isolate the variable.

## Worked Examples

**Example 1: $3(x + 4) = 18$**

Distribute: $3x + 12 = 18$. Subtract 12: $3x = 6$. Divide: $x = 2$.

---

**Example 2: $2(x - 5) = 3x + 1$**

Distribute left: $2x - 10 = 3x + 1$. Move $x$ terms: $-10 - 1 = 3x - 2x$, so $x = -11$.

---

**Example 3: $4(2x + 1) - 3(x - 2) = 25$**

Distribute: $8x + 4 - 3x + 6 = 25$. Combine: $5x + 10 = 25$. Solve: $x = 3$.

## Common Mistakes

- **Only distributing to the first term inside the parentheses.** $3(x + 4) = 3x + 4$ is wrong; it should be $3x + 12$.
- **Sign errors with negative distribution.** $-2(x - 3) = -2x + 6$, not $-2x - 6$.

## Quick Check

1. $2(x + 5) = 16$
2. $3(2x - 1) = 15$
3. $5(x + 2) - 2(x - 1) = 20$

*(Answers: 3, 3, 8/3)*
""",

"eq-quadratic": """\
# Quadratic Equations

## Overview

A **quadratic equation** has the form $ax^2 + bx + c = 0$. It can have 0, 1, or 2 real solutions. The main methods are factoring, completing the square, and the quadratic formula.

## Key Idea

The **quadratic formula** always works:

$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$

The **discriminant** $\\Delta = b^2 - 4ac$ determines the number of real solutions: positive → 2, zero → 1, negative → none (real).

## Worked Examples

**Example 1: Solve $x^2 - 5x + 6 = 0$ by factoring**

Factor: $(x - 2)(x - 3) = 0$. Solutions: $x = 2$ or $x = 3$.

---

**Example 2: Solve $x^2 - 4x - 5 = 0$ using the formula**

$a=1, b=-4, c=-5$. Discriminant: $16 + 20 = 36$.

$$x = \\frac{4 \\pm 6}{2} \\Rightarrow x = 5 \\text{ or } x = -1$$

---

**Example 3: Solve $2x^2 + 3x - 2 = 0$**

$a=2, b=3, c=-2$. Discriminant: $9 + 16 = 25$.

$$x = \\frac{-3 \\pm 5}{4} \\Rightarrow x = \\frac{1}{2} \\text{ or } x = -2$$

## Common Mistakes

- **Forgetting $\\pm$ in the formula** — giving only one root.
- **Using the formula with $a \\ne 0$ not checked.** If $a = 0$ it's linear, not quadratic.

## Quick Check

1. Solve $x^2 - x - 6 = 0$ by factoring.
2. Solve $x^2 + 2x - 8 = 0$.
3. Use the formula for $x^2 - 2x - 3 = 0$.

*(Answers: $x=3, -2$; $x=2, -4$; $x=3, -1$)*
""",

# ── Logarithms ─────────────────────────────────────────────────────────────────
"log-definition": """\
# Definition of Logarithm

## Overview

The **logarithm** base $b$ of a number $x$, written $\\log_b x$, answers the question: "To what power must I raise $b$ to get $x$?" Logarithms are the inverse of exponential functions.

## Key Idea

$$\\log_b x = y \\iff b^y = x \\quad (b > 0,\\ b \\ne 1,\\ x > 0)$$

Common special cases: $\\log_{10}$ is written $\\log$; $\\log_e$ is written $\\ln$.

## Worked Examples

**Example 1: $\\log_2 8$**

"What power of 2 equals 8?" Since $2^3 = 8$, the answer is **3**.

---

**Example 2: $\\log_3 \\frac{1}{9}$**

$3^? = \\frac{1}{9} = 3^{-2}$, so $\\log_3 \\frac{1}{9} = -2$.

---

**Example 3: $\\ln e^5$**

$\\ln e^5 = 5$ because $e^5 = e^5$.

## Common Mistakes

- **Thinking $\\log_b 0$ is defined.** Logarithms of zero or negative numbers are undefined in the reals.
- **Confusing the base and the argument.** $\\log_3 9 = 2$ (base 3, argument 9), not $\\log_9 3$.

## Quick Check

1. $\\log_2 16$
2. $\\log_5 125$
3. $\\log_{10} 0.01$

*(Answers: 4, 3, −2)*
""",

"log-exponential": """\
# Exponential Form and Log Form

## Overview

Every logarithmic equation has an equivalent exponential form, and vice versa. Being able to convert between the two forms is essential for solving log and exponential equations.

## Key Idea

$$\\log_b x = y \\iff b^y = x$$

This single equivalence is the bridge between the two forms. Practice until the conversion is instant.

## Worked Examples

**Example 1: Convert $\\log_4 64 = 3$ to exponential form**

$$4^3 = 64$$

---

**Example 2: Convert $5^2 = 25$ to log form**

$$\\log_5 25 = 2$$

---

**Example 3: Solve $\\log_x 27 = 3$**

Convert to exponential form: $x^3 = 27$, so $x = 3$.

## Common Mistakes

- **Placing the base as the argument.** $\\log_4 64 = 3$ converts to $4^3 = 64$, not $64^3 = 4$.
- **Forgetting the equation has three pieces:** base, exponent, and result.

## Quick Check

1. Write $\\log_2 32 = 5$ in exponential form.
2. Write $3^4 = 81$ in log form.
3. Solve $\\log_b 49 = 2$.

*(Answers: $2^5=32$; $\\log_3 81 = 4$; $b = 7$)*
""",

"log-rules": """\
# Logarithm Rules

## Overview

The **logarithm rules** let you expand, condense, and simplify logarithmic expressions. They mirror the exponent rules because logs and exponents are inverses.

## Key Idea

The three fundamental rules:

$$\\log_b(MN) = \\log_b M + \\log_b N$$

$$\\log_b\\!\\left(\\frac{M}{N}\\right) = \\log_b M - \\log_b N$$

$$\\log_b M^p = p\\,\\log_b M$$

Change-of-base: $\\log_b x = \\frac{\\ln x}{\\ln b}$.

## Worked Examples

**Example 1: Expand $\\log_2(8x^3)$**

$$\\log_2 8 + \\log_2 x^3 = 3 + 3\\log_2 x$$

---

**Example 2: Condense $2\\log x - \\log 5$**

$$\\log x^2 - \\log 5 = \\log\\frac{x^2}{5}$$

---

**Example 3: Evaluate $\\log_9 27$ using change-of-base**

$$\\log_9 27 = \\frac{\\ln 27}{\\ln 9} = \\frac{3\\ln 3}{2\\ln 3} = \\frac{3}{2}$$

## Common Mistakes

- **Adding when you should multiply the arguments:** $\\log(M + N) \\ne \\log M + \\log N$.
- **Applying a coefficient to the base:** $2\\log_3 x = \\log_3 x^2$, not $\\log_6 x$.

## Quick Check

1. Expand $\\ln(x^2 y)$
2. Condense $\\log 4 + \\log 3$
3. Evaluate $\\log_4 8$ using change-of-base

*(Answers: $2\\ln x + \\ln y$; $\\log 12$; $3/2$)*
""",

"log-equations": """\
# Solving Logarithmic Equations

## Overview

A **logarithmic equation** contains the variable inside a logarithm. The main strategy is to isolate the log and convert to exponential form, or use log properties to combine logs before converting.

## Key Idea

Isolate the logarithm, then apply the definition $\\log_b x = y \\iff b^y = x$. Always **check for extraneous solutions**: the argument of any log must be positive.

## Worked Examples

**Example 1: $\\log_3(x + 1) = 4$**

Convert: $x + 1 = 3^4 = 81$. Solution: $x = 80$. Check: $80 + 1 = 81 > 0$ ✓

---

**Example 2: $\\log x + \\log(x - 3) = 1$**

Combine: $\\log[x(x-3)] = 1$, so $x(x-3) = 10$. Quadratic: $x^2 - 3x - 10 = 0 \\Rightarrow (x-5)(x+2)=0$.

$x = 5$ (valid) or $x = -2$ (invalid, since $\\log(-2)$ is undefined).

---

**Example 3: $2\\ln x - \\ln(x - 1) = \\ln 4$**

$$\\ln\\frac{x^2}{x-1} = \\ln 4 \\Rightarrow x^2 = 4(x-1) \\Rightarrow x^2 - 4x + 4 = 0 \\Rightarrow x = 2$$

## Common Mistakes

- **Forgetting to check for extraneous solutions.** Squaring or multiplying can introduce invalid answers.
- **Applying $\\log_b(M + N) = \\log_b M + \\log_b N$ (false rule).**

## Quick Check

1. $\\log_2(x - 1) = 3$
2. $\\log(x) + \\log(x+9) = 1$
3. $\\ln(2x) = \\ln(x + 3)$

*(Answers: 9; $x=1$ (reject $x=-10$); $x=3$)*
""",

# ── Summation ──────────────────────────────────────────────────────────────────
"sum-sigma": """\
# Sigma Notation

## Overview

**Sigma notation** $\\sum$ is a compact way to write a sum of many terms. The index variable runs from a lower bound to an upper bound, and the formula inside gives each term.

## Key Idea

$$\\sum_{i=m}^{n} a_i = a_m + a_{m+1} + \\cdots + a_n$$

The symbol $i$ is a dummy variable — you can use any letter. The index starts at $m$ and increments by 1 until it reaches $n$.

## Worked Examples

**Example 1: Expand $\\sum_{i=1}^{4} i^2$**

$$1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30$$

---

**Example 2: Write $2 + 4 + 6 + 8 + 10$ in sigma notation**

Each term is $2i$ for $i$ from 1 to 5:

$$\\sum_{i=1}^{5} 2i$$

---

**Example 3: Evaluate $\\sum_{k=0}^{3} 3^k$**

$$3^0 + 3^1 + 3^2 + 3^3 = 1 + 3 + 9 + 27 = 40$$

## Common Mistakes

- **Off-by-one errors** — the sum $\\sum_{i=1}^{n}$ has $n$ terms, but $\\sum_{i=0}^{n}$ has $n+1$ terms.
- **Confusing the index with the formula.** In $\\sum_{i=1}^5 2i$, the formula is $2i$, not $i$.

## Quick Check

1. Expand $\\sum_{i=1}^{3} i$
2. Evaluate $\\sum_{k=1}^{4} 2^k$
3. Write $1 + 4 + 9 + 16$ using sigma notation

*(Answers: 6; 30; $\\sum_{i=1}^4 i^2$)*
""",

"sum-arithmetic": """\
# Arithmetic Series

## Overview

An **arithmetic series** is the sum of an arithmetic sequence — one where consecutive terms differ by a fixed constant $d$ called the common difference. There is a closed-form formula for the sum.

## Key Idea

For an arithmetic series with first term $a_1$, last term $a_n$, and $n$ terms:

$$S_n = \\frac{n}{2}(a_1 + a_n) = \\frac{n}{2}[2a_1 + (n-1)d]$$

## Worked Examples

**Example 1: Sum $1 + 2 + 3 + \\cdots + 100$**

$a_1 = 1$, $a_n = 100$, $n = 100$:

$$S_{100} = \\frac{100}{2}(1 + 100) = 50 \\times 101 = 5050$$

---

**Example 2: Sum the first 10 terms of $3, 7, 11, 15, \\ldots$**

$a_1=3$, $d=4$, $n=10$. Last term: $3 + 9 \\times 4 = 39$.

$$S_{10} = \\frac{10}{2}(3 + 39) = 5 \\times 42 = 210$$

---

**Example 3: Find $\\sum_{k=1}^{20} (2k + 1)$**

$a_1 = 3$, $a_{20} = 41$, $n = 20$:

$$S_{20} = \\frac{20}{2}(3 + 41) = 10 \\times 44 = 440$$

## Common Mistakes

- **Using the wrong formula for $n$.** If the series runs $i=1$ to $n$, there are $n$ terms.
- **Confusing arithmetic with geometric.** Arithmetic: constant difference; geometric: constant ratio.

## Quick Check

1. Sum $1 + 3 + 5 + \\cdots + 19$
2. Find $S_{15}$ for $a_1 = 2$, $d = 3$.
3. Sum $5 + 8 + 11 + \\cdots + 35$.

*(Answers: 100; 347; 220)*
""",

"sum-nested": """\
# Nested Sums

## Overview

A **nested sum** is a double (or higher) summation where one sigma appears inside another. Evaluate the inner sum first for each value of the outer index, then sum those results.

## Key Idea

$$\\sum_{i=1}^{m}\\sum_{j=1}^{n} a_{ij} = \\sum_{i=1}^{m}\\left(\\sum_{j=1}^{n} a_{ij}\\right)$$

You can also exchange the order of summation when limits are independent.

## Worked Examples

**Example 1: $\\sum_{i=1}^{2}\\sum_{j=1}^{3} i$**

Inner sum (fixed $i$): $\\sum_{j=1}^{3} i = 3i$. Outer sum: $3(1) + 3(2) = 9$.

---

**Example 2: $\\sum_{i=1}^{3}\\sum_{j=1}^{i} 1$**

The inner sum goes to $i$, so it equals $i$. Outer: $1 + 2 + 3 = 6$.

---

**Example 3: $\\sum_{i=1}^{2}\\sum_{j=1}^{2} ij$**

$i=1$: $1\\cdot1 + 1\\cdot2 = 3$. $i=2$: $2\\cdot1 + 2\\cdot2 = 6$. Total: $3 + 6 = 9$.

## Common Mistakes

- **Treating the outer index as constant when evaluating the outer sum.** After evaluating the inner sum, $i$ is free again.
- **Swapping limits incorrectly when bounds depend on each other.**

## Quick Check

1. $\\sum_{i=1}^{3}\\sum_{j=1}^{2} 1$
2. $\\sum_{i=1}^{2}\\sum_{j=1}^{3} j$
3. $\\sum_{i=1}^{3}\\sum_{j=1}^{i} j$

*(Answers: 6; 12; 10)*
""",

# ── Combinatorics ──────────────────────────────────────────────────────────────
"comb-counting": """\
# Fundamental Counting Principle

## Overview

The **Fundamental Counting Principle** states that if you make a sequence of independent choices — $k_1$ options for the first, $k_2$ for the second, and so on — the total number of outcomes is the product $k_1 \\times k_2 \\times \\cdots$.

## Key Idea

If task 1 can be done in $m$ ways and task 2 in $n$ ways, together they can be done in:

$$m \\times n \\text{ ways}$$

This extends to any number of independent tasks.

## Worked Examples

**Example 1: How many 2-digit codes using digits 1–4 (repetition allowed)?**

4 choices for the first digit × 4 for the second = $4 \\times 4 = 16$.

---

**Example 2: A restaurant has 3 soups, 5 entrees, 2 desserts. How many 3-course meals?**

$$3 \\times 5 \\times 2 = 30$$

---

**Example 3: How many license plates of 3 letters followed by 3 digits?**

$$26^3 \\times 10^3 = 17{,}576{,}000$$

## Common Mistakes

- **Adding instead of multiplying.** Independent sequential choices multiply.
- **Not accounting for repetition.** If repetition is allowed, each slot has the full number of options.

## Quick Check

1. Toss a coin 3 times. How many outcomes?
2. 4 shirts, 3 pants, 2 shoes. How many outfits?
3. How many 4-digit PINs (0–9, repetition allowed)?

*(Answers: 8; 24; 10,000)*
""",

"comb-permutations": """\
# Permutations

## Overview

A **permutation** is an ordered arrangement of items. The order matters — "ABC" and "BAC" are different permutations. Permutations count the number of ways to select and arrange $r$ items from $n$ distinct items.

## Key Idea

$$P(n, r) = \\frac{n!}{(n-r)!}$$

If you arrange all $n$ items, the count is simply $n!$ (n factorial).

## Worked Examples

**Example 1: How many ways to arrange 3 books chosen from 5?**

$$P(5, 3) = \\frac{5!}{2!} = \\frac{120}{2} = 60$$

---

**Example 2: How many 4-digit codes using digits 1–9 without repetition?**

$$P(9, 4) = \\frac{9!}{5!} = 9 \\times 8 \\times 7 \\times 6 = 3024$$

---

**Example 3: A race with 8 runners. In how many ways can 1st, 2nd, 3rd be assigned?**

$$P(8, 3) = 8 \\times 7 \\times 6 = 336$$

## Common Mistakes

- **Using combinations when order matters.** Gold/Silver/Bronze is not the same as a committee.
- **Computing $n!$ when you only need $n!/(n-r)!$.** Write it as a falling product: $n(n-1)\\cdots(n-r+1)$.

## Quick Check

1. $P(6, 2)$
2. Arrange 4 people in a line: how many ways?
3. Choose and rank 2 winners from 10 contestants.

*(Answers: 30; 24; 90)*
""",

"comb-combinations": """\
# Combinations

## Overview

A **combination** is a selection of items where order does **not** matter. Choosing a committee of 3 from 10 people is a combination problem — the group $\\{A, B, C\\}$ is the same regardless of the order you list them.

## Key Idea

$$C(n, r) = \\binom{n}{r} = \\frac{n!}{r!\\,(n-r)!}$$

Combinations equal permutations divided by $r!$ (the number of orderings of $r$ items we don't care about).

## Worked Examples

**Example 1: $\\binom{5}{2}$**

$$\\binom{5}{2} = \\frac{5!}{2! \\cdot 3!} = \\frac{20}{2} = 10$$

---

**Example 2: A class of 10. How many committees of 4?**

$$\\binom{10}{4} = \\frac{10 \\cdot 9 \\cdot 8 \\cdot 7}{4!} = \\frac{5040}{24} = 210$$

---

**Example 3: 52-card deck. How many 5-card hands?**

$$\\binom{52}{5} = \\frac{52 \\cdot 51 \\cdot 50 \\cdot 49 \\cdot 48}{120} = 2{,}598{,}960$$

## Common Mistakes

- **Using permutations when order doesn't matter.** Committees and hands use combinations.
- **Forgetting $\\binom{n}{0} = \\binom{n}{n} = 1$.**

## Quick Check

1. $\\binom{6}{3}$
2. $\\binom{8}{1}$
3. How many ways to choose 2 from 7?

*(Answers: 20; 8; 21)*
""",

# ── Geometric Series ───────────────────────────────────────────────────────────
"geo-sequences": """\
# Geometric Sequences

## Overview

A **geometric sequence** is a sequence in which each term is obtained by multiplying the previous term by a fixed constant $r$, called the **common ratio**.

## Key Idea

The $n$-th term of a geometric sequence with first term $a_1$ and ratio $r$ is:

$$a_n = a_1 \\cdot r^{n-1}$$

To find $r$, divide any term by the previous one: $r = a_{n+1}/a_n$.

## Worked Examples

**Example 1: Find the 6th term of $2, 6, 18, 54, \\ldots$**

$r = 6/2 = 3$. Then $a_6 = 2 \\cdot 3^5 = 2 \\times 243 = 486$.

---

**Example 2: In a sequence $5, 10, 20, \\ldots$, what is the 8th term?**

$r = 2$. $a_8 = 5 \\cdot 2^7 = 640$.

---

**Example 3: Find the common ratio if $a_1 = 3$ and $a_4 = 81$**

$81 = 3 \\cdot r^3 \\Rightarrow r^3 = 27 \\Rightarrow r = 3$.

## Common Mistakes

- **Confusing geometric with arithmetic sequences.** Geometric has a constant ratio; arithmetic has a constant difference.
- **Using $r^n$ instead of $r^{n-1}$.** The first term corresponds to exponent 0.

## Quick Check

1. Find $a_5$ for $1, 3, 9, \\ldots$
2. What is $r$ for $100, 50, 25, \\ldots$?
3. Find $a_3$ if $a_1 = 4$ and $r = -2$.

*(Answers: 81; 1/2; −16)*
""",

"geo-finite": """\
# Finite Geometric Series

## Overview

A **finite geometric series** is the sum of a finite number of terms from a geometric sequence. There is a closed-form formula that avoids adding every term individually.

## Key Idea

For $n$ terms with first term $a_1$ and ratio $r \\ne 1$:

$$S_n = a_1 \\cdot \\frac{1 - r^n}{1 - r}$$

If $r = 1$, then $S_n = n \\cdot a_1$.

## Worked Examples

**Example 1: Sum the first 5 terms of $2, 6, 18, 54, \\ldots$**

$a_1 = 2$, $r = 3$, $n = 5$:

$$S_5 = 2 \\cdot \\frac{1 - 3^5}{1 - 3} = 2 \\cdot \\frac{-242}{-2} = 2 \\times 121 = 242$$

---

**Example 2: Sum $1 + 2 + 4 + \\cdots + 512$**

$r = 2$, $a_1 = 1$. Last term $512 = 2^9$, so $n = 10$:

$$S_{10} = \\frac{1 - 2^{10}}{1 - 2} = \\frac{-1023}{-1} = 1023$$

---

**Example 3: Find $\\sum_{k=0}^{4} 3 \\cdot (0.5)^k$**

$a_1 = 3$, $r = 0.5$, $n = 5$:

$$S_5 = 3 \\cdot \\frac{1 - (0.5)^5}{1 - 0.5} = 3 \\cdot \\frac{1 - 1/32}{0.5} = 3 \\cdot \\frac{31/32}{1/2} = 3 \\cdot \\frac{31}{16} = \\frac{93}{16}$$

## Common Mistakes

- **Using the infinite series formula when $|r| \\ge 1$.** The infinite formula only converges for $|r| < 1$.
- **Off-by-one in $n$.** Count terms carefully.

## Quick Check

1. Sum the first 4 terms of $1, 2, 4, 8, \\ldots$
2. $S_6$ for $a_1=1$, $r=-1$.
3. Sum $3 + 3(0.5) + 3(0.25) + 3(0.125)$.

*(Answers: 15; 0; $45/8$)*
""",

"geo-infinite": """\
# Infinite Geometric Series

## Overview

When a geometric series goes on forever with $|r| < 1$, the terms shrink toward zero and the series converges to a finite sum. For $|r| \\ge 1$, the series diverges.

## Key Idea

$$S_\\infty = \\frac{a_1}{1 - r} \\quad \\text{provided } |r| < 1$$

This comes from taking $n \\to \\infty$ in the finite formula: $r^n \\to 0$ when $|r| < 1$.

## Worked Examples

**Example 1: $\\sum_{k=0}^{\\infty} \\left(\\frac{1}{2}\\right)^k$**

$a_1 = 1$, $r = 1/2$:

$$S = \\frac{1}{1 - 1/2} = 2$$

---

**Example 2: $\\sum_{k=0}^{\\infty} 3\\left(\\frac{2}{3}\\right)^k$**

$$S = \\frac{3}{1 - 2/3} = \\frac{3}{1/3} = 9$$

---

**Example 3: Write $0.\\overline{3}$ as a fraction**

$0.333\\ldots = 3/10 + 3/100 + \\cdots$. Here $a_1 = 3/10$, $r = 1/10$:

$$S = \\frac{3/10}{1 - 1/10} = \\frac{3/10}{9/10} = \\frac{1}{3}$$

## Common Mistakes

- **Applying the formula when $|r| \\ge 1$.** Series with $|r| \\ge 1$ diverge.
- **Confusing $a_1$ with the first term written.** If the sum starts at $k=0$, then $a_1$ is that first term.

## Quick Check

1. $\\sum_{k=0}^{\\infty}(0.1)^k$
2. $4 + 2 + 1 + 0.5 + \\cdots$
3. Write $0.\\overline{9}$ as a fraction using geometric series.

*(Answers: 10/9; 8; 1)*
""",


# ── Algebra ────────────────────────────────────────────────────────────────────
"alg-linear-graphs": """\
# Graphing Linear Equations

## Overview

A **linear equation** in two variables produces a straight line when graphed. The most common forms are slope-intercept ($y = mx + b$) and standard form ($Ax + By = C$).

## Key Idea

In slope-intercept form $y = mx + b$:
- $m$ = slope (rise over run)
- $b$ = $y$-intercept (where the line crosses the $y$-axis)

Plot the intercept, then use the slope to find a second point.

## Worked Examples

**Example 1: Graph $y = 2x - 3$**

$y$-intercept: $(0, -3)$. Slope $= 2$, so go up 2, right 1: point $(1, -1)$. Draw the line.

---

**Example 2: Graph $3x + 2y = 6$**

Find intercepts: $x=0 \\Rightarrow y=3$; $y=0 \\Rightarrow x=2$. Plot $(0,3)$ and $(2,0)$.

---

**Example 3: Write $y = -\\frac{1}{2}x + 4$ in standard form**

Multiply by 2: $2y = -x + 8$, so $x + 2y = 8$.

## Common Mistakes

- **Plotting slope as $\\frac{\\text{run}}{\\text{rise}}$ instead of $\\frac{\\text{rise}}{\\text{run}}$.**
- **Confusing $x$-intercept with $y$-intercept.**

## Quick Check

1. What is the slope of $y = 3x - 5$?
2. What is the $y$-intercept of $2x + y = 7$?
3. Does the point $(2, 1)$ lie on $y = -x + 3$?

*(Answers: 3; 7; yes)*
""",

"alg-slope": """\
# Slope and Rate of Change

## Overview

The **slope** of a line measures its steepness and direction — how much $y$ changes for each unit increase in $x$. It equals the ratio of vertical change (rise) to horizontal change (run).

## Key Idea

Given two points $(x_1, y_1)$ and $(x_2, y_2)$:

$$m = \\frac{y_2 - y_1}{x_2 - x_1} = \\frac{\\Delta y}{\\Delta x}$$

Positive slope → rising left to right. Negative → falling. Zero → horizontal. Undefined → vertical.

## Worked Examples

**Example 1: Slope through $(1, 3)$ and $(4, 9)$**

$$m = \\frac{9-3}{4-1} = \\frac{6}{3} = 2$$

---

**Example 2: Slope through $(-2, 5)$ and $(3, 5)$**

$$m = \\frac{5-5}{3-(-2)} = \\frac{0}{5} = 0 \\quad\\text{(horizontal line)}$$

---

**Example 3: A car travels 150 km in 3 hours. Rate of change of distance?**

$$m = \\frac{150 \\text{ km}}{3 \\text{ h}} = 50 \\text{ km/h}$$

## Common Mistakes

- **Subtracting coordinates in different orders.** $y_2 - y_1$ must match $x_2 - x_1$ (same pair).
- **Confusing zero slope with undefined slope.** Horizontal = zero; vertical = undefined.

## Quick Check

1. Slope through $(0, 0)$ and $(3, 6)$
2. Slope through $(2, 7)$ and $(2, -1)$
3. Slope of $y = -4x + 1$

*(Answers: 2; undefined; −4)*
""",

"alg-systems-sub": """\
# Systems of Equations (Substitution)

## Overview

A **system of equations** is two or more equations with the same variables. The **substitution method** solves it by isolating one variable in one equation and substituting into the other.

## Key Idea

1. Isolate one variable (choose the simplest).
2. Substitute the expression into the other equation.
3. Solve for the remaining variable, then back-substitute.

## Worked Examples

**Example 1: $y = 2x - 1$ and $3x + y = 9$**

Substitute $y = 2x - 1$: $3x + (2x-1) = 9 \\Rightarrow 5x = 10 \\Rightarrow x = 2$. Then $y = 3$.

---

**Example 2: $x + 2y = 8$ and $3x - y = 3$**

From first equation: $x = 8 - 2y$. Substitute: $3(8-2y) - y = 3 \\Rightarrow 24 - 6y - y = 3 \\Rightarrow y = 3$, $x = 2$.

---

**Example 3: $2x + 3y = 12$ and $x - y = 1$**

$x = y + 1$. Substitute: $2(y+1) + 3y = 12 \\Rightarrow 5y = 10 \\Rightarrow y = 2$, $x = 3$.

## Common Mistakes

- **Substituting into the same equation you isolated from.** Always substitute into the other equation.
- **Arithmetic errors in the substitution step.** Write it out carefully.

## Quick Check

1. Solve: $y = x + 1$, $2x + y = 7$
2. Solve: $x = 3y$, $x + y = 8$
3. Solve: $y = -x + 5$, $y = 2x - 1$

*(Answers: $(2,3)$; $(6,2)$; $(2,3)$)*
""",

"alg-systems-elim": """\
# Systems of Equations (Elimination)

## Overview

The **elimination method** (also called addition method) solves a system by adding equations together to eliminate one variable. It works best when coefficients can be made equal and opposite with minimal manipulation.

## Key Idea

Multiply one or both equations by constants so the coefficient of one variable sums to zero, then add the equations.

## Worked Examples

**Example 1: $2x + 3y = 13$ and $2x - y = 5$**

Subtract: $(2x+3y)-(2x-y) = 13-5 \\Rightarrow 4y = 8 \\Rightarrow y = 2$. Then $x = 3.5$.

---

**Example 2: $3x + 4y = 10$ and $x + 2y = 4$**

Multiply second by 2: $2x + 4y = 8$. Subtract from first: $x = 2$. Then $y = 1$.

---

**Example 3: $5x + 2y = 16$ and $3x - 4y = -4$**

Multiply first by 2: $10x + 4y = 32$. Add to second: $13x = 28 \\Rightarrow x = 28/13$. Back-sub for $y$.

## Common Mistakes

- **Adding instead of subtracting when coefficients have the same sign.** Check whether they cancel.
- **Forgetting to multiply every term** when scaling an equation.

## Quick Check

1. $x + y = 5$, $x - y = 1$
2. $2x + y = 7$, $x + y = 5$
3. $3x + 2y = 11$, $x - 2y = 1$

*(Answers: $(3,2)$; $(2,3)$; $(3,1)$)*
""",

"alg-inequalities": """\
# Linear Inequalities

## Overview

A **linear inequality** looks like a linear equation but uses $<$, $>$, $\\le$, or $\\ge$. The solution is a range of values, not a single value, and you solve it like an equation with one important exception.

## Key Idea

Solve like a linear equation, but **reverse the inequality sign when multiplying or dividing by a negative number**.

For a two-variable inequality like $y > 2x - 1$, the solution is a half-plane; use a dashed boundary for $<$ or $>$, solid for $\\le$ or $\\ge$.

## Worked Examples

**Example 1: Solve $3x - 5 > 7$**

Add 5: $3x > 12$. Divide by 3: $x > 4$.

---

**Example 2: Solve $-2x + 6 \\ge 10$**

Subtract 6: $-2x \\ge 4$. Divide by $-2$ (flip sign): $x \\le -2$.

---

**Example 3: Solve $1 < 2x + 3 \\le 9$**

Subtract 3 throughout: $-2 < 2x \\le 6$. Divide by 2: $-1 < x \\le 3$.

## Common Mistakes

- **Forgetting to flip the inequality when dividing by a negative.** The most common error.
- **Using a solid line for strict inequalities.** Strict ($<$, $>$) uses a dashed boundary.

## Quick Check

1. $2x + 1 < 9$
2. $-3x \\ge 12$
3. $-1 \\le x + 2 < 5$

*(Answers: $x < 4$; $x \\le -4$; $-3 \\le x < 3$)*
""",

"alg-poly-ops": """\
# Polynomial Operations

## Overview

**Polynomial operations** include adding, subtracting, and multiplying polynomials. These are foundational for all algebraic work involving higher-degree expressions.

## Key Idea

- **Add/Subtract:** Combine like terms (same variable and exponent).
- **Multiply:** Use the distributive property (FOIL for two binomials).

$$\\text{FOIL: }(a+b)(c+d) = ac + ad + bc + bd$$

## Worked Examples

**Example 1: Add $(3x^2 + 2x - 1) + (x^2 - 5x + 4)$**

$$4x^2 - 3x + 3$$

---

**Example 2: Multiply $(x + 3)(x - 2)$**

$$x^2 - 2x + 3x - 6 = x^2 + x - 6$$

---

**Example 3: Multiply $(2x + 1)(3x^2 - x + 2)$**

Distribute: $6x^3 - 2x^2 + 4x + 3x^2 - x + 2 = 6x^3 + x^2 + 3x + 2$.

## Common Mistakes

- **Adding exponents when combining like terms.** $3x^2 + x^2 = 4x^2$, not $4x^4$.
- **Sign errors when subtracting polynomials.** Distribute the negative sign to every term.

## Quick Check

1. $(2x + 3) + (x - 5)$
2. $(x + 4)(x - 4)$
3. $(3x - 1)^2$

*(Answers: $3x-2$; $x^2-16$; $9x^2-6x+1$)*
""",

"alg-factoring-gcf": """\
# Factoring: GCF

## Overview

**Factoring out the GCF** is the first step in any factoring problem. You find the greatest common factor of all terms and factor it out front, leaving a simpler polynomial inside the parentheses.

## Key Idea

$$ab + ac = a(b + c)$$

The GCF is the largest factor (including variable parts) that divides every term evenly.

## Worked Examples

**Example 1: Factor $12x^3 + 8x^2$**

GCF = $4x^2$. Result: $4x^2(3x + 2)$.

---

**Example 2: Factor $6a^2b - 9ab^2 + 3ab$**

GCF = $3ab$. Result: $3ab(2a - 3b + 1)$.

---

**Example 3: Factor $5(x+2) + 3x(x+2)$**

GCF = $(x+2)$. Result: $(x+2)(5 + 3x)$.

## Common Mistakes

- **Taking out only part of the GCF.** Factor completely — include all variable and numerical factors.
- **Forgetting to include the remaining 1.** Factoring $3x + 3$ gives $3(x + 1)$, not $3(x)$.

## Quick Check

1. Factor $10x^2 + 15x$
2. Factor $4a^3 - 2a^2 + 6a$
3. Factor $7y(y-3) - 2(y-3)$

*(Answers: $5x(2x+3)$; $2a(2a^2-a+3)$; $(y-3)(7y-2)$)*
""",

"alg-factoring-quad": """\
# Factoring Quadratics

## Overview

**Factoring a quadratic** $ax^2 + bx + c$ means writing it as a product of two binomials. When $a = 1$, find two numbers that multiply to $c$ and add to $b$.

## Key Idea

For $x^2 + bx + c$, find $p$ and $q$ such that $p \\cdot q = c$ and $p + q = b$:

$$x^2 + bx + c = (x + p)(x + q)$$

When $a \\ne 1$, use the AC method or trial-and-error.

## Worked Examples

**Example 1: Factor $x^2 + 5x + 6$**

Find two numbers with product 6 and sum 5: $2 \\times 3 = 6$, $2 + 3 = 5$.

$$(x + 2)(x + 3)$$

---

**Example 2: Factor $x^2 - 7x + 12$**

Product 12, sum $-7$: $(-3)(-4) = 12$, $-3 + (-4) = -7$.

$$(x - 3)(x - 4)$$

---

**Example 3: Factor $2x^2 + 7x + 3$**

AC = $2 \\times 3 = 6$. Find factors of 6 summing to 7: 6 and 1. Split middle: $2x^2 + 6x + x + 3 = 2x(x+3) + 1(x+3) = (2x+1)(x+3)$.

## Common Mistakes

- **Sign errors.** With $x^2 - 7x + 12$, both factors are negative.
- **Not checking by expanding.** Always verify $(x+p)(x+q)$ returns the original quadratic.

## Quick Check

1. Factor $x^2 + 7x + 10$
2. Factor $x^2 - x - 6$
3. Factor $3x^2 + 10x - 8$

*(Answers: $(x+2)(x+5)$; $(x-3)(x+2)$; $(3x-2)(x+4)$)*
""",

"alg-completing-square": """\
# Completing the Square

## Overview

**Completing the square** converts a quadratic $ax^2 + bx + c$ into vertex form $a(x - h)^2 + k$. This technique is essential for deriving the quadratic formula and finding the vertex of a parabola.

## Key Idea

For $x^2 + bx$, add and subtract $(b/2)^2$:

$$x^2 + bx + \\left(\\frac{b}{2}\\right)^2 - \\left(\\frac{b}{2}\\right)^2 = \\left(x + \\frac{b}{2}\\right)^2 - \\frac{b^2}{4}$$

## Worked Examples

**Example 1: Complete the square for $x^2 + 6x$**

$(b/2)^2 = 9$. Result: $(x+3)^2 - 9$.

---

**Example 2: Write $x^2 - 4x + 7$ in vertex form**

$(b/2)^2 = 4$. So $x^2 - 4x + 4 - 4 + 7 = (x-2)^2 + 3$. Vertex: $(2, 3)$.

---

**Example 3: Solve $x^2 + 6x + 5 = 0$ by completing the square**

$(x+3)^2 - 9 + 5 = 0 \\Rightarrow (x+3)^2 = 4 \\Rightarrow x + 3 = \\pm 2 \\Rightarrow x = -1$ or $x = -5$.

## Common Mistakes

- **Forgetting to subtract what you added.** Adding $(b/2)^2$ inside changes the expression; you must compensate.
- **Not dividing by $a$ first when $a \\ne 1$.** Factor out $a$ before completing the square.

## Quick Check

1. Complete the square: $x^2 + 8x$
2. Vertex of $x^2 - 10x + 22$?
3. Solve $x^2 + 2x - 8 = 0$ by completing the square.

*(Answers: $(x+4)^2 - 16$; $(5, -3)$; $x=2,-4$)*
""",

"alg-rational-expr": """\
# Rational Expressions

## Overview

A **rational expression** is a fraction where the numerator and/or denominator are polynomials. You simplify, add, subtract, multiply, and divide them using the same rules as numeric fractions.

## Key Idea

To simplify, factor numerator and denominator completely, then cancel common factors. Always state any values that make the denominator zero (they are excluded from the domain).

## Worked Examples

**Example 1: Simplify $\\frac{x^2 - 9}{x^2 - x - 6}$**

Factor: $\\frac{(x-3)(x+3)}{(x-3)(x+2)}$. Cancel $(x-3)$: $\\frac{x+3}{x+2}$, $x \\ne 3$ and $x \\ne -2$.

---

**Example 2: Multiply $\\frac{2x}{x+1} \\cdot \\frac{x^2-1}{4x^2}$**

$\\frac{2x(x-1)(x+1)}{(x+1) \\cdot 4x^2} = \\frac{x-1}{2x}$.

---

**Example 3: Add $\\frac{1}{x} + \\frac{2}{x+1}$**

LCD = $x(x+1)$: $\\frac{x+1 + 2x}{x(x+1)} = \\frac{3x+1}{x(x+1)}$.

## Common Mistakes

- **Canceling terms instead of factors.** $\\frac{x+3}{x+5}$: you cannot cancel the $x$'s.
- **Forgetting domain restrictions after canceling.**

## Quick Check

1. Simplify $\\frac{2x+4}{x^2-4}$
2. Simplify $\\frac{x^2+5x+6}{x+3}$
3. Add $\\frac{1}{x-1} + \\frac{1}{x+1}$

*(Answers: $\\frac{2}{x-2}$, $x\\ne\\pm2$; $x+2$; $\\frac{2x}{x^2-1}$)*
""",

"alg-radical-simplify": """\
# Simplifying Radicals

## Overview

**Simplifying a radical** means removing perfect-power factors from under the radical sign. A radical $\\sqrt[n]{a^n b} = a\\sqrt[n]{b}$ when $a^n$ is the largest perfect-power factor of the radicand.

## Key Idea

$$\\sqrt{a \\cdot b} = \\sqrt{a} \\cdot \\sqrt{b}$$

Factor out the largest perfect square (or cube, etc.) from under the radical.

## Worked Examples

**Example 1: Simplify $\\sqrt{72}$**

$72 = 36 \\times 2$. So $\\sqrt{72} = 6\\sqrt{2}$.

---

**Example 2: Simplify $\\sqrt{50x^3}$**

$50x^3 = 25x^2 \\cdot 2x$. So $\\sqrt{50x^3} = 5x\\sqrt{2x}$ (assuming $x \\ge 0$).

---

**Example 3: Simplify $\\sqrt[3]{54}$**

$54 = 27 \\times 2$. So $\\sqrt[3]{54} = 3\\sqrt[3]{2}$.

## Common Mistakes

- **Not finding the largest perfect square.** $\\sqrt{72} = \\sqrt{4 \\times 18} = 2\\sqrt{18}$ is not fully simplified yet.
- **Splitting $\\sqrt{a+b}$ into $\\sqrt{a} + \\sqrt{b}$.** This is false.

## Quick Check

1. Simplify $\\sqrt{48}$
2. Simplify $\\sqrt{18x^4}$
3. Simplify $\\sqrt[3]{16}$

*(Answers: $4\\sqrt{3}$; $3x^2\\sqrt{2}$; $2\\sqrt[3]{2}$)*
""",

"alg-radical-equations": """\
# Radical Equations

## Overview

A **radical equation** contains the variable inside a radical. The strategy is to isolate the radical and then raise both sides to the appropriate power to eliminate it. Always check for extraneous solutions.

## Key Idea

Isolate the radical, then square both sides (for square roots). After solving, substitute back to verify — squaring can introduce solutions that don't satisfy the original equation.

## Worked Examples

**Example 1: Solve $\\sqrt{x - 1} = 4$**

Square both sides: $x - 1 = 16 \\Rightarrow x = 17$. Check: $\\sqrt{16} = 4$ ✓

---

**Example 2: Solve $\\sqrt{2x + 3} - 1 = 4$**

Isolate: $\\sqrt{2x+3} = 5$. Square: $2x + 3 = 25 \\Rightarrow x = 11$. Check ✓

---

**Example 3: Solve $\\sqrt{x + 5} = x - 1$**

Square: $x + 5 = x^2 - 2x + 1 \\Rightarrow x^2 - 3x - 4 = 0 \\Rightarrow (x-4)(x+1) = 0$.

$x = 4$: $\\sqrt{9} = 3 = 4 - 1$ ✓. $x = -1$: $\\sqrt{4} = 2 \\ne -2$ ✗ (extraneous).

## Common Mistakes

- **Not checking for extraneous solutions.** Squaring can introduce false solutions.
- **Squaring before isolating.** Always isolate the radical first.

## Quick Check

1. Solve $\\sqrt{x} = 5$
2. Solve $\\sqrt{3x - 2} = 4$
3. Solve $\\sqrt{x + 3} = x - 3$

*(Answers: 25; 6; $x=6$ only)*
""",

# ── Precalculus ────────────────────────────────────────────────────────────────
"precalc-functions": """\
# Function Notation and Evaluation

## Overview

A **function** is a rule that assigns exactly one output to each input. Function notation $f(x)$ means "the output of function $f$ when the input is $x$."

## Key Idea

To evaluate $f(a)$, substitute $a$ for every occurrence of $x$ in the formula. The expression $f(x)$ is not $f$ times $x$ — it is a composite symbol for the output value.

## Worked Examples

**Example 1: $f(x) = 3x^2 - 2x + 1$. Find $f(2)$.**

$$f(2) = 3(4) - 2(2) + 1 = 12 - 4 + 1 = 9$$

---

**Example 2: $g(x) = \\frac{x+1}{x-2}$. Find $g(5)$.**

$$g(5) = \\frac{6}{3} = 2$$

---

**Example 3: $h(x) = x^2 + 1$. Find $h(a + 1)$.**

$$h(a+1) = (a+1)^2 + 1 = a^2 + 2a + 2$$

## Common Mistakes

- **Writing $f(x) = f \\cdot x$.** $f(x)$ is not multiplication.
- **Partial substitution.** Replace every $x$ with the argument, not just the first occurrence.

## Quick Check

1. $f(x) = 2x - 5$. Find $f(3)$.
2. $g(x) = x^2 - 1$. Find $g(-2)$.
3. $h(x) = 4x + 1$. Find $h(t+2)$.

*(Answers: 1; 3; $4t+9$)*
""",

"precalc-domain-range": """\
# Domain and Range

## Overview

The **domain** of a function is the set of all valid inputs ($x$-values). The **range** is the set of all possible outputs ($y$-values). Restrictions arise from square roots (must be $\\ge 0$), denominators (cannot be 0), and logarithms (must be $> 0$).

## Key Idea

To find the domain:
1. Identify any values of $x$ that cause division by zero.
2. Identify any values that make an even-index radical negative.
3. Everything else is in the domain.

## Worked Examples

**Example 1: Domain of $f(x) = \\frac{1}{x - 3}$**

Denominator $\\ne 0$: $x \\ne 3$. Domain: $(-\\infty, 3) \\cup (3, \\infty)$.

---

**Example 2: Domain of $g(x) = \\sqrt{2x - 6}$**

$2x - 6 \\ge 0 \\Rightarrow x \\ge 3$. Domain: $[3, \\infty)$.

---

**Example 3: Range of $f(x) = x^2 + 2$**

Since $x^2 \\ge 0$, the minimum output is 2. Range: $[2, \\infty)$.

## Common Mistakes

- **Confusing domain and range.** Domain: inputs; Range: outputs.
- **Forgetting that $\\sqrt{x}$ requires $x \\ge 0$, not $x > 0$** — zero is allowed.

## Quick Check

1. Domain of $h(x) = \\sqrt{x+4}$
2. Domain of $\\frac{x}{x^2-1}$
3. Range of $g(x) = -x^2 + 3$

*(Answers: $[-4,\\infty)$; $x\\ne\\pm1$; $(-\\infty,3]$)*
""",

"precalc-composition": """\
# Composition of Functions

## Overview

The **composition** of functions $f$ and $g$, written $(f \\circ g)(x)$ or $f(g(x))$, applies $g$ first, then feeds its output into $f$. The order matters.

## Key Idea

$$(f \\circ g)(x) = f(g(x))$$

The domain of $f \\circ g$ is restricted to inputs $x$ in the domain of $g$ for which $g(x)$ is in the domain of $f$.

## Worked Examples

**Example 1: $f(x) = x^2$, $g(x) = 2x + 1$. Find $(f \\circ g)(3)$.**

$g(3) = 7$. Then $f(7) = 49$.

---

**Example 2: Same functions. Find $(f \\circ g)(x)$.**

$$f(g(x)) = f(2x+1) = (2x+1)^2 = 4x^2 + 4x + 1$$

---

**Example 3: $f(x) = \\sqrt{x}$, $g(x) = x - 5$. Find the domain of $f \\circ g$.**

Need $g(x) \\ge 0$: $x - 5 \\ge 0 \\Rightarrow x \\ge 5$. Domain: $[5, \\infty)$.

## Common Mistakes

- **Reversing order:** $f(g(x)) \\ne g(f(x))$ in general.
- **Using $f \\circ g$ notation to mean $f \\cdot g$ (multiplication).**

## Quick Check

1. $f(x)=3x$, $g(x)=x-2$. Find $(f \\circ g)(x)$.
2. Same functions. Find $(g \\circ f)(x)$.
3. Evaluate $(f \\circ g)(4)$ with $f(x)=x^2$, $g(x)=x+1$.

*(Answers: $3x-6$; $3x-2$; 25)*
""",

"precalc-inverse-func": """\
# Inverse Functions

## Overview

The **inverse function** $f^{-1}$ "undoes" what $f$ does. If $f(a) = b$, then $f^{-1}(b) = a$. Not every function has an inverse — a function must be one-to-one (pass the horizontal line test) to have an inverse that is also a function.

## Key Idea

To find $f^{-1}(x)$: replace $f(x)$ with $y$, swap $x$ and $y$, then solve for $y$.

$$f(f^{-1}(x)) = x \\quad\\text{and}\\quad f^{-1}(f(x)) = x$$

## Worked Examples

**Example 1: Find the inverse of $f(x) = 2x + 3$**

$y = 2x + 3 \\to x = 2y + 3 \\to y = \\frac{x-3}{2}$. So $f^{-1}(x) = \\frac{x-3}{2}$.

---

**Example 2: Find the inverse of $f(x) = x^3 - 1$**

$y = x^3 - 1 \\to x = y^3 - 1 \\to y = \\sqrt[3]{x + 1}$.

---

**Example 3: Verify $f^{-1}$ for $f(x) = 2x + 3$**

$f(f^{-1}(x)) = 2 \\cdot \\frac{x-3}{2} + 3 = x$ ✓

## Common Mistakes

- **Writing $f^{-1}(x) = 1/f(x)$.** The $-1$ superscript denotes the inverse function, not a reciprocal.
- **Finding an inverse for a non-one-to-one function without restricting the domain.**

## Quick Check

1. Find the inverse of $f(x) = x - 7$.
2. Find the inverse of $g(x) = 5x$.
3. What is $f^{-1}(3)$ if $f(x) = 2x - 1$?

*(Answers: $f^{-1}(x)=x+7$; $g^{-1}(x)=x/5$; 2)*
""",

"precalc-poly-func": """\
# Polynomial Functions

## Overview

A **polynomial function** has the form $p(x) = a_n x^n + \\cdots + a_1 x + a_0$. The degree $n$ determines its end behavior and maximum number of real zeros and turning points.

## Key Idea

- **End behavior** is governed by the leading term $a_n x^n$.
- The function has at most $n$ real zeros and at most $n-1$ turning points.
- Real zeros correspond to $x$-intercepts; their multiplicity tells you whether the graph crosses or touches the axis.

## Worked Examples

**Example 1: Describe the end behavior of $f(x) = -2x^3 + x$**

Leading term: $-2x^3$. As $x \\to +\\infty$, $f \\to -\\infty$; as $x \\to -\\infty$, $f \\to +\\infty$.

---

**Example 2: Zeros of $p(x) = x(x-2)^2(x+3)$**

Zeros: $x = 0$ (multiplicity 1, crosses), $x = 2$ (mult. 2, touches), $x = -3$ (mult. 1, crosses).

---

**Example 3: Find all real zeros of $f(x) = x^3 - 4x$**

Factor: $x(x^2-4) = x(x-2)(x+2)$. Zeros: $0, 2, -2$.

## Common Mistakes

- **Assuming the degree equals the number of real zeros.** A degree-4 polynomial may have 0, 2, or 4 real zeros.
- **Misidentifying end behavior for even vs. odd degree.**

## Quick Check

1. End behavior of $f(x) = 3x^4 - x$?
2. How many turning points can $p(x) = x^5 + 1$ have at most?
3. Find the real zeros of $q(x) = x^2(x+1)(x-1)$.

*(Answers: both ends up; 4; $0, -1, 1$)*
""",

# ── Calculus ───────────────────────────────────────────────────────────────────
"calc-limits": """\
# Limits

## Overview

The **limit** of $f(x)$ as $x$ approaches $a$, written $\\lim_{x \\to a} f(x) = L$, means $f(x)$ can be made arbitrarily close to $L$ by taking $x$ sufficiently close to $a$ (but $x \\ne a$). The function need not be defined at $a$.

## Key Idea

$$\\lim_{x \\to a} f(x) = L$$

The limit exists if and only if the left-hand limit $\\lim_{x \\to a^-} f(x)$ and right-hand limit $\\lim_{x \\to a^+} f(x)$ both equal $L$.

## Worked Examples

**Example 1: $\\lim_{x \\to 3} (2x + 1)$**

Substitute directly (no issues): $2(3) + 1 = 7$.

---

**Example 2: $\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2}$**

Substituting gives $0/0$ — indeterminate. Factor: $\\frac{(x-2)(x+2)}{x-2} = x + 2$. Limit $= 4$.

---

**Example 3: $\\lim_{x \\to 0} \\frac{\\sin x}{x}$**

This standard limit equals 1 (proof via squeeze theorem). It cannot be found by simple substitution.

## Common Mistakes

- **Equating $\\lim_{x\\to a} f(x)$ with $f(a)$.** They are equal when $f$ is continuous at $a$, but not in general.
- **Assuming $0/0$ means the limit is 0 or undefined.** It's indeterminate — more work is needed.

## Quick Check

1. $\\lim_{x \\to 4}(x^2 - 1)$
2. $\\lim_{x \\to 3} \\frac{x^2-9}{x-3}$
3. $\\lim_{x \\to 0} \\frac{\\tan x}{x}$

*(Answers: 15; 6; 1)*
""",

"calc-limit-laws": """\
# Limit Laws

## Overview

**Limit laws** let you break complicated limits into simpler pieces. Rather than analyzing each limit from scratch, you can combine limits using rules for sums, products, and quotients.

## Key Idea

If $\\lim_{x\\to a} f(x) = L$ and $\\lim_{x\\to a} g(x) = M$, then:

$$\\lim_{x\\to a}[f(x) + g(x)] = L + M, \\quad \\lim_{x\\to a}[f(x)\\cdot g(x)] = LM$$

$$\\lim_{x\\to a}\\frac{f(x)}{g(x)} = \\frac{L}{M} \\quad (M \\ne 0), \\quad \\lim_{x\\to a}[f(x)]^n = L^n$$

## Worked Examples

**Example 1: $\\lim_{x\\to 2}(3x^2 - 5x + 1)$**

Apply sum/power laws: $3(4) - 5(2) + 1 = 12 - 10 + 1 = 3$.

---

**Example 2: $\\lim_{x\\to 3}\\sqrt{x^2 + 7}$**

$$\\sqrt{\\lim_{x\\to 3}(x^2 + 7)} = \\sqrt{9 + 7} = 4$$

---

**Example 3: $\\lim_{x\\to 1}\\frac{x^2 - 1}{x - 1}$**

Factor first: $x + 1 \\to 2$. (Can't use quotient law directly since denominator $\\to 0$.)

## Common Mistakes

- **Applying the quotient law when the denominator limit is 0.** Factor and simplify first.
- **Forgetting that limit laws require both limits to exist.**

## Quick Check

1. $\\lim_{x\\to 0}(x^3 + 5)$
2. $\\lim_{x\\to 4}\\sqrt{x+12}$
3. $\\lim_{x\\to 2}(x^2+1)(x-3)$

*(Answers: 5; 4; −5)*
""",

"calc-continuity": """\
# Continuity

## Overview

A function is **continuous at $a$** if its graph has no holes, jumps, or vertical asymptotes at $a$. Informally, you can draw it without lifting your pencil. Most functions you encounter in calculus are continuous on their domains.

## Key Idea

$f$ is continuous at $a$ if all three conditions hold:
1. $f(a)$ is defined.
2. $\\lim_{x\\to a} f(x)$ exists.
3. $\\lim_{x\\to a} f(x) = f(a)$.

## Worked Examples

**Example 1: Is $f(x) = x^2 + 1$ continuous at $x = 2$?**

$f(2) = 5$; $\\lim_{x\\to2}(x^2+1) = 5$. Both equal ✓ — continuous.

---

**Example 2: Is $g(x) = \\frac{x^2-4}{x-2}$ continuous at $x = 2$?**

$g(2)$ is undefined (division by zero). Not continuous at 2. (Removable discontinuity.)

---

**Example 3: Intermediate Value Theorem**

$f(x) = x^3 - 2$ is continuous. $f(1) = -1 < 0$ and $f(2) = 6 > 0$, so by IVT there exists $c \\in (1,2)$ with $f(c) = 0$.

## Common Mistakes

- **Assuming a limit existing means continuity.** You also need $f(a)$ defined and equal to the limit.
- **Confusing removable discontinuities (holes) with jump discontinuities.**

## Quick Check

1. Is $f(x) = |x|$ continuous at 0?
2. Where is $g(x) = \\frac{1}{x-3}$ discontinuous?
3. $h(x) = 5$ for $x<1$ and $h(x) = x+4$ for $x\\ge1$. Continuous at $x=1$?

*(Answers: yes; $x=3$; yes)*
""",

"calc-deriv-def": """\
# Definition of the Derivative

## Overview

The **derivative** $f'(a)$ measures the instantaneous rate of change of $f$ at $x = a$. It equals the slope of the tangent line to the curve at that point. It is defined as a limit.

## Key Idea

$$f'(a) = \\lim_{h \\to 0} \\frac{f(a + h) - f(a)}{h}$$

If this limit exists, $f$ is **differentiable** at $a$. The function $f'(x)$ is the derivative at every point.

## Worked Examples

**Example 1: Find $f'(x)$ for $f(x) = x^2$ using the definition**

$$f'(x) = \\lim_{h\\to0}\\frac{(x+h)^2 - x^2}{h} = \\lim_{h\\to0}\\frac{2xh + h^2}{h} = \\lim_{h\\to0}(2x + h) = 2x$$

---

**Example 2: Find the slope of $f(x) = 3x + 1$ at any point**

$$f'(x) = \\lim_{h\\to0}\\frac{3(x+h)+1-(3x+1)}{h} = \\lim_{h\\to0} 3 = 3$$

---

**Example 3: Find $f'(2)$ for $f(x) = x^3$**

Using the definition: $f'(x) = 3x^2$, so $f'(2) = 12$.

## Common Mistakes

- **Forgetting to take the limit.** The difference quotient by itself is not the derivative.
- **Algebraic errors expanding $(x+h)^n$.** Use binomial expansion carefully.

## Quick Check

1. Find $f'(x)$ from the definition for $f(x) = 5x - 2$.
2. What is $f'(0)$ if $f(x) = x^2$?
3. Is $f(x) = |x|$ differentiable at $x = 0$?

*(Answers: 5; 0; no — left and right limits differ)*
""",

"calc-deriv-power": """\
# Power Rule

## Overview

The **power rule** is the most-used differentiation rule. It gives the derivative of any power of $x$ in one step, without using the limit definition each time.

## Key Idea

$$\\frac{d}{dx}[x^n] = n x^{n-1}$$

This works for all real $n$ — integers, fractions, and even negative powers.

## Worked Examples

**Example 1: Differentiate $f(x) = x^5$**

$$f'(x) = 5x^4$$

---

**Example 2: Differentiate $g(x) = 3x^4 - 2x^2 + 7$**

$$g'(x) = 12x^3 - 4x + 0 = 12x^3 - 4x$$

---

**Example 3: Differentiate $h(x) = \\sqrt{x} = x^{1/2}$**

$$h'(x) = \\frac{1}{2} x^{-1/2} = \\frac{1}{2\\sqrt{x}}$$

## Common Mistakes

- **Forgetting constants.** The derivative of $c$ is 0, not $c$.
- **Not bringing the exponent down.** $\\frac{d}{dx}x^3 = 3x^2$, not $x^3 \\cdot 3$.

## Quick Check

1. $\\frac{d}{dx}(x^7)$
2. $\\frac{d}{dx}(4x^3 - x)$
3. $\\frac{d}{dx}(x^{-2})$

*(Answers: $7x^6$; $12x^2-1$; $-2x^{-3}$)*
""",

"calc-deriv-product": """\
# Product Rule

## Overview

The derivative of a product of two functions is not simply the product of their derivatives. The **product rule** gives the correct formula.

## Key Idea

$$\\frac{d}{dx}[f(x)\\,g(x)] = f'(x)\\,g(x) + f(x)\\,g'(x)$$

A helpful mnemonic: "derivative of first times second, plus first times derivative of second."

## Worked Examples

**Example 1: Differentiate $h(x) = x^2 \\sin x$**

$$h'(x) = 2x \\sin x + x^2 \\cos x$$

---

**Example 2: Differentiate $f(x) = (3x + 1)(x^2 - 2)$**

$f' = 3(x^2-2) + (3x+1)(2x) = 3x^2 - 6 + 6x^2 + 2x = 9x^2 + 2x - 6$.

---

**Example 3: Differentiate $g(x) = e^x \\ln x$**

$$g'(x) = e^x \\ln x + e^x \\cdot \\frac{1}{x} = e^x\\!\\left(\\ln x + \\frac{1}{x}\\right)$$

## Common Mistakes

- **Multiplying derivatives:** $(fg)' \\ne f' g'$.
- **Forgetting the second term in the product rule.**

## Quick Check

1. $\\frac{d}{dx}[x \\cdot e^x]$
2. $\\frac{d}{dx}[(x^2+1)(2x-3)]$
3. $\\frac{d}{dx}[x \\ln x]$

*(Answers: $e^x(1+x)$; $6x^2-6x+2$; $\\ln x + 1$)*
""",

"calc-deriv-chain": """\
# Chain Rule

## Overview

The **chain rule** differentiates composite functions $f(g(x))$. It says: differentiate the outer function (keeping the inner function intact), then multiply by the derivative of the inner function.

## Key Idea

$$\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$$

Think of it as: (derivative of outer at inner) × (derivative of inner).

## Worked Examples

**Example 1: Differentiate $h(x) = (3x + 1)^5$**

Outer: $u^5$, inner: $3x+1$. $h'(x) = 5(3x+1)^4 \\cdot 3 = 15(3x+1)^4$.

---

**Example 2: Differentiate $f(x) = \\sin(x^2)$**

$f'(x) = \\cos(x^2) \\cdot 2x = 2x\\cos(x^2)$.

---

**Example 3: Differentiate $g(x) = e^{-x^2}$**

$g'(x) = e^{-x^2} \\cdot (-2x) = -2x e^{-x^2}$.

## Common Mistakes

- **Forgetting the chain rule entirely** when differentiating a composite.
- **Applying chain rule when it's not needed** (e.g., $f(x) = x^3$ is not a composition).

## Quick Check

1. $\\frac{d}{dx}(\\sqrt{2x+3})$
2. $\\frac{d}{dx}(\\cos(5x))$
3. $\\frac{d}{dx}((x^2+1)^4)$

*(Answers: $\\frac{1}{\\sqrt{2x+3}}$; $-5\\sin(5x)$; $8x(x^2+1)^3$)*
""",

"calc-deriv-exp-log": """\
# Derivatives of Exponential and Log Functions

## Overview

The derivatives of $e^x$ and $\\ln x$ have elegant formulas. Exponential functions with base $e$ are their own derivatives; logarithms introduce a reciprocal.

## Key Idea

$$\\frac{d}{dx}[e^x] = e^x, \\quad \\frac{d}{dx}[\\ln x] = \\frac{1}{x}$$

For other bases: $\\frac{d}{dx}[a^x] = a^x \\ln a$ and $\\frac{d}{dx}[\\log_a x] = \\frac{1}{x \\ln a}$.

## Worked Examples

**Example 1: Differentiate $f(x) = 5e^x + \\ln x$**

$$f'(x) = 5e^x + \\frac{1}{x}$$

---

**Example 2: Differentiate $g(x) = e^{3x}$**

Chain rule: $g'(x) = 3e^{3x}$.

---

**Example 3: Differentiate $h(x) = \\ln(x^2 + 1)$**

Chain rule: $h'(x) = \\frac{2x}{x^2 + 1}$.

## Common Mistakes

- **Writing $(e^x)' = xe^{x-1}$.** That's the power rule — $e^x$ is exponential, not a power of $x$.
- **Forgetting the chain rule** when the exponent is not just $x$.

## Quick Check

1. $\\frac{d}{dx}(e^{-x})$
2. $\\frac{d}{dx}(\\ln(3x))$
3. $\\frac{d}{dx}(2^x)$

*(Answers: $-e^{-x}$; $1/x$; $2^x \\ln 2$)*
""",

"calc-implicit": """\
# Implicit Differentiation

## Overview

When a curve is defined by an equation involving both $x$ and $y$ (like $x^2 + y^2 = 25$), you can still find $dy/dx$ by differentiating both sides with respect to $x$ and treating $y$ as a function of $x$.

## Key Idea

Differentiate every term with respect to $x$. Whenever you differentiate a term containing $y$, multiply by $dy/dx$ (chain rule). Then isolate $dy/dx$.

## Worked Examples

**Example 1: Find $dy/dx$ for $x^2 + y^2 = 25$**

Differentiate: $2x + 2y\\,\\frac{dy}{dx} = 0$. Solve: $\\frac{dy}{dx} = -\\frac{x}{y}$.

---

**Example 2: Find $dy/dx$ for $x^3 + y^3 = 6xy$**

$3x^2 + 3y^2\\,y' = 6y + 6x\\,y'$. Isolate: $y'(3y^2 - 6x) = 6y - 3x^2 \\Rightarrow y' = \\frac{6y - 3x^2}{3y^2 - 6x}$.

---

**Example 3: Tangent line to $x^2 + y^2 = 25$ at $(3,4)$**

$dy/dx = -3/4$. Line: $y - 4 = -\\frac{3}{4}(x - 3)$.

## Common Mistakes

- **Forgetting $dy/dx$ when differentiating $y$ terms.** Every $y$ term needs the chain rule.
- **Not simplifying before solving for $dy/dx$.**

## Quick Check

1. Find $dy/dx$ for $x^2 + 2y = 10$.
2. Find $dy/dx$ for $xy = 5$.
3. Find the slope of $x^2 + y^2 = 100$ at $(6, 8)$.

*(Answers: $-x$; $-y/x$; $-3/4$)*
""",

"calc-optim": """\
# Optimization

## Overview

**Optimization** uses calculus to find the maximum or minimum value of a function on a domain. You find critical points (where $f'(x) = 0$ or is undefined) and test them using the first or second derivative test.

## Key Idea

Critical points occur where $f'(x) = 0$ or $f'(x)$ is undefined. On a closed interval $[a,b]$, also check the endpoints. Use the second derivative to classify: $f''(c) > 0$ → local min; $f''(c) < 0$ → local max.

## Worked Examples

**Example 1: Find the maximum of $f(x) = -x^2 + 4x$ on $[0, 4]$**

$f'(x) = -2x + 4 = 0 \\Rightarrow x = 2$. $f(0)=0$, $f(2)=4$, $f(4)=0$. Maximum = 4 at $x=2$.

---

**Example 2: A box with square base and open top has volume 32. Minimize surface area.**

Let side $= s$, height $= h$. Volume: $s^2 h = 32$, so $h = 32/s^2$. Surface: $S = s^2 + 4sh = s^2 + 128/s$. $S' = 2s - 128/s^2 = 0 \\Rightarrow s = 4$, $h = 2$.

---

**Example 3: Find local extrema of $f(x) = x^3 - 3x$**

$f'(x) = 3x^2 - 3 = 0 \\Rightarrow x = \\pm 1$. $f''(1) = 6 > 0$ (min), $f''(-1) = -6 < 0$ (max).

## Common Mistakes

- **Forgetting to check endpoints** on closed intervals.
- **Assuming a critical point is always an extremum.** Inflection points are also critical points.

## Quick Check

1. Critical points of $f(x) = x^3 - 6x^2$?
2. Classify $f'(x) = 0$ at $x=2$ if $f''(2) = 5$.
3. Max of $f(x) = 4x - x^2$?

*(Answers: $x=0, 4$; local min; 4 at $x=2$)*
""",

"calc-antideriv": """\
# Antiderivatives

## Overview

An **antiderivative** of $f(x)$ is any function $F(x)$ with $F'(x) = f(x)$. The general antiderivative includes an arbitrary constant $C$ because derivatives of constants vanish.

## Key Idea

$$\\int f(x)\\,dx = F(x) + C \\quad\\text{where}\\quad F'(x) = f(x)$$

Power rule for integration:

$$\\int x^n\\,dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\ne -1)$$

## Worked Examples

**Example 1: $\\int x^3\\,dx$**

$$\\frac{x^4}{4} + C$$

---

**Example 2: $\\int (3x^2 - 2x + 5)\\,dx$**

$$x^3 - x^2 + 5x + C$$

---

**Example 3: $\\int \\sqrt{x}\\,dx$**

Rewrite: $\\int x^{1/2}\\,dx = \\frac{x^{3/2}}{3/2} + C = \\frac{2}{3}x^{3/2} + C$.

## Common Mistakes

- **Forgetting $+C$.** The constant is essential; without it you have only one function, not the family.
- **Using the power rule for $n = -1$.** $\\int x^{-1}\\,dx = \\ln|x| + C$, not $x^0/0$.

## Quick Check

1. $\\int 4x^3\\,dx$
2. $\\int (2x + 3)\\,dx$
3. $\\int x^{-2}\\,dx$

*(Answers: $x^4+C$; $x^2+3x+C$; $-x^{-1}+C$)*
""",

"calc-riemann": """\
# Riemann Sums

## Overview

A **Riemann sum** approximates the area under a curve by dividing it into $n$ rectangles and summing their areas. As $n \\to \\infty$, the Riemann sum converges to the definite integral.

## Key Idea

Partition $[a, b]$ into $n$ equal subintervals of width $\\Delta x = (b-a)/n$. Choose a sample point $x_i^*$ in each. The Riemann sum is:

$$S_n = \\sum_{i=1}^{n} f(x_i^*)\\,\\Delta x$$

Right, left, and midpoint rules differ in the choice of $x_i^*$.

## Worked Examples

**Example 1: Left Riemann sum for $f(x) = x^2$ on $[0,2]$ with $n=4$**

$\\Delta x = 0.5$. Left endpoints: $0, 0.5, 1, 1.5$. Sum: $0.5(0 + 0.25 + 1 + 2.25) = 1.75$.

---

**Example 2: Right Riemann sum, same setup**

Right endpoints: $0.5, 1, 1.5, 2$. Sum: $0.5(0.25 + 1 + 2.25 + 4) = 3.75$.

---

**Example 3: Midpoint rule, same setup**

Midpoints: $0.25, 0.75, 1.25, 1.75$. Sum: $0.5(0.0625 + 0.5625 + 1.5625 + 3.0625) = 2.625$.

The exact integral $\\int_0^2 x^2\\,dx = 8/3 \\approx 2.667$.

## Common Mistakes

- **Confusing left, right, and midpoint sums** — each uses different sample points.
- **Wrong $\\Delta x$.** It should be the total width divided by $n$.

## Quick Check

1. $\\Delta x$ for $[1,5]$ with $n=4$?
2. Left endpoints for $[0,6]$ with $n=3$?
3. Right Riemann sum for $f(x)=1$ on $[0,4]$ with $n=4$?

*(Answers: 1; $0, 2, 4$; 4)*
""",

"calc-ftc": """\
# Fundamental Theorem of Calculus

## Overview

The **Fundamental Theorem of Calculus (FTC)** connects differentiation and integration. It has two parts: Part 1 says an integral with a variable upper limit is an antiderivative; Part 2 gives a formula for computing definite integrals.

## Key Idea

**FTC Part 1:** If $F(x) = \\int_a^x f(t)\\,dt$, then $F'(x) = f(x)$.

**FTC Part 2:** If $F$ is an antiderivative of $f$, then:

$$\\int_a^b f(x)\\,dx = F(b) - F(a)$$

## Worked Examples

**Example 1: $\\int_1^3 (2x + 1)\\,dx$**

Antiderivative: $F(x) = x^2 + x$. Result: $F(3) - F(1) = 12 - 2 = 10$.

---

**Example 2: $\\int_0^{\\pi} \\sin x\\,dx$**

$F(x) = -\\cos x$. Result: $-\\cos\\pi - (-\\cos 0) = 1 + 1 = 2$.

---

**Example 3: $\\frac{d}{dx}\\int_0^{x^2} \\sin t\\,dt$**

By FTC Part 1 + chain rule: $\\sin(x^2) \\cdot 2x = 2x\\sin(x^2)$.

## Common Mistakes

- **Not applying FTC Part 1 with the chain rule** when the upper limit is a function of $x$.
- **Forgetting to subtract $F(a)$** — it's $F(b) - F(a)$, not just $F(b)$.

## Quick Check

1. $\\int_0^2 3x^2\\,dx$
2. $\\int_1^4 \\sqrt{x}\\,dx$
3. $\\frac{d}{dx}\\int_0^x e^t\\,dt$

*(Answers: 8; $14/3$; $e^x$)*
""",

"calc-usub": """\
# U-Substitution

## Overview

**U-substitution** is the integration analogue of the chain rule. It works by substituting $u = g(x)$ to simplify an integral of the form $\\int f(g(x))\\,g'(x)\\,dx$.

## Key Idea

Let $u = g(x)$, then $du = g'(x)\\,dx$. The integral becomes:

$$\\int f(g(x))\\,g'(x)\\,dx = \\int f(u)\\,du$$

Integrate in terms of $u$, then substitute back.

## Worked Examples

**Example 1: $\\int 2x(x^2+1)^4\\,dx$**

$u = x^2+1$, $du = 2x\\,dx$. Integral: $\\int u^4\\,du = \\frac{u^5}{5} + C = \\frac{(x^2+1)^5}{5} + C$.

---

**Example 2: $\\int \\sin(3x)\\,dx$**

$u = 3x$, $du = 3\\,dx$, so $dx = du/3$. Integral: $\\frac{1}{3}\\int \\sin u\\,du = -\\frac{\\cos(3x)}{3} + C$.

---

**Example 3: $\\int_0^1 2x e^{x^2}\\,dx$**

$u = x^2$, $du = 2x\\,dx$. New limits: $u(0)=0$, $u(1)=1$. Integral: $\\int_0^1 e^u\\,du = e-1$.

## Common Mistakes

- **Forgetting to change $dx$ (or limits for definite integrals).**
- **Choosing a $u$ that leaves leftover $x$'s you can't express in terms of $u$.**

## Quick Check

1. $\\int 3(3x-1)^2\\,dx$
2. $\\int \\frac{2x}{x^2+4}\\,dx$
3. $\\int_0^{\\pi/2} \\cos x \\cdot e^{\\sin x}\\,dx$

*(Answers: $(3x-1)^3+C$; $\\ln(x^2+4)+C$; $e-1$)*
""",

"calc-byparts": """\
# Integration by Parts

## Overview

**Integration by parts** handles integrals of products where $u$-substitution doesn't apply. The rule comes from integrating the product rule.

## Key Idea

$$\\int u\\,dv = uv - \\int v\\,du$$

Choose $u$ and $dv$ using the LIATE priority: Logarithm, Inverse trig, Algebraic, Trigonometric, Exponential — pick the first type in this list as $u$.

## Worked Examples

**Example 1: $\\int x e^x\\,dx$**

$u = x$, $dv = e^x\\,dx$. Then $du = dx$, $v = e^x$.

$$\\int x e^x\\,dx = x e^x - \\int e^x\\,dx = xe^x - e^x + C = e^x(x-1) + C$$

---

**Example 2: $\\int x \\ln x\\,dx$**

$u = \\ln x$, $dv = x\\,dx$. Then $du = dx/x$, $v = x^2/2$.

$$\\frac{x^2}{2}\\ln x - \\int \\frac{x}{2}\\,dx = \\frac{x^2}{2}\\ln x - \\frac{x^2}{4} + C$$

---

**Example 3: $\\int e^x \\sin x\\,dx$**

Apply integration by parts twice (both times $u = \\sin x$ or $u = \\cos x$, keeping exponential as $dv$). After two steps, the original integral appears on both sides — solve algebraically.

$$\\int e^x \\sin x\\,dx = \\frac{e^x(\\sin x - \\cos x)}{2} + C$$

## Common Mistakes

- **Bad choice of $u$ and $dv$** — if $v$ is harder to integrate than the original, switch the assignment.
- **Forgetting to subtract the whole $\\int v\\,du$, not just $v$.**

## Quick Check

1. $\\int x \\cos x\\,dx$
2. $\\int \\ln x\\,dx$
3. $\\int x^2 e^x\\,dx$

*(Answers: $x\\sin x + \\cos x + C$; $x\\ln x - x + C$; $e^x(x^2-2x+2)+C$)*
""",

"calc-improper": """\
# Improper Integrals

## Overview

An **improper integral** has either an infinite limit of integration (Type I) or an integrand with a vertical asymptote on the interval (Type II). You evaluate them using limits.

## Key Idea

**Type I** (infinite limits):

$$\\int_a^\\infty f(x)\\,dx = \\lim_{b\\to\\infty}\\int_a^b f(x)\\,dx$$

**Type II** (infinite integrand at $x = c$):

$$\\int_a^b f(x)\\,dx = \\lim_{t\\to c^-}\\int_a^t f(x)\\,dx \\quad\\text{(if } f \\to \\infty \\text{ at } c)$$

## Worked Examples

**Example 1: Type I — $\\int_1^\\infty \\frac{1}{x^2}\\,dx$**

$$\\lim_{b\\to\\infty}\\left[-\\frac{1}{x}\\right]_1^b = \\lim_{b\\to\\infty}\\left(-\\frac{1}{b} + 1\\right) = 1$$

Converges to 1.

---

**Example 2: Type I — $\\int_1^\\infty \\frac{1}{x}\\,dx$**

$$\\lim_{b\\to\\infty}[\\ln x]_1^b = \\lim_{b\\to\\infty}\\ln b = \\infty$$

Diverges.

---

**Example 3: Type II — $\\int_0^1 \\frac{1}{\\sqrt{x}}\\,dx$**

Integrand blows up at $x=0$: $\\lim_{t\\to0^+}\\int_t^1 x^{-1/2}\\,dx = \\lim_{t\\to0^+}[2\\sqrt{x}]_t^1 = 2 - 0 = 2$.

## Common Mistakes

- **Evaluating without taking a limit.** Writing $\\int_0^\\infty e^{-x}\\,dx = [-e^{-x}]_0^\\infty = 1$ requires the limit argument.
- **Missing a discontinuity inside the interval** (Type II). Check the integrand carefully.

## Quick Check

1. Does $\\int_1^\\infty x^{-3}\\,dx$ converge? If so, find its value.
2. Does $\\int_0^\\infty e^{-x}\\,dx$ converge?
3. Evaluate $\\int_0^1 \\frac{1}{\\sqrt{1-x}}\\,dx$.

*(Answers: yes, 1/2; yes, 1; 2)*
""",

"calc-series-conv": """\
# Series Convergence

## Overview

An **infinite series** $\\sum_{n=1}^\\infty a_n$ converges if its partial sums approach a finite limit. Several tests determine whether a series converges without finding the actual sum.

## Key Idea

Key tests:
- **Divergence test:** If $a_n \\not\\to 0$, the series diverges.
- **$p$-series:** $\\sum 1/n^p$ converges iff $p > 1$.
- **Ratio test:** $L = \\lim |a_{n+1}/a_n|$; converges if $L < 1$, diverges if $L > 1$.
- **Comparison test:** Compare to a known series.

## Worked Examples

**Example 1: Does $\\sum_{n=1}^\\infty \\frac{1}{n^2}$ converge?**

$p = 2 > 1$, so yes (p-series). Sum $= \\pi^2/6$.

---

**Example 2: Does $\\sum_{n=1}^\\infty \\frac{n}{n+1}$ converge?**

$a_n = n/(n+1) \\to 1 \\ne 0$. Diverges by the divergence test.

---

**Example 3: Does $\\sum_{n=0}^\\infty \\frac{2^n}{n!}$ converge?**

Ratio test: $L = \\lim \\frac{2^{n+1}/(n+1)!}{2^n/n!} = \\lim \\frac{2}{n+1} = 0 < 1$. Converges.

## Common Mistakes

- **Concluding convergence from $a_n \\to 0$ alone.** The harmonic series $\\sum 1/n$ diverges even though $1/n \\to 0$.
- **Applying the ratio test when $L = 1$** — the test is inconclusive there.

## Quick Check

1. Does $\\sum 1/n^3$ converge?
2. Does $\\sum (-1)^n$ converge?
3. Does $\\sum n!/2^n$ converge?

*(Answers: yes (p-series, p=3); no (terms don't → 0); no (ratio test, L = ∞))*
""",

# ── Multivariable Calculus ─────────────────────────────────────────────────────
"mv-partial": """\
# Partial Derivatives

## Overview

A **partial derivative** measures how a function of several variables changes with respect to one variable, while holding all others constant. They are written $\\partial f/\\partial x$ or $f_x$.

## Key Idea

$$f_x(x, y) = \\lim_{h \\to 0} \\frac{f(x+h, y) - f(x, y)}{h}$$

To compute $\\partial f/\\partial x$: differentiate with respect to $x$, treating $y$ as a constant.

## Worked Examples

**Example 1: $f(x,y) = x^3 y + 2xy^2$. Find $f_x$ and $f_y$.**

$f_x = 3x^2 y + 2y^2$; $f_y = x^3 + 4xy$.

---

**Example 2: $g(x,y) = e^{xy}$. Find $g_x$.**

Treat $y$ as constant: $g_x = y e^{xy}$.

---

**Example 3: Find all second-order partial derivatives of $f(x,y) = x^2 y^3$.**

$f_x = 2xy^3$, $f_{xx} = 2y^3$. $f_y = 3x^2y^2$, $f_{yy} = 6x^2 y$. $f_{xy} = 6xy^2 = f_{yx}$.

## Common Mistakes

- **Differentiating the "constant" variable.** When computing $f_x$, treat $y$ as a number.
- **Mixing up $f_{xy}$ and $f_{yx}$.** By Clairaut's theorem, they're equal for smooth functions.

## Quick Check

1. $f_x$ for $f = 3x^2 + xy - y^3$?
2. $f_y$ for $f = \\sin(xy)$?
3. $f_{xx}$ for $f = x^3 + y^3$?

*(Answers: $6x+y$; $x\\cos(xy)$; $6x$)*
""",

"mv-double-integral": """\
# Double Integrals

## Overview

A **double integral** $\\iint_R f(x,y)\\,dA$ computes volume under a surface $z = f(x,y)$ over a region $R$, or the area/mass of a 2D region. You evaluate it as an iterated integral.

## Key Idea

For a rectangular region $[a,b] \\times [c,d]$ (Fubini's theorem):

$$\\iint_R f(x,y)\\,dA = \\int_a^b \\int_c^d f(x,y)\\,dy\\,dx = \\int_c^d \\int_a^b f(x,y)\\,dx\\,dy$$

For non-rectangular regions, the inner limits depend on the outer variable.

## Worked Examples

**Example 1: $\\int_0^1 \\int_0^2 (x + y)\\,dy\\,dx$**

Inner integral: $\\int_0^2 (x+y)\\,dy = [xy + y^2/2]_0^2 = 2x + 2$.

Outer: $\\int_0^1 (2x+2)\\,dx = [x^2 + 2x]_0^1 = 3$.

---

**Example 2: $\\iint_R x y\\,dA$ where $R = [0,2]\\times[0,3]$**

$\\int_0^2 \\int_0^3 xy\\,dy\\,dx = \\int_0^2 x \\cdot \\frac{9}{2}\\,dx = \\frac{9}{2} \\cdot 2 = 9$.

---

**Example 3: Region $0 \\le x \\le 1$, $0 \\le y \\le x$**

$\\int_0^1 \\int_0^x (x+y)\\,dy\\,dx = \\int_0^1 \\left[xy + y^2/2\\right]_0^x dx = \\int_0^1 \\frac{3x^2}{2}\\,dx = \\frac{1}{2}$.

## Common Mistakes

- **Integrating the outer limits along the inner variable.** The inner integral is a function of the outer variable.
- **Wrong order for non-rectangular regions** — draw the region and set up limits carefully.

## Quick Check

1. $\\int_0^1 \\int_0^1 2xy\\,dy\\,dx$
2. $\\int_0^2 \\int_0^y x\\,dx\\,dy$
3. Area of $R = [0,3]\\times[0,2]$ via double integral of 1.

*(Answers: 1; 4/3; 6)*
""",

"mv-change-vars": """\
# Change of Variables (Jacobian)

## Overview

**Changing variables** in a double (or triple) integral can simplify the region of integration or the integrand. The **Jacobian** is a scaling factor that accounts for how the transformation stretches or shrinks area.

## Key Idea

For a transformation $(x,y) = T(u,v)$, the Jacobian is:

$$J = \\frac{\\partial(x,y)}{\\partial(u,v)} = \\begin{vmatrix} \\partial x/\\partial u & \\partial x/\\partial v \\\\ \\partial y/\\partial u & \\partial y/\\partial v \\end{vmatrix}$$

Then $\\iint f(x,y)\\,dx\\,dy = \\iint f(T(u,v))\\,|J|\\,du\\,dv$.

## Worked Examples

**Example 1: Polar coordinates $x = r\\cos\\theta$, $y = r\\sin\\theta$**

$$J = \\begin{vmatrix} \\cos\\theta & -r\\sin\\theta \\\\ \\sin\\theta & r\\cos\\theta \\end{vmatrix} = r$$

So $dx\\,dy = r\\,dr\\,d\\theta$.

---

**Example 2: Area of disk $x^2+y^2 \\le 4$**

In polar: $\\int_0^{2\\pi}\\int_0^2 r\\,dr\\,d\\theta = 2\\pi \\cdot 2 = 4\\pi$.

---

**Example 3: $\\iint_R (x^2+y^2)\\,dA$ over $x^2+y^2 \\le 9$**

$\\int_0^{2\\pi}\\int_0^3 r^2 \\cdot r\\,dr\\,d\\theta = 2\\pi \\cdot \\frac{81}{4} = \\frac{81\\pi}{2}$.

## Common Mistakes

- **Forgetting $|J|$ in the integral.** The Jacobian is not optional.
- **Not changing the region of integration.** Transform both the integrand and the limits.

## Quick Check

1. What is the Jacobian for polar coordinates?
2. Write $\\iint e^{x^2+y^2}\\,dA$ over $x^2+y^2 \\le 1$ in polar form.
3. Evaluate that integral.

*(Answers: $r$; $\\int_0^{2\\pi}\\int_0^1 e^{r^2} r\\,dr\\,d\\theta$; $\\pi(e-1)$)*
""",


# ── Linear Algebra ─────────────────────────────────────────────────────────────
"linalg-vectors": """\
# Vectors: Dot Product and Magnitude

## Overview

A **vector** in $\\mathbb{R}^n$ is an ordered list of $n$ numbers representing direction and magnitude. The **dot product** and **magnitude** are fundamental operations used throughout linear algebra and physics.

## Key Idea

For vectors $\\mathbf{u} = (u_1, \\ldots, u_n)$ and $\\mathbf{v} = (v_1, \\ldots, v_n)$:

$$\\mathbf{u} \\cdot \\mathbf{v} = \\sum_{i=1}^n u_i v_i, \\quad \\|\\mathbf{u}\\| = \\sqrt{\\mathbf{u} \\cdot \\mathbf{u}}$$

The dot product also satisfies $\\mathbf{u} \\cdot \\mathbf{v} = \\|\\mathbf{u}\\|\\|\\mathbf{v}\\|\\cos\\theta$, where $\\theta$ is the angle between them.

## Worked Examples

**Example 1: $\\mathbf{u} = (1, 2, 3)$, $\\mathbf{v} = (4, -1, 2)$. Find $\\mathbf{u} \\cdot \\mathbf{v}$.**

$$1(4) + 2(-1) + 3(2) = 4 - 2 + 6 = 8$$

---

**Example 2: Find $\\|\\mathbf{u}\\|$ for $\\mathbf{u} = (3, 4)$.**

$$\\|\\mathbf{u}\\| = \\sqrt{9 + 16} = 5$$

---

**Example 3: Are $\\mathbf{u} = (1, -1)$ and $\\mathbf{v} = (1, 1)$ orthogonal?**

$\\mathbf{u} \\cdot \\mathbf{v} = 1 - 1 = 0$. Yes, they are orthogonal.

## Common Mistakes

- **Confusing dot product with cross product.** Dot product is a scalar; cross product is a vector.
- **Forgetting that orthogonal means dot product = 0, not equal magnitudes.**

## Quick Check

1. $\\mathbf{u} = (2,1)$, $\\mathbf{v} = (3,4)$. Find $\\mathbf{u} \\cdot \\mathbf{v}$.
2. $\\|(1,2,2)\\|$?
3. Are $(1,0)$ and $(0,1)$ orthogonal?

*(Answers: 10; 3; yes)*
""",

"linalg-matrix-ops": """\
# Matrix Addition and Scalar Multiplication

## Overview

**Matrix addition** and **scalar multiplication** are the building blocks of linear algebra. Matrices must have the same dimensions to be added; scalar multiplication scales every entry.

## Key Idea

For matrices $A$ and $B$ of the same size, and scalar $c$:

$$(A + B)_{ij} = A_{ij} + B_{ij}, \\quad (cA)_{ij} = c \\cdot A_{ij}$$

## Worked Examples

**Example 1: Add $A = \\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$ and $B = \\begin{pmatrix}5&-1\\\\0&2\\end{pmatrix}$**

$$A + B = \\begin{pmatrix}6&1\\\\3&6\\end{pmatrix}$$

---

**Example 2: Compute $3A$ for $A = \\begin{pmatrix}1&-1\\\\2&0\\end{pmatrix}$**

$$3A = \\begin{pmatrix}3&-3\\\\6&0\\end{pmatrix}$$

---

**Example 3: Compute $2A - B$**

$2A = \\begin{pmatrix}2&4\\\\6&8\\end{pmatrix}$. Then $2A - B = \\begin{pmatrix}-3&5\\\\6&6\\end{pmatrix}$.

## Common Mistakes

- **Adding matrices of different sizes.** Not defined.
- **Misapplying scalar multiplication** — every single entry gets multiplied.

## Quick Check

1. $\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix} + \\begin{pmatrix}-1&0\\\\2&1\\end{pmatrix}$
2. $5 \\cdot \\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}$
3. Can you add a $2\\times3$ matrix to a $3\\times2$ matrix?

*(Answers: $\\begin{pmatrix}0&2\\\\5&5\\end{pmatrix}$; $5I_2$; no)*
""",

"linalg-matrix-mult": """\
# Matrix Multiplication

## Overview

**Matrix multiplication** combines two matrices to produce a third. It is not component-wise — the $(i,j)$ entry of the product is the dot product of the $i$-th row of $A$ with the $j$-th column of $B$.

## Key Idea

$(AB)_{ij} = \\sum_k A_{ik} B_{kj}$. For $A$ to multiply $B$, the number of columns of $A$ must equal the number of rows of $B$. If $A$ is $m\\times n$ and $B$ is $n\\times p$, then $AB$ is $m\\times p$.

## Worked Examples

**Example 1: $A = \\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$, $B = \\begin{pmatrix}5&6\\\\7&8\\end{pmatrix}$. Find $AB$.**

$AB = \\begin{pmatrix}1\\cdot5+2\\cdot7 & 1\\cdot6+2\\cdot8\\\\3\\cdot5+4\\cdot7 & 3\\cdot6+4\\cdot8\\end{pmatrix} = \\begin{pmatrix}19&22\\\\43&50\\end{pmatrix}$

---

**Example 2: $A = \\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}$, $B = \\begin{pmatrix}3&-1\\\\2&4\\end{pmatrix}$. Find $AB$.**

$AB = B$ (identity matrix).

---

**Example 3: Is matrix multiplication commutative?**

No. Even when both $AB$ and $BA$ are defined and the same size, they are generally unequal.

## Common Mistakes

- **Multiplying component-wise.** That's not how matrix multiplication works.
- **Assuming $AB = BA$** — matrix multiplication is not commutative.

## Quick Check

1. Dimensions of $(3\\times4)\\cdot(4\\times2)$?
2. Find $\\begin{pmatrix}1&2\\end{pmatrix} \\begin{pmatrix}3\\\\4\\end{pmatrix}$.
3. Does $AB = BA$ always?

*(Answers: $3\\times2$; 11; no)*
""",

"linalg-transpose": """\
# Transpose

## Overview

The **transpose** of a matrix $A$, denoted $A^T$, flips rows and columns: the $(i,j)$ entry of $A^T$ is the $(j,i)$ entry of $A$. A matrix is **symmetric** if $A = A^T$.

## Key Idea

$$(A^T)_{ij} = A_{ji}, \\quad (AB)^T = B^T A^T, \\quad (A^T)^T = A$$

## Worked Examples

**Example 1: Transpose of $A = \\begin{pmatrix}1&2&3\\\\4&5&6\\end{pmatrix}$**

$$A^T = \\begin{pmatrix}1&4\\\\2&5\\\\3&6\\end{pmatrix}$$

---

**Example 2: Is $B = \\begin{pmatrix}1&2\\\\2&3\\end{pmatrix}$ symmetric?**

$B^T = B$, so yes.

---

**Example 3: Verify $(AB)^T = B^T A^T$ for simple matrices**

$A = \\begin{pmatrix}1&0\\\\0&2\\end{pmatrix}$, $B = \\begin{pmatrix}3\\\\1\\end{pmatrix}$. $AB = \\begin{pmatrix}3\\\\2\\end{pmatrix}$, $(AB)^T = \\begin{pmatrix}3&2\\end{pmatrix}$. $B^T A^T = \\begin{pmatrix}3&1\\end{pmatrix}\\begin{pmatrix}1&0\\\\0&2\\end{pmatrix} = \\begin{pmatrix}3&2\\end{pmatrix}$ ✓

## Common Mistakes

- **Reversing the order in $(AB)^T$:** it is $B^T A^T$, not $A^T B^T$.
- **Thinking all matrices are symmetric.**

## Quick Check

1. Transpose $\\begin{pmatrix}1&3\\\\2&4\\end{pmatrix}$.
2. Is $\\begin{pmatrix}1&2\\\\3&1\\end{pmatrix}$ symmetric?
3. $(AB)^T = ?$

*(Answers: $\\begin{pmatrix}1&2\\\\3&4\\end{pmatrix}$; no ($2\\ne3$); $B^T A^T$)*
""",

"linalg-row-reduce": """\
# Row Reduction

## Overview

**Row reduction** (Gaussian elimination) transforms a matrix into row echelon form using three elementary row operations: swap rows, scale a row, add a multiple of one row to another. It is the standard algorithm for solving linear systems.

## Key Idea

The three row operations:
1. Swap $R_i \\leftrightarrow R_j$
2. Scale: $R_i \\leftarrow cR_i$ ($c \\ne 0$)
3. Add: $R_i \\leftarrow R_i + kR_j$

These preserve the solution set. **Reduced row echelon form (RREF)** has leading 1s with zeros above and below.

## Worked Examples

**Example 1: Solve $x + 2y = 5$, $3x - y = 4$**

Augmented matrix: $\\begin{pmatrix}1&2&5\\\\3&-1&4\\end{pmatrix}$. $R_2 \\leftarrow R_2 - 3R_1$: $\\begin{pmatrix}1&2&5\\\\0&-7&-11\\end{pmatrix}$. Scale: $y = 11/7$, then $x = 5 - 2(11/7) = 13/7$.

---

**Example 2: Identify a free variable**

$\\begin{pmatrix}1&2&3\\\\0&0&1\\end{pmatrix}$: pivot in columns 1 and 3; $x_2$ is free.

---

**Example 3: RREF of $\\begin{pmatrix}2&4\\\\1&2\\end{pmatrix}$**

$R_1 \\leftarrow R_1/2$: $\\begin{pmatrix}1&2\\\\1&2\\end{pmatrix}$. $R_2 \\leftarrow R_2 - R_1$: $\\begin{pmatrix}1&2\\\\0&0\\end{pmatrix}$. One free variable — infinitely many solutions.

## Common Mistakes

- **Dividing by zero when scaling.** Check your pivot is nonzero.
- **Arithmetic errors when adding multiples of rows.** Work carefully, sign by sign.

## Quick Check

1. What are the three elementary row operations?
2. How many solutions if RREF has a row $[0\\ 0\\ |\\ 1]$?
3. What does a free variable in RREF indicate?

*(Answers: swap, scale, add; none (inconsistent); infinitely many solutions)*
""",

"linalg-determinant": """\
# Determinants

## Overview

The **determinant** of a square matrix is a scalar that encodes important geometric and algebraic information. If $\\det A = 0$, the matrix is singular (not invertible). Geometrically, $|\\det A|$ is the volume scaling factor of the linear transformation.

## Key Idea

For $2\\times2$: $\\det\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix} = ad - bc$.

For $3\\times3$ (cofactor expansion along first row):

$$\\det A = a_{11}M_{11} - a_{12}M_{12} + a_{13}M_{13}$$

where $M_{ij}$ is the minor (determinant of the submatrix with row $i$, column $j$ deleted).

## Worked Examples

**Example 1: $\\det\\begin{pmatrix}3&1\\\\2&4\\end{pmatrix}$**

$$3(4) - 1(2) = 10$$

---

**Example 2: $\\det\\begin{pmatrix}1&0&0\\\\2&3&0\\\\4&5&6\\end{pmatrix}$**

Lower triangular — determinant = product of diagonal = $1 \\cdot 3 \\cdot 6 = 18$.

---

**Example 3: Effect of row operations on determinant**

Swapping rows changes sign. Scaling row $i$ by $c$ multiplies $\\det$ by $c$. Adding a multiple of one row to another leaves $\\det$ unchanged.

## Common Mistakes

- **Using $2\\times2$ formula for $3\\times3$ matrices.**
- **Forgetting the alternating signs** in cofactor expansion.

## Quick Check

1. $\\det\\begin{pmatrix}2&0\\\\0&5\\end{pmatrix}$
2. $\\det\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}$
3. If $\\det A = 3$, what is $\\det(2A)$ for a $2\\times2$ matrix?

*(Answers: 10; 0; 12)*
""",

"linalg-inverse": """\
# Matrix Inverse

## Overview

The **inverse** of a square matrix $A$ is the matrix $A^{-1}$ satisfying $AA^{-1} = A^{-1}A = I$. A matrix is invertible if and only if $\\det A \\ne 0$. The inverse undoes the linear transformation.

## Key Idea

For $2\\times2$: $A^{-1} = \\frac{1}{\\det A}\\begin{pmatrix}d&-b\\\\-c&a\\end{pmatrix}$ when $A = \\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}$.

For larger matrices: row-reduce the augmented matrix $[A | I]$ until the left block becomes $I$; the right block is $A^{-1}$.

## Worked Examples

**Example 1: Find the inverse of $A = \\begin{pmatrix}2&1\\\\5&3\\end{pmatrix}$**

$\\det A = 1$. $A^{-1} = \\begin{pmatrix}3&-1\\\\-5&2\\end{pmatrix}$.

---

**Example 2: Verify: $AA^{-1} = I$**

$\\begin{pmatrix}2&1\\\\5&3\\end{pmatrix}\\begin{pmatrix}3&-1\\\\-5&2\\end{pmatrix} = \\begin{pmatrix}1&0\\\\0&1\\end{pmatrix}$ ✓

---

**Example 3: Use inverse to solve $Ax = b$**

If $A^{-1}$ exists, then $x = A^{-1}b$. For $A$ above and $b = \\begin{pmatrix}4\\\\11\\end{pmatrix}$: $x = \\begin{pmatrix}3&-1\\\\-5&2\\end{pmatrix}\\begin{pmatrix}4\\\\11\\end{pmatrix} = \\begin{pmatrix}1\\\\2\\end{pmatrix}$.

## Common Mistakes

- **Inverting a singular matrix.** If $\\det A = 0$, no inverse exists.
- **$(AB)^{-1} = A^{-1}B^{-1}$.** Wrong — it's $B^{-1}A^{-1}$ (reverse order).

## Quick Check

1. Find the inverse of $\\begin{pmatrix}1&2\\\\0&1\\end{pmatrix}$.
2. Is $\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}$ invertible?
3. $(AB)^{-1} = ?$

*(Answers: $\\begin{pmatrix}1&-2\\\\0&1\\end{pmatrix}$; no (det=0); $B^{-1}A^{-1}$)*
""",

"linalg-linear-systems": """\
# Linear Systems

## Overview

A **linear system** is a set of linear equations in the same unknowns. Solutions can be unique, infinitely many (underdetermined), or none (inconsistent). Row reduction is the systematic method for classifying and solving them.

## Key Idea

Write the system as an augmented matrix $[A | b]$, row-reduce to RREF, then read off solutions. A system is inconsistent if RREF has a row $[0 \\cdots 0 | c]$ with $c \\ne 0$.

## Worked Examples

**Example 1: Unique solution**

$x + y = 3$, $x - y = 1$. RREF gives $x = 2$, $y = 1$.

---

**Example 2: Infinite solutions**

$x + 2y = 4$, $2x + 4y = 8$. Second equation is twice the first — one free variable: $y = t$, $x = 4 - 2t$.

---

**Example 3: No solution (inconsistent)**

$x + y = 3$, $x + y = 5$. Contradiction — no solution.

## Common Mistakes

- **Stopping before full RREF.** Back-substitution is needed for non-RREF forms.
- **Missing free variables** when a column has no pivot.

## Quick Check

1. How many solutions can a linear system have?
2. What does a row $[0\\ 0\\ |\\ 5]$ mean in an augmented matrix?
3. Identify: $x + y = 2$, $2x + 2y = 5$.

*(Answers: 0, 1, or infinitely many; no solution (inconsistent); inconsistent)*
""",

"linalg-span-independence": """\
# Span and Linear Independence

## Overview

The **span** of a set of vectors is the set of all linear combinations. Vectors are **linearly independent** if no vector in the set can be written as a linear combination of the others.

## Key Idea

$\\{\\mathbf{v}_1, \\ldots, \\mathbf{v}_k\\}$ is linearly independent iff the only solution to $c_1 \\mathbf{v}_1 + \\cdots + c_k \\mathbf{v}_k = \\mathbf{0}$ is $c_1 = \\cdots = c_k = 0$.

Equivalently, they are independent iff the matrix with these as columns has full column rank.

## Worked Examples

**Example 1: Are $(1,0)$ and $(0,1)$ linearly independent?**

$c_1(1,0) + c_2(0,1) = (0,0) \\Rightarrow c_1 = c_2 = 0$. Yes.

---

**Example 2: Are $(1,2)$ and $(2,4)$ linearly independent?**

$(2,4) = 2(1,2)$, so they are **dependent**.

---

**Example 3: Does $(3,1)$ lie in span$\\{(1,0),(0,1)\\}$?**

$(3,1) = 3(1,0) + 1(0,1)$. Yes.

## Common Mistakes

- **Confusing span with independence.** A large set can span a space but still contain dependent vectors.
- **Testing only one combination.** Linear independence requires the zero combination to be the only one.

## Quick Check

1. Is $\\{(1,2),(3,6)\\}$ linearly independent?
2. Does $(5,3)$ lie in span$\\{(1,0),(0,1)\\}$?
3. If $k > n$, can $k$ vectors in $\\mathbb{R}^n$ be independent?

*(Answers: no; yes; no)*
""",

"linalg-subspaces": """\
# Subspaces and Column Space

## Overview

A **subspace** of $\\mathbb{R}^n$ is a subset closed under addition and scalar multiplication that contains the zero vector. The **column space** (or range) of a matrix $A$ is the span of its columns.

## Key Idea

A set $V$ is a subspace iff:
1. $\\mathbf{0} \\in V$
2. $\\mathbf{u}, \\mathbf{v} \\in V \\Rightarrow \\mathbf{u} + \\mathbf{v} \\in V$
3. $\\mathbf{u} \\in V$, $c \\in \\mathbb{R} \\Rightarrow c\\mathbf{u} \\in V$

The column space of $A$ is the set of all $b$ for which $Ax = b$ has a solution.

## Worked Examples

**Example 1: Is $V = \\{(x,y): y = 2x\\}$ a subspace of $\\mathbb{R}^2$?**

$\\mathbf{0} = (0,0)$ satisfies $y=2x$ ✓. Sum of two elements: $(x_1,2x_1)+(x_2,2x_2) = (x_1+x_2, 2(x_1+x_2))$ ✓. Subspace.

---

**Example 2: Column space of $\\begin{pmatrix}1&2\\\\3&6\\end{pmatrix}$**

Columns are $(1,3)$ and $(2,6)=2(1,3)$. Column space = span$\\{(1,3)\\}$, a line through the origin.

---

**Example 3: Is $W = \\{(x,y): y = 2x + 1\\}$ a subspace?**

$\\mathbf{0}$ does not satisfy $y = 2x+1$ ($0 \\ne 1$). Not a subspace.

## Common Mistakes

- **Forgetting to check that $\\mathbf{0}$ is in the set.** Affine subsets (like planes not through the origin) are not subspaces.

## Quick Check

1. Is $\\{\\mathbf{0}\\}$ a subspace?
2. Is the set of all vectors with non-negative entries a subspace?
3. What is the column space of the identity matrix?

*(Answers: yes; no (not closed under scalar mult by $-1$); all of $\\mathbb{R}^n$)*
""",

"linalg-rank-nullity": """\
# Rank-Nullity Theorem

## Overview

The **rank** of a matrix $A$ is the dimension of its column space (= number of pivot columns). The **nullity** is the dimension of the null space (solutions to $Ax = 0$). The Rank-Nullity Theorem links the two.

## Key Idea

For an $m \\times n$ matrix $A$:

$$\\text{rank}(A) + \\text{nullity}(A) = n$$

The null space (kernel) is the set of all $x$ with $Ax = 0$; its dimension is the number of free variables.

## Worked Examples

**Example 1: $A = \\begin{pmatrix}1&2&3\\\\0&1&1\\end{pmatrix}$. Find rank and nullity.**

Two pivot columns → rank = 2. $n = 3$. Nullity = 1 (one free variable).

---

**Example 2: Find a basis for the null space of $A$ above.**

From RREF: $x_1 = -x_3$, $x_2 = -x_3$. Free variable $x_3 = t$. Null space = span$\\{(-1,-1,1)\\}$.

---

**Example 3: $A$ is $4\\times6$ with rank 3. What is its nullity?**

$6 - 3 = 3$.

## Common Mistakes

- **Confusing rank with the number of rows.** Rank is the number of pivot rows, which may be less.
- **Computing rank as the number of nonzero rows before row reduction.**

## Quick Check

1. A $3\\times5$ matrix has rank 2. What is its nullity?
2. If $A$ is $4\\times4$ and has rank 4, what is the nullity?
3. What does nullity 0 imply about $Ax=0$?

*(Answers: 3; 0; only the trivial solution)*
""",

"linalg-linear-transforms": """\
# Linear Transformations

## Overview

A **linear transformation** $T: \\mathbb{R}^n \\to \\mathbb{R}^m$ satisfies additivity and homogeneity: $T(u+v) = T(u)+T(v)$ and $T(cu) = cT(u)$. Every linear transformation can be represented by a matrix.

## Key Idea

Every linear $T: \\mathbb{R}^n \\to \\mathbb{R}^m$ has a unique matrix $A$ (the **standard matrix**) such that $T(x) = Ax$ for all $x$. The columns of $A$ are the images of the standard basis vectors.

## Worked Examples

**Example 1: $T(x_1, x_2) = (2x_1 + x_2, x_1 - 3x_2)$. Find the matrix.**

$T(e_1) = (2,1)$, $T(e_2) = (1,-3)$. Matrix: $\\begin{pmatrix}2&1\\\\1&-3\\end{pmatrix}$.

---

**Example 2: Is $T(x,y) = (x+1, y)$ linear?**

$T(0,0) = (1,0) \\ne (0,0)$. Not linear (fails $T(\\mathbf{0}) = \\mathbf{0}$).

---

**Example 3: Rotation by $\\theta$ in $\\mathbb{R}^2$**

$$A = \\begin{pmatrix}\\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta\\end{pmatrix}$$

## Common Mistakes

- **Thinking any transformation can be written as $Ax$.** Only linear ones can.
- **Not checking $T(\\mathbf{0}) = \\mathbf{0}$** as a quick linearity test.

## Quick Check

1. Is $T(x,y) = (3x, y)$ linear?
2. Find the standard matrix of $T(x,y) = (y,x)$.
3. Image of $(1,2)$ under the $90°$ rotation matrix?

*(Answers: yes; $\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}$; $(-2,1)$)*
""",

"linalg-change-basis": """\
# Change of Basis

## Overview

**Change of basis** converts the representation of a vector (or transformation) from one basis to another. This is useful when a different basis makes a problem simpler — especially for diagonalization.

## Key Idea

If $B = \\{b_1, \\ldots, b_n\\}$ is a basis and $P = [b_1 \\mid \\cdots \\mid b_n]$ is the change-of-basis matrix (columns are basis vectors), then:

$$[x]_B = P^{-1} x, \\quad x = P[x]_B$$

For a transformation $T$ with matrix $A$ (standard) and new basis $P$: the matrix in the new basis is $P^{-1}AP$.

## Worked Examples

**Example 1: Express $(3, 1)$ in the basis $\\{(1,1),(1,-1)\\}$**

$P = \\begin{pmatrix}1&1\\\\1&-1\\end{pmatrix}$. $P^{-1} = \\frac{1}{-2}\\begin{pmatrix}-1&-1\\\\-1&1\\end{pmatrix}$. $(3,1)$ in new basis: $P^{-1}\\begin{pmatrix}3\\\\1\\end{pmatrix} = \\begin{pmatrix}2\\\\1\\end{pmatrix}$ (up to scaling).

---

**Example 2: Verify by reconstruction**

$2(1,1) + 1(1,-1) = (2,2) + (1,-1) = (3,1)$ ✓

---

**Example 3: New basis matrix for $A = \\begin{pmatrix}3&0\\\\0&1\\end{pmatrix}$ in eigenbasis**

If $A$ is already diagonal, the eigenbasis is the standard basis.

## Common Mistakes

- **Using $P$ instead of $P^{-1}$.** Converting to the new basis uses $P^{-1}$; converting back uses $P$.

## Quick Check

1. $P = \\begin{pmatrix}1&0\\\\0&2\\end{pmatrix}$. What is $P^{-1}(2,4)^T$?
2. What does $P^{-1}AP$ represent geometrically?
3. Is change of basis a linear operation?

*(Answers: $(2,2)^T$; $A$ in the new basis; yes)*
""",

"linalg-eigenvalues": """\
# Eigenvalues and Eigenvectors

## Overview

An **eigenvector** of $A$ is a nonzero vector $v$ such that $Av = \\lambda v$ for some scalar $\\lambda$ (the **eigenvalue**). Eigenvectors point in directions that the transformation scales but doesn't rotate.

## Key Idea

Find eigenvalues by solving the **characteristic equation**:

$$\\det(A - \\lambda I) = 0$$

For each $\\lambda$, find eigenvectors by solving $(A - \\lambda I)v = 0$.

## Worked Examples

**Example 1: Find eigenvalues of $A = \\begin{pmatrix}3&1\\\\0&2\\end{pmatrix}$**

$\\det(A - \\lambda I) = (3-\\lambda)(2-\\lambda) = 0$. Eigenvalues: $\\lambda = 3$ and $\\lambda = 2$.

---

**Example 2: Eigenvector for $\\lambda = 3$**

$(A - 3I)v = \\begin{pmatrix}0&1\\\\0&-1\\end{pmatrix}v = 0 \\Rightarrow v = \\begin{pmatrix}1\\\\0\\end{pmatrix}$.

---

**Example 3: Eigenvalues of $A = \\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$**

$\\det(A-\\lambda I) = (2-\\lambda)^2 - 1 = 0 \\Rightarrow \\lambda = 3$ or $\\lambda = 1$.

## Common Mistakes

- **Setting $Av = \\lambda v$ to find $\\lambda$ before finding eigenvectors.** You need the characteristic equation first.
- **Thinking eigenvectors are unique.** Any nonzero multiple of an eigenvector is also an eigenvector.

## Quick Check

1. Find eigenvalues of $\\begin{pmatrix}4&0\\\\0&-1\\end{pmatrix}$.
2. Eigenvector for $\\lambda = 4$ above?
3. What does $\\lambda = 0$ imply?

*(Answers: 4, −1; $(1,0)$; $A$ is singular)*
""",

"linalg-diagonalization": """\
# Diagonalization

## Overview

A matrix $A$ is **diagonalizable** if there exists an invertible $P$ such that $P^{-1}AP = D$ is diagonal. This is possible when $A$ has $n$ linearly independent eigenvectors. Diagonalization simplifies powers and functions of matrices.

## Key Idea

$A = PDP^{-1}$ where $D = \\text{diag}(\\lambda_1, \\ldots, \\lambda_n)$ and the columns of $P$ are the corresponding eigenvectors.

Then $A^k = PD^kP^{-1}$, and $D^k$ is just diagonal entries raised to the $k$-th power.

## Worked Examples

**Example 1: Diagonalize $A = \\begin{pmatrix}3&1\\\\0&2\\end{pmatrix}$**

Eigenvalues $\\lambda_1=3$, $\\lambda_2=2$; eigenvectors $(1,0)$, $(-1,1)$.

$P = \\begin{pmatrix}1&-1\\\\0&1\\end{pmatrix}$, $D = \\begin{pmatrix}3&0\\\\0&2\\end{pmatrix}$.

---

**Example 2: Compute $A^3$ via diagonalization**

$A^3 = PD^3P^{-1}$, where $D^3 = \\begin{pmatrix}27&0\\\\0&8\\end{pmatrix}$.

---

**Example 3: When is a matrix not diagonalizable?**

If it doesn't have $n$ independent eigenvectors. Example: $\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}$ has only one independent eigenvector for $\\lambda=1$.

## Common Mistakes

- **Assuming symmetric matrices can have complex eigenvalues.** Real symmetric matrices always have real eigenvalues.
- **Mixing up column order in $P$ vs. diagonal order in $D$.**

## Quick Check

1. A matrix has eigenvalues 2 and 5. What is $D$?
2. Is the identity matrix diagonalizable?
3. If $A = PDP^{-1}$, what is $A^2$?

*(Answers: $\\text{diag}(2,5)$; yes ($A=I=ID I^{-1}$); $PD^2P^{-1}$)*
""",

"linalg-symmetric-spectral": """\
# Symmetric Matrices and Spectral Theorem

## Overview

A **symmetric matrix** satisfies $A = A^T$. The **Spectral Theorem** guarantees that every real symmetric matrix is orthogonally diagonalizable: $A = Q\\Lambda Q^T$, where $Q$ has orthonormal eigenvectors as columns.

## Key Idea

**Spectral Theorem:** If $A$ is real symmetric ($n\\times n$), then:
1. All eigenvalues are real.
2. Eigenvectors for distinct eigenvalues are orthogonal.
3. $A = Q\\Lambda Q^T$ where $Q$ is orthogonal ($Q^T = Q^{-1}$).

## Worked Examples

**Example 1: Eigenvalues of $A = \\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$**

$\\lambda_1 = 3$ (eigenvector $(1,1)/\\sqrt{2}$), $\\lambda_2 = 1$ (eigenvector $(1,-1)/\\sqrt{2}$). Note: orthogonal ✓

---

**Example 2: Spectral decomposition of $A$ above**

$A = 3 \\cdot v_1 v_1^T + 1 \\cdot v_2 v_2^T$ where $v_i$ are the unit eigenvectors.

---

**Example 3: Verify $Q^T Q = I$**

Columns of $Q$ are orthonormal by construction, so $Q^T Q = I$.

## Common Mistakes

- **Forgetting to normalize eigenvectors** when constructing $Q$.
- **Applying the Spectral Theorem to non-symmetric matrices.**

## Quick Check

1. Are eigenvalues of a real symmetric matrix always real?
2. Are eigenvectors for distinct eigenvalues always orthogonal (symmetric case)?
3. What does $A = Q\\Lambda Q^T$ mean geometrically?

*(Answers: yes; yes; rotate, scale, rotate back)*
""",

"linalg-orthogonality": """\
# Orthogonality

## Overview

Two vectors are **orthogonal** if their dot product is zero. A set of vectors is **orthonormal** if they are pairwise orthogonal and each has unit length. Orthogonality is the generalization of perpendicularity.

## Key Idea

$\\mathbf{u}$ and $\\mathbf{v}$ are orthogonal iff $\\mathbf{u} \\cdot \\mathbf{v} = 0$.

A matrix $Q$ is **orthogonal** if its columns form an orthonormal set: $Q^T Q = I$, so $Q^{-1} = Q^T$.

## Worked Examples

**Example 1: Are $(1,2,-1)$ and $(3,0,3)$ orthogonal?**

$1(3) + 2(0) + (-1)(3) = 0$. Yes.

---

**Example 2: Normalize $v = (3,4)$**

$\\|v\\| = 5$. Unit vector: $(3/5, 4/5)$.

---

**Example 3: Verify $Q = \\frac{1}{\\sqrt{2}}\\begin{pmatrix}1&-1\\\\1&1\\end{pmatrix}$ is orthogonal**

$Q^T Q = \\frac{1}{2}\\begin{pmatrix}1&1\\\\-1&1\\end{pmatrix}\\begin{pmatrix}1&-1\\\\1&1\\end{pmatrix} = \\frac{1}{2}\\begin{pmatrix}2&0\\\\0&2\\end{pmatrix} = I$ ✓

## Common Mistakes

- **Confusing orthogonal (dot product = 0) with parallel (one is a scalar multiple of the other).**
- **Thinking $Q^T = Q^{-1}$ holds for all matrices.** Only for orthogonal matrices.

## Quick Check

1. Are $(1,0,0)$ and $(0,1,0)$ orthogonal?
2. Normalize $(0,0,5)$.
3. If $Q$ is orthogonal, what is $Q^{-1}$?

*(Answers: yes; $(0,0,1)$; $Q^T$)*
""",

"linalg-gram-schmidt": """\
# Gram-Schmidt Process

## Overview

The **Gram-Schmidt process** converts a set of linearly independent vectors into an orthonormal basis for the same span. It works by successive projection and subtraction.

## Key Idea

Given $\\{v_1, v_2, \\ldots\\}$, construct orthogonal vectors $\\{u_1, u_2, \\ldots\\}$:

$$u_1 = v_1, \\quad u_k = v_k - \\sum_{j=1}^{k-1} \\frac{v_k \\cdot u_j}{u_j \\cdot u_j}\\, u_j$$

Normalize each $u_i$ to get the orthonormal basis $e_i = u_i/\\|u_i\\|$.

## Worked Examples

**Example 1: $v_1 = (1,1)$, $v_2 = (1,0)$. Apply Gram-Schmidt.**

$u_1 = (1,1)$. Projection of $v_2$ onto $u_1$: $\\frac{(1)(1)+(0)(1)}{2}(1,1) = (1/2, 1/2)$.

$u_2 = (1,0) - (1/2,1/2) = (1/2,-1/2)$.

Normalize: $e_1 = (1,1)/\\sqrt{2}$, $e_2 = (1,-1)/\\sqrt{2}$.

---

**Example 2: Verify orthogonality of result**

$e_1 \\cdot e_2 = \\frac{1}{2}(1)(1) + \\frac{1}{2}(1)(-1) = 0$ ✓

---

**Example 3: Use of QR decomposition**

Gram-Schmidt produces $Q$ (orthonormal columns) and implicitly $R$ (upper triangular), giving $A = QR$.

## Common Mistakes

- **Subtracting projections from the normalized vectors** instead of the unnormalized ones.
- **Normalizing before completing all Gram-Schmidt steps.**

## Quick Check

1. What does Gram-Schmidt produce from a set of independent vectors?
2. After Gram-Schmidt, are the result vectors orthonormal?
3. What is QR decomposition used for?

*(Answers: orthonormal basis for the same span; yes (after normalizing); solving least-squares, numerics)*
""",

"linalg-orthogonal-projection": """\
# Orthogonal Projection

## Overview

The **orthogonal projection** of a vector $b$ onto a subspace $W$ is the closest point in $W$ to $b$. It decomposes $b$ into a component in $W$ and a component orthogonal to $W$.

## Key Idea

Projection onto a vector $a$:

$$\\text{proj}_a b = \\frac{a \\cdot b}{a \\cdot a}\\, a$$

Projection onto a subspace with orthonormal basis $\\{q_1, \\ldots, q_k\\}$:

$$\\hat{b} = (b \\cdot q_1)q_1 + \\cdots + (b \\cdot q_k)q_k = QQ^T b$$

## Worked Examples

**Example 1: Project $(3, 4)$ onto the direction $(1, 0)$**

$$\\text{proj} = \\frac{(3)(1)+(4)(0)}{1}(1,0) = (3,0)$$

---

**Example 2: Project $b = (1,1,1)^T$ onto $a = (1,1,0)^T$**

$$\\hat{b} = \\frac{2}{2}(1,1,0) = (1,1,0)$$

---

**Example 3: Projection matrix**

If $A$ has orthonormal columns, $P = AA^T$ is the projection matrix onto $\\text{col}(A)$.

## Common Mistakes

- **Dividing by $\\|a\\|$ instead of $\\|a\\|^2$ in the scalar formula.**
- **Projecting onto a non-unit vector and forgetting to normalize.**

## Quick Check

1. Project $(5,2)$ onto $(1,0)$.
2. What is $\\|b - \\hat{b}\\|$ called?
3. Is $P^2 = P$ for a projection matrix?

*(Answers: $(5,0)$; the error; yes (idempotent))*
""",

"linalg-least-squares": """\
# Least Squares

## Overview

When $Ax = b$ has no solution (overdetermined system), the **least-squares solution** minimizes $\\|Ax - b\\|^2$ — the closest solution in the column space of $A$.

## Key Idea

The least-squares solution satisfies the **normal equations**:

$$A^T A \\hat{x} = A^T b$$

If $A$ has full column rank, $\\hat{x} = (A^T A)^{-1} A^T b$.

## Worked Examples

**Example 1: Fit a line $y = mx + c$ to $(1,1), (2,2), (3,4)$**

$A = \\begin{pmatrix}1&1\\\\2&1\\\\3&1\\end{pmatrix}$, $b = \\begin{pmatrix}1\\\\2\\\\4\\end{pmatrix}$.

$A^T A = \\begin{pmatrix}14&6\\\\6&3\\end{pmatrix}$, $A^T b = \\begin{pmatrix}17\\\\7\\end{pmatrix}$.

Normal equations give $m = 3/2$, $c = -1/3$.

---

**Example 2: Geometric meaning**

$\\hat{b} = A\\hat{x}$ is the projection of $b$ onto $\\text{col}(A)$.

---

**Example 3: Residual is orthogonal to column space**

$A^T(b - A\\hat{x}) = 0$, meaning the error is perpendicular to all columns of $A$.

## Common Mistakes

- **Solving $Ax = b$ directly when it's inconsistent.** Use normal equations instead.
- **Forgetting that $A^T A$ must be invertible** (requires $A$ to have independent columns).

## Quick Check

1. What equation do least-squares solutions satisfy?
2. Is the least-squares solution exact when $b \\in \\text{col}(A)$?
3. What does minimizing $\\|Ax - b\\|^2$ find geometrically?

*(Answers: $A^T A\\hat{x} = A^T b$; yes, residual = 0; projection of $b$ onto col($A$))*
""",

"linalg-svd": """\
# Singular Value Decomposition

## Overview

The **Singular Value Decomposition (SVD)** decomposes any $m\\times n$ matrix $A$ as $A = U\\Sigma V^T$, where $U$ and $V$ are orthogonal and $\\Sigma$ is diagonal with non-negative entries. It is the most informative matrix factorization.

## Key Idea

$$A = U \\Sigma V^T$$

- $U$: $m\\times m$ orthogonal (left singular vectors)
- $\\Sigma$: $m\\times n$ diagonal ($\\sigma_1 \\ge \\sigma_2 \\ge \\cdots \\ge 0$ are singular values)
- $V$: $n\\times n$ orthogonal (right singular vectors)

Singular values $\\sigma_i = \\sqrt{\\lambda_i(A^T A)}$.

## Worked Examples

**Example 1: SVD of $A = \\begin{pmatrix}3&0\\\\0&2\\end{pmatrix}$ (diagonal)**

$\\Sigma = A$, $U = V = I$. Singular values: 3 and 2.

---

**Example 2: Geometric interpretation**

$A = U\\Sigma V^T$: $V^T$ rotates, $\\Sigma$ scales axes, $U$ rotates again. Every linear map is "rotate–scale–rotate."

---

**Example 3: Low-rank approximation**

Rank-$k$ approximation: $A_k = \\sum_{i=1}^k \\sigma_i u_i v_i^T$. Best rank-$k$ approximation in 2-norm.

## Common Mistakes

- **Confusing singular values with eigenvalues.** For symmetric $A$, they coincide, but not in general.
- **Thinking $U$ and $V$ must be the same matrix.** They are different orthogonal matrices.

## Quick Check

1. What is the rank of $A$ in terms of its singular values?
2. If $A$ is symmetric positive definite, how do singular values relate to eigenvalues?
3. What does a near-zero singular value indicate?

*(Answers: number of nonzero $\\sigma_i$; they are equal; near-linear dependence)*
""",


# ── Probability ────────────────────────────────────────────────────────────────
"prob-sample-space": """\
# Sample Spaces

## Overview

A **sample space** $\\Omega$ is the set of all possible outcomes of a random experiment. An **event** is any subset of $\\Omega$. Probability theory is built on this foundation.

## Key Idea

Every probability problem starts with defining $\\Omega$. Outcomes must be **mutually exclusive** and **exhaustive** — no outcome is repeated and together they cover all possibilities.

## Worked Examples

**Example 1: Flip a coin once**

$\\Omega = \\{H, T\\}$. Event "heads" = $\\{H\\}$.

---

**Example 2: Roll a die**

$\\Omega = \\{1, 2, 3, 4, 5, 6\\}$. Event "even" = $\\{2, 4, 6\\}$.

---

**Example 3: Flip two coins**

$\\Omega = \\{HH, HT, TH, TT\\}$. Event "at least one head" = $\\{HH, HT, TH\\}$.

## Common Mistakes

- **Missing outcomes.** For two dice, $\\Omega$ has 36 elements, not 11.
- **Treating ordered and unordered outcomes interchangeably.** $(H,T)$ and $(T,H)$ are different outcomes.

## Quick Check

1. $|\\Omega|$ for rolling two dice?
2. Sample space for drawing one card from {A, K, Q}?
3. Event "sum > 10" when rolling two dice: how many outcomes?

*(Answers: 36; {A,K,Q}; 6: (5,6),(6,5),(6,6),(4,… wait — (5,6),(6,5),(4,… let me recalculate: (5,6),(6,5),(6,6) if sum>11, or (3,…) — sums >10: 11,12 → (5,6),(6,5),(6,6) plus (4,… no. Sum=11: (5,6),(6,5). Sum=12: (6,6). Sum=10: excluded. So 3 outcomes)*
""",

"prob-set-ops": """\
# Set Operations

## Overview

Probability events are sets, and the fundamental operations — **union**, **intersection**, and **complement** — correspond to "or", "and", and "not". Mastering these is essential for computing probabilities of compound events.

## Key Idea

For events $A$ and $B$:
- **Union** $A \\cup B$: $A$ or $B$ (or both) occurs
- **Intersection** $A \\cap B$: both $A$ and $B$ occur
- **Complement** $A^c$: $A$ does not occur

De Morgan's laws: $(A \\cup B)^c = A^c \\cap B^c$ and $(A \\cap B)^c = A^c \\cup B^c$.

## Worked Examples

**Example 1: Roll a die. $A = \\{\\text{even}\\}$, $B = \\{\\text{>3}\\}$. Find $A \\cup B$ and $A \\cap B$.**

$A = \\{2,4,6\\}$, $B = \\{4,5,6\\}$. $A \\cup B = \\{2,4,5,6\\}$, $A \\cap B = \\{4,6\\}$.

---

**Example 2: $A^c$ when $A = \\{2,4,6\\}$ on a die**

$A^c = \\{1,3,5\\}$ (odd numbers).

---

**Example 3: De Morgan on $A \\cup B = \\{2,4,5,6\\}$**

$(A \\cup B)^c = \\{1,3\\} = \\{1,3,5\\} \\cap \\{1,2,3\\} = A^c \\cap B^c$ ✓

## Common Mistakes

- **Confusing $A \\cup B$ with $A \\cap B$.** Union is "or"; intersection is "and".
- **Forgetting that $P(A \\cup B) \\ne P(A) + P(B)$ when they overlap.**

## Quick Check

1. $A = \\{1,2\\}$, $B = \\{2,3\\}$. Find $A \\cup B$ and $A \\cap B$.
2. $A^c$ if $\\Omega = \\{1,2,3,4\\}$ and $A = \\{1,2\\}$?
3. $(A \\cap B)^c = ?$

*(Answers: $\\{1,2,3\\}$, $\\{2\\}$; $\\{3,4\\}$; $A^c \\cup B^c$)*
""",

"prob-axioms": """\
# Axioms of Probability

## Overview

The **Kolmogorov axioms** provide the mathematical foundation for probability. They define what it means for a function $P$ to be a valid probability measure, and all probability rules follow from them.

## Key Idea

The three axioms:
1. $P(A) \\ge 0$ for all events $A$
2. $P(\\Omega) = 1$
3. For mutually exclusive events $A_1, A_2, \\ldots$: $P(A_1 \\cup A_2 \\cup \\cdots) = \\sum P(A_i)$

From these: $P(\\emptyset) = 0$, $P(A^c) = 1 - P(A)$, and $P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$.

## Worked Examples

**Example 1: $P(A^c)$ when $P(A) = 0.3$**

$P(A^c) = 1 - 0.3 = 0.7$.

---

**Example 2: $P(A \\cup B)$ when $P(A) = 0.4$, $P(B) = 0.5$, $P(A \\cap B) = 0.2$**

$$P(A \\cup B) = 0.4 + 0.5 - 0.2 = 0.7$$

---

**Example 3: Verify axiom 3 for a die**

$P(\\text{odd or even}) = P(\\{1,3,5\\}) + P(\\{2,4,6\\}) = 1/2 + 1/2 = 1 = P(\\Omega)$ ✓

## Common Mistakes

- **Adding probabilities without checking mutual exclusivity.** Use inclusion-exclusion when events overlap.
- **Assigning negative probabilities.** Axiom 1 forbids this.

## Quick Check

1. $P(A) = 0.6$. Find $P(A^c)$.
2. $P(A) = 0.3$, $P(B) = 0.5$, disjoint. Find $P(A \\cup B)$.
3. Can $P(A) = 1.2$?

*(Answers: 0.4; 0.8; no)*
""",

"prob-inclusion-excl": """\
# Inclusion-Exclusion

## Overview

The **inclusion-exclusion principle** computes the probability of a union of events by alternately adding and subtracting intersection probabilities. It prevents double-counting overlapping events.

## Key Idea

$$P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$$

For three events:

$$P(A \\cup B \\cup C) = P(A) + P(B) + P(C) - P(A\\cap B) - P(A\\cap C) - P(B\\cap C) + P(A\\cap B\\cap C)$$

## Worked Examples

**Example 1: $P(A) = 0.5$, $P(B) = 0.4$, $P(A\\cap B) = 0.2$**

$$P(A \\cup B) = 0.5 + 0.4 - 0.2 = 0.7$$

---

**Example 2: What fraction of students passed math or science if 60% passed math, 50% science, 30% both?**

$$P(M \\cup S) = 0.6 + 0.5 - 0.3 = 0.8$$

---

**Example 3: Three events, all probabilities given**

$P(A)=P(B)=P(C)=0.4$, all pairwise intersections $= 0.1$, triple intersection $= 0.05$.

$P(A\\cup B\\cup C) = 1.2 - 0.3 + 0.05 = 0.95$.

## Common Mistakes

- **Forgetting to subtract pairwise intersections.** $P(A)+P(B)$ overcounts $P(A\\cap B)$.
- **Sign errors in the three-event formula** (triple intersection is added, not subtracted).

## Quick Check

1. $P(A)=0.6$, $P(B)=0.7$, $P(A\\cap B)=0.4$. Find $P(A\\cup B)$.
2. If $A$ and $B$ are mutually exclusive, what is $P(A\\cup B)$?
3. $P(A\\cup B\\cup C)$ if all three are mutually exclusive with probs 0.2, 0.3, 0.4.

*(Answers: 0.9; $P(A)+P(B)$; 0.9)*
""",

"prob-area-probability": """\
# Geometric Probability

## Overview

**Geometric probability** assigns probabilities proportional to length, area, or volume. It is used when outcomes form a continuous set (like a point chosen uniformly at random in a region).

## Key Idea

$$P(\\text{event}) = \\frac{\\text{measure of favorable region}}{\\text{measure of total region}}$$

The "measure" is length (1D), area (2D), or volume (3D).

## Worked Examples

**Example 1: A point is chosen uniformly in $[0, 10]$. Probability it falls in $[3, 7]$?**

$$P = \\frac{7-3}{10-0} = \\frac{4}{10} = 0.4$$

---

**Example 2: A point is chosen uniformly in the unit square. Probability it is inside the quarter-circle $x^2+y^2 \\le 1$?**

Area of quarter-circle: $\\pi/4$. Area of square: 1. $P = \\pi/4 \\approx 0.785$.

---

**Example 3: Two buses arrive uniformly at random in an hour. Probability they arrive within 15 minutes of each other?**

Total area: $60^2$. Favorable: region $|x-y| \\le 15$. $P = 1 - (45/60)^2 = 1 - 9/16 = 7/16$.

## Common Mistakes

- **Treating continuous outcomes as discrete.** A single point has probability 0 in a continuous distribution.
- **Computing ratio of lengths when areas are needed (2D problems).**

## Quick Check

1. Uniform on $[0,5]$. $P(X < 2)$?
2. Point in unit circle. $P(\\text{in unit square around origin})$?
3. If $P = \\pi/4$ approximates $\\pi$, what experiment estimates $\\pi$?

*(Answers: 2/5; $1/\\pi$ (sq. area 4, circle area $\\pi$); Monte Carlo dart throwing)*
""",

"prob-conditional": """\
# Conditional Probability

## Overview

**Conditional probability** $P(A|B)$ is the probability of $A$ given that $B$ has occurred. It updates probability based on new information by restricting the sample space to $B$.

## Key Idea

$$P(A|B) = \\frac{P(A \\cap B)}{P(B)} \\quad (P(B) > 0)$$

## Worked Examples

**Example 1: Roll a die. $P(\\text{even} | \\text{>3})$?**

$B = \\{4,5,6\\}$, $A \\cap B = \\{4,6\\}$. $P = (2/6)/(3/6) = 2/3$.

---

**Example 2: Deck of cards. $P(\\text{ace} | \\text{red})$?**

$P(\\text{ace} \\cap \\text{red}) = 2/52$. $P(\\text{red}) = 26/52$. $P = 2/26 = 1/13$.

---

**Example 3: From a table: $P(A \\cap B) = 0.3$, $P(B) = 0.6$. Find $P(A|B)$.**

$P(A|B) = 0.3/0.6 = 0.5$.

## Common Mistakes

- **Confusing $P(A|B)$ with $P(B|A)$.** These are generally different (Bayes' theorem relates them).
- **Applying conditional probability when $P(B) = 0$** — it's undefined.

## Quick Check

1. $P(B|A)$ if $P(A\\cap B) = 0.1$ and $P(A) = 0.4$.
2. Two cards drawn. $P(\\text{2nd is ace} | \\text{1st is ace})$?
3. $P(A|B)$ if $A$ and $B$ are mutually exclusive?

*(Answers: 0.25; 3/51; 0)*
""",

"prob-independence": """\
# Independence

## Overview

Events $A$ and $B$ are **independent** if knowing that $B$ occurred does not change the probability of $A$. Independence is a specific mathematical condition, not just intuitive lack of connection.

## Key Idea

$A$ and $B$ are independent iff:

$$P(A \\cap B) = P(A) \\cdot P(B)$$

Equivalently, $P(A|B) = P(A)$ (when $P(B) > 0$). For multiple events, pairwise independence does NOT imply mutual independence.

## Worked Examples

**Example 1: Flip two fair coins. Are "first is H" and "second is H" independent?**

$P(\\text{both H}) = 1/4 = (1/2)(1/2)$. Yes, independent.

---

**Example 2: Roll a die. $A = \\{\\text{even}\\}$, $B = \\{1,2,3,4\\}$. Independent?**

$P(A) = 1/2$, $P(B) = 2/3$, $P(A\\cap B) = P(\\{2,4\\}) = 1/3 = (1/2)(2/3)$. Yes.

---

**Example 3: $P(A) = 0.6$, $P(B) = 0.4$, $P(A\\cap B) = 0.3$. Independent?**

$P(A)P(B) = 0.24 \\ne 0.3$. Not independent.

## Common Mistakes

- **Confusing mutually exclusive with independent.** If $P(A),P(B)>0$, they can't be both mutually exclusive AND independent.
- **Assuming independence from context** without verification.

## Quick Check

1. $P(A)=0.3$, $P(B)=0.5$. If independent, $P(A\\cap B)$?
2. Are mutually exclusive events (with positive probability) independent?
3. $P(A\\cap B) = P(A)P(B)$ is the definition of what?

*(Answers: 0.15; no; independence)*
""",

"prob-total-prob": """\
# Law of Total Probability

## Overview

The **Law of Total Probability** computes $P(B)$ by partitioning the sample space into mutually exclusive events $A_1, \\ldots, A_n$ and summing conditional probabilities.

## Key Idea

If $A_1, \\ldots, A_n$ partition $\\Omega$ (mutually exclusive and exhaustive):

$$P(B) = \\sum_{i=1}^n P(B | A_i)\\, P(A_i)$$

## Worked Examples

**Example 1: Two boxes. Box 1 has 3 red, 2 blue. Box 2 has 1 red, 4 blue. Pick a box at random, then a ball. $P(\\text{red})$?**

$P(R|B_1) = 3/5$, $P(R|B_2) = 1/5$, $P(B_1) = P(B_2) = 1/2$.

$$P(R) = (3/5)(1/2) + (1/5)(1/2) = 3/10 + 1/10 = 2/5$$

---

**Example 2: Factory defects**

Machine A produces 60% of parts (1% defective). Machine B produces 40% (2% defective). $P(\\text{defective}) = 0.01(0.6) + 0.02(0.4) = 0.014$.

---

**Example 3: Weather model**

$P(\\text{rain}|\\text{cloudy}) = 0.7$, $P(\\text{rain}|\\text{clear}) = 0.1$. $P(\\text{cloudy}) = 0.4$. $P(\\text{rain}) = 0.7(0.4) + 0.1(0.6) = 0.34$.

## Common Mistakes

- **Partition not exhaustive or not mutually exclusive.** The $A_i$ must cover all cases exactly once.
- **Mixing up $P(B|A_i)$ and $P(A_i|B)$.**

## Quick Check

1. $P(A_1)=0.4$, $P(A_2)=0.6$, $P(B|A_1)=0.3$, $P(B|A_2)=0.7$. Find $P(B)$.
2. Is the law needed when all $A_i$ have equal probability?
3. How many terms if the partition has 3 events?

*(Answers: 0.54; yes (it still applies); 3)*
""",

"prob-bayes": """\
# Bayes' Theorem

## Overview

**Bayes' theorem** inverts conditional probability: it computes $P(A|B)$ from $P(B|A)$, $P(A)$, and $P(B)$. It is the foundation of Bayesian inference.

## Key Idea

$$P(A|B) = \\frac{P(B|A)\\, P(A)}{P(B)}$$

Combined with the law of total probability:

$$P(A_i | B) = \\frac{P(B|A_i)\\,P(A_i)}{\\sum_j P(B|A_j)\\,P(A_j)}$$

## Worked Examples

**Example 1: Medical test. Disease prevalence 1%. Test sensitivity 99%, specificity 95%. $P(\\text{disease}|\\text{positive})$?**

$P(+|D)=0.99$, $P(+|D^c)=0.05$, $P(D)=0.01$.

$P(+) = 0.99(0.01) + 0.05(0.99) = 0.0594$.

$$P(D|+) = \\frac{0.99 \\times 0.01}{0.0594} \\approx 0.167$$

---

**Example 2: Box problem (from Total Probability lesson)**

$P(B_1|\\text{red}) = \\frac{P(R|B_1)P(B_1)}{P(R)} = \\frac{(3/5)(1/2)}{2/5} = 3/4$.

---

**Example 3: Prior vs. posterior**

$P(A)$ is the **prior** (before observing $B$). $P(A|B)$ is the **posterior** (after). Bayes' theorem updates beliefs.

## Common Mistakes

- **Confusing $P(A|B)$ with $P(B|A)$.** The classic prosecutor's fallacy.
- **Using $P(+)$ without total probability.** Compute $P(B)$ in the denominator carefully.

## Quick Check

1. $P(A)=0.3$, $P(B|A)=0.8$, $P(B)=0.5$. Find $P(A|B)$.
2. What is the denominator in Bayes' theorem?
3. If $P(B|A) = P(B)$, what does that imply about $A$ and $B$?

*(Answers: 0.48; $P(B)$; they are independent)*
""",

"prob-discrete-rv": """\
# Discrete Random Variables

## Overview

A **discrete random variable** $X$ takes countable values, each with a certain probability. Its **probability mass function (PMF)** specifies $P(X = x)$ for each value $x$.

## Key Idea

The PMF $p(x) = P(X = x)$ must satisfy:
1. $p(x) \\ge 0$ for all $x$
2. $\\sum_x p(x) = 1$

The **CDF** is $F(x) = P(X \\le x) = \\sum_{t \\le x} p(t)$.

## Worked Examples

**Example 1: Roll a fair die. PMF?**

$p(k) = 1/6$ for $k = 1, 2, 3, 4, 5, 6$; $p(k) = 0$ otherwise.

---

**Example 2: $X$ has PMF $p(1)=0.2$, $p(2)=0.5$, $p(3)=0.3$. Find $P(X \\le 2)$.**

$F(2) = p(1) + p(2) = 0.7$.

---

**Example 3: Valid PMF?**

$p(0)=0.4$, $p(1)=0.3$, $p(2)=0.4$. Sum $= 1.1 \\ne 1$. Not valid.

## Common Mistakes

- **PMF summing to more or less than 1.** Always verify.
- **Confusing PMF and CDF.** PMF gives probability at a point; CDF gives cumulative probability.

## Quick Check

1. Valid PMF: $p(1)=p(2)=p(3)=1/3$?
2. For the die, $P(X \\le 3)$?
3. $F(2)$ vs. $p(2)$: what's the difference?

*(Answers: yes; 1/2; $F(2)$ is cumulative; $p(2)$ is just $P(X=2)$)*
""",

"prob-expected-value": """\
# Expected Value

## Overview

The **expected value** (mean) of a random variable $X$ is its probability-weighted average. It represents the long-run average if you repeated the experiment many times.

## Key Idea

For discrete $X$:

$$E[X] = \\sum_x x \\cdot P(X = x)$$

For continuous $X$ with density $f$:

$$E[X] = \\int_{-\\infty}^{\\infty} x\\, f(x)\\, dx$$

Linearity: $E[aX + b] = aE[X] + b$.

## Worked Examples

**Example 1: Fair die. $E[X]$?**

$$E[X] = \\frac{1}{6}(1+2+3+4+5+6) = 3.5$$

---

**Example 2: $X$ with $P(X=0)=0.5$, $P(X=2)=0.3$, $P(X=5)=0.2$**

$$E[X] = 0(0.5) + 2(0.3) + 5(0.2) = 1.6$$

---

**Example 3: $E[3X - 2]$ if $E[X] = 4$**

$$E[3X-2] = 3(4) - 2 = 10$$

## Common Mistakes

- **Interpreting $E[X]$ as the most likely value.** It's the average, not the mode.
- **Forgetting linearity.** $E[aX+b] = aE[X]+b$ always holds.

## Quick Check

1. $P(X=1)=0.6$, $P(X=4)=0.4$. Find $E[X]$.
2. $E[X]=3$. Find $E[2X+1]$.
3. Is $E[X]$ always a possible value of $X$?

*(Answers: 2.2; 7; no — e.g., die expected value 3.5)*
""",

"prob-indicators": """\
# Indicator Random Variables

## Overview

An **indicator random variable** $I_A$ equals 1 if event $A$ occurs and 0 otherwise. Despite their simplicity, indicator variables are a powerful tool for computing expectations of complex quantities.

## Key Idea

$$I_A = \\begin{cases}1 & \\text{if } A \\text{ occurs} \\\\ 0 & \\text{otherwise}\\end{cases}, \\quad E[I_A] = P(A)$$

The key trick: many complicated random variables can be written as sums of indicator variables, and linearity of expectation applies term-by-term.

## Worked Examples

**Example 1: Number of heads in $n$ flips**

$X = I_1 + \\cdots + I_n$. $E[X] = nP(H) = n/2$.

---

**Example 2: Expected number of matches when shuffling**

$X = \\sum_{i=1}^n I_i$ where $I_i = 1$ if card $i$ is in position $i$. $E[I_i] = 1/n$. $E[X] = n \\cdot (1/n) = 1$.

---

**Example 3: Expected number of pairs in a group of $n$ people with birthdays**

For each pair $(i,j)$, let $I_{ij} = 1$ if they share a birthday. $E[I_{ij}] = 1/365$.

Number of pairs = $\\binom{n}{2}$. Expected matches = $\\binom{n}{2}/365$.

## Common Mistakes

- **Using $E[I_A] = P(A)$ only when $I_A^2 = I_A$** (always true for indicators).
- **Assuming $I_A$ and $I_B$ are independent when $A$ and $B$ may not be.**

## Quick Check

1. $E[I_A]$ if $P(A) = 0.3$?
2. Roll three dice. Expected number showing a 6?
3. Is $I_A^2 = I_A$?

*(Answers: 0.3; 1/2; yes)*
""",

"prob-variance": """\
# Variance

## Overview

**Variance** measures the spread of a distribution around its mean. A large variance means values tend to be far from the mean; variance 0 means the variable is constant.

## Key Idea

$$\\text{Var}(X) = E[(X - \\mu)^2] = E[X^2] - (E[X])^2$$

Standard deviation $\\sigma = \\sqrt{\\text{Var}(X)}$.

For independent $X$ and $Y$: $\\text{Var}(aX + bY) = a^2\\text{Var}(X) + b^2\\text{Var}(Y)$.

## Worked Examples

**Example 1: Variance of a fair die**

$E[X]=3.5$, $E[X^2] = \\frac{1}{6}(1+4+9+16+25+36) = 91/6 \\approx 15.17$.

$\\text{Var}(X) = 91/6 - (3.5)^2 = 91/6 - 49/4 = 35/12 \\approx 2.92$.

---

**Example 2: $\\text{Var}(3X + 2)$ if $\\text{Var}(X) = 5$**

$\\text{Var}(3X+2) = 9\\text{Var}(X) = 45$. (Constants don't add variance.)

---

**Example 3: Bernoulli$(p)$ variance**

$E[X] = p$, $E[X^2] = p$ (since $X^2 = X$ for 0/1). $\\text{Var}(X) = p - p^2 = p(1-p)$.

## Common Mistakes

- **Adding variances for non-independent variables.** The formula $\\text{Var}(X+Y)=\\text{Var}(X)+\\text{Var}(Y)$ requires independence.
- **Confusing standard deviation with variance.** $\\text{SD} = \\sqrt{\\text{Var}}$.

## Quick Check

1. $E[X]=2$, $E[X^2]=8$. Find $\\text{Var}(X)$.
2. $\\text{Var}(5X)$ if $\\text{Var}(X)=4$?
3. Minimum possible variance?

*(Answers: 4; 100; 0 (constant variable))*
""",

"prob-bernoulli-binom": """\
# Bernoulli and Binomial Distributions

## Overview

A **Bernoulli** trial is a single experiment with two outcomes (success/failure) with probability $p$. The **Binomial distribution** counts successes in $n$ independent Bernoulli trials.

## Key Idea

$X \\sim \\text{Binomial}(n, p)$:

$$P(X = k) = \\binom{n}{k} p^k (1-p)^{n-k}, \\quad k = 0,1,\\ldots,n$$

$$E[X] = np, \\quad \\text{Var}(X) = np(1-p)$$

## Worked Examples

**Example 1: Flip a fair coin 5 times. $P(X = 3)$?**

$$\\binom{5}{3}(0.5)^3(0.5)^2 = 10 \\cdot (0.5)^5 = 10/32 = 5/16$$

---

**Example 2: 10 free throws, $p = 0.7$. Expected number made?**

$E[X] = 10(0.7) = 7$.

---

**Example 3: $P(X \\ge 1)$ for $\\text{Bin}(5, 0.2)$**

$P(X \\ge 1) = 1 - P(X=0) = 1 - (0.8)^5 = 1 - 0.328 = 0.672$.

## Common Mistakes

- **Forgetting the $\\binom{n}{k}$ factor.** Order matters for counting the arrangements.
- **Using Binomial when trials are not independent.** Sampling without replacement requires Hypergeometric.

## Quick Check

1. $P(X=0)$ for $\\text{Bin}(3, 0.5)$?
2. $E[X]$ for $\\text{Bin}(20, 0.3)$?
3. $\\text{Var}(X)$ for $\\text{Bin}(10, 0.4)$?

*(Answers: 1/8; 6; 2.4)*
""",

"prob-hypergeometric": """\
# Hypergeometric Distribution

## Overview

The **Hypergeometric distribution** counts successes when sampling **without replacement** from a finite population. It differs from Binomial in that trials are not independent.

## Key Idea

Population: $N$ items, $K$ successes. Draw $n$ without replacement. Number of successes $X$:

$$P(X = k) = \\frac{\\binom{K}{k}\\binom{N-K}{n-k}}{\\binom{N}{n}}$$

$$E[X] = \\frac{nK}{N}, \\quad \\text{Var}(X) = n\\frac{K}{N}\\frac{N-K}{N}\\frac{N-n}{N-1}$$

## Worked Examples

**Example 1: Deck of 52 cards, 13 hearts. Draw 5. $P(\\text{exactly 2 hearts})$?**

$$\\frac{\\binom{13}{2}\\binom{39}{3}}{\\binom{52}{5}} = \\frac{78 \\times 9139}{2598960} \\approx 0.274$$

---

**Example 2: Lot of 20 items, 4 defective. Inspect 5. Expected defects?**

$E[X] = 5 \\times 4/20 = 1$.

---

**Example 3: When does Hypergeometric ≈ Binomial?**

When $N$ is large relative to $n$ (say $n < 5\\%$ of $N$), sampling with vs. without replacement makes little difference.

## Common Mistakes

- **Using Binomial when sampling without replacement** from a small population.
- **Mixing up $K$, $N-K$, $n$, $k$** in the formula.

## Quick Check

1. $N=10$, $K=4$, $n=3$. $E[X]$?
2. When is $\\text{Bin}(n,K/N)$ a good approximation?
3. The variance-reducing factor $(N-n)/(N-1)$ is called what?

*(Answers: 1.2; when $N \\gg n$; finite population correction factor)*
""",

"prob-geometric-dist": """\
# Geometric Distribution

## Overview

The **Geometric distribution** counts the number of trials until the first success in a sequence of independent Bernoulli trials with success probability $p$.

## Key Idea

$X \\sim \\text{Geom}(p)$: number of trials until (and including) first success.

$$P(X = k) = (1-p)^{k-1} p, \\quad k = 1, 2, 3, \\ldots$$

$$E[X] = \\frac{1}{p}, \\quad \\text{Var}(X) = \\frac{1-p}{p^2}$$

## Worked Examples

**Example 1: Roll a die until a 6. $P(X = 3)$?**

$(5/6)^2(1/6) = 25/216 \\approx 0.116$.

---

**Example 2: Expected rolls to get a 6?**

$E[X] = 1/(1/6) = 6$.

---

**Example 3: $P(X > 3)$ for $p = 1/4$?**

Fail first 3 times: $(3/4)^3 = 27/64 \\approx 0.422$.

## Common Mistakes

- **Two versions of geometric exist.** $X$ = number of trials (starting from 1) vs. $X$ = number of failures before first success. Know which convention is used.
- **Thinking variance is $1/p^2$.** It's $(1-p)/p^2$.

## Quick Check

1. $P(X=1)$ for $\\text{Geom}(0.3)$?
2. $E[X]$ for $p=0.5$?
3. $P(X \\ge 2)$ for $p=0.4$?

*(Answers: 0.3; 2; 0.6)*
""",

"prob-poisson": """\
# Poisson Distribution

## Overview

The **Poisson distribution** models the number of rare events in a fixed time or space interval, when events occur independently at a constant average rate $\\lambda$.

## Key Idea

$X \\sim \\text{Poisson}(\\lambda)$:

$$P(X = k) = \\frac{e^{-\\lambda} \\lambda^k}{k!}, \\quad k = 0, 1, 2, \\ldots$$

$$E[X] = \\lambda, \\quad \\text{Var}(X) = \\lambda$$

The mean equals the variance — a hallmark of the Poisson.

## Worked Examples

**Example 1: On average 3 customers arrive per minute. $P(X = 5)$?**

$$P(X=5) = \\frac{e^{-3} 3^5}{5!} = \\frac{e^{-3} \\cdot 243}{120} \\approx 0.101$$

---

**Example 2: $P(X = 0)$ for $\\lambda = 2$?**

$e^{-2} \\approx 0.135$.

---

**Example 3: $P(X \\ge 1)$ for $\\lambda = 1$?**

$P(X \\ge 1) = 1 - P(X=0) = 1 - e^{-1} \\approx 0.632$.

## Common Mistakes

- **Using Poisson with a non-rare event.** It works when $n$ is large and $p$ is small.
- **Forgetting $k!$ in the denominator.**

## Quick Check

1. $P(X=0)$ for $\\text{Pois}(3)$?
2. $E[X]$ and $\\text{Var}(X)$ for $\\text{Pois}(5)$?
3. $P(X=2)$ for $\\lambda=1$?

*(Answers: $e^{-3}\\approx0.050$; both 5; $e^{-1}/2\\approx0.184$)*
""",

"prob-poisson-approx": """\
# Poisson Approximation to Binomial

## Overview

When $n$ is large and $p$ is small, the **Binomial$(n,p)$** distribution is well-approximated by **Poisson$( \\lambda = np)$**. This avoids computing large binomial coefficients.

## Key Idea

$\\text{Bin}(n,p) \\approx \\text{Pois}(np)$ when $n \\to \\infty$ and $p \\to 0$ with $np = \\lambda$ fixed.

Rule of thumb: use this approximation when $n \\ge 20$ and $p \\le 0.05$.

## Worked Examples

**Example 1: $n=100$, $p=0.02$. $P(X=3)$ via Poisson.**

$\\lambda = 2$. $P(X=3) = e^{-2}(2)^3/3! = 8e^{-2}/6 \\approx 0.180$.

---

**Example 2: Number of typos per page**

If a book has 500 characters per page and each has a 0.001 chance of being a typo, $\\lambda = 0.5$. $P(0 \\text{ typos}) = e^{-0.5} \\approx 0.607$.

---

**Example 3: Compare Binomial and Poisson for $n=50, p=0.02, k=2$**

Exact: $\\binom{50}{2}(0.02)^2(0.98)^{48} \\approx 0.184$. Poisson ($\\lambda=1$): $e^{-1}/2 \\approx 0.184$. Close!

## Common Mistakes

- **Using the approximation when $p$ is large.** If $p = 0.4$, use Binomial directly.
- **Forgetting $\\lambda = np$, not $n$ alone.**

## Quick Check

1. $n=200$, $p=0.01$. What is $\\lambda$?
2. $P(X=0)$ for the approximation above?
3. When is the approximation accurate?

*(Answers: 2; $e^{-2}\\approx0.135$; $n$ large, $p$ small, $np$ moderate)*
""",

"prob-continuous-rv": """\
# Continuous Random Variables

## Overview

A **continuous random variable** $X$ takes values on a continuum. Its distribution is specified by a **probability density function (PDF)** $f(x)$, where $P(a \\le X \\le b) = \\int_a^b f(x)\\,dx$.

## Key Idea

Properties of a valid PDF:
1. $f(x) \\ge 0$ for all $x$
2. $\\int_{-\\infty}^{\\infty} f(x)\\,dx = 1$

$P(X = c) = 0$ for any single point — continuous RVs have zero probability at individual values.

## Worked Examples

**Example 1: $f(x) = 2x$ on $[0,1]$. Verify it is a PDF.**

$\\int_0^1 2x\\,dx = [x^2]_0^1 = 1$ ✓. $f(x) \\ge 0$ on $[0,1]$ ✓.

---

**Example 2: $P(0.5 \\le X \\le 1)$ for $f(x) = 2x$**

$$\\int_{0.5}^1 2x\\,dx = [x^2]_{0.5}^1 = 1 - 0.25 = 0.75$$

---

**Example 3: CDF $F(x)$ for $f(x) = 2x$ on $[0,1]$**

$$F(x) = \\int_0^x 2t\\,dt = x^2 \\quad (0 \\le x \\le 1)$$

## Common Mistakes

- **Thinking $f(x) = P(X=x)$.** For continuous RVs, $P(X=x)=0$. The PDF is a density, not a probability.
- **$f(x)$ can exceed 1** (it's a density, not a probability).

## Quick Check

1. $f(x) = 3x^2$ on $[0,1]$. Is it a valid PDF?
2. Find $P(X \\le 0.5)$ for $f(x) = 2x$ on $[0,1]$.
3. What is $P(X = 0.7)$ for any continuous RV?

*(Answers: yes; 0.25; 0)*
""",

"prob-normal": """\
# Normal Distribution

## Overview

The **Normal (Gaussian) distribution** is the bell-shaped, symmetric distribution that appears throughout statistics due to the Central Limit Theorem. It is parameterized by mean $\\mu$ and variance $\\sigma^2$.

## Key Idea

$X \\sim N(\\mu, \\sigma^2)$ has PDF:

$$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$$

**Standardize:** $Z = (X - \\mu)/\\sigma \\sim N(0,1)$. Use $Z$-tables or software to find probabilities.

## Worked Examples

**Example 1: $X \\sim N(100, 225)$. $P(X < 112)$?**

$Z = (112-100)/15 = 0.8$. $P(Z < 0.8) \\approx 0.788$.

---

**Example 2: 68-95-99.7 rule**

$P(\\mu - \\sigma < X < \\mu + \\sigma) \\approx 0.68$. $P(|Z| < 2) \\approx 0.954$. $P(|Z| < 3) \\approx 0.997$.

---

**Example 3: $P(a < X < b)$**

$P(80 < X < 110) = P(-4/3 < Z < 2/3) \\approx P(Z < 0.67) - P(Z < -1.33) \\approx 0.749 - 0.092 = 0.657$.

## Common Mistakes

- **Forgetting to standardize before using the $Z$-table.**
- **Confusing $N(\\mu, \\sigma^2)$ with $N(\\mu, \\sigma)$.** Always check whether the second parameter is variance or SD.

## Quick Check

1. $Z$ for $x=75$ if $X \\sim N(80, 100)$?
2. $P(-1 < Z < 1) \\approx ?$
3. $P(X > \\mu)$ for any normal distribution?

*(Answers: $-0.5$; 0.68; 0.5)*
""",

"prob-exponential-dist": """\
# Exponential Distribution

## Overview

The **Exponential distribution** models the time between events in a Poisson process. It is the continuous analogue of the Geometric distribution and is widely used to model lifetimes and waiting times.

## Key Idea

$X \\sim \\text{Exp}(\\lambda)$ (rate parameter $\\lambda > 0$):

$$f(x) = \\lambda e^{-\\lambda x}, \\quad x \\ge 0, \\qquad F(x) = 1 - e^{-\\lambda x}$$

$$E[X] = \\frac{1}{\\lambda}, \\quad \\text{Var}(X) = \\frac{1}{\\lambda^2}$$

## Worked Examples

**Example 1: $\\lambda = 2$ (avg 0.5 units between events). $P(X > 1)$?**

$P(X > 1) = e^{-2} \\approx 0.135$.

---

**Example 2: Avg lifetime of a bulb is 1000 hours ($\\lambda = 0.001$). $P(X > 500)$?**

$P(X > 500) = e^{-0.5} \\approx 0.607$.

---

**Example 3: Median of $\\text{Exp}(\\lambda)$**

$F(m) = 1/2 \\Rightarrow 1 - e^{-\\lambda m} = 1/2 \\Rightarrow m = \\ln 2/\\lambda$.

## Common Mistakes

- **Confusing $\\lambda$ as rate vs. mean.** $\\lambda = 2$ means rate = 2 events per unit time, mean = 1/2.
- **Applying exponential to non-continuous or non-memoryless situations.**

## Quick Check

1. $E[X]$ for $\\text{Exp}(5)$?
2. $P(X > 2)$ for $\\text{Exp}(1)$?
3. $F(3)$ for $\\text{Exp}(2)$?

*(Answers: 1/5; $e^{-2}$; $1-e^{-6}$)*
""",

"prob-memoryless": """\
# Memoryless Property

## Overview

The **memoryless property** means the past doesn't affect the future: given that you've already waited time $s$, the remaining wait is distributed the same as starting fresh. Only the Exponential (continuous) and Geometric (discrete) distributions have this property.

## Key Idea

$P(X > s + t \\mid X > s) = P(X > t)$ for Exp$(\\lambda)$ and Geom$(p)$.

This follows directly from the CDF: $P(X > s+t) = e^{-\\lambda(s+t)} = e^{-\\lambda s} e^{-\\lambda t}$.

## Worked Examples

**Example 1: A component lasts $\\text{Exp}(0.1)$ years. It has survived 3 years. $P(\\text{surviving 2 more years})$?**

By memorylessness, this equals $P(X > 2) = e^{-0.2} \\approx 0.819$.

---

**Example 2: Conditional computation directly**

$P(X > 5 | X > 3) = \\frac{P(X>5)}{P(X>3)} = \\frac{e^{-5\\lambda}}{e^{-3\\lambda}} = e^{-2\\lambda} = P(X>2)$ ✓

---

**Example 3: Geometric has memoryless property**

Flip a coin until heads ($p = 0.4$). After 5 tails, $P(X > 8 | X > 5) = P(X > 3) = (0.6)^3$.

## Common Mistakes

- **Assuming all waiting-time distributions are memoryless.** Normal, Gamma, Weibull are not.
- **Confusing memoryless with "no aging" physically.** Mathematically, the surviving unit is statistically identical to a new one.

## Quick Check

1. $P(X > 4 | X > 2)$ for $\\text{Exp}(1)$?
2. Is the Normal distribution memoryless?
3. For Geom$(p)$, $P(X > m+n | X > m) = ?$

*(Answers: $e^{-2}$; no; $(1-p)^n = P(X > n)$)*
""",

"prob-gamma-dist": """\
# Gamma Distribution

## Overview

The **Gamma distribution** generalizes the Exponential: it models the waiting time until the $r$-th event in a Poisson process. It is also a flexible two-parameter family used for skewed positive data.

## Key Idea

$X \\sim \\text{Gamma}(r, \\lambda)$ (shape $r$, rate $\\lambda$):

$$f(x) = \\frac{\\lambda^r x^{r-1} e^{-\\lambda x}}{\\Gamma(r)}, \\quad x > 0$$

$$E[X] = \\frac{r}{\\lambda}, \\quad \\text{Var}(X) = \\frac{r}{\\lambda^2}$$

Gamma$(1, \\lambda) = $ Exp$(\\lambda)$. The sum of $r$ independent Exp$(\\lambda)$ variables is Gamma$(r, \\lambda)$.

## Worked Examples

**Example 1: $r=3$, $\\lambda=2$. Find $E[X]$ and $\\text{Var}(X)$.**

$E[X] = 3/2 = 1.5$. $\\text{Var}(X) = 3/4$.

---

**Example 2: Wait for 3rd customer (rate 2/hr). Expected wait?**

$E[X] = 3/2 = 1.5$ hours.

---

**Example 3: $\\Gamma(n/2, 1/2)$ is the chi-squared distribution $\\chi^2(n)$.**

This connection is used in statistical testing.

## Common Mistakes

- **Confusing shape and rate parameterizations.** Some texts use scale $\\theta = 1/\\lambda$ instead.
- **Thinking Gamma$(r,\\lambda)$ requires integer $r$.** $r$ can be any positive real number.

## Quick Check

1. What distribution is Gamma$(1, \\lambda)$?
2. $E[X]$ for Gamma$(4, 2)$?
3. Sum of 5 independent Exp$(3)$ variables has what distribution?

*(Answers: Exp($\\lambda$); 2; Gamma(5,3))*
""",

"prob-normal-approx": """\
# Normal Approximation

## Overview

The **Normal approximation** uses the Central Limit Theorem to approximate the distribution of a sum or mean by a Normal distribution. It is especially useful for the Binomial when $n$ is large.

## Key Idea

$X \\sim \\text{Bin}(n,p) \\approx N(np, np(1-p))$ when $np \\ge 5$ and $n(1-p) \\ge 5$.

**Continuity correction:** To improve accuracy, use $P(X \\le k) \\approx P\\!\\left(Z \\le \\frac{k + 0.5 - np}{\\sqrt{np(1-p)}}\\right)$.

## Worked Examples

**Example 1: $X \\sim \\text{Bin}(100, 0.4)$. Approximate $P(X \\le 35)$.**

$\\mu = 40$, $\\sigma = \\sqrt{24} \\approx 4.9$. $Z = (35.5-40)/4.9 \\approx -0.92$. $P(Z \\le -0.92) \\approx 0.179$.

---

**Example 2: Without continuity correction**

$Z = (35-40)/4.9 \\approx -1.02$. $P \\approx 0.154$ (less accurate).

---

**Example 3: Rule of thumb check**

$np = 40 \\ge 5$ and $n(1-p) = 60 \\ge 5$ ✓ — approximation is valid.

## Common Mistakes

- **Forgetting the continuity correction for discrete → continuous approximation.**
- **Using the approximation when $n$ is small or $p$ is near 0 or 1.**

## Quick Check

1. Is Normal approx appropriate for Bin(10, 0.5)?
2. $P(X \\le 50)$ with continuity correction for Bin$(100, 0.5)$?
3. $\\mu$ and $\\sigma$ for Bin$(200, 0.3)$?

*(Answers: borderline ($np=5$); $P(Z \\le 0.1)\\approx0.54$; $\\mu=60$, $\\sigma=\\sqrt{42}\\approx6.48$)*
""",

"prob-cdf-method": """\
# CDF Method

## Overview

The **CDF method** (also called the distribution function method) finds the distribution of a transformed variable $Y = g(X)$ by expressing the CDF of $Y$ in terms of the CDF of $X$, then differentiating to get the PDF.

## Key Idea

To find the distribution of $Y = g(X)$:
1. Write $F_Y(y) = P(Y \\le y) = P(g(X) \\le y)$
2. Express as $P(X \\in A)$ for some set $A$
3. Use $F_X$ to evaluate
4. Differentiate to get $f_Y(y)$

## Worked Examples

**Example 1: $X \\sim \\text{Uniform}(0,1)$. Find the distribution of $Y = X^2$.**

$F_Y(y) = P(X^2 \\le y) = P(X \\le \\sqrt{y}) = \\sqrt{y}$ for $0 \\le y \\le 1$.

$f_Y(y) = \\frac{1}{2\\sqrt{y}}$.

---

**Example 2: $X \\sim \\text{Exp}(1)$. Distribution of $Y = 2X$.**

$F_Y(y) = P(2X \\le y) = P(X \\le y/2) = 1 - e^{-y/2}$. So $Y \\sim \\text{Exp}(1/2)$.

---

**Example 3: $Y = |X|$ where $X \\sim N(0,1)$**

$F_Y(y) = P(|X| \\le y) = 2\\Phi(y) - 1$ for $y \\ge 0$. $f_Y(y) = 2\\phi(y)$ (half-normal).

## Common Mistakes

- **Forgetting to account for the support** of the new variable.
- **Not checking whether $g$ is monotone** before using the change-of-variable formula.

## Quick Check

1. $X \\sim U(0,1)$. CDF of $Y = \\sqrt{X}$?
2. $X \\sim \\text{Exp}(\\lambda)$. Distribution of $Y = aX$?
3. What is the CDF method used for?

*(Answers: $F_Y(y)=y^2$; Exp$(\\lambda/a)$; finding distributions of transformed random variables)*
""",

"prob-transformations": """\
# Transformations of Random Variables

## Overview

When you apply a function to a random variable, the **change-of-variables formula** gives the PDF of the result directly for monotone transformations — a shortcut vs. the full CDF method.

## Key Idea

If $Y = g(X)$ and $g$ is monotone and differentiable:

$$f_Y(y) = f_X(g^{-1}(y)) \\cdot \\left|\\frac{d}{dy}g^{-1}(y)\\right|$$

For multivariate: include the absolute Jacobian determinant.

## Worked Examples

**Example 1: $X \\sim \\text{Exp}(1)$. PDF of $Y = \\ln X$.**

$g^{-1}(y) = e^y$, $|dg^{-1}/dy| = e^y$. $f_Y(y) = f_X(e^y) \\cdot e^y = e^{-e^y} \\cdot e^y$ for $y \\in \\mathbb{R}$.

---

**Example 2: $X \\sim N(0,1)$. PDF of $Y = X^2$ (chi-squared with 1 df).**

$g^{-1}(y) = \\pm\\sqrt{y}$. For $y > 0$: $f_Y(y) = \\frac{1}{\\sqrt{2\\pi y}} e^{-y/2}$.

---

**Example 3: $X \\sim U(0,1)$. PDF of $Y = -\\ln X$.**

$g^{-1}(y) = e^{-y}$, $|d/dy| = e^{-y}$. $f_Y(y) = 1 \\cdot e^{-y} = e^{-y}$ — so $Y \\sim \\text{Exp}(1)$.

## Common Mistakes

- **Forgetting the absolute value of the derivative.** Sign errors change the PDF.
- **Using the formula for non-monotone $g$.** Split the domain or use the CDF method instead.

## Quick Check

1. What is the Jacobian for a 1D monotone transformation?
2. If $X \\sim U(0,1)$, what is the distribution of $-\\ln X$?
3. Why do we need $|dg^{-1}/dy|$?

*(Answers: $|dg^{-1}/dy|$; Exp(1); to account for stretching/squishing of the density)*
""",

"prob-inverse-cdf": """\
# Inverse CDF / Quantile Function

## Overview

The **quantile function** (inverse CDF) $F^{-1}(p)$ returns the value $x$ such that $P(X \\le x) = p$. It is used to find percentiles and to generate random samples from any distribution.

## Key Idea

$$F^{-1}(p) = \\inf\\{x : F(x) \\ge p\\}, \\quad 0 < p < 1$$

**Inverse CDF sampling:** If $U \\sim U(0,1)$, then $X = F^{-1}(U)$ has distribution $F$.

## Worked Examples

**Example 1: Median of $\\text{Exp}(\\lambda)$**

$F(m) = 0.5 \\Rightarrow 1 - e^{-\\lambda m} = 0.5 \\Rightarrow m = \\ln 2 / \\lambda$.

---

**Example 2: 90th percentile of $N(0,1)$**

$F^{-1}(0.9) = z_{0.9} \\approx 1.282$ (from $Z$-table).

---

**Example 3: Generate Exp(1) samples from Uniform**

$U \\sim U(0,1)$. $F^{-1}(u) = -\\ln(1-u)$. Compute $X = -\\ln(1-U)$ — this follows Exp(1).

## Common Mistakes

- **Confusing percentile with percentage.** The 90th percentile is a value $x$, not a probability.
- **Inverse CDF requires $F$ to be invertible.** For discrete distributions, use generalized inverse.

## Quick Check

1. Median of $U(0,1)$?
2. 25th percentile of $N(0,1)$?
3. What does $F^{-1}(0.5)$ always equal?

*(Answers: 0.5; $\\approx -0.674$; median)*
""",

"prob-joint-discrete": """\
# Joint Discrete Distributions

## Overview

The **joint distribution** of two discrete random variables $X$ and $Y$ specifies $P(X=x, Y=y)$ for all $(x,y)$ pairs. From it, you can recover marginal distributions, check independence, and compute joint expectations.

## Key Idea

Joint PMF: $p(x,y) = P(X=x, Y=y)$.

Marginals: $p_X(x) = \\sum_y p(x,y)$ and $p_Y(y) = \\sum_x p(x,y)$.

Independence: $X \\perp Y$ iff $p(x,y) = p_X(x)\\,p_Y(y)$ for all $(x,y)$.

## Worked Examples

**Example 1: Roll two dice. Joint PMF of $(X,Y)$.**

$P(X=i, Y=j) = 1/36$ for $i,j \\in \\{1,\\ldots,6\\}$. Independent and uniform.

---

**Example 2: Marginal of $X$ from the table below**

| $p(x,y)$ | $y=0$ | $y=1$ |
|---|---|---|
| $x=0$ | 0.1 | 0.2 |
| $x=1$ | 0.3 | 0.4 |

$p_X(0) = 0.3$, $p_X(1) = 0.7$.

---

**Example 3: Check independence**

$p_X(0)\\,p_Y(0) = 0.3 \\times 0.4 = 0.12 \\ne 0.1 = p(0,0)$. Not independent.

## Common Mistakes

- **Confusing joint PMF with conditional PMF.** $p(x|y) = p(x,y)/p_Y(y)$.
- **Forgetting to verify $\\sum_{x,y} p(x,y) = 1$.**

## Quick Check

1. How do you get $p_Y(y)$ from the joint PMF?
2. If $X \\perp Y$, how does the joint PMF factor?
3. Can $p(x,y) > p_X(x)$?

*(Answers: sum over all $x$; $p_X(x)p_Y(y)$; no)*
""",

"prob-joint-continuous": """\
# Joint Continuous Distributions

## Overview

The **joint density** $f(x,y)$ of two continuous random variables satisfies $P(X \\in A, Y \\in B) = \\iint_{A\\times B} f(x,y)\\,dx\\,dy$. Joint continuous distributions generalize everything from the discrete case.

## Key Idea

Valid joint PDF: $f(x,y) \\ge 0$ and $\\int\\int f(x,y)\\,dx\\,dy = 1$.

Marginals: $f_X(x) = \\int_{-\\infty}^{\\infty} f(x,y)\\,dy$ and $f_Y(y) = \\int_{-\\infty}^{\\infty} f(x,y)\\,dx$.

Independence: $f(x,y) = f_X(x)\\,f_Y(y)$.

## Worked Examples

**Example 1: $f(x,y) = 6xy^2$ on $0 \\le x \\le 1$, $0 \\le y \\le 1$. Valid PDF?**

$\\int_0^1\\int_0^1 6xy^2\\,dy\\,dx = 6 \\cdot (1/2)(1/3) = 1$ ✓.

---

**Example 2: Find the marginal $f_X(x)$ for Example 1.**

$f_X(x) = \\int_0^1 6xy^2\\,dy = 6x(1/3) = 2x$.

---

**Example 3: $P(X > Y)$ for $f(x,y) = 2$ on $0<y<x<1$.**

$\\int_0^1\\int_0^x 2\\,dy\\,dx = \\int_0^1 2x\\,dx = 1$.

## Common Mistakes

- **Integrating over the wrong region when the joint PDF has a triangular or non-rectangular support.**
- **Forgetting to find the correct marginal limits.**

## Quick Check

1. $\\int\\int f(x,y)\\,dx\\,dy = ?$ for a valid PDF?
2. If $f(x,y) = f_X(x)f_Y(y)$, are $X$ and $Y$ independent?
3. $f_Y(y)$ for $f(x,y) = 6xy^2$ on $[0,1]^2$?

*(Answers: 1; yes; $3y^2$)*
""",

"prob-marginal": """\
# Marginal Distributions

## Overview

The **marginal distribution** of one variable is obtained by integrating (or summing) the joint distribution over all values of the other variable. It tells you about one variable without conditioning on the other.

## Key Idea

From joint distribution $f(x,y)$ or $p(x,y)$:

$$f_X(x) = \\int_{-\\infty}^{\\infty} f(x,y)\\,dy \\quad \\text{(continuous)}$$

$$p_X(x) = \\sum_y p(x,y) \\quad \\text{(discrete)}$$

## Worked Examples

**Example 1: From joint table**

| | $Y=0$ | $Y=1$ |
|---|---|---|
|$X=0$| 0.2 | 0.1 |
|$X=1$| 0.3 | 0.4 |

$p_X(0) = 0.3$, $p_X(1) = 0.7$, $p_Y(0) = 0.5$, $p_Y(1) = 0.5$.

---

**Example 2: Marginal of $X \\sim N(\\mu_X, \\sigma_X^2)$ from bivariate normal**

The marginal of a bivariate normal is univariate normal. You "integrate out" $y$.

---

**Example 3: Marginal from $f(x,y) = e^{-(x+y)}$ on $x,y > 0$**

$f_X(x) = \\int_0^\\infty e^{-(x+y)}\\,dy = e^{-x}$ — so $X \\sim \\text{Exp}(1)$.

## Common Mistakes

- **Confusing marginal with conditional.** Marginal integrates out $y$; conditional fixes $y$.
- **Wrong integration limits** when support is not the full plane.

## Quick Check

1. How do you get the marginal PMF $p_X(x)$?
2. $f_Y(y)$ for $f(x,y) = e^{-(x+y)}$ on $x,y>0$?
3. If $X$ and $Y$ are independent, do the marginals determine the joint?

*(Answers: sum over all $y$; $e^{-y}$; yes, $f(x,y)=f_Xf_Y$)*
""",

"prob-conditional-dist": """\
# Conditional Distributions

## Overview

The **conditional distribution** of $Y$ given $X = x$ describes how $Y$ behaves when you know $X$. It is computed by dividing the joint by the marginal.

## Key Idea

$$f_{Y|X}(y|x) = \\frac{f(x,y)}{f_X(x)}, \\quad f_X(x) > 0$$

The conditional expectation $E[Y|X=x] = \\int y\\, f_{Y|X}(y|x)\\,dy$ is a function of $x$.

## Worked Examples

**Example 1: $f(x,y) = 6xy^2$ on $[0,1]^2$. Find $f_{Y|X}(y|x)$.**

$f_X(x) = 2x$. $f_{Y|X}(y|x) = \\frac{6xy^2}{2x} = 3y^2$ — uniform in $y$ regardless of $x$.

---

**Example 2: $E[Y|X=x]$ for Example 1**

$E[Y|X=x] = \\int_0^1 y \\cdot 3y^2\\,dy = 3/4$.

---

**Example 3: Discrete case**

$P(Y=1|X=0) = p(0,1)/p_X(0) = 0.1/0.3 = 1/3$.

## Common Mistakes

- **Forgetting to normalize** by the marginal.
- **Treating conditional distribution as the same as the marginal** when variables are not independent.

## Quick Check

1. $f_{Y|X}(y|x)$ vs. $f_Y(y)$: when are they equal?
2. $P(Y=0|X=1)$ from Example 1 table in marginal lesson?
3. $E[Y|X=x]$ is a function of what?

*(Answers: when $X \\perp Y$; $0.3/0.7\\approx0.43$; $x$)*
""",

"prob-covariance": """\
# Covariance and Variance of Sums

## Overview

**Covariance** measures the linear relationship between two random variables. If $X$ tends to be large when $Y$ is large, $\\text{Cov}(X,Y) > 0$. Covariance is essential for computing the variance of sums.

## Key Idea

$$\\text{Cov}(X,Y) = E[(X-\\mu_X)(Y-\\mu_Y)] = E[XY] - E[X]E[Y]$$

$$\\text{Var}(X + Y) = \\text{Var}(X) + \\text{Var}(Y) + 2\\text{Cov}(X,Y)$$

If $X \\perp Y$: $\\text{Cov}(X,Y) = 0$ and $\\text{Var}(X+Y) = \\text{Var}(X) + \\text{Var}(Y)$.

## Worked Examples

**Example 1: $E[XY] = 10$, $E[X] = 2$, $E[Y] = 4$. Find $\\text{Cov}(X,Y)$.**

$\\text{Cov} = 10 - 8 = 2$.

---

**Example 2: $\\text{Var}(X+Y)$ if $\\text{Var}(X)=4$, $\\text{Var}(Y)=9$, $\\text{Cov}(X,Y)=3$**

$\\text{Var}(X+Y) = 4 + 9 + 6 = 19$.

---

**Example 3: Correlation**

$\\text{Corr}(X,Y) = \\frac{\\text{Cov}(X,Y)}{\\sigma_X \\sigma_Y} \\in [-1,1]$.

## Common Mistakes

- **Assuming $\\text{Cov}=0$ implies independence.** Zero covariance does not imply independence in general.
- **Wrong sign when $X$ and $Y$ tend to go in opposite directions.**

## Quick Check

1. $\\text{Cov}(X,X) = ?$
2. $\\text{Var}(X-Y)$ in terms of Var and Cov?
3. If $X \\perp Y$, what is $\\text{Cov}(X,Y)$?

*(Answers: $\\text{Var}(X)$; $\\text{Var}(X)+\\text{Var}(Y)-2\\text{Cov}(X,Y)$; 0)*
""",

"prob-conditional-expect": """\
# Conditional Expectation

## Overview

**Conditional expectation** $E[Y|X]$ is a random variable (a function of $X$) that gives the expected value of $Y$ given the value of $X$. It is central to prediction and the tower property.

## Key Idea

$$E[Y|X=x] = \\int y\\, f_{Y|X}(y|x)\\,dy \\quad \\text{(or sum for discrete)}$$

**Tower property (Law of Total Expectation):** $E[Y] = E[E[Y|X]]$.

**Law of Total Variance:** $\\text{Var}(Y) = E[\\text{Var}(Y|X)] + \\text{Var}(E[Y|X])$.

## Worked Examples

**Example 1: $Y|X=x \\sim N(x, 1)$, $X \\sim N(0,1)$. Find $E[Y]$.**

$E[Y] = E[E[Y|X]] = E[X] = 0$.

---

**Example 2: $N$ is random, $X_1, \\ldots, X_N$ iid with mean $\\mu$. $E[S_N]$ where $S_N = \\sum_{i=1}^N X_i$.**

$E[S_N|N=n] = n\\mu$. By tower: $E[S_N] = E[N\\mu] = \\mu E[N]$.

---

**Example 3: Eve's law (Law of Total Variance)**

$\\text{Var}(Y) = E[\\text{Var}(Y|X)] + \\text{Var}(E[Y|X])$.

## Common Mistakes

- **Treating $E[Y|X]$ as a number.** It is a random variable (function of $X$).
- **Using $E[Y|X=x]$ when you need $E[Y|X]$.** The former is a number; the latter is a RV.

## Quick Check

1. $E[E[Y|X]] = ?$
2. $E[Y|X=x] = 2x + 3$. If $E[X] = 1$, find $E[Y]$.
3. Var$(Y) \\ge$ Var$(E[Y|X])$?

*(Answers: $E[Y]$; 5; yes)*
""",

"prob-bivariate-normal": """\
# Bivariate Normal Distribution

## Overview

The **bivariate normal distribution** is the joint normal distribution of two random variables $(X,Y)$. It is fully characterized by the means, variances, and correlation $\\rho$ of $X$ and $Y$.

## Key Idea

$(X,Y) \\sim N_2(\\mu_X, \\mu_Y, \\sigma_X^2, \\sigma_Y^2, \\rho)$.

Key facts:
- Marginals: $X \\sim N(\\mu_X, \\sigma_X^2)$, $Y \\sim N(\\mu_Y, \\sigma_Y^2)$
- Conditional: $Y|X=x \\sim N\\!\\left(\\mu_Y + \\rho\\frac{\\sigma_Y}{\\sigma_X}(x-\\mu_X),\\; \\sigma_Y^2(1-\\rho^2)\\right)$
- $X \\perp Y \\iff \\rho = 0$ (unique to the normal family!)

## Worked Examples

**Example 1: $X, Y$ bivariate normal with $\\rho = 0$. Are they independent?**

Yes — for bivariate normals, zero correlation implies independence.

---

**Example 2: $X \\sim N(0,1)$, $Y \\sim N(0,1)$, $\\rho = 0.8$. $E[Y|X=2]$?**

$E[Y|X=2] = 0 + 0.8(1/1)(2-0) = 1.6$.

---

**Example 3: Conditional variance**

$\\text{Var}(Y|X=2) = 1(1 - 0.64) = 0.36$.

## Common Mistakes

- **Assuming zero correlation implies independence in general.** This only holds for the normal family.
- **Confusing the conditional distribution's mean and variance with the unconditional ones.**

## Quick Check

1. $(X,Y)$ bivariate normal with $\\rho=0$. Are they independent?
2. Marginal of $X$ from bivariate normal?
3. $\\text{Var}(Y|X=x)$ depends on $x$?

*(Answers: yes; $N(\\mu_X,\\sigma_X^2)$; no — it's constant $\\sigma_Y^2(1-\\rho^2)$)*
""",

"prob-mgf": """\
# Moment Generating Functions

## Overview

The **moment generating function (MGF)** of a random variable $X$ uniquely characterizes its distribution and provides a convenient way to compute all moments. It is used to prove convergence results and derive distributions of sums.

## Key Idea

$$M_X(t) = E[e^{tX}] = \\sum_x e^{tx} p(x) \\quad \\text{or} \\quad \\int e^{tx} f(x)\\,dx$$

The $n$-th moment: $E[X^n] = M_X^{(n)}(0)$.

If $X \\perp Y$: $M_{X+Y}(t) = M_X(t)\\,M_Y(t)$.

## Worked Examples

**Example 1: MGF of Bernoulli$(p)$**

$M(t) = (1-p) + pe^t$.

---

**Example 2: MGF of $N(0,1)$**

$M(t) = e^{t^2/2}$. In general, $N(\\mu,\\sigma^2)$ has MGF $e^{\\mu t + \\sigma^2 t^2/2}$.

---

**Example 3: Sum of independent normals via MGF**

$M_{X+Y}(t) = e^{\\mu_1 t + \\sigma_1^2 t^2/2} \\cdot e^{\\mu_2 t + \\sigma_2^2 t^2/2} = e^{(\\mu_1+\\mu_2)t + (\\sigma_1^2+\\sigma_2^2)t^2/2}$, which is the MGF of $N(\\mu_1+\\mu_2, \\sigma_1^2+\\sigma_2^2)$.

## Common Mistakes

- **Differentiating $M(t)$ without evaluating at $t=0$.** The $n$-th moment requires $M^{(n)}(0)$.
- **MGF may not exist for all distributions** (e.g., Cauchy has no MGF).

## Quick Check

1. $E[X] = M'(0)$ — where is this evaluated?
2. MGF of Poisson$(\\lambda)$?
3. Sum of independent Exp$(1)$ variables: what is its distribution? (use MGFs)

*(Answers: at $t=0$; $e^{\\lambda(e^t-1)}$; Gamma$(n,1)$)*
""",

"prob-poisson-process": """\
# Poisson Process

## Overview

A **Poisson process** models a sequence of events occurring randomly in time (or space), with a constant average rate $\\lambda$ and independent increments. It connects the Poisson, Exponential, and Gamma distributions.

## Key Idea

$N(t)$ = number of events in $[0,t]$, $N(t) \\sim \\text{Poisson}(\\lambda t)$.

Inter-arrival times $T_1, T_2, \\ldots \\overset{iid}{\\sim} \\text{Exp}(\\lambda)$.

Time to $n$-th event: $S_n = T_1 + \\cdots + T_n \\sim \\text{Gamma}(n, \\lambda)$.

## Worked Examples

**Example 1: Customers arrive at rate 3/hour. $P(\\text{exactly 5 arrive in 2 hours})$?**

$\\lambda t = 6$. $P(N=5) = e^{-6}6^5/5! \\approx 0.161$.

---

**Example 2: Expected inter-arrival time?**

$E[T_i] = 1/3$ hour.

---

**Example 3: $P(\\text{wait more than 1 hour for 1st customer})$?**

$P(T_1 > 1) = e^{-3} \\approx 0.050$.

## Common Mistakes

- **Confusing the rate and the mean.** Rate $\\lambda = 3$/hr means mean inter-arrival time $= 1/3$ hr.
- **Adding rates for two independent Poisson processes.** The merged process has rate $\\lambda_1 + \\lambda_2$.

## Quick Check

1. $N(t) \\sim ?$ for Poisson process with rate $\\lambda$?
2. Inter-arrival times follow what distribution?
3. Time to $k$-th event follows what distribution?

*(Answers: Poisson($\\lambda t$); Exp($\\lambda$); Gamma($k,\\lambda$))*
""",

"prob-order-stats": """\
# Order Statistics

## Overview

Given $n$ iid random variables, the **order statistics** $X_{(1)} \\le X_{(2)} \\le \\cdots \\le X_{(n)}$ are the values sorted in ascending order. $X_{(1)}$ is the minimum and $X_{(n)}$ is the maximum.

## Key Idea

PDF of the $k$-th order statistic $X_{(k)}$ (from iid $X_i$ with CDF $F$ and PDF $f$):

$$f_{(k)}(x) = \\frac{n!}{(k-1)!(n-k)!} [F(x)]^{k-1}[1-F(x)]^{n-k} f(x)$$

For minimum: $F_{(1)}(x) = 1 - [1-F(x)]^n$.

For maximum: $F_{(n)}(x) = [F(x)]^n$.

## Worked Examples

**Example 1: CDF of maximum of $n$ iid $U(0,1)$**

$F_{(n)}(x) = x^n$ for $x \\in [0,1]$. $f_{(n)}(x) = nx^{n-1}$.

---

**Example 2: CDF of minimum**

$F_{(1)}(x) = 1 - (1-x)^n$. $f_{(1)}(x) = n(1-x)^{n-1}$.

---

**Example 3: Expected maximum of $n = 2$ iid $U(0,1)$**

$E[X_{(2)}] = \\int_0^1 x \\cdot 2x\\,dx = 2/3$.

## Common Mistakes

- **Using the marginal PDF of $X_i$ for $X_{(k)}$.** Order statistics have different PDFs.
- **Forgetting the multinomial coefficient** in the general $k$-th order statistic formula.

## Quick Check

1. $F_{X_{(n)}}(x)$ for $n$ iid variables with CDF $F$?
2. $E[\\min(X_1,X_2)]$ for iid $U(0,1)$?
3. What is $X_{(1)}$ called?

*(Answers: $[F(x)]^n$; 1/3; the minimum (first order statistic))*
""",

"prob-lln": """\
# Law of Large Numbers

## Overview

The **Law of Large Numbers (LLN)** guarantees that the sample mean $\\bar{X}_n$ converges to the population mean $\\mu$ as $n \\to \\infty$. It justifies using averages to estimate expected values.

## Key Idea

Let $X_1, X_2, \\ldots$ be iid with $E[X_i] = \\mu$. Then $\\bar{X}_n = \\frac{1}{n}\\sum_{i=1}^n X_i \\to \\mu$.

- **Weak LLN:** $\\bar{X}_n \\xrightarrow{P} \\mu$ (convergence in probability)
- **Strong LLN:** $\\bar{X}_n \\to \\mu$ almost surely

## Worked Examples

**Example 1: Coin flip. $\\bar{X}_n$ for $X_i \\in \\{0,1\\}$ with $p=0.5$.**

$E[X] = 0.5$. By LLN, the proportion of heads approaches 0.5 as $n \\to \\infty$.

---

**Example 2: Gambling fallacy**

After 10 tails, it is tempting to think "heads is due." LLN says the long-run frequency goes to 0.5, but individual future flips are still fair.

---

**Example 3: Monte Carlo integration**

$E[g(X)] \\approx \\frac{1}{n}\\sum_{i=1}^n g(X_i)$. By LLN, this converges to the true integral.

## Common Mistakes

- **Gambler's fallacy.** LLN says the average converges, not that individual outcomes "correct" themselves.
- **Applying LLN when variables are not iid.** Some conditions on dependence are needed.

## Quick Check

1. What does $\\bar{X}_n \\xrightarrow{P} \\mu$ mean?
2. Does LLN say $\\bar{X}_{100}$ will be exactly $\\mu$?
3. What distribution assumption does the Weak LLN require?

*(Answers: $P(|\\bar{X}_n - \\mu| > \\epsilon) \\to 0$; no, approximately; finite mean)*
""",

"prob-clt": """\
# Central Limit Theorem

## Overview

The **Central Limit Theorem (CLT)** says that the standardized sum of iid random variables with finite variance converges in distribution to a standard normal, regardless of the original distribution. It is one of the most important results in probability.

## Key Idea

$X_1, \\ldots, X_n$ iid with mean $\\mu$, variance $\\sigma^2 < \\infty$. Then:

$$\\frac{\\sqrt{n}(\\bar{X}_n - \\mu)}{\\sigma} \\xrightarrow{d} N(0,1) \\quad \\text{as } n \\to \\infty$$

Equivalently: $\\bar{X}_n \\approx N(\\mu, \\sigma^2/n)$ for large $n$.

## Worked Examples

**Example 1: $X_i \\sim U(0,1)$. Approximate distribution of $\\bar{X}_{50}$.**

$\\mu = 0.5$, $\\sigma^2 = 1/12$. $\\bar{X}_{50} \\approx N(0.5, 1/600)$.

---

**Example 2: $P(\\bar{X}_{100} > 55)$ for iid Exp$(0.01)$ ($\\mu=100, \\sigma=100$)**

$\\bar{X}_{100} \\approx N(100, 100)$. $Z = (55-100)/10 = -4.5$... (wait, $P(\\bar{X}>55)$ — $Z=(55-100)/10=-4.5$, so $P\\approx 1$). Actually $P(\\bar{X}>105) = P(Z>0.5) \\approx 0.31$.

---

**Example 3: How large must $n$ be?**

For many distributions, $n \\ge 30$ is a common rule of thumb. For highly skewed distributions, larger $n$ may be needed.

## Common Mistakes

- **Applying CLT for very small $n$ or very skewed distributions.** The approximation quality depends on $n$ and the distribution.
- **Forgetting to standardize properly** — divide by $\\sigma/\\sqrt{n}$, not $\\sigma$.

## Quick Check

1. $\\bar{X}_n \\approx N(?,?)$ for large $n$?
2. Why does the CLT matter for statistics?
3. Does CLT require the original distribution to be normal?

*(Answers: $N(\\mu, \\sigma^2/n)$; it justifies normal-based inference; no)*
""",


# ── Statistics ─────────────────────────────────────────────────────────────────
"stat-sampling-dist": """\
# Sampling Distributions

## Overview

The **sampling distribution** of a statistic is the distribution of that statistic over all possible samples of size $n$ from a population. It describes how the statistic varies from sample to sample.

## Key Idea

For iid $X_1,\\ldots,X_n$ with mean $\\mu$ and variance $\\sigma^2$:

$$E[\\bar{X}] = \\mu, \\quad \\text{Var}(\\bar{X}) = \\frac{\\sigma^2}{n}, \\quad \\text{SE}(\\bar{X}) = \\frac{\\sigma}{\\sqrt{n}}$$

By the CLT, $\\bar{X} \\approx N(\\mu, \\sigma^2/n)$ for large $n$.

## Worked Examples

**Example 1: $X_i \\sim N(10, 4)$, $n=25$. Distribution of $\\bar{X}$?**

$\\bar{X} \\sim N(10, 4/25) = N(10, 0.16)$.

---

**Example 2: $P(\\bar{X} > 10.5)$ from Example 1**

$Z = (10.5 - 10)/0.4 = 1.25$. $P(Z > 1.25) \\approx 0.106$.

---

**Example 3: Effect of sample size**

Doubling $n$ reduces $\\text{SE}$ by factor $\\sqrt{2}$, not 2. Precision grows slowly.

## Common Mistakes

- **Confusing the population SD with the SE.** $\\text{SE} = \\sigma/\\sqrt{n}$ depends on $n$.
- **Using the sampling distribution of $X_i$ instead of $\\bar{X}$** when asked about the sample mean.

## Quick Check

1. $\\text{SE}$ for $n=100$, $\\sigma=20$?
2. $E[\\bar{X}]$ always equals what?
3. As $n \\to \\infty$, what happens to $\\text{Var}(\\bar{X})$?

*(Answers: 2; $\\mu$; → 0)*
""",

"stat-estimator-props": """\
# Properties of Estimators

## Overview

An **estimator** $\\hat{\\theta}$ is a statistic used to estimate a population parameter $\\theta$. Good estimators are unbiased, consistent, and efficient. These properties determine how reliable an estimator is.

## Key Idea

- **Unbiased:** $E[\\hat{\\theta}] = \\theta$
- **Consistent:** $\\hat{\\theta} \\xrightarrow{P} \\theta$ as $n \\to \\infty$
- **Efficient:** minimum variance among all unbiased estimators (MVUE)

**MSE:** $\\text{MSE}(\\hat{\\theta}) = \\text{Var}(\\hat{\\theta}) + [\\text{Bias}(\\hat{\\theta})]^2$

## Worked Examples

**Example 1: Is $\\bar{X}$ unbiased for $\\mu$?**

$E[\\bar{X}] = \\mu$ ✓ — unbiased.

---

**Example 2: Biased estimator of $\\sigma^2$**

$\\hat{\\sigma}^2 = \\frac{1}{n}\\sum(X_i - \\bar{X})^2$ has $E[\\hat{\\sigma}^2] = \\frac{n-1}{n}\\sigma^2$ — biased. The unbiased version uses $n-1$ in the denominator.

---

**Example 3: MSE tradeoff**

A biased estimator with smaller variance can have smaller MSE than an unbiased one. Bias-variance tradeoff is fundamental.

## Common Mistakes

- **Assuming unbiased = best.** An unbiased estimator can have high variance.
- **Confusing bias and MSE.** MSE combines both bias and variance.

## Quick Check

1. $E[\\hat{\\theta}] = \\theta + 2$. What is the bias?
2. Does $S^2 = \\frac{1}{n-1}\\sum(X_i-\\bar{X})^2$ overestimate or underestimate $\\sigma^2$?
3. MSE formula in terms of bias and variance?

*(Answers: 2; neither (unbiased); Var + Bias²)*
""",

"stat-survey-srs": """\
# Simple Random Sampling

## Overview

**Simple random sampling (SRS)** is the most basic probability sampling method: every sample of size $n$ from a population of size $N$ has an equal chance of being selected. It is the benchmark for all other sampling designs.

## Key Idea

Under SRS without replacement: $E[\\bar{x}] = \\mu$, and the variance includes a **finite population correction (FPC)**:

$$\\text{Var}(\\bar{x}) = \\frac{\\sigma^2}{n} \\cdot \\frac{N-n}{N-1}$$

When $n/N < 5\\%$, the FPC $\\approx 1$ and you can ignore it.

## Worked Examples

**Example 1: Population of 1000, $\\sigma=10$. SRS of $n=50$. SE?**

FPC $= \\sqrt{(1000-50)/999} \\approx 0.975$. $\\text{SE} = (10/\\sqrt{50}) \\times 0.975 \\approx 1.38$.

---

**Example 2: When is FPC negligible?**

$n/N = 50/1000 = 5\\%$ — borderline. If $n/N < 5\\%$, skip FPC.

---

**Example 3: Sampling frame vs. sample**

The **sampling frame** is the list from which you draw. Bias occurs when the frame misses parts of the population.

## Common Mistakes

- **Using SRS when systematic bias exists** (e.g., convenience sampling is not SRS).
- **Ignoring FPC for large sampling fractions.**

## Quick Check

1. Every sample of size $n$ has equal probability in SRS — true?
2. FPC for $n=100$, $N=200$?
3. What is the sampling frame?

*(Answers: yes; $\\sqrt{100/199}\\approx0.708$; list of units from which sample is drawn)*
""",

"stat-mom": """\
# Method of Moments

## Overview

The **Method of Moments (MOM)** estimates parameters by equating population moments (expressed in terms of parameters) to sample moments. It is simple and often provides consistent estimators.

## Key Idea

Set the $k$-th population moment $\\mu_k' = E[X^k]$ equal to the sample moment $m_k' = \\frac{1}{n}\\sum X_i^k$, and solve for the parameters.

## Worked Examples

**Example 1: MOM estimator of $\\lambda$ for Poisson$(\\lambda)$**

$E[X] = \\lambda$. Set $\\lambda = \\bar{X}$. So $\\hat{\\lambda}_{MOM} = \\bar{X}$.

---

**Example 2: MOM for Normal$(\\mu, \\sigma^2)$**

First moment: $\\hat{\\mu} = \\bar{X}$.

Second central moment: $\\hat{\\sigma}^2 = \\frac{1}{n}\\sum(X_i - \\bar{X})^2$.

---

**Example 3: MOM for Uniform$(0, \\theta)$**

$E[X] = \\theta/2$. Set $\\bar{X} = \\hat{\\theta}/2$. So $\\hat{\\theta} = 2\\bar{X}$.

## Common Mistakes

- **MOM estimators can be outside the parameter space.** For example, $2\\bar{X}$ could be less than the observed maximum.
- **MOM may not be efficient** — it doesn't always minimize MSE.

## Quick Check

1. MOM estimator of $p$ for Bernoulli$(p)$?
2. MOM for Exp$(\\lambda)$?
3. MOM requires solving what kind of equations?

*(Answers: $\\bar{X}$; $\\hat{\\lambda}=1/\\bar{X}$; setting population moments equal to sample moments)*
""",

"stat-mle-univariate": """\
# MLE: Univariate

## Overview

**Maximum Likelihood Estimation (MLE)** finds the parameter value that makes the observed data most probable. It is the most widely used estimation method, with strong theoretical properties.

## Key Idea

The **likelihood** is $L(\\theta) = \\prod_{i=1}^n f(x_i;\\theta)$. Maximize $\\ell(\\theta) = \\log L(\\theta)$ (the log-likelihood) by solving $\\frac{d\\ell}{d\\theta} = 0$.

## Worked Examples

**Example 1: MLE of $\\lambda$ for Poisson$(\\lambda)$**

$\\ell(\\lambda) = \\sum x_i \\ln\\lambda - n\\lambda$. Setting $d\\ell/d\\lambda = \\sum x_i/\\lambda - n = 0$ gives $\\hat{\\lambda} = \\bar{X}$.

---

**Example 2: MLE of $p$ for Bernoulli$(p)$**

$\\ell(p) = \\sum x_i \\ln p + (n - \\sum x_i)\\ln(1-p)$. Solution: $\\hat{p} = \\bar{X}$.

---

**Example 3: MLE of $\\mu$ for $N(\\mu, \\sigma_0^2)$ (known $\\sigma^2$)**

Minimizing $\\sum(x_i - \\mu)^2$ gives $\\hat{\\mu} = \\bar{X}$.

## Common Mistakes

- **Forgetting to take the log.** The log-likelihood is much easier to maximize.
- **Not checking the second derivative** to confirm it's a maximum.

## Quick Check

1. Why use log-likelihood instead of likelihood?
2. MLE for $\\theta$ in Uniform$(0,\\theta)$?
3. Is $d\\ell/d\\theta = 0$ always sufficient?

*(Answers: converts product to sum; $\\hat{\\theta}=X_{(n)}$ (max obs); no — also check 2nd derivative or boundary)*
""",

"stat-mle-multiparameter": """\
# MLE: Multiparameter

## Overview

When a distribution has multiple parameters (e.g., $\\mu$ and $\\sigma^2$ in the normal), MLE requires simultaneous maximization over all parameters using a system of score equations.

## Key Idea

Take partial derivatives of the log-likelihood with respect to each parameter and set all equal to zero:

$$\\frac{\\partial \\ell}{\\partial \\theta_j} = 0 \\quad \\text{for all } j$$

## Worked Examples

**Example 1: MLE for $N(\\mu, \\sigma^2)$ (both unknown)**

Score equations: $\\partial\\ell/\\partial\\mu = 0 \\Rightarrow \\hat{\\mu} = \\bar{X}$; $\\partial\\ell/\\partial\\sigma^2 = 0 \\Rightarrow \\hat{\\sigma}^2 = \\frac{1}{n}\\sum(X_i-\\bar{X})^2$.

Note: $\\hat{\\sigma}^2_{MLE}$ uses $n$, making it biased.

---

**Example 2: MLE for Gamma$(r, \\lambda)$**

Coupled equations — no closed form for $r$; numerical optimization is needed.

---

**Example 3: Fisher information matrix**

The inverse of the Fisher information matrix gives the asymptotic covariance of the MLE vector.

## Common Mistakes

- **Solving score equations one at a time ignoring interactions.** They must be solved simultaneously.
- **Ignoring boundary solutions.** Always check if the maximum is interior or on the boundary of the parameter space.

## Quick Check

1. MLE of $\\mu$ for Normal$(\\mu,\\sigma^2)$?
2. MLE of $\\sigma^2$ for Normal$(\\mu,\\sigma^2)$ — is it biased?
3. How many score equations for a 3-parameter model?

*(Answers: $\\bar{X}$; yes (divides by $n$, not $n-1$); 3)*
""",

"stat-mle-properties": """\
# MLE: Properties and Invariance

## Overview

MLEs have strong theoretical properties: they are **consistent**, **asymptotically normal**, and **asymptotically efficient**. The **invariance principle** says the MLE of $g(\\theta)$ is $g(\\hat{\\theta}_{MLE})$.

## Key Idea

- **Invariance:** $\\widehat{g(\\theta)} = g(\\hat{\\theta})$
- **Asymptotic normality:** $\\sqrt{n}(\\hat{\\theta} - \\theta) \\xrightarrow{d} N(0, I(\\theta)^{-1})$
- **Asymptotic efficiency:** Achieves the Cramér-Rao lower bound asymptotically

## Worked Examples

**Example 1: MLE of $\\sigma$ given MLE of $\\sigma^2$**

$\\hat{\\sigma}^2 = \\frac{1}{n}\\sum(X_i-\\bar{X})^2$. By invariance, $\\hat{\\sigma} = \\sqrt{\\hat{\\sigma}^2}$.

---

**Example 2: MLE of $e^\\mu$ for Normal$(\\mu,1)$**

$\\hat{\\mu} = \\bar{X}$. By invariance, $\\widehat{e^\\mu} = e^{\\bar{X}}$.

---

**Example 3: Asymptotic variance**

The asymptotic variance of the MLE $\\hat{\\theta}$ is $1/(nI(\\theta))$, where $I(\\theta)$ is the Fisher information.

## Common Mistakes

- **Thinking invariance applies to bias.** Invariance is about the estimator's functional form, not its bias properties.
- **Assuming MLEs are always unbiased.** The MLE of $\\sigma^2$ is biased.

## Quick Check

1. MLE of $\\lambda^2$ if $\\hat{\\lambda} = \\bar{X}$?
2. Are MLEs always unbiased?
3. What is asymptotic efficiency?

*(Answers: $\\bar{X}^2$; no; achieving the CRLB as $n \\to \\infty$)*
""",

"stat-sufficiency": """\
# Sufficient Statistics

## Overview

A **sufficient statistic** $T(X)$ captures all the information in the data about the parameter $\\theta$: once you know $T$, the conditional distribution of the data given $T$ does not depend on $\\theta$.

## Key Idea

**Factorization theorem (Neyman-Fisher):** $T(X)$ is sufficient for $\\theta$ iff the joint density factors as:

$$f(x_1,\\ldots,x_n; \\theta) = g(T(x), \\theta) \\cdot h(x_1,\\ldots,x_n)$$

## Worked Examples

**Example 1: $X_i \\sim \\text{Bernoulli}(p)$. Show $T = \\sum X_i$ is sufficient.**

$L(p) = p^{\\sum x_i}(1-p)^{n-\\sum x_i} = g(\\sum x_i, p) \\cdot 1$. Factorization confirms sufficiency.

---

**Example 2: $X_i \\sim N(\\mu, 1)$. Sufficient statistic?**

$L(\\mu) \\propto \\exp\\left(-\\frac{1}{2}\\sum(x_i-\\mu)^2\\right) \\propto \\exp\\left(\\mu\\bar{x} - n\\mu^2/2\\right)$. So $T = \\bar{X}$ is sufficient.

---

**Example 3: Complete sufficient statistic**

A sufficient statistic is **complete** if $E[g(T)] = 0$ for all $\\theta$ implies $g(T) = 0$ a.s. Complete sufficient statistics lead to UMVUEs.

## Common Mistakes

- **Sufficient ≠ minimal sufficient.** Minimal sufficient contains the least information needed.
- **$T$ sufficient doesn't mean it's unbiased or efficient alone.**

## Quick Check

1. Factorization theorem: what does $g$ depend on?
2. For Poisson$(\\lambda)$, is $\\sum X_i$ sufficient?
3. What is a complete sufficient statistic used for?

*(Answers: $T(x)$ and $\\theta$; yes; constructing UMVUEs via Lehmann-Scheffé)*
""",

"stat-fisher-info": """\
# Fisher Information

## Overview

**Fisher information** $I(\\theta)$ quantifies how much information a random variable (or sample) carries about an unknown parameter. Higher Fisher information means the parameter can be estimated more precisely.

## Key Idea

$$I(\\theta) = E\\left[\\left(\\frac{\\partial}{\\partial\\theta} \\ln f(X;\\theta)\\right)^2\\right] = -E\\left[\\frac{\\partial^2}{\\partial\\theta^2} \\ln f(X;\\theta)\\right]$$

For $n$ iid observations: $I_n(\\theta) = n \\cdot I_1(\\theta)$.

## Worked Examples

**Example 1: Fisher information for Bernoulli$(p)$**

$\\ln f = x\\ln p + (1-x)\\ln(1-p)$. Score: $x/p - (1-x)/(1-p)$. $I(p) = 1/(p(1-p))$.

---

**Example 2: Fisher information for $N(\\mu, \\sigma^2)$ (known $\\sigma^2$)**

$I(\\mu) = 1/\\sigma^2$. More variance = less information.

---

**Example 3: Information and sample size**

For $n$ iid observations from Bernoulli$(p)$: $I_n(p) = n/(p(1-p))$.

## Common Mistakes

- **Fisher information is not the same as the observed information.** Observed information is $-d^2\\ell/d\\theta^2$ at $\\hat{\\theta}$.
- **I(θ) can depend on θ.** It is generally a function of the true parameter.

## Quick Check

1. $I(\\lambda)$ for Poisson$(\\lambda)$?
2. What does high $I(\\theta)$ imply about estimation?
3. $I_n(\\theta) = ?$ for $n$ iid observations?

*(Answers: $1/\\lambda$; can estimate $\\theta$ precisely; $nI_1(\\theta)$)*
""",

"stat-crlb": """\
# Cramér-Rao Lower Bound

## Overview

The **Cramér-Rao Lower Bound (CRLB)** gives a lower bound on the variance of any unbiased estimator. No unbiased estimator can do better than the CRLB, so it defines the best possible precision.

## Key Idea

For any unbiased estimator $\\hat{\\theta}$:

$$\\text{Var}(\\hat{\\theta}) \\ge \\frac{1}{I_n(\\theta)} = \\frac{1}{n\\,I_1(\\theta)}$$

An estimator achieving the CRLB is **efficient**.

## Worked Examples

**Example 1: CRLB for $\\mu$ in $N(\\mu, \\sigma^2)$ known $\\sigma^2$**

$I_n(\\mu) = n/\\sigma^2$. CRLB $= \\sigma^2/n$. $\\bar{X}$ achieves this ✓ — efficient.

---

**Example 2: CRLB for $p$ in Binomial$(n,p)$**

$I_n(p) = n/(p(1-p))$. CRLB $= p(1-p)/n$. $\\hat{p} = X/n$ achieves it.

---

**Example 3: When is the CRLB not achieved?**

Many estimators don't achieve the CRLB. The CRLB is a lower bound, not necessarily attainable.

## Common Mistakes

- **The CRLB only applies to unbiased estimators.** Biased estimators have a generalized version.
- **Assuming the minimum variance estimator always exists.** MVUE may not exist for all distributions.

## Quick Check

1. CRLB $= ?$
2. If $\\text{Var}(\\hat{\\theta}) = 1/(nI(\\theta))$, what is $\\hat{\\theta}$ called?
3. CRLB for Exp$(\\lambda)$ given $n$ observations?

*(Answers: $1/(nI(\\theta))$; efficient estimator; $\\lambda^2/n$)*
""",

"stat-mvue": """\
# MVUE

## Overview

The **Minimum Variance Unbiased Estimator (MVUE)** is the unique unbiased estimator with the smallest possible variance among all unbiased estimators. It is the gold standard for point estimation.

## Key Idea

**Lehmann-Scheffé theorem:** If $T$ is a complete sufficient statistic and $\\hat{\\theta} = g(T)$ is unbiased, then $\\hat{\\theta}$ is the MVUE.

**Rao-Blackwell:** Conditioning an unbiased estimator on a sufficient statistic always improves (or maintains) it.

## Worked Examples

**Example 1: MVUE of $\\mu$ for $N(\\mu,\\sigma^2)$ known $\\sigma^2$**

$\\bar{X}$ is unbiased and a function of the complete sufficient statistic. It is the MVUE.

---

**Example 2: Rao-Blackwellization**

If $\\hat{\\theta}$ is unbiased and $T$ is sufficient, then $\\hat{\\theta}_{RB} = E[\\hat{\\theta}|T]$ is at least as good (lower or equal MSE).

---

**Example 3: Poisson MVUE**

For Poisson$(\\lambda)$, $\\bar{X}$ is the MVUE of $\\lambda$. But the MVUE of $e^{-\\lambda}$ (probability of 0 events) requires more work.

## Common Mistakes

- **MVUE requires the estimator to be based on the complete sufficient statistic.** Regular sufficient is not enough.
- **Assuming MVUE always exists.** For some problems there is no MVUE.

## Quick Check

1. What theorem guarantees the MVUE from a complete sufficient statistic?
2. Rao-Blackwell improves what property?
3. Is $\\bar{X}$ the MVUE of $\\mu$ for any distribution?

*(Answers: Lehmann-Scheffé; variance (reduces or maintains it); no — only when it's the complete suff. stat.)*
""",

"stat-delta-method": """\
# Delta Method

## Overview

The **delta method** gives the asymptotic distribution of a transformed estimator. If $\\sqrt{n}(\\hat{\\theta} - \\theta) \\xrightarrow{d} N(0, \\sigma^2)$, then you can find the asymptotic distribution of $g(\\hat{\\theta})$.

## Key Idea

If $\\sqrt{n}(\\hat{\\theta} - \\theta) \\xrightarrow{d} N(0,\\sigma^2)$ and $g$ is differentiable at $\\theta$:

$$\\sqrt{n}(g(\\hat{\\theta}) - g(\\theta)) \\xrightarrow{d} N(0, [g'(\\theta)]^2 \\sigma^2)$$

## Worked Examples

**Example 1: Distribution of $\\log\\hat{p}$ where $\\hat{p} = X/n \\sim N(p, p(1-p)/n)$**

$g(p) = \\log p$, $g'(p) = 1/p$.

$$\\sqrt{n}(\\log\\hat{p} - \\log p) \\xrightarrow{d} N\\!\\left(0, \\frac{1-p}{p}\\right)$$

---

**Example 2: Variance-stabilizing transformation**

Choose $g$ so that $[g'(\\theta)]^2 \\sigma^2(\\theta) = \\text{const}$. For Binomial, $g(p) = \\arcsin(\\sqrt{p})$ works.

---

**Example 3: Multivariate delta method**

For vector-valued $\\hat{\\theta}$: asymptotic variance of $g(\\hat{\\theta})$ is $\\nabla g^T \\Sigma \\nabla g$.

## Common Mistakes

- **Forgetting to square $g'(\\theta)$.** The variance transforms by $[g'(\\theta)]^2$.
- **Using delta method when $g'(\\theta) = 0$.** The first-order approximation fails; you need the second-order delta method.

## Quick Check

1. If $\\sqrt{n}(\\hat{\\theta}-\\theta)\\to N(0,4)$, asymptotic variance of $g(\\hat{\\theta})$?
2. $g(x) = x^2$. $g'(\\theta) = ?$
3. What assumption on $g$ does the delta method require?

*(Answers: $4[g'(\\theta)]^2$; $2\\theta$; differentiability at $\\theta$)*
""",

"stat-bootstrap": """\
# Bootstrap

## Overview

The **bootstrap** estimates the sampling distribution of a statistic by repeatedly resampling from the observed data **with replacement**. It requires no distributional assumptions and works for almost any estimator.

## Key Idea

1. Draw $B$ bootstrap samples of size $n$ from the data (with replacement).
2. Compute the statistic $\\hat{\\theta}^*$ for each.
3. Use the distribution of $\\hat{\\theta}^*$ values to estimate the SE, bias, or confidence interval of $\\hat{\\theta}$.

**Bootstrap SE:** $\\widehat{\\text{SE}} = \\text{SD of }\\{\\hat{\\theta}^*_1, \\ldots, \\hat{\\theta}^*_B\\}$.

## Worked Examples

**Example 1: Bootstrap SE of the median**

No closed-form formula for SE of median. Bootstrap: resample 1000 times, compute median each time, take SD.

---

**Example 2: Percentile confidence interval**

Sort $\\hat{\\theta}^*$ values. 95% CI: $(\\hat{\\theta}^*_{0.025}, \\hat{\\theta}^*_{0.975})$.

---

**Example 3: When is $B = 1000$ enough?**

For SE estimation, $B = 200$–$500$ often suffices. For CI, $B \\ge 1000$ is safer.

## Common Mistakes

- **Resampling without replacement.** Bootstrap requires replacement.
- **Thinking bootstrap overcomes small $n$.** It cannot fix a fundamentally unrepresentative sample.

## Quick Check

1. What is the bootstrap principle?
2. Bootstrap SE is estimated by what?
3. Does bootstrap require parametric assumptions?

*(Answers: resample from data with replacement; SD of bootstrap statistics; no)*
""",

"stat-ci-z": """\
# Z Confidence Intervals

## Overview

A **Z confidence interval** for $\\mu$ uses the standard normal distribution and requires either known $\\sigma$ or large $n$ (where $s \\approx \\sigma$ by LLN). It gives a range likely to contain the true mean.

## Key Idea

$$\\bar{X} \\pm z_{\\alpha/2} \\frac{\\sigma}{\\sqrt{n}}$$

For 95% CI: $z_{0.025} = 1.96$. Interpretation: 95% of intervals constructed this way contain $\\mu$.

## Worked Examples

**Example 1: $n=100$, $\\bar{x}=50$, $\\sigma=10$. 95% CI.**

$$50 \\pm 1.96(10/10) = 50 \\pm 1.96 = (48.04, 51.96)$$

---

**Example 2: 99% CI for the same data**

$z_{0.005} = 2.576$. $(50-2.576, 50+2.576) = (47.42, 52.58)$.

---

**Example 3: Effect of sample size**

Doubling $n$ reduces margin of error by $\\sqrt{2}$. To halve margin of error, quadruple $n$.

## Common Mistakes

- **"95% probability that $\\mu$ is in the interval."** Wrong. $\\mu$ is fixed; the interval is random. 95% of such intervals contain $\\mu$.
- **Using $Z$ CI when $\\sigma$ is unknown and $n$ is small.** Use $t$ CI instead.

## Quick Check

1. Margin of error for $n=64$, $\\sigma=8$, 95%?
2. $z_{0.025} = ?$
3. How does CI width change if $n$ quadruples?

*(Answers: 1.96; 1.96; halves)*
""",

"stat-ci-t": """\
# t Confidence Intervals

## Overview

When $\\sigma$ is unknown, replace $z$ with the $t$-statistic. The **$t$ confidence interval** uses Student's $t$-distribution with $n-1$ degrees of freedom, which has heavier tails to account for estimating $\\sigma$.

## Key Idea

$$\\bar{X} \\pm t_{n-1, \\alpha/2} \\frac{S}{\\sqrt{n}}$$

where $S = \\sqrt{\\frac{1}{n-1}\\sum(X_i-\\bar{X})^2}$.

As $n \\to \\infty$, $t_{n-1} \\to N(0,1)$.

## Worked Examples

**Example 1: $n=10$, $\\bar{x}=25$, $s=4$. 95% CI.**

$t_{9,0.025} = 2.262$. $25 \\pm 2.262(4/\\sqrt{10}) = 25 \\pm 2.86 = (22.14, 27.86)$.

---

**Example 2: Compare to $Z$ CI**

Same data: $Z$ CI would use $1.96$ instead of $2.262$ — narrower but less accurate with unknown $\\sigma$.

---

**Example 3: Assumptions**

$X_i$ must be approximately normal (or $n$ large). Robust to mild non-normality.

## Common Mistakes

- **Using $z$ instead of $t$ when $\\sigma$ is unknown and $n$ is small.**
- **Wrong degrees of freedom.** Use $n-1$, not $n$.

## Quick Check

1. df for $t$ CI with $n=25$?
2. $t_{9,0.025}$ vs. $z_{0.025}$: which is larger?
3. When does $t_{n-1}$ approximate $N(0,1)$?

*(Answers: 24; $t$ is larger; when $n$ is large)*
""",

"stat-ci-proportion": """\
# CI for Proportions

## Overview

A **confidence interval for a proportion** $p$ uses the fact that $\\hat{p} = X/n$ is approximately normal for large $n$. Several constructions exist; the Wilson interval is more accurate than the Wald interval for small $n$.

## Key Idea

**Wald interval:**

$$\\hat{p} \\pm z_{\\alpha/2}\\sqrt{\\frac{\\hat{p}(1-\\hat{p})}{n}}$$

Valid when $n\\hat{p} \\ge 5$ and $n(1-\\hat{p}) \\ge 5$.

## Worked Examples

**Example 1: 120 out of 200 surveyed prefer Brand A. 95% CI for $p$.**

$\\hat{p} = 0.6$, $\\text{SE} = \\sqrt{0.6(0.4)/200} \\approx 0.0346$.

$0.6 \\pm 1.96(0.0346) = (0.532, 0.668)$.

---

**Example 2: Sample size for margin of error $\\le 0.03$ at 95%**

$n \\ge \\left(\\frac{1.96}{2 \\times 0.03}\\right)^2 = 1068$ (using $\\hat{p}=0.5$ for worst case).

---

**Example 3: Wilson interval**

More accurate for small $n$, especially when $\\hat{p}$ is near 0 or 1. Tilts toward 0.5.

## Common Mistakes

- **Using Wald when $n\\hat{p} < 5$.** The normal approximation is poor.
- **Ignoring the continuity correction for discrete data.**

## Quick Check

1. $\\hat{p}=0.4$, $n=100$. SE?
2. Margin of error for $n=400$, 95%?
3. Worst-case $\\hat{p}$ for conservative sample size?

*(Answers: 0.049; $1.96 \\cdot 0.5/\\sqrt{400} = 0.049$; $\\hat{p}=0.5$)*
""",

"stat-hyp-setup": """\
# Hypothesis Test Setup

## Overview

A **hypothesis test** starts with a null hypothesis $H_0$ (the default claim) and an alternative $H_1$. Data is used to decide whether to reject $H_0$ in favor of $H_1$, controlling the probability of error.

## Key Idea

- **$H_0$:** default (e.g., $\\mu = 0$, no effect)
- **$H_1$:** the research claim (e.g., $\\mu \\ne 0$, $\\mu > 0$, or $\\mu < 0$)
- **Test statistic:** a function of the data computed under $H_0$
- **Rejection region:** values of the test statistic leading to rejection

## Worked Examples

**Example 1: Coin fairness. Set up the test.**

$H_0: p = 0.5$ vs. $H_1: p \\ne 0.5$ (two-sided). Test statistic: $Z = (\\hat{p} - 0.5)/\\sqrt{0.25/n}$.

---

**Example 2: One-sided test**

Drug lowers blood pressure. $H_0: \\mu = 0$ vs. $H_1: \\mu < 0$ (reduction).

---

**Example 3: Simple vs. composite**

$H_0: \\mu = 5$ is simple (single value). $H_1: \\mu > 5$ is composite (many values).

## Common Mistakes

- **Setting up $H_1$ based on the data** — hypotheses must be stated before seeing data.
- **Reversing null and alternative.** The burden of proof is on $H_1$; $H_0$ is rejected only with strong evidence.

## Quick Check

1. Which is the "innocent until proven guilty" hypothesis?
2. One-sided vs. two-sided: when do you use each?
3. Can $H_0$ be "accepted"?

*(Answers: $H_0$; one-sided when direction is known in advance; no — only "fail to reject")*
""",

"stat-errors-power": """\
# Type I/II Errors and Power

## Overview

**Type I error** (false positive): rejecting $H_0$ when it's true. **Type II error** (false negative): failing to reject $H_0$ when $H_1$ is true. **Power** is the probability of correctly rejecting a false $H_0$.

## Key Idea

- $\\alpha = P(\\text{Type I}) = P(\\text{reject } H_0 | H_0 \\text{ true})$ (significance level)
- $\\beta = P(\\text{Type II}) = P(\\text{fail to reject } H_0 | H_1 \\text{ true})$
- $\\text{Power} = 1 - \\beta = P(\\text{reject } H_0 | H_1 \\text{ true})$

Reducing $\\alpha$ increases $\\beta$; increasing $n$ reduces both simultaneously.

## Worked Examples

**Example 1: $\\alpha = 0.05$ means what?**

A 5% chance of rejecting $H_0$ when it is actually true.

---

**Example 2: Power calculation for $Z$-test, $\\mu_1 = 1$, $\\sigma = 2$, $n = 25$, $\\alpha = 0.05$**

$\\text{SE} = 0.4$. Reject when $Z > 1.645$. Under $H_1$: $Z' = (Z - 1/0.4) = Z - 2.5$. Power $= P(Z > 1.645 - 2.5) = P(Z > -0.855) \\approx 0.804$.

---

**Example 3: Effect of $n$ on power**

Quadrupling $n$ cuts SE by half, moving the power curve right and increasing power.

## Common Mistakes

- **Confusing $\\alpha$ and $\\beta$.** $\\alpha$ is set by the researcher; $\\beta$ depends on the true effect.
- **Thinking high power is always desirable at all costs.** It comes at the expense of sample size.

## Quick Check

1. What is power in terms of $\\beta$?
2. Increasing $n$ affects $\\alpha$?
3. Trade-off: decreasing $\\alpha$ does what to $\\beta$?

*(Answers: $1-\\beta$; no (fixed by researcher); increases $\\beta$ (unless $n$ increases too))*
""",

"stat-pvalue": """\
# p-Values

## Overview

The **p-value** is the probability, under $H_0$, of observing a test statistic at least as extreme as the one computed. It measures the evidence against $H_0$: smaller p-value = stronger evidence against $H_0$.

## Key Idea

$$p = P(T \\ge t_{\\text{obs}} | H_0) \\quad \\text{(one-sided)}$$

Reject $H_0$ at level $\\alpha$ if $p < \\alpha$. The p-value is NOT the probability that $H_0$ is true.

## Worked Examples

**Example 1: $Z = 2.1$, two-sided test**

$p = 2 \\times P(Z > 2.1) = 2 \\times 0.018 = 0.036$. Reject at $\\alpha = 0.05$.

---

**Example 2: $t = 1.8$, $n = 20$, one-sided**

$p = P(t_{19} > 1.8) \\approx 0.044$. Reject at $\\alpha = 0.05$.

---

**Example 3: p-value = 0.20**

Fail to reject $H_0$ at any standard level. The data is consistent with $H_0$.

## Common Mistakes

- **"p = 0.04 means 4% chance $H_0$ is true."** The p-value is a probability under $H_0$, not about $H_0$.
- **Comparing p-value to $\\beta$, not $\\alpha$.**

## Quick Check

1. $p = 0.03$, $\\alpha = 0.05$. Decision?
2. $p = 0.10$, $\\alpha = 0.05$. Decision?
3. Is $p < 0.05$ always practically significant?

*(Answers: reject $H_0$; fail to reject; no — statistical vs. practical significance differ)*
""",

"stat-neyman-pearson": """\
# Neyman-Pearson Lemma

## Overview

The **Neyman-Pearson Lemma** identifies the most powerful test for a simple null vs. simple alternative hypothesis. The optimal test uses the likelihood ratio as the test statistic.

## Key Idea

For $H_0: \\theta = \\theta_0$ vs. $H_1: \\theta = \\theta_1$, the most powerful level-$\\alpha$ test rejects when:

$$\\frac{L(\\theta_1)}{L(\\theta_0)} > k$$

where $k$ is chosen so that $P(\\text{reject} | H_0) = \\alpha$.

## Worked Examples

**Example 1: $X \\sim N(\\theta, 1)$. $H_0: \\theta=0$ vs. $H_1: \\theta=1$. MP test.**

LR $= e^{x - 1/2} > k$, i.e., $X > c$. Reject when $X > z_{\\alpha}$. This is the UMP test.

---

**Example 2: $X \\sim \\text{Pois}(\\lambda)$. $H_0: \\lambda=1$ vs. $H_1: \\lambda=3$.**

LR $= 3^x e^{-2}$. Reject when $X > c$. Larger $\\lambda$ → large observed count is evidence against $H_0$.

---

**Example 3: NP is for simple vs. simple**

The lemma applies only when both $H_0$ and $H_1$ specify a single parameter value.

## Common Mistakes

- **Applying NP to composite hypotheses.** Use UMP tests or GLRT for composite hypotheses.
- **Forgetting that the critical value $k$ is determined by $\\alpha$.**

## Quick Check

1. What does the NP Lemma guarantee?
2. What is the test statistic in the NP framework?
3. NP applies to simple vs. simple — what does "simple" mean?

*(Answers: most powerful level-$\\alpha$ test; likelihood ratio; $H$ specifies a single parameter value)*
""",

"stat-ump": """\
# Uniformly Most Powerful Tests

## Overview

A **Uniformly Most Powerful (UMP) test** is the most powerful test at level $\\alpha$ for every possible value in $H_1$. UMP tests exist for one-sided hypotheses in one-parameter exponential families.

## Key Idea

A level-$\\alpha$ test $\\phi$ is UMP if $E_\\theta[\\phi(X)] \\ge E_\\theta[\\psi(X)]$ for all $\\theta \\in H_1$ and all other level-$\\alpha$ tests $\\psi$.

For exponential families, the NP likelihood ratio test with a monotone likelihood ratio (MLR) provides the UMP.

## Worked Examples

**Example 1: UMP for $H_1: \\mu > \\mu_0$ in normal testing**

Reject when $\\bar{X} > \\bar{X}_{\\alpha}$. This is UMP for all $\\mu > \\mu_0$ because the normal has MLR in $\\bar{X}$.

---

**Example 2: No UMP for two-sided alternatives**

$H_1: \\mu \\ne \\mu_0$ — no single rejection region maximizes power at both $\\mu > \\mu_0$ and $\\mu < \\mu_0$ simultaneously.

---

**Example 3: MLR property**

A family has monotone likelihood ratio in $T(X)$ if $L(\\theta_1)/L(\\theta_0)$ is monotone in $T$ for $\\theta_1 > \\theta_0$. This implies UMP tests exist for one-sided hypotheses.

## Common Mistakes

- **Assuming UMP tests always exist.** Two-sided and multi-parameter problems often have no UMP.
- **Confusing UMP with UMPU** (uniformly most powerful unbiased, for two-sided tests).

## Quick Check

1. Does a UMP test exist for $H_1: \\mu \\ne 0$?
2. What property guarantees a UMP test for a one-parameter exponential family?
3. Power function of UMP must satisfy what for all $\\theta \\in H_1$?

*(Answers: generally no; MLR property; it is $\\ge$ power of any other level-$\\alpha$ test)*
""",

"stat-glrt": """\
# Generalized Likelihood Ratio Test

## Overview

The **Generalized Likelihood Ratio Test (GLRT)** extends the NP framework to composite hypotheses and multi-parameter settings. It compares the maximum likelihood under the full model to the maximum under the restricted null model.

## Key Idea

$$\\Lambda = \\frac{\\sup_{\\theta \\in \\Theta_0} L(\\theta)}{\\sup_{\\theta \\in \\Theta} L(\\theta)}$$

Reject $H_0$ when $\\Lambda$ is small (or $-2\\ln\\Lambda$ is large). By Wilks' theorem, $-2\\ln\\Lambda \\xrightarrow{d} \\chi^2_k$ under $H_0$, where $k$ is the number of constraints.

## Worked Examples

**Example 1: Test $H_0: \\mu = 0$ in $N(\\mu,\\sigma^2)$**

$-2\\ln\\Lambda = n\\ln(1 + t^2/(n-1)) \\approx t^2$ for large $n$, which is $\\chi^2_1$. Equivalent to $t$-test.

---

**Example 2: Degrees of freedom in Wilks' theorem**

$k = \\dim(\\Theta) - \\dim(\\Theta_0)$. Testing 1 constraint: $\\chi^2_1$. Testing 2 constraints simultaneously: $\\chi^2_2$.

---

**Example 3: Practical use**

GLRT provides a general testing procedure when no UMP test exists.

## Common Mistakes

- **Wrong degrees of freedom.** Count the number of parameters restricted by $H_0$.
- **Wilks' theorem is asymptotic.** For small $n$, the $\\chi^2$ approximation may be poor.

## Quick Check

1. What is the GLRT statistic $\\Lambda$?
2. $-2\\ln\\Lambda$ has what asymptotic distribution?
3. Degrees of freedom for testing $H_0: \\mu_1 = \\mu_2 = 0$ in a 3-parameter model?

*(Answers: ratio of constrained to unconstrained max likelihood; $\\chi^2_k$; 2)*
""",

"stat-power-sample-size": """\
# Power and Sample Size

## Overview

**Sample size determination** calculates the minimum $n$ needed to achieve a target power (e.g., 80%) at a specified effect size, given $\\alpha$. It is done at the design stage before collecting data.

## Key Idea

For a one-sample $Z$-test:

$$n = \\left(\\frac{(z_{\\alpha/2} + z_\\beta)\\sigma}{\\delta}\\right)^2$$

where $\\delta = |\\mu_1 - \\mu_0|$ is the minimum effect size to detect and $z_\\beta$ comes from the desired power $1-\\beta$.

## Worked Examples

**Example 1: $\\alpha=0.05$, power$=0.8$, $\\sigma=10$, $\\delta=5$**

$z_{0.025} = 1.96$, $z_{0.2} = 0.842$.

$n = ((1.96+0.842)\\cdot10/5)^2 = (5.604)^2 \\approx 31.4$. Use $n=32$.

---

**Example 2: Effect of halving $\\delta$**

Halving the effect size quadruples the required $n$ (since $n \\propto 1/\\delta^2$).

---

**Example 3: Power given $n$**

Rearrange to find power: $\\text{power} = P(Z > z_{\\alpha/2} - \\delta\\sqrt{n}/\\sigma)$.

## Common Mistakes

- **Using $z_{\\alpha}$ instead of $z_{\\alpha/2}$ for two-sided tests.**
- **Forgetting to round $n$ up** to the nearest integer.

## Quick Check

1. $n$ doubles — what happens to power?
2. $n$ formula for one-sided test vs. two-sided?
3. Effect size $\\delta$ = 0 means what about sample size?

*(Answers: increases; replace $z_{\\alpha/2}$ with $z_{\\alpha}$; no finite $n$ achieves power > $\\alpha$)*
""",

"stat-ztest-one": """\
# One-Sample Z-Test

## Overview

The **one-sample Z-test** tests whether a population mean equals a specified value, using a known $\\sigma$ (or large $n$ where $s \\approx \\sigma$). It is the prototype of all hypothesis tests.

## Key Idea

$$Z = \\frac{\\bar{X} - \\mu_0}{\\sigma/\\sqrt{n}} \\sim N(0,1) \\text{ under } H_0$$

Reject $H_0$ at level $\\alpha$ if $|Z| > z_{\\alpha/2}$ (two-sided) or $Z > z_\\alpha$ (one-sided).

## Worked Examples

**Example 1: $\\mu_0 = 100$, $\\sigma = 15$, $n = 25$, $\\bar{x} = 106$. Two-sided, $\\alpha = 0.05$.**

$Z = (106-100)/(15/5) = 2.0$. $|2.0| > 1.96$. Reject $H_0$.

---

**Example 2: Compute the p-value**

$p = 2P(Z > 2.0) = 2(0.023) = 0.046 < 0.05$. Reject.

---

**Example 3: One-sided test**

$H_1: \\mu > 100$. Reject when $Z > 1.645$. Same data: $Z = 2.0 > 1.645$. Reject.

## Common Mistakes

- **Using $Z$-test when $\\sigma$ is unknown and $n$ is small.** Use $t$-test.
- **Computing one-sided $p$-value but using two-sided critical value** (or vice versa).

## Quick Check

1. Test statistic formula for one-sample $Z$-test?
2. Critical value for $\\alpha = 0.01$, two-sided?
3. $n=36$, $\\sigma=12$, $\\bar{x}=52$, $\\mu_0=50$. $Z = ?$

*(Answers: $(\\bar{X}-\\mu_0)/(\\sigma/\\sqrt{n})$; 2.576; 1.0)*
""",

"stat-ttest-one": """\
# One-Sample t-Test

## Overview

The **one-sample $t$-test** tests whether the population mean equals $\\mu_0$ when $\\sigma$ is unknown. It uses the sample standard deviation $S$ and the $t$-distribution.

## Key Idea

$$T = \\frac{\\bar{X} - \\mu_0}{S/\\sqrt{n}} \\sim t_{n-1} \\text{ under } H_0 \\text{ (for normal data)}$$

The $t$-distribution has heavier tails than $N(0,1)$, accounting for the uncertainty in estimating $\\sigma$.

## Worked Examples

**Example 1: $\\mu_0 = 5$, $n = 10$, $\\bar{x} = 6$, $s = 2$. $\\alpha = 0.05$, two-sided.**

$T = (6-5)/(2/\\sqrt{10}) = 1.58$. $t_{9,0.025} = 2.262$. $1.58 < 2.262$. Fail to reject.

---

**Example 2: 95% CI using $t$**

$(6 - 2.262 \\cdot 0.632, 6 + 2.262 \\cdot 0.632) = (4.57, 7.43)$.

---

**Example 3: Assumption**

Data should be approximately normal. Robust to mild departures when $n \\ge 15$.

## Common Mistakes

- **Using $n$ instead of $n-1$ degrees of freedom.**
- **Applying $t$-test to heavily skewed data with small $n$.** Use nonparametric alternatives.

## Quick Check

1. df for one-sample $t$-test with $n=20$?
2. For large $n$, $t_{n-1} \\approx ?$
3. $T = 3.0$, $n = 15$. Reject at $\\alpha = 0.05$ (two-sided)?

*(Answers: 19; $N(0,1)$; yes, $t_{14,0.025} = 2.145 < 3.0$)*
""",

"stat-ttest-two": """\
# Two-Sample t-Test

## Overview

The **two-sample $t$-test** compares the means of two independent groups. It tests $H_0: \\mu_1 = \\mu_2$ (no difference between groups).

## Key Idea

Assuming equal variances (pooled $t$-test):

$$T = \\frac{\\bar{X}_1 - \\bar{X}_2}{S_p\\sqrt{1/n_1 + 1/n_2}} \\sim t_{n_1+n_2-2}$$

where $S_p^2 = \\frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{n_1+n_2-2}$ is the pooled variance.

Welch's $t$-test (unequal variances) uses a different denominator and approximate df.

## Worked Examples

**Example 1: $\\bar{x}_1 = 10$, $\\bar{x}_2 = 8$, $s_1 = s_2 = 3$, $n_1 = n_2 = 16$. Pooled $t$-test, $\\alpha = 0.05$.**

$S_p = 3$, SE $= 3\\sqrt{2/16} = 1.06$. $T = 2/1.06 = 1.89$. $t_{30,0.025} = 2.042$. Fail to reject.

---

**Example 2: Checking equal variances**

Use Levene's test or compare $s_1/s_2$; if ratio is extreme, use Welch.

---

**Example 3: 95% CI for $\\mu_1 - \\mu_2$**

$(2 \\pm 2.042 \\times 1.06) = (-0.16, 4.16)$. Contains 0 → consistent with no difference.

## Common Mistakes

- **Using pooled test when variances are very unequal.** Use Welch's test instead.
- **Wrong df.** Pooled: $n_1+n_2-2$; Welch: approximate (Satterthwaite).

## Quick Check

1. $H_0$ in a two-sample $t$-test?
2. Pooled df for $n_1=10$, $n_2=15$?
3. What does Welch's test assume about variances?

*(Answers: $\\mu_1=\\mu_2$; 23; they need not be equal)*
""",

"stat-pooled-variance": """\
# Pooled Variance

## Overview

**Pooled variance** $S_p^2$ combines the sample variances from two groups into a single estimate of the common population variance, assuming both groups have the same $\\sigma^2$.

## Key Idea

$$S_p^2 = \\frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{n_1+n_2-2}$$

This is a weighted average of $S_1^2$ and $S_2^2$, with larger samples getting more weight. Used in the pooled two-sample $t$-test.

## Worked Examples

**Example 1: $S_1^2 = 9$, $n_1 = 5$; $S_2^2 = 16$, $n_2 = 9$.**

$S_p^2 = (4(9) + 8(16))/12 = (36 + 128)/12 = 164/12 \\approx 13.67$.

---

**Example 2: Equal sample sizes simplify things**

If $n_1 = n_2$: $S_p^2 = (S_1^2 + S_2^2)/2$.

---

**Example 3: SE for two-sample $t$-test**

$\\text{SE} = S_p\\sqrt{1/n_1 + 1/n_2}$.

## Common Mistakes

- **Using $S_p^2 = (S_1^2 + S_2^2)/2$ when $n_1 \\ne n_2$.** Always use the weighted formula.
- **Pooling when variances are clearly unequal** (use Levene's test first).

## Quick Check

1. $S_p^2$ for $S_1^2=4$, $n_1=3$, $S_2^2=8$, $n_2=3$?
2. When is $S_p^2$ closer to $S_1^2$ vs. $S_2^2$?
3. df for $S_p^2$?

*(Answers: 6; when $n_1 > n_2$ (or closer to whichever has larger $n$); $n_1+n_2-2$)*
""",

"stat-ttest-paired": """\
# Paired t-Test

## Overview

The **paired $t$-test** compares means when each observation in group 1 is naturally matched to one in group 2 (e.g., before/after, twin pairs). It reduces variability by analyzing differences $D_i = X_{i1} - X_{i2}$.

## Key Idea

Compute $D_i = X_{i1} - X_{i2}$. Then apply a one-sample $t$-test to $\\{D_i\\}$:

$$T = \\frac{\\bar{D} - 0}{S_D/\\sqrt{n}} \\sim t_{n-1}$$

## Worked Examples

**Example 1: Blood pressure before (B) and after (A) treatment.**

| Person | B | A | D |
|--------|---|---|---|
| 1 | 130 | 120 | 10 |
| 2 | 140 | 128 | 12 |
| 3 | 125 | 120 | 5 |

$\\bar{D} = 9$, $S_D \\approx 3.6$. $T = 9/(3.6/\\sqrt{3}) = 4.33$. Reject $H_0$.

---

**Example 2: Why paired > two-sample?**

Pairing removes person-to-person variation, leaving only the treatment effect in $D_i$.

---

**Example 3: CI for mean difference**

$\\bar{D} \\pm t_{n-1,\\alpha/2} \\cdot S_D/\\sqrt{n}$.

## Common Mistakes

- **Using two-sample $t$-test when data is paired.** This inflates variance and reduces power.
- **Wrong sample size.** $n$ is the number of pairs, not total observations.

## Quick Check

1. What are the "observations" in a paired $t$-test?
2. df for $n = 12$ pairs?
3. Why is paired usually more powerful than two-sample?

*(Answers: the differences $D_i$; 11; pairing removes nuisance variation)*
""",

"stat-mannwhitney": """\
# Mann-Whitney U Test

## Overview

The **Mann-Whitney U test** (Wilcoxon rank-sum test) is a nonparametric alternative to the two-sample $t$-test. It tests whether one group tends to have larger values than the other, without assuming normality.

## Key Idea

Rank all $n_1 + n_2$ observations from both groups together. The test statistic $U$ is based on the sum of ranks in one group. Under $H_0$ (no difference in distribution), $U$ has a known distribution.

$$U_1 = n_1 n_2 + \\frac{n_1(n_1+1)}{2} - W_1$$

where $W_1$ is the sum of ranks in group 1.

## Worked Examples

**Example 1: Group A: 3,5,8; Group B: 1,4,6. $H_0$: same distribution.**

Ranks: 1→1, 3→2, 4→3, 5→4, 6→5, 8→6. $W_A = 2+4+6 = 12$. $U_A = 9 + 6 - 12 = 3$. $U_B = 9 - 3 = 6$.

---

**Example 2: Interpretation**

$U = 0$ means all of group A ranks above all of group B. $U = n_1 n_2 / 2$ is the expected value under $H_0$.

---

**Example 3: When to use**

Use when normality is doubtful, data is ordinal, or there are outliers.

## Common Mistakes

- **Using Mann-Whitney when data is paired.** Use Wilcoxon signed-rank test instead.
- **Thinking U tests the median.** It tests whether one distribution tends to be stochastically larger.

## Quick Check

1. What is the Mann-Whitney test's null hypothesis?
2. What does $U = 0$ indicate?
3. Normal equivalent of Mann-Whitney?

*(Answers: the two populations have the same distribution (stochastic equality); group 1 dominates entirely; two-sample t-test)*
""",

"stat-wilcoxon-signed": """\
# Wilcoxon Signed-Rank Test

## Overview

The **Wilcoxon signed-rank test** is a nonparametric alternative to the one-sample or paired $t$-test. It tests whether the median of differences equals zero, using the ranks of the absolute differences.

## Key Idea

1. Compute $D_i = X_i - \\mu_0$ (or paired differences).
2. Rank $|D_i|$ from smallest to largest (drop zeros).
3. $W^+ = $ sum of ranks for positive $D_i$.

Under $H_0$ (symmetric around 0), $E[W^+] = n(n+1)/4$.

## Worked Examples

**Example 1: Data: 3, -1, 4, -2. $H_0$: median $= 0$.**

$|D|$: 3, 1, 4, 2. Ranks: 1→2, 2→1, 3→3, 4→4. $W^+ = 3 + 4 = 7$ (positive values: 3 and 4). Compare to table.

---

**Example 2: Advantage over sign test**

Signed-rank uses magnitude, not just sign — more powerful.

---

**Example 3: Assumption**

The distribution of differences must be symmetric around the median.

## Common Mistakes

- **Using Wilcoxon signed-rank when the distribution is asymmetric.** The symmetry assumption is required.
- **Confusing with Mann-Whitney.** Signed-rank is one-sample or paired; Mann-Whitney is two independent samples.

## Quick Check

1. What does the signed-rank test assume?
2. When do you drop differences?
3. Nonparametric equivalent of the paired $t$-test?

*(Answers: symmetric distribution around $\\mu_0$; when $D_i = 0$; Wilcoxon signed-rank)*
""",

"stat-permutation": """\
# Permutation Tests

## Overview

A **permutation test** is a nonparametric test that generates the null distribution by reassigning the group labels many times. It requires minimal assumptions and is exact for exchangeable data.

## Key Idea

1. Compute the observed test statistic $T_{\\text{obs}}$.
2. Randomly permute the group labels $B$ times; compute $T^*_b$ for each.
3. $p$-value $= $ fraction of $T^*_b \\ge T_{\\text{obs}}$.

## Worked Examples

**Example 1: Two groups, 3 observations each. Observed mean difference = 5.**

There are $\\binom{6}{3} = 20$ possible permutations. Count how many yield a difference $\\ge 5$. If 1 out of 20: $p = 0.05$.

---

**Example 2: Continuous test statistic**

Use $B = 10{,}000$ random permutations. p-value = fraction with statistic more extreme than observed.

---

**Example 3: What null hypothesis does it test?**

$H_0$: the labels are exchangeable — the two groups come from the same distribution.

## Common Mistakes

- **Insufficient permutations $B$.** Use at least 1000, preferably 10000+.
- **Permuting when observations are not exchangeable under $H_0$** (e.g., dependent data).

## Quick Check

1. What is the null distribution in a permutation test?
2. Exact p-value for $B = 20$ permutations with 2 more extreme?
3. Advantage over $t$-test?

*(Answers: distribution of $T^*$ over all permutations; 2/20 = 0.1; no normality assumption needed)*
""",

"stat-chi-gof": """\
# Chi-Squared Goodness-of-Fit

## Overview

The **chi-squared goodness-of-fit test** tests whether observed frequencies match expected frequencies from a specified distribution.

## Key Idea

$$\\chi^2 = \\sum_{i=1}^k \\frac{(O_i - E_i)^2}{E_i} \\overset{\\text{approx}}{\\sim} \\chi^2_{k-1-p}$$

where $O_i$ are observed counts, $E_i = n p_i$ are expected, $k$ is the number of categories, and $p$ is the number of estimated parameters.

## Worked Examples

**Example 1: Fair die. Roll 60 times. Expected = 10 per face. Observed: 8,11,9,12,10,10.**

$\\chi^2 = (4+1+1+4+0+0)/10 = 1.0$. df $= 5$. $p > 0.9$. Fail to reject.

---

**Example 2: $E_i < 5$**

Cells with expected count $< 5$ should be merged. The $\\chi^2$ approximation requires all $E_i \\ge 5$.

---

**Example 3: Estimating parameters**

If you estimate $m$ parameters from the data to get $E_i$, df $= k - 1 - m$.

## Common Mistakes

- **Using $\\chi^2$ GOF with small expected counts.** Merge cells.
- **Wrong df.** Subtract 1 for the constraint $\\sum O_i = n$, and one more for each estimated parameter.

## Quick Check

1. df for $k=6$ categories, no estimated parameters?
2. Minimum $E_i$ for the $\\chi^2$ approximation?
3. $\\chi^2 = 0$ means what?

*(Answers: 5; 5; observed = expected exactly)*
""",

"stat-chi-indep": """\
# Chi-Squared Test of Independence

## Overview

The **chi-squared test of independence** tests whether two categorical variables are associated in a contingency table. $H_0$: the two variables are independent.

## Key Idea

For an $r \\times c$ contingency table with observed counts $O_{ij}$, the expected counts under independence are:

$$E_{ij} = \\frac{(\\text{row } i \\text{ total})(\\text{col } j \\text{ total})}{n}$$

$$\\chi^2 = \\sum_{i,j} \\frac{(O_{ij} - E_{ij})^2}{E_{ij}} \\sim \\chi^2_{(r-1)(c-1)}$$

## Worked Examples

**Example 1: $2 \\times 2$ table**

| | Smoker | Non-smoker |
|---|---|---|
| Disease | 30 | 20 |
| No disease | 10 | 40 |

$n=100$. $E_{11} = 50 \\times 40/100 = 20$. $\\chi^2 = (30-20)^2/20 + \\ldots \\approx 16.7$. df $= 1$. Reject at $\\alpha = 0.05$.

---

**Example 2: df for $3 \\times 4$ table**

df $= (3-1)(4-1) = 6$.

---

**Example 3: $\\chi^2$ large means?**

Large $\\chi^2$ → large discrepancy between observed and expected → evidence against independence.

## Common Mistakes

- **Confusing independence test with homogeneity test.** Same formula, different sampling design.
- **Using $\\chi^2$ with small $E_{ij}$.** Apply Fisher's exact test for 2×2 tables with small counts.

## Quick Check

1. df for $2\\times3$ table?
2. $E_{ij}$ formula?
3. Reject $H_0$ when $\\chi^2 > ?$ ($\\alpha = 0.05$, df$=1$)?

*(Answers: 2; (row total)(col total)/n; 3.84)*
""",

"stat-chi-homog": """\
# Chi-Squared Test of Homogeneity

## Overview

The **chi-squared test of homogeneity** tests whether multiple populations have the same distribution across categories. It uses the same formula as the independence test but arises from a different sampling design.

## Key Idea

Same test statistic as independence:

$$\\chi^2 = \\sum_{i,j} \\frac{(O_{ij} - E_{ij})^2}{E_{ij}} \\sim \\chi^2_{(r-1)(c-1)}$$

**Key difference from independence test:** In homogeneity, row totals are fixed by design (you sample a predetermined number from each group).

## Worked Examples

**Example 1: 100 Democrats, 100 Republicans asked if they support a policy.**

| | Support | Oppose |
|---|---|---|
| Dem | 60 | 40 |
| Rep | 45 | 55 |

$E_{11} = 100 \\times 105/200 = 52.5$. $\\chi^2 \\approx 4.52$. df $= 1$. Reject at $\\alpha = 0.05$.

---

**Example 2: Homogeneity vs. independence**

Homogeneity: fixed row totals, testing if column distributions are the same across rows.

Independence: one random sample, testing if row and column variables are associated.

---

**Example 3: Interpretation**

Reject → the distributions differ across groups. The proportions in each category are not homogeneous.

## Common Mistakes

- **Applying the independence test formula to homogeneity data** (they're the same formula, but interpretation differs).
- **Using counts less than 5** — merge cells.

## Quick Check

1. Null hypothesis for homogeneity test?
2. Same formula as which other test?
3. df for comparing 4 groups on 3 categories?

*(Answers: all groups have the same distribution; independence test; $(4-1)(3-1)=6$)*
""",

"stat-anova-one": """\
# One-Way ANOVA

## Overview

**One-way ANOVA** tests whether the means of three or more groups are equal. It partitions total variability into variability between groups (explained) and within groups (unexplained).

## Key Idea

$H_0: \\mu_1 = \\mu_2 = \\cdots = \\mu_k$.

$$F = \\frac{\\text{MS}_{\\text{between}}}{\\text{MS}_{\\text{within}}} = \\frac{SS_B/(k-1)}{SS_W/(n-k)} \\sim F_{k-1,\\, n-k}$$

Reject when $F > F_{k-1,n-k,\\alpha}$.

## Worked Examples

**Example 1: Three groups with equal size $n=5$ each. $SS_B = 40$, $SS_W = 30$.**

$MS_B = 40/2 = 20$. $MS_W = 30/12 = 2.5$. $F = 8$. $F_{2,12,0.05} = 3.89$. Reject.

---

**Example 2: ANOVA table**

| Source | SS | df | MS | F |
|---|---|---|---|---|
| Between | 40 | 2 | 20 | 8 |
| Within | 30 | 12 | 2.5 | |
| Total | 70 | 14 | | |

---

**Example 3: Post-hoc tests**

ANOVA tells you if any means differ; post-hoc tests (Tukey, Bonferroni) identify which pairs.

## Common Mistakes

- **Running multiple $t$-tests instead of ANOVA.** Multiple tests inflate Type I error.
- **Assuming ANOVA identifies which groups differ.** Need post-hoc tests for pairwise comparisons.

## Quick Check

1. $H_0$ in one-way ANOVA?
2. df for $F$ ratio with $k=4$ groups, $n=20$ total?
3. Large $F$ means what?

*(Answers: all group means equal; $F_{3,16}$; between-group variance >> within-group)*
""",

"stat-anova-kruskal": """\
# Kruskal-Wallis Test

## Overview

The **Kruskal-Wallis test** is the nonparametric alternative to one-way ANOVA. It tests whether samples from $k$ groups come from the same distribution, using ranks instead of raw values.

## Key Idea

Rank all $N$ observations across groups. Let $R_i$ be the sum of ranks in group $i$.

$$H = \\frac{12}{N(N+1)} \\sum_{i=1}^k \\frac{R_i^2}{n_i} - 3(N+1) \\sim \\chi^2_{k-1}$$

## Worked Examples

**Example 1: 3 groups, $n_i = 4$ each, $N = 12$. Rank sums $R_1 = 30, R_2 = 25, R_3 = 23$.**

$H = \\frac{12}{12 \\times 13}\\left(\\frac{900+625+529}{4}\\right) - 3(13) = \\frac{12}{156} \\times 513.5 - 39 \\approx 0.48$.

---

**Example 2: When to use**

When ANOVA normality assumption is violated or data is ordinal.

---

**Example 3: Post-hoc for Kruskal-Wallis**

Use Dunn's test or pairwise Mann-Whitney with Bonferroni correction.

## Common Mistakes

- **Applying Kruskal-Wallis for continuous, normally distributed data.** ANOVA is more powerful in that case.
- **Concluding equal means from fail-to-reject.** KW tests the distribution, not just the mean.

## Quick Check

1. What does the Kruskal-Wallis test use instead of raw values?
2. $H \\sim ?$ asymptotically?
3. Parametric equivalent of Kruskal-Wallis?

*(Answers: ranks; $\\chi^2_{k-1}$; one-way ANOVA)*
""",

"stat-multiple-testing": """\
# Multiple Testing Correction

## Overview

When conducting many hypothesis tests simultaneously, the probability of at least one false positive grows rapidly. **Multiple testing correction** controls either the family-wise error rate (FWER) or the false discovery rate (FDR).

## Key Idea

With $m$ tests, each at level $\\alpha$, the probability of at least one false positive is up to $1 - (1-\\alpha)^m$.

- **Bonferroni correction:** Use $\\alpha^* = \\alpha/m$ for each test. Controls FWER.
- **Benjamini-Hochberg (BH):** Controls FDR — less conservative, higher power.

## Worked Examples

**Example 1: 20 tests at $\\alpha = 0.05$**

$P(\\ge 1 \\text{ false positive}) \\le 1 - (0.95)^{20} \\approx 0.64$.

Bonferroni: use $0.05/20 = 0.0025$ per test.

---

**Example 2: BH procedure**

Sort p-values: $p_{(1)} \\le \\cdots \\le p_{(m)}$. Reject all $H_{(i)}$ where $p_{(i)} \\le (i/m)\\alpha$.

---

**Example 3: FWER vs. FDR**

FWER: control probability of any false positive. FDR: control expected proportion of false discoveries among rejections.

## Common Mistakes

- **Not correcting at all in genome-wide studies** — where $m = 10^6$, FWER correction is essential.
- **Over-correcting with Bonferroni when tests are correlated** — it's too conservative.

## Quick Check

1. Bonferroni-corrected $\\alpha$ for 50 tests at overall level 0.05?
2. Which is less conservative: Bonferroni or BH?
3. FDR controls what?

*(Answers: 0.001; BH; expected proportion of false rejections among all rejections)*
""",

"stat-slr": """\
# Simple Linear Regression

## Overview

**Simple linear regression (SLR)** models the relationship between a response $Y$ and a predictor $X$ as a line. The goal is to estimate the intercept and slope from data.

## Key Idea

Model: $Y_i = \\beta_0 + \\beta_1 X_i + \\varepsilon_i$, where $\\varepsilon_i \\overset{iid}{\\sim} N(0,\\sigma^2)$.

OLS estimates:

$$\\hat{\\beta}_1 = \\frac{\\sum(X_i - \\bar{X})(Y_i - \\bar{Y})}{\\sum(X_i - \\bar{X})^2} = \\frac{S_{XY}}{S_{XX}}, \\quad \\hat{\\beta}_0 = \\bar{Y} - \\hat{\\beta}_1 \\bar{X}$$

## Worked Examples

**Example 1: $(X,Y)$ pairs: $(1,2),(2,4),(3,5)$. Fit SLR.**

$\\bar{X}=2$, $\\bar{Y}=11/3$. $S_{XY} = 1.5+0+(-5/3) = ...$. Actually: $S_{XY}=(1-2)(2-11/3)+(2-2)(...)+(3-2)(5-11/3) = 5/3 + 0 + 4/3 = 3$. $S_{XX} = 2$. $\\hat{\\beta}_1 = 1.5$. $\\hat{\\beta}_0 = 11/3 - 3 = 2/3$.

---

**Example 2: Interpretation of $\\hat{\\beta}_1$**

For each 1-unit increase in $X$, $Y$ is expected to increase by $\\hat{\\beta}_1$.

---

**Example 3: $R^2$ coefficient of determination**

$R^2 = 1 - SS_E/SS_T$. Proportion of variance in $Y$ explained by $X$.

## Common Mistakes

- **Extrapolating outside the data range.** The linear model may not hold there.
- **Interpreting $\\hat{\\beta}_1$ causally.** Correlation $\\ne$ causation.

## Quick Check

1. OLS minimizes what?
2. $\\hat{\\beta}_0$ interpretation when $X=0$?
3. $R^2=0.8$ means what?

*(Answers: $\\sum(Y_i - \\hat{Y}_i)^2$; estimated mean of $Y$ when $X=0$; 80% of variance in $Y$ explained by $X$)*
""",

"stat-slr-matrix": """\
# SLR in Matrix Form

## Overview

Writing **simple (and multiple) linear regression in matrix form** compactly represents the entire estimation problem and generalizes to any number of predictors.

## Key Idea

Model: $\\mathbf{Y} = \\mathbf{X}\\boldsymbol{\\beta} + \\boldsymbol{\\varepsilon}$, where $\\mathbf{X}$ is the $n \\times p$ design matrix (first column all 1s).

OLS estimate: $\\hat{\\boldsymbol{\\beta}} = (\\mathbf{X}^T \\mathbf{X})^{-1}\\mathbf{X}^T \\mathbf{Y}$.

Hat matrix: $\\mathbf{H} = \\mathbf{X}(\\mathbf{X}^T\\mathbf{X})^{-1}\\mathbf{X}^T$. Fitted values: $\\hat{\\mathbf{Y}} = \\mathbf{H}\\mathbf{Y}$.

## Worked Examples

**Example 1: Design matrix for SLR with $n=3$, $X=(1,2,3)$**

$$\\mathbf{X} = \\begin{pmatrix}1&1\\\\1&2\\\\1&3\\end{pmatrix}$$

---

**Example 2: OLS formula derivation**

Minimize $\\|\\mathbf{Y} - \\mathbf{X}\\boldsymbol{\\beta}\\|^2$. Normal equations: $\\mathbf{X}^T\\mathbf{X}\\hat{\\boldsymbol{\\beta}} = \\mathbf{X}^T\\mathbf{Y}$.

---

**Example 3: Hat matrix properties**

$\\mathbf{H}$ is symmetric ($\\mathbf{H}^T = \\mathbf{H}$) and idempotent ($\\mathbf{H}^2 = \\mathbf{H}$). It's a projection matrix onto $\\text{col}(\\mathbf{X})$.

## Common Mistakes

- **Forgetting the intercept column of 1s** in $\\mathbf{X}$.
- **Assuming $\\mathbf{X}^T\\mathbf{X}$ is always invertible.** Fails if predictors are perfectly collinear.

## Quick Check

1. OLS estimator formula in matrix form?
2. $\\hat{\\mathbf{Y}} = ?$ in matrix form?
3. What does the hat matrix project onto?

*(Answers: $(X^TX)^{-1}X^TY$; $HY$; column space of $X$)*
""",

"stat-slr-inference": """\
# SLR Inference

## Overview

After fitting a regression line, we want to make inferences: is $\\beta_1$ significantly different from zero? What is the confidence interval for the mean response? **SLR inference** provides $t$-tests and intervals for each coefficient.

## Key Idea

Under normality: $\\hat{\\beta}_1 \\sim N(\\beta_1, \\sigma^2/S_{XX})$.

$$T = \\frac{\\hat{\\beta}_1 - \\beta_{1,0}}{S/\\sqrt{S_{XX}}} \\sim t_{n-2} \\quad \\text{under } H_0: \\beta_1 = \\beta_{1,0}$$

where $S^2 = SS_E/(n-2)$ is the residual variance estimate.

## Worked Examples

**Example 1: Test $H_0: \\beta_1 = 0$, $\\hat{\\beta}_1 = 2.5$, $S/\\sqrt{S_{XX}} = 0.8$, $n=15$**

$T = 2.5/0.8 = 3.13$. $t_{13,0.025} = 2.16$. Reject — slope is significant.

---

**Example 2: 95% CI for $\\beta_1$**

$\\hat{\\beta}_1 \\pm t_{n-2,0.025} \\cdot S/\\sqrt{S_{XX}} = 2.5 \\pm 2.16(0.8) = (0.77, 4.23)$.

---

**Example 3: CI for mean response vs. prediction interval**

CI for $E[Y|X=x_0]$: narrower. Prediction interval for a new $Y$: wider (adds $\\sigma^2$ from $\\varepsilon$).

## Common Mistakes

- **Using df $= n-1$ instead of $n-2$.** Regression uses $n-2$ df (estimating 2 parameters).
- **Confusing CI for mean response with PI for a new observation.**

## Quick Check

1. df for $t$-test of $\\beta_1$ in SLR with $n=20$?
2. What does rejecting $H_0: \\beta_1 = 0$ imply?
3. Which is wider: CI for mean or PI for new obs?

*(Answers: 18; $X$ is a significant predictor of $Y$; PI)*
""",

"stat-mlr": """\
# Multiple Linear Regression

## Overview

**Multiple linear regression (MLR)** extends SLR to multiple predictors: $Y = \\beta_0 + \\beta_1 X_1 + \\cdots + \\beta_p X_p + \\varepsilon$. The OLS estimator and matrix formulas remain the same.

## Key Idea

$\\hat{\\boldsymbol{\\beta}} = (\\mathbf{X}^T\\mathbf{X})^{-1}\\mathbf{X}^T\\mathbf{Y}$.

$\\hat{\\beta}_j$ is the estimated change in $Y$ per unit increase in $X_j$, holding all other predictors fixed.

**Adjusted $R^2$** penalizes for the number of predictors: $R^2_{adj} = 1 - (1-R^2)(n-1)/(n-p-1)$.

## Worked Examples

**Example 1: Interpret $\\hat{\\beta}_1 = 2.5$ in a model with $X_1$ = hours studied and $X_2$ = prior GPA.**

Each extra hour of study is associated with a 2.5-point score increase, holding prior GPA constant.

---

**Example 2: Adding a useless predictor**

$R^2$ always increases when adding variables. Adjusted $R^2$ may decrease — signaling the variable is not useful.

---

**Example 3: Multicollinearity**

If predictors are highly correlated, $\\mathbf{X}^T\\mathbf{X}$ is near-singular, inflating standard errors. Check VIF (variance inflation factor).

## Common Mistakes

- **Interpreting coefficients marginally.** MLR coefficients are partial (holding others fixed).
- **Using $R^2$ to compare models with different numbers of predictors.** Use adjusted $R^2$ or AIC.

## Quick Check

1. $\\hat{\\beta}_j$ in MLR represents what?
2. Why prefer adjusted $R^2$ over $R^2$?
3. What is multicollinearity?

*(Answers: partial effect of $X_j$ controlling for others; it penalizes for more predictors; high correlation among predictors)*
""",

"stat-mlr-inference": """\
# MLR Inference

## Overview

In MLR, inference involves testing individual coefficients, testing groups of coefficients simultaneously (F-test), and constructing confidence intervals.

## Key Idea

Individual test: $T_j = \\hat{\\beta}_j / \\text{SE}(\\hat{\\beta}_j) \\sim t_{n-p-1}$ under $H_0: \\beta_j = 0$.

**Global F-test:** $H_0: \\beta_1 = \\cdots = \\beta_p = 0$:

$$F = \\frac{SS_R/p}{SS_E/(n-p-1)} \\sim F_{p, n-p-1}$$

## Worked Examples

**Example 1: $t$-test for $\\beta_1$**

$\\hat{\\beta}_1 = 3.2$, $\\text{SE} = 1.1$, $n=50$, $p=3$. $T = 3.2/1.1 = 2.91$. $t_{46,0.025} \\approx 2.01$. Reject.

---

**Example 2: Global F-test**

If the global $F$ is not significant, no individual predictors are likely significant.

---

**Example 3: Partial F-test**

Test whether adding 2 new predictors improves the model: $F = \\frac{(SS_{E,\\text{reduced}} - SS_{E,\\text{full}})/2}{SS_{E,\\text{full}}/(n-p-1)}$.

## Common Mistakes

- **Performing many individual $t$-tests without a global test.** Multiple comparisons inflate Type I error.
- **Wrong df.** $t_{n-p-1}$ has $n-p-1$ df ($p$ predictors, not counting intercept), or $n-p-1$ where $p$ includes intercept.

## Quick Check

1. df for individual $t$-test in MLR with $n=30$, 4 predictors (+ intercept)?
2. What does the global F-test test?
3. How do you test if two additional predictors improve model fit?

*(Answers: 25; whether ALL predictors together explain anything; partial F-test)*
""",

"stat-model-comparison": """\
# Model Comparison (AIC/BIC)

## Overview

**AIC** (Akaike Information Criterion) and **BIC** (Bayesian Information Criterion) balance model fit against complexity. They are used to select the best model when comparing nested or non-nested models.

## Key Idea

$$\\text{AIC} = -2\\ell(\\hat{\\theta}) + 2k, \\quad \\text{BIC} = -2\\ell(\\hat{\\theta}) + k\\ln n$$

where $\\ell(\\hat{\\theta})$ is the maximized log-likelihood and $k$ is the number of parameters. **Smaller is better.** BIC penalizes complexity more heavily for large $n$.

## Worked Examples

**Example 1: Two models, $\\ell_1 = -100$, $k_1 = 3$; $\\ell_2 = -98$, $k_2 = 5$, $n = 50$.**

$\\text{AIC}_1 = 206$, $\\text{AIC}_2 = 206$. $\\text{BIC}_1 = 200+3\\ln50 \\approx 211.7$, $\\text{BIC}_2 = 196+5\\ln50 \\approx 215.5$. BIC prefers model 1.

---

**Example 2: AIC vs. BIC**

AIC asymptotically selects the model with best predictive accuracy. BIC selects the true model (if in the candidate set) for large $n$.

---

**Example 3: Delta AIC**

$\\Delta\\text{AIC} < 2$: little evidence to prefer one model. $\\Delta\\text{AIC} > 10$: strong preference.

## Common Mistakes

- **Minimizing AIC/BIC from different datasets.** They are comparable only on the same data.
- **Using AIC to compare models with different response transformations** (e.g., $Y$ vs. $\\ln Y$).

## Quick Check

1. AIC formula?
2. Which penalizes extra parameters more for large $n$?
3. If $\\text{AIC}_1 < \\text{AIC}_2$, prefer which?

*(Answers: $-2\\ell+2k$; BIC; model 1)*
""",

"stat-regression-checks": """\
# Regression Diagnostics

## Overview

**Regression diagnostics** check whether the assumptions of linear regression (linearity, normality of errors, homoscedasticity, independence) are satisfied. Violations can invalidate inferences.

## Key Idea

Four key assumptions (LINE):
1. **L**inearity: $E[Y|X]$ is linear in $X$
2. **I**ndependence: residuals are independent
3. **N**ormality: residuals $\\sim N(0,\\sigma^2)$
4. **E**qual variance (homoscedasticity): $\\text{Var}(\\varepsilon_i) = \\sigma^2$

Check with residual plots, QQ-plots, and statistical tests.

## Worked Examples

**Example 1: Residual vs. fitted plot**

Random scatter around zero → OK. Fan-shaped → heteroscedasticity. Curved → non-linearity.

---

**Example 2: QQ-plot of residuals**

Points near the diagonal → normality. Heavy tails → violation.

---

**Example 3: Influential observations**

Cook's distance measures how much the estimates change if observation $i$ is removed. Cook's $D > 1$ is often flagged.

## Common Mistakes

- **Ignoring outliers without investigation.** An outlier may reveal a data error or an important phenomenon.
- **Concluding non-normality from small samples.** QQ-plots are unreliable for $n < 30$.

## Quick Check

1. What plot reveals heteroscedasticity?
2. What does a curved residual vs. fitted plot suggest?
3. What does Cook's distance measure?

*(Answers: residuals vs. fitted (fan shape); non-linearity; influence of each observation on $\\hat{\\boldsymbol{\\beta}}$)*
""",

"stat-bayes-posterior": """\
# Bayesian Posterior

## Overview

In **Bayesian statistics**, the parameter $\\theta$ is treated as a random variable. The **posterior distribution** $p(\\theta | \\text{data})$ combines the prior $p(\\theta)$ with the likelihood via Bayes' theorem to give updated beliefs about $\\theta$.

## Key Idea

$$p(\\theta | x) \\propto L(\\theta; x) \\cdot p(\\theta)$$

**Posterior $\\propto$ Likelihood $\\times$ Prior**

A **conjugate prior** is one where the posterior has the same family as the prior (e.g., Beta prior for Binomial likelihood gives Beta posterior).

## Worked Examples

**Example 1: Binomial likelihood, Beta prior**

$X|p \\sim \\text{Bin}(n,p)$, $p \\sim \\text{Beta}(\\alpha, \\beta)$.

Posterior: $p|X \\sim \\text{Beta}(\\alpha + X, \\beta + n - X)$.

---

**Example 2: Posterior mean**

With $n=10$, $X=7$, prior Beta$(1,1)$ (uniform): posterior Beta$(8,4)$, mean $= 8/12 = 2/3$.

---

**Example 3: Credible interval**

A 95% **credible interval** $[a,b]$ satisfies $P(a \\le \\theta \\le b | \\text{data}) = 0.95$. Direct probability statement about $\\theta$ — not the same as frequentist CI.

## Common Mistakes

- **Interpreting frequentist CI as Bayesian credible interval.** Only the Bayesian CI makes a direct probability statement about $\\theta$.
- **Choosing an informative prior without justification.**

## Quick Check

1. Posterior formula?
2. What is a conjugate prior?
3. Difference between 95% CI and 95% credible interval?

*(Answers: $p(\\theta|x) \\propto L(\\theta;x)p(\\theta)$; prior where posterior has same distributional form; CI is about procedure; credible interval is about $\\theta$ given data)*
""",

"stat-order-statistics": """\
# Order Statistics (Stat)

## Overview

In statistics, **order statistics** are used for non-parametric inference: estimating quantiles, constructing distribution-free confidence intervals, and building rank-based tests. This node covers their statistical applications.

## Key Idea

The $k$-th order statistic from an iid sample $X_1,\\ldots,X_n$ with CDF $F$ and PDF $f$ has PDF:

$$f_{X_{(k)}}(x) = \\frac{n!}{(k-1)!(n-k)!} F(x)^{k-1}[1-F(x)]^{n-k} f(x)$$

Sample quantile $\\hat{q}_p \\approx X_{(\\lceil np \\rceil)}$. For $F$ continuous, $F(X_{(k)}) \\sim \\text{Beta}(k, n-k+1)$.

## Worked Examples

**Example 1: Distribution-free CI for the median using order statistics**

For large $n$, use $X_{(n/2 \\pm z_{0.025}\\sqrt{n}/2)}$ as bounds — no assumption on $F$ needed.

---

**Example 2: Range $= X_{(n)} - X_{(1)}$**

PDF of range characterizes sample spread without parametric assumptions.

---

**Example 3: $P(X_{(1)} > t)$ for Exp$(\\lambda)$**

$P(\\min > t) = (1-F(t))^n = e^{-n\\lambda t}$, so $X_{(1)} \\sim \\text{Exp}(n\\lambda)$.

## Common Mistakes

- **Confusing order statistics with the raw sample moments.** Order statistics depend on the rank position.
- **Assuming order statistics are independent.** They are not (except extreme cases).

## Quick Check

1. What is the distribution of $F(X_{(k)})$ for continuous $F$?
2. Min of $n$ iid Exp$( \\lambda)$ has what distribution?
3. What is the sample median for $n=7$?

*(Answers: Beta$(k, n-k+1)$; Exp$(n\\lambda)$; $X_{(4)}$)*
""",

"stat-simulation": """\
# Monte Carlo Simulation

## Overview

**Monte Carlo simulation** uses random sampling to estimate quantities that are difficult to compute analytically — integrals, probabilities, expected values, and sampling distributions of complex estimators.

## Key Idea

To estimate $E[g(X)]$: generate $X_1, \\ldots, X_B$ from $F$, then:

$$\\hat{E} = \\frac{1}{B}\\sum_{b=1}^B g(X_b) \\xrightarrow{P} E[g(X)]$$

by the LLN. The error is $O(1/\\sqrt{B})$ regardless of dimension.

## Worked Examples

**Example 1: Estimate $\\pi$ via Monte Carlo**

Sample $(X,Y) \\sim U(-1,1)^2$. $\\pi/4 \\approx $ fraction with $X^2+Y^2 < 1$.

---

**Example 2: Estimate $\\int_0^1 e^{-x^2}\\,dx$**

Sample $X \\sim U(0,1)$, estimate $E[e^{-X^2}] \\approx \\frac{1}{B}\\sum e^{-X_b^2}$.

---

**Example 3: Simulate power of a test**

Generate data under $H_1$ many times. Fraction of times $H_0$ is rejected $\\approx$ power.

## Common Mistakes

- **Insufficient replicates.** Error $\\propto 1/\\sqrt{B}$; to halve error, quadruple $B$.
- **Using a poor random number generator.** Always use a well-tested PRNG.

## Quick Check

1. Monte Carlo error scales as?
2. How would you simulate a 95% CI coverage probability?
3. What fundamental theorem justifies Monte Carlo?

*(Answers: $O(1/\\sqrt{B})$; generate many datasets, compute CI each time, count fraction containing $\\theta$; Law of Large Numbers)*
""",

"stat-confounding": """\
# Confounding

## Overview

**Confounding** occurs when a third variable (the confounder) is associated with both the exposure and the outcome, creating a spurious or distorted association. Ignoring confounders leads to biased estimates of causal effects.

## Key Idea

A variable $C$ is a **confounder** if:
1. $C$ is associated with the exposure $X$
2. $C$ is associated with the outcome $Y$
3. $C$ is not on the causal pathway from $X$ to $Y$

Confounders cannot be removed by larger samples — only by study design (randomization) or statistical adjustment (regression, stratification).

## Worked Examples

**Example 1: Ice cream and drowning**

Both are associated, but both are caused by warm weather (the confounder). No causal relationship between ice cream and drowning.

---

**Example 2: Coffee and lung cancer**

Early studies found a link, but smokers drink more coffee. Smoking is the confounder.

---

**Example 3: Controlling for confounders**

Include the confounder in a regression model. $\\hat{\\beta}_X$ after adjustment estimates the effect of $X$ holding $C$ fixed.

## Common Mistakes

- **Adjusting for mediators.** A variable on the causal pathway should not be adjusted for.
- **Thinking observational studies can always be fixed with regression.** Unmeasured confounders remain a problem.

## Quick Check

1. Three criteria for confounding?
2. Best way to eliminate confounding at the design stage?
3. Can confounding be fixed by collecting more data?

*(Answers: associated with X, associated with Y, not a mediator; randomization; no — only by adjusting or better design)*
""",

"stat-causal-intro": """\
# Causal Inference: Introduction

## Overview

**Causal inference** aims to estimate the effect of an intervention, not just an association. The key challenge is that we can never observe both the treated and untreated outcome for the same unit — the **fundamental problem of causal inference**.

## Key Idea

**Potential outcomes framework:** For each unit $i$, let $Y_i(1)$ be the outcome if treated and $Y_i(0)$ if untreated. The causal effect is $Y_i(1) - Y_i(0)$.

The **Average Treatment Effect (ATE)**: $E[Y(1) - Y(0)]$.

Randomization ensures $Y(1), Y(0) \\perp T$ (treatment), so the ATE can be estimated by comparing group means.

## Worked Examples

**Example 1: Randomized experiment**

Randomly assign half to treatment. $E[\\bar{Y}_1 - \\bar{Y}_0] = \\text{ATE}$ because randomization balances confounders.

---

**Example 2: Observational study**

Without randomization, treated and control groups may differ on covariates. Simple mean difference is biased.

---

**Example 3: Propensity score**

Propensity score $e(x) = P(T=1|X=x)$. Conditioning on propensity score removes confounding due to $X$.

## Common Mistakes

- **Equating statistical association with causation.** Regression coefficients are not causal without additional assumptions.
- **Ignoring positivity assumption.** Every unit must have a nonzero probability of receiving either treatment.

## Quick Check

1. What is the fundamental problem of causal inference?
2. Why does randomization enable causal inference?
3. What is the ATE?

*(Answers: can't observe both $Y(1)$ and $Y(0)$ for same unit; it balances confounders so treatment is independent of potential outcomes; $E[Y(1)-Y(0)]$)*
""",

}  # end of LESSONS (final)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for node_id, content in LESSONS.items():
        path = os.path.join(OUTPUT_DIR, f"{node_id}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    print(f"Generated {len(LESSONS)} lesson files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
