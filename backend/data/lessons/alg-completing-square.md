# Completing the Square

## Overview

**Completing the square** is a technique that rewrites a quadratic $x^2 + bx + c$ into vertex form $(x - h)^2 + k$. It works by adding a carefully chosen constant to create a perfect square trinomial, then compensating for what you added. This technique also underlies the derivation of the quadratic formula and is essential for identifying the vertex of a parabola.

## Key Idea

The key identity: $x^2 + bx + \left(\frac{b}{2}\right)^2$ is a perfect square. So add and subtract $\left(\frac{b}{2}\right)^2$:

$$x^2 + bx = \left(x + \frac{b}{2}\right)^2 - \left(\frac{b}{2}\right)^2$$

The $-\left(\frac{b}{2}\right)^2$ compensates for what you added, ensuring the expression's value is unchanged.

## Worked Examples

**Example 1: Complete the square for $x^2 + 6x$**

Here $b = 6$, so $\left(\frac{b}{2}\right)^2 = \left(3\right)^2 = 9$.

Add and subtract 9:

$$x^2 + 6x = x^2 + 6x + 9 - 9 = (x + 3)^2 - 9$$

Check: expand $(x+3)^2 - 9 = x^2 + 6x + 9 - 9 = x^2 + 6x$ ✓

---

**Example 2: Write $x^2 - 4x + 7$ in vertex form**

Here $b = -4$, so $\left(\frac{-4}{2}\right)^2 = 4$.

$$x^2 - 4x + 7 = (x^2 - 4x + 4) - 4 + 7 = (x - 2)^2 + 3$$

The vertex of the parabola is at $(h, k) = (2, 3)$. The form $(x - h)^2 + k$ has a subtraction inside, so $(x - 2)^2$ corresponds to $h = +2$.

---

**Example 3: Solve $x^2 + 6x + 5 = 0$ by completing the square**

Move the constant to the right: $x^2 + 6x = -5$. Complete the square with $\left(\frac{6}{2}\right)^2 = 9$:

$$x^2 + 6x + 9 = -5 + 9 \implies (x + 3)^2 = 4$$

Add 9 to both sides (crucial: you add to both sides when solving an equation). Take square roots:

$$x + 3 = \pm 2 \implies x = -1 \text{ or } x = -5$$

## Common Mistakes

- **Forgetting to subtract what you added.** When completing the square in an expression (not an equation), you must both add and subtract $\left(\frac{b}{2}\right)^2$. Adding only 9 to $x^2 + 6x$ changes the expression's value.
- **Not dividing by $a$ first when $a \ne 1$.** To complete the square on $2x^2 + 8x + 3$, first factor out 2: $2(x^2 + 4x) + 3$. Then complete the square inside the parentheses.
- **Sign error in vertex form.** $(x - h)^2 + k$ with $h = 2$ comes from $(x - 2)^2$. If your expression is $(x + 3)^2 - 9$, the vertex is at $x = -3$, not $+3$.

## Quick Check

Try these before using hints:

1. Complete the square: $x^2 + 8x$
2. Find the vertex of $x^2 - 10x + 22$
3. Solve $x^2 + 2x - 8 = 0$ by completing the square

*(Answers: $(x+4)^2 - 16$; $(5, -3)$; $x = 2$ or $x = -4$)*
