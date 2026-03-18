# Inverse CDF / Quantile Function

## Overview

The **quantile function** (inverse CDF) $F^{-1}(p)$ returns the value $x$ such that $P(X \le x) = p$. It is used to find percentiles and to generate random samples from any distribution.

## Key Idea

$$F^{-1}(p) = \inf\{x : F(x) \ge p\}, \quad 0 < p < 1$$

**Inverse CDF sampling:** If $U \sim U(0,1)$, then $X = F^{-1}(U)$ has distribution $F$.

## Worked Examples

**Example 1: Median of $\text{Exp}(\lambda)$**

$F(m) = 0.5 \Rightarrow 1 - e^{-\lambda m} = 0.5 \Rightarrow m = \ln 2 / \lambda$.

---

**Example 2: 90th percentile of $N(0,1)$**

$F^{-1}(0.9) = z_{0.9} \approx 1.282$ (from $Z$-table).

---

**Example 3: Generate Exp(1) samples from Uniform**

$U \sim U(0,1)$. $F^{-1}(u) = -\ln(1-u)$. Compute $X = -\ln(1-U)$ — this follows Exp(1).

## Common Mistakes

- **Confusing percentile with percentage.** The 90th percentile is a value $x$, not a probability.
- **Inverse CDF requires $F$ to be invertible.** For discrete distributions, use generalized inverse.

## Quick Check

1. Median of $U(0,1)$?
2. 25th percentile of $N(0,1)$?
3. What does $F^{-1}(0.5)$ always equal?

*(Answers: 0.5; $\approx -0.674$; median)*
