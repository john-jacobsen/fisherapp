# Order Statistics (Stat)

## Overview

In statistics, **order statistics** are used for non-parametric inference: estimating quantiles, constructing distribution-free confidence intervals, and building rank-based tests. This node covers their statistical applications.

## Key Idea

The $k$-th order statistic from an iid sample $X_1,\ldots,X_n$ with CDF $F$ and PDF $f$ has PDF:

$$f_{X_{(k)}}(x) = \frac{n!}{(k-1)!(n-k)!} F(x)^{k-1}[1-F(x)]^{n-k} f(x)$$

Sample quantile $\hat{q}_p \approx X_{(\lceil np \rceil)}$. For $F$ continuous, $F(X_{(k)}) \sim \text{Beta}(k, n-k+1)$.

## Worked Examples

**Example 1: Distribution-free CI for the median using order statistics**

For large $n$, use $X_{(n/2 \pm z_{0.025}\sqrt{n}/2)}$ as bounds — no assumption on $F$ needed.

---

**Example 2: Range $= X_{(n)} - X_{(1)}$**

PDF of range characterizes sample spread without parametric assumptions.

---

**Example 3: $P(X_{(1)} > t)$ for Exp$(\lambda)$**

$P(\min > t) = (1-F(t))^n = e^{-n\lambda t}$, so $X_{(1)} \sim \text{Exp}(n\lambda)$.

## Common Mistakes

- **Confusing order statistics with the raw sample moments.** Order statistics depend on the rank position.
- **Assuming order statistics are independent.** They are not (except extreme cases).

## Quick Check

1. What is the distribution of $F(X_{(k)})$ for continuous $F$?
2. Min of $n$ iid Exp$( \lambda)$ has what distribution?
3. What is the sample median for $n=7$?

*(Answers: Beta$(k, n-k+1)$; Exp$(n\lambda)$; $X_{(4)}$)*
