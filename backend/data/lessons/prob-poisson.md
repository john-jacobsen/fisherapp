# Poisson Distribution

## Overview

The **Poisson distribution** models the number of rare events in a fixed time or space interval, when events occur independently at a constant average rate $\lambda$.

## Key Idea

$X \sim \text{Poisson}(\lambda)$:

$$P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}, \quad k = 0, 1, 2, \ldots$$

$$E[X] = \lambda, \quad \text{Var}(X) = \lambda$$

The mean equals the variance — a hallmark of the Poisson.

## Worked Examples

**Example 1: On average 3 customers arrive per minute. $P(X = 5)$?**

$$P(X=5) = \frac{e^{-3} 3^5}{5!} = \frac{e^{-3} \cdot 243}{120} \approx 0.101$$

---

**Example 2: $P(X = 0)$ for $\lambda = 2$?**

$e^{-2} \approx 0.135$.

---

**Example 3: $P(X \ge 1)$ for $\lambda = 1$?**

$P(X \ge 1) = 1 - P(X=0) = 1 - e^{-1} \approx 0.632$.

## Common Mistakes

- **Using Poisson with a non-rare event.** It works when $n$ is large and $p$ is small.
- **Forgetting $k!$ in the denominator.**

## Quick Check

1. $P(X=0)$ for $\text{Pois}(3)$?
2. $E[X]$ and $\text{Var}(X)$ for $\text{Pois}(5)$?
3. $P(X=2)$ for $\lambda=1$?

*(Answers: $e^{-3}\approx0.050$; both 5; $e^{-1}/2\approx0.184$)*
