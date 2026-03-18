# Central Limit Theorem

## Overview

The **Central Limit Theorem (CLT)** says that the standardized sum of iid random variables with finite variance converges in distribution to a standard normal, regardless of the original distribution. It is one of the most important results in probability.

## Key Idea

$X_1, \ldots, X_n$ iid with mean $\mu$, variance $\sigma^2 < \infty$. Then:

$$\frac{\sqrt{n}(\bar{X}_n - \mu)}{\sigma} \xrightarrow{d} N(0,1) \quad \text{as } n \to \infty$$

Equivalently: $\bar{X}_n \approx N(\mu, \sigma^2/n)$ for large $n$.

## Worked Examples

**Example 1: $X_i \sim U(0,1)$. Approximate distribution of $\bar{X}_{50}$.**

$\mu = 0.5$, $\sigma^2 = 1/12$. $\bar{X}_{50} \approx N(0.5, 1/600)$.

---

**Example 2: $P(\bar{X}_{100} > 55)$ for iid Exp$(0.01)$ ($\mu=100, \sigma=100$)**

$\bar{X}_{100} \approx N(100, 100)$. $Z = (55-100)/10 = -4.5$... (wait, $P(\bar{X}>55)$ — $Z=(55-100)/10=-4.5$, so $P\approx 1$). Actually $P(\bar{X}>105) = P(Z>0.5) \approx 0.31$.

---

**Example 3: How large must $n$ be?**

For many distributions, $n \ge 30$ is a common rule of thumb. For highly skewed distributions, larger $n$ may be needed.

## Common Mistakes

- **Applying CLT for very small $n$ or very skewed distributions.** The approximation quality depends on $n$ and the distribution.
- **Forgetting to standardize properly** — divide by $\sigma/\sqrt{n}$, not $\sigma$.

## Quick Check

1. $\bar{X}_n \approx N(?,?)$ for large $n$?
2. Why does the CLT matter for statistics?
3. Does CLT require the original distribution to be normal?

*(Answers: $N(\mu, \sigma^2/n)$; it justifies normal-based inference; no)*
