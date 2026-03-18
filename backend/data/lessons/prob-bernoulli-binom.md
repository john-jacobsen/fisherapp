# Bernoulli and Binomial Distributions

## Overview

A **Bernoulli** trial is a single experiment with two outcomes (success/failure) with probability $p$. The **Binomial distribution** counts successes in $n$ independent Bernoulli trials.

## Key Idea

$X \sim \text{Binomial}(n, p)$:

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0,1,\ldots,n$$

$$E[X] = np, \quad \text{Var}(X) = np(1-p)$$

## Worked Examples

**Example 1: Flip a fair coin 5 times. $P(X = 3)$?**

$$\binom{5}{3}(0.5)^3(0.5)^2 = 10 \cdot (0.5)^5 = 10/32 = 5/16$$

---

**Example 2: 10 free throws, $p = 0.7$. Expected number made?**

$E[X] = 10(0.7) = 7$.

---

**Example 3: $P(X \ge 1)$ for $\text{Bin}(5, 0.2)$**

$P(X \ge 1) = 1 - P(X=0) = 1 - (0.8)^5 = 1 - 0.328 = 0.672$.

## Common Mistakes

- **Forgetting the $\binom{n}{k}$ factor.** Order matters for counting the arrangements.
- **Using Binomial when trials are not independent.** Sampling without replacement requires Hypergeometric.

## Quick Check

1. $P(X=0)$ for $\text{Bin}(3, 0.5)$?
2. $E[X]$ for $\text{Bin}(20, 0.3)$?
3. $\text{Var}(X)$ for $\text{Bin}(10, 0.4)$?

*(Answers: 1/8; 6; 2.4)*
