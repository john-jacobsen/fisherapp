# Equations with Fractions

## Overview

Equations containing fractions can look intimidating, but there is a technique that removes all the fractions at once: **multiply both sides by the least common denominator (LCD)**. After that, you have a normal equation with whole numbers.

## Key Idea

Multiplying both sides of an equation by the same nonzero number preserves equality — it does not change the solution. When that number is the LCD of all the denominators, every fraction in the equation becomes a whole number.

$$\frac{x}{a} + \frac{b}{c} = d \xrightarrow{\times \text{ LCD}} \text{integer equation} \rightarrow \text{solve normally}$$

The LCD is the smallest number that all denominators divide into evenly. Multiplying a fraction $\frac{p}{q}$ by LCD gives $\frac{p \cdot \text{LCD}}{q}$, which is a whole number because LCD is a multiple of $q$.

## Worked Examples

**Example 1: Solve $\dfrac{x}{3} + 2 = 5$**

The only denominator is 3, so the LCD is 3. Multiply every term on both sides by 3. On the left: $3 \cdot \frac{x}{3} = x$ and $3 \cdot 2 = 6$. On the right: $3 \cdot 5 = 15$. The fractions are gone, leaving a simple one-step equation.

$$3 \cdot \frac{x}{3} + 3 \cdot 2 = 3 \cdot 5 \implies x + 6 = 15 \implies x = 9$$

Check: $\frac{9}{3} + 2 = 3 + 2 = 5$. Correct.

---

**Example 2: Solve $\dfrac{x}{4} + \dfrac{1}{2} = \dfrac{3}{4}$**

The denominators are 4 and 2. The LCD is 4 because 4 is divisible by both 4 and 2. Multiply every term by 4: $4 \cdot \frac{x}{4} = x$, $4 \cdot \frac{1}{2} = 2$, $4 \cdot \frac{3}{4} = 3$. Now solve the resulting whole-number equation.

$$x + 2 = 3 \implies x = 1$$

Check: $\frac{1}{4} + \frac{1}{2} = \frac{1}{4} + \frac{2}{4} = \frac{3}{4}$. Correct.

---

**Example 3: Solve $\dfrac{x + 1}{3} = \dfrac{x - 1}{2}$**

The denominators are 3 and 2, so the LCD is 6. Multiply every term by 6. On the left: $6 \cdot \frac{x+1}{3} = 2(x+1)$. On the right: $6 \cdot \frac{x-1}{2} = 3(x-1)$. Distribute, then collect $x$ terms on one side.

$$2(x + 1) = 3(x - 1) \implies 2x + 2 = 3x - 3 \implies 5 = x$$

Check: $\frac{6}{3} = 2$ and $\frac{4}{2} = 2$. Correct.

## Common Mistakes

- **Multiplying only some terms by the LCD, not all.** Every single term on both sides must be multiplied. Missing even one term produces an incorrect equation.
- **Forgetting to distribute when the numerator contains a sum.** In $\frac{x+1}{3}$, multiplying by 6 gives $2(x+1) = 2x + 2$, not $2x + 1$. The LCD multiplies the entire numerator.
- **Finding a common denominator instead of the LCD.** Any common multiple works mathematically, but using the LCD keeps the numbers as small as possible and reduces arithmetic errors.

## Quick Check

1. Solve $\dfrac{x}{5} + 1 = 4$
2. Solve $\dfrac{x}{6} + \dfrac{1}{3} = 1$
3. Solve $\dfrac{x+2}{4} = \dfrac{x-1}{3}$

*(Answers: $x = 15$, $x = 4$, $x = 10$)*
