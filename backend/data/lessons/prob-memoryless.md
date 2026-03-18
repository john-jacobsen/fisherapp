# Memoryless Property

## Overview

The **memoryless property** means the past doesn't affect the future: given that you've already waited time $s$, the remaining wait is distributed the same as starting fresh. Only the Exponential (continuous) and Geometric (discrete) distributions have this property.

## Key Idea

$P(X > s + t \mid X > s) = P(X > t)$ for Exp$(\lambda)$ and Geom$(p)$.

This follows directly from the CDF: $P(X > s+t) = e^{-\lambda(s+t)} = e^{-\lambda s} e^{-\lambda t}$.

## Worked Examples

**Example 1: A component lasts $\text{Exp}(0.1)$ years. It has survived 3 years. $P(\text{surviving 2 more years})$?**

By memorylessness, this equals $P(X > 2) = e^{-0.2} \approx 0.819$.

---

**Example 2: Conditional computation directly**

$P(X > 5 | X > 3) = \frac{P(X>5)}{P(X>3)} = \frac{e^{-5\lambda}}{e^{-3\lambda}} = e^{-2\lambda} = P(X>2)$ ✓

---

**Example 3: Geometric has memoryless property**

Flip a coin until heads ($p = 0.4$). After 5 tails, $P(X > 8 | X > 5) = P(X > 3) = (0.6)^3$.

## Common Mistakes

- **Assuming all waiting-time distributions are memoryless.** Normal, Gamma, Weibull are not.
- **Confusing memoryless with "no aging" physically.** Mathematically, the surviving unit is statistically identical to a new one.

## Quick Check

1. $P(X > 4 | X > 2)$ for $\text{Exp}(1)$?
2. Is the Normal distribution memoryless?
3. For Geom$(p)$, $P(X > m+n | X > m) = ?$

*(Answers: $e^{-2}$; no; $(1-p)^n = P(X > n)$)*
