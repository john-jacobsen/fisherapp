# Expected Value

## Overview

The **expected value** (mean) of a random variable $X$ is its probability-weighted average. It represents the long-run average if you repeated the experiment many times.

## Key Idea

For discrete $X$:

$$E[X] = \sum_x x \cdot P(X = x)$$

For continuous $X$ with density $f$:

$$E[X] = \int_{-\infty}^{\infty} x\, f(x)\, dx$$

Linearity: $E[aX + b] = aE[X] + b$.

## Worked Examples

**Example 1: Fair die. $E[X]$?**

$$E[X] = \frac{1}{6}(1+2+3+4+5+6) = 3.5$$

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
