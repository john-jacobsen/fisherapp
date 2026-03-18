# Poisson Approximation to Binomial

## Overview

When $n$ is large and $p$ is small, the **Binomial$(n,p)$** distribution is well-approximated by **Poisson$( \lambda = np)$**. This avoids computing large binomial coefficients.

## Key Idea

$\text{Bin}(n,p) \approx \text{Pois}(np)$ when $n \to \infty$ and $p \to 0$ with $np = \lambda$ fixed.

Rule of thumb: use this approximation when $n \ge 20$ and $p \le 0.05$.

## Worked Examples

**Example 1: $n=100$, $p=0.02$. $P(X=3)$ via Poisson.**

$\lambda = 2$. $P(X=3) = e^{-2}(2)^3/3! = 8e^{-2}/6 \approx 0.180$.

---

**Example 2: Number of typos per page**

If a book has 500 characters per page and each has a 0.001 chance of being a typo, $\lambda = 0.5$. $P(0 \text{ typos}) = e^{-0.5} \approx 0.607$.

---

**Example 3: Compare Binomial and Poisson for $n=50, p=0.02, k=2$**

Exact: $\binom{50}{2}(0.02)^2(0.98)^{48} \approx 0.184$. Poisson ($\lambda=1$): $e^{-1}/2 \approx 0.184$. Close!

## Common Mistakes

- **Using the approximation when $p$ is large.** If $p = 0.4$, use Binomial directly.
- **Forgetting $\lambda = np$, not $n$ alone.**

## Quick Check

1. $n=200$, $p=0.01$. What is $\lambda$?
2. $P(X=0)$ for the approximation above?
3. When is the approximation accurate?

*(Answers: 2; $e^{-2}\approx0.135$; $n$ large, $p$ small, $np$ moderate)*
