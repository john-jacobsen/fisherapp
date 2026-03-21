# Quadratic Equations

## Overview

A **quadratic equation** is any equation that can be written in the form $ax^2 + bx + c = 0$ where $a \ne 0$. The presence of the $x^2$ term means the equation can have up to two solutions. Your two main tools are factoring (fast when it works) and the quadratic formula (always works).

## Key Idea

The **quadratic formula** solves any equation in standard form $ax^2 + bx + c = 0$:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

The expression under the radical, $\Delta = b^2 - 4ac$, is called the **discriminant**. If $\Delta > 0$ there are two real solutions; if $\Delta = 0$ there is exactly one; if $\Delta < 0$ there are no real solutions.

## Worked Examples

**Example 1: Solve $x^2 - 5x + 6 = 0$ by factoring**

Factoring works when you can find two integers that multiply to $c = 6$ and add to $b = -5$. Those integers are $-2$ and $-3$ because $(-2)(-3) = 6$ and $(-2) + (-3) = -5$.

Write the factored form:

$$(x - 2)(x - 3) = 0$$

A product equals zero when at least one factor equals zero — this is the Zero Product Property. Set each factor to zero:

$$x - 2 = 0 \implies x = 2 \qquad x - 3 = 0 \implies x = 3$$

Both values satisfy the original equation, so there are two solutions: $x = 2$ or $x = 3$.

---

**Example 2: Solve $2x^2 + 3x - 2 = 0$ using the quadratic formula**

Factoring is less obvious here, so use the formula. Identify the coefficients: $a = 2$, $b = 3$, $c = -2$.

Compute the discriminant first — it tells you how many solutions to expect before you finish the calculation:

$$\Delta = b^2 - 4ac = 9 - 4(2)(-2) = 9 + 16 = 25$$

Since $\Delta = 25 > 0$, you know there are two distinct real solutions. Now apply the formula:

$$x = \frac{-3 \pm \sqrt{25}}{2(2)} = \frac{-3 \pm 5}{4}$$

Split into the two cases:

$$x = \frac{-3 + 5}{4} = \frac{2}{4} = \frac{1}{2} \qquad \text{or} \qquad x = \frac{-3 - 5}{4} = \frac{-8}{4} = -2$$

---

**Example 3: Solve $x^2 - 4x + 4 = 0$**

Check the discriminant: $\Delta = (-4)^2 - 4(1)(4) = 16 - 16 = 0$. A discriminant of zero means there is exactly one solution — the two roots coincide. This equation is a perfect square:

$$(x - 2)^2 = 0 \implies x = 2$$

Alternatively, using the formula confirms it: $x = \frac{4 \pm 0}{2} = 2$.

## Common Mistakes

- **Forgetting the $\pm$ in the formula.** The $\pm$ is what produces two solutions — dropping it gives you only half the answer.
- **Misidentifying $a$, $b$, $c$ when the equation is not in standard form.** Always rearrange to $ax^2 + bx + c = 0$ before reading off the coefficients.
- **Sign error on $b$.** The formula starts with $-b$, not $b$. If $b = -4$, then $-b = 4$.

## Quick Check

1. Solve $x^2 - x - 6 = 0$ by factoring.
2. Solve $x^2 + 2x - 8 = 0$.
3. Use the quadratic formula to solve $x^2 - 2x - 3 = 0$.

*(Answers: $x = 3$ or $x = -2$; $x = 2$ or $x = -4$; $x = 3$ or $x = -1$)*
