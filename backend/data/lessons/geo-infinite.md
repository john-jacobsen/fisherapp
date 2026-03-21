# Infinite Geometric Series

## Overview

An **infinite geometric series** is a geometric series that never stops. Surprisingly, when the common ratio satisfies $|r| < 1$, the terms shrink fast enough that the infinite sum converges to a single finite number. When $|r| \ge 1$, the terms do not shrink and the sum grows without bound — it diverges.

## Key Idea

$$S = \frac{a_1}{1 - r} \qquad \text{provided } |r| < 1$$

**Why this works.** Recall the finite sum formula: $S_n = a_1 \cdot \dfrac{1 - r^n}{1 - r}$. Now take $n \to \infty$. When $|r| < 1$, the term $r^n$ approaches $0$ because you are repeatedly multiplying a number smaller than 1 by itself. Substituting $r^n = 0$ gives:

$$S = a_1 \cdot \frac{1 - 0}{1 - r} = \frac{a_1}{1 - r}$$

When $|r| \ge 1$, the term $r^n$ does not shrink — it stays at 1 or grows larger — so the formula breaks down and the series has no finite sum.

**Real-world intuition.** Imagine walking toward a wall by repeatedly covering half the remaining distance. After the 1st step you have covered $\frac{1}{2}$ of the total distance; after the 2nd step, $\frac{3}{4}$; after the 3rd, $\frac{7}{8}$. The series $\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \cdots$ sums to exactly 1 — you eventually reach the wall, even though the steps go on forever.

## Worked Examples

**Example 1: Compute $\displaystyle\sum_{k=0}^{\infty} \left(\frac{1}{2}\right)^k$.**

The first term ($k = 0$) is $\left(\frac{1}{2}\right)^0 = 1$, so $a_1 = 1$. The ratio is $r = \frac{1}{2}$, and since $|r| = \frac{1}{2} < 1$, the series converges.

$$S = \frac{1}{1 - \tfrac{1}{2}} = \frac{1}{\tfrac{1}{2}} = 2$$

This matches the wall-walking intuition: $\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \cdots = 1$ for the first term alone would only give 1 if $a_1 = \frac{1}{2}$, but here the first term is 1, giving the full sum of 2.

---

**Example 2: Compute $\displaystyle\sum_{k=0}^{\infty} 3\left(\frac{2}{3}\right)^k$.**

Here $a_1 = 3$ (the value at $k = 0$) and $r = \frac{2}{3}$. Since $\frac{2}{3} < 1$, the series converges.

$$S = \frac{3}{1 - \tfrac{2}{3}} = \frac{3}{\tfrac{1}{3}} = 3 \times 3 = 9$$

Each term is $\frac{2}{3}$ of the previous one, so the terms are $3, 2, \frac{4}{3}, \frac{8}{9}, \ldots$ — shrinking steadily toward 0, summing to 9.

---

**Example 3: Express the repeating decimal $0.\overline{3} = 0.3333\ldots$ as a fraction.**

Write the decimal as a sum: $0.\overline{3} = \frac{3}{10} + \frac{3}{100} + \frac{3}{1000} + \cdots$

This is a geometric series with $a_1 = \frac{3}{10}$ and $r = \frac{1}{10}$. Since $\frac{1}{10} < 1$, it converges:

$$S = \frac{\tfrac{3}{10}}{1 - \tfrac{1}{10}} = \frac{\tfrac{3}{10}}{\tfrac{9}{10}} = \frac{3}{10} \times \frac{10}{9} = \frac{3}{9} = \frac{1}{3}$$

This confirms that $0.\overline{3} = \frac{1}{3}$ — the infinite sum genuinely equals the fraction.

## Common Mistakes

- **Applying the formula when $|r| \ge 1$.** The series $1 + 2 + 4 + \cdots$ diverges; plugging into $\frac{a_1}{1-r}$ gives $\frac{1}{-1} = -1$, which is meaningless. Always check $|r| < 1$ first.
- **Confusing $a_1$ with the written coefficient.** If the sum starts at $k = 1$ rather than $k = 0$, the first term changes. Read the lower limit of the sum carefully.
- **Forgetting that $r$ can be negative.** A series like $1 - \frac{1}{2} + \frac{1}{4} - \cdots$ has $r = -\frac{1}{2}$, and $|-\frac{1}{2}| < 1$, so it still converges: $S = \frac{1}{1-(-\frac{1}{2})} = \frac{2}{3}$.

## Quick Check

1. Compute $\displaystyle\sum_{k=0}^{\infty} (0.1)^k$.
2. Find the sum of $4 + 2 + 1 + 0.5 + \cdots$
3. Use the geometric series formula to show that $0.\overline{9} = 1$.

*(Answers: $\frac{10}{9}$; 8; $a_1 = \frac{9}{10}$, $r = \frac{1}{10}$, $S = \frac{9/10}{9/10} = 1$)*
