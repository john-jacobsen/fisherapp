# Exponential Distribution

## Overview

The **Exponential distribution** models the time between events in a Poisson process. It is the continuous analogue of the Geometric distribution and is widely used to model lifetimes and waiting times.

## Key Idea

$X \sim \text{Exp}(\lambda)$ (rate parameter $\lambda > 0$):

$$f(x) = \lambda e^{-\lambda x}, \quad x \ge 0, \qquad F(x) = 1 - e^{-\lambda x}$$

$$E[X] = \frac{1}{\lambda}, \quad \text{Var}(X) = \frac{1}{\lambda^2}$$

## Worked Examples

**Example 1: $\lambda = 2$ (avg 0.5 units between events). $P(X > 1)$?**

$P(X > 1) = e^{-2} \approx 0.135$.

---

**Example 2: Avg lifetime of a bulb is 1000 hours ($\lambda = 0.001$). $P(X > 500)$?**

$P(X > 500) = e^{-0.5} \approx 0.607$.

---

**Example 3: Median of $\text{Exp}(\lambda)$**

$F(m) = 1/2 \Rightarrow 1 - e^{-\lambda m} = 1/2 \Rightarrow m = \ln 2/\lambda$.

## Common Mistakes

- **Confusing $\lambda$ as rate vs. mean.** $\lambda = 2$ means rate = 2 events per unit time, mean = 1/2.
- **Applying exponential to non-continuous or non-memoryless situations.**

## Quick Check

1. $E[X]$ for $\text{Exp}(5)$?
2. $P(X > 2)$ for $\text{Exp}(1)$?
3. $F(3)$ for $\text{Exp}(2)$?

*(Answers: 1/5; $e^{-2}$; $1-e^{-6}$)*
