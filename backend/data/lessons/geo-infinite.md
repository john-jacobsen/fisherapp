# Infinite Geometric Series

## Overview

When a geometric series goes on forever with $|r| < 1$, the terms shrink toward zero and the series converges to a finite sum. For $|r| \ge 1$, the series diverges.

## Key Idea

$$S_\infty = \frac{a_1}{1 - r} \quad \text{provided } |r| < 1$$

This comes from taking $n \to \infty$ in the finite formula: $r^n \to 0$ when $|r| < 1$.

## Worked Examples

**Example 1: $\sum_{k=0}^{\infty} \left(\frac{1}{2}\right)^k$**

$a_1 = 1$, $r = 1/2$:

$$S = \frac{1}{1 - 1/2} = 2$$

---

**Example 2: $\sum_{k=0}^{\infty} 3\left(\frac{2}{3}\right)^k$**

$$S = \frac{3}{1 - 2/3} = \frac{3}{1/3} = 9$$

---

**Example 3: Write $0.\overline{3}$ as a fraction**

$0.333\ldots = 3/10 + 3/100 + \cdots$. Here $a_1 = 3/10$, $r = 1/10$:

$$S = \frac{3/10}{1 - 1/10} = \frac{3/10}{9/10} = \frac{1}{3}$$

## Common Mistakes

- **Applying the formula when $|r| \ge 1$.** Series with $|r| \ge 1$ diverge.
- **Confusing $a_1$ with the first term written.** If the sum starts at $k=0$, then $a_1$ is that first term.

## Quick Check

1. $\sum_{k=0}^{\infty}(0.1)^k$
2. $4 + 2 + 1 + 0.5 + \cdots$
3. Write $0.\overline{9}$ as a fraction using geometric series.

*(Answers: 10/9; 8; 1)*
