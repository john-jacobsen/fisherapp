# Radical Equations

## Overview

A **radical equation** contains the variable inside a radical. The strategy is to isolate the radical, then raise both sides to the power that matches the index — squaring for square roots, cubing for cube roots, etc. This removes the radical but can introduce extraneous solutions, so checking is not optional.

## Key Idea

Isolate the radical, then eliminate it by raising to the $n$-th power:

$$\sqrt[n]{f(x)} = g(x) \implies f(x) = [g(x)]^n$$

Always substitute your solutions back into the original equation. Squaring both sides is valid, but it can turn a false equation (like $\sqrt{x} = -3$) into a true one ($x = 9$), creating a solution that does not actually work.

## Worked Examples

**Example 1: Solve $\sqrt{x - 1} = 4$**

The radical is already isolated. Square both sides:

$$x - 1 = 16 \implies x = 17$$

Check in the original: $\sqrt{17 - 1} = \sqrt{16} = 4$ ✓. The solution is $x = 17$.

---

**Example 2: Solve $\sqrt{2x + 3} - 1 = 4$**

Isolate the radical first — add 1 to both sides:

$$\sqrt{2x + 3} = 5$$

Now square: $2x + 3 = 25 \implies 2x = 22 \implies x = 11$.

Check: $\sqrt{2(11) + 3} - 1 = \sqrt{25} - 1 = 5 - 1 = 4$ ✓.

---

**Example 3: Solve $\sqrt{x + 5} = x - 1$**

The radical is isolated. Square both sides:

$$x + 5 = (x-1)^2 = x^2 - 2x + 1$$

Rearrange: $0 = x^2 - 3x - 4 = (x-4)(x+1)$.

So $x = 4$ or $x = -1$. Check both:
- $x = 4$: $\sqrt{9} = 3$ and $4 - 1 = 3$ ✓
- $x = -1$: $\sqrt{4} = 2$ but $-1 - 1 = -2$ ✗ (extraneous — the square root is positive, the right side is negative)

The only solution is $x = 4$.

## Common Mistakes

- **Not checking for extraneous solutions.** Squaring both sides of $\sqrt{x} = -3$ gives $x = 9$, but $\sqrt{9} = 3 \ne -3$. The check is mandatory, not optional.
- **Squaring before isolating.** If you square $\sqrt{2x+3} - 1 = 4$ directly, you get the messy expression $(\sqrt{2x+3} - 1)^2 = 16$, which still contains a radical. Isolate first.
- **Squaring incorrectly on the right side.** $(x - 1)^2 = x^2 - 2x + 1$, not $x^2 - 1$. Always fully expand the squared binomial.

## Quick Check

Try these before using hints:

1. Solve $\sqrt{x} = 5$
2. Solve $\sqrt{3x - 2} = 4$
3. Solve $\sqrt{x + 3} = x - 3$

*(Answers: $x = 25$; $x = 6$; $x = 6$ only — $x = 1$ is extraneous)*
