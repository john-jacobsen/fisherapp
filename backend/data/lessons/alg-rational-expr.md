# Rational Expressions

## Overview

A **rational expression** is a ratio of two polynomials, like $\frac{x^2 - 4}{x + 3}$. You work with rational expressions using the same rules as numeric fractions: factor completely, cancel common factors, find common denominators. The critical difference from numeric fractions is that you must identify which values of $x$ make the denominator zero — those values are excluded from the domain.

## Key Idea

To simplify a rational expression, factor numerator and denominator completely, then cancel any common factors:

$$\frac{p(x) \cdot r(x)}{q(x) \cdot r(x)} = \frac{p(x)}{q(x)}, \quad x \ne \text{zeros of } r(x)$$

The excluded values must always be stated — they are part of the answer even after cancellation.

## Worked Examples

**Example 1: Simplify $\frac{x^2 - 9}{x^2 - x - 6}$**

Factor completely. Numerator: $x^2 - 9 = (x-3)(x+3)$ (difference of squares). Denominator: $x^2 - x - 6 = (x-3)(x+2)$ (two numbers with product $-6$ and sum $-1$).

$$\frac{(x-3)(x+3)}{(x-3)(x+2)} = \frac{x+3}{x+2}, \quad x \ne 3 \text{ and } x \ne -2$$

$x \ne 3$ because the original denominator was zero there; $x \ne -2$ because $x + 2 = 0$ in the simplified form.

---

**Example 2: Multiply $\frac{2x}{x+1} \cdot \frac{x^2-1}{4x^2}$**

Factor before multiplying. $x^2 - 1 = (x-1)(x+1)$. Then:

$$\frac{2x \cdot (x-1)(x+1)}{(x+1) \cdot 4x^2} = \frac{2x(x-1)(x+1)}{4x^2(x+1)}$$

Cancel $2x$ from top and bottom (yielding $\frac{1}{2x}$) and cancel $(x+1)$:

$$= \frac{x-1}{2x}, \quad x \ne 0 \text{ and } x \ne -1$$

---

**Example 3: Add $\frac{1}{x} + \frac{2}{x+1}$**

The denominators are $x$ and $x+1$ — they share no common factor, so the LCD is $x(x+1)$. Rewrite each fraction:

$$\frac{x+1}{x(x+1)} + \frac{2x}{x(x+1)} = \frac{x+1+2x}{x(x+1)} = \frac{3x+1}{x(x+1)}$$

The numerators simply add once the denominators match, just as with numeric fractions.

## Common Mistakes

- **Canceling terms instead of factors.** In $\frac{x+3}{x+5}$, there is no cancellation — you can only cancel factors that multiply the entire numerator or denominator. Since $x$ is part of a sum (not a product), it cannot be canceled.
- **Forgetting domain restrictions after canceling.** Canceling $(x-3)$ removes it from view but does not restore $x = 3$ to the domain — the original expression was undefined there.
- **Incorrect LCD.** When denominators share common factors (e.g., $x^2$ and $x$), the LCD is $x^2$, not $x^3$. Use the least common multiple, not the product.

## Quick Check

Try these before using hints:

1. Simplify $\frac{2x+4}{x^2-4}$
2. Simplify $\frac{x^2+5x+6}{x+3}$
3. Add $\frac{1}{x-1} + \frac{1}{x+1}$

*(Answers: $\frac{2}{x-2}$, $x \ne \pm2$; $x+2$, $x \ne -3$; $\frac{2x}{x^2-1}$)*
