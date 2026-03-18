# Sampling Distributions

## Overview

The **sampling distribution** of a statistic is the distribution of that statistic over all possible samples of size $n$ from a population. It describes how the statistic varies from sample to sample.

## Key Idea

For iid $X_1,\ldots,X_n$ with mean $\mu$ and variance $\sigma^2$:

$$E[\bar{X}] = \mu, \quad \text{Var}(\bar{X}) = \frac{\sigma^2}{n}, \quad \text{SE}(\bar{X}) = \frac{\sigma}{\sqrt{n}}$$

By the CLT, $\bar{X} \approx N(\mu, \sigma^2/n)$ for large $n$.

## Worked Examples

**Example 1: $X_i \sim N(10, 4)$, $n=25$. Distribution of $\bar{X}$?**

$\bar{X} \sim N(10, 4/25) = N(10, 0.16)$.

---

**Example 2: $P(\bar{X} > 10.5)$ from Example 1**

$Z = (10.5 - 10)/0.4 = 1.25$. $P(Z > 1.25) \approx 0.106$.

---

**Example 3: Effect of sample size**

Doubling $n$ reduces $\text{SE}$ by factor $\sqrt{2}$, not 2. Precision grows slowly.

## Common Mistakes

- **Confusing the population SD with the SE.** $\text{SE} = \sigma/\sqrt{n}$ depends on $n$.
- **Using the sampling distribution of $X_i$ instead of $\bar{X}$** when asked about the sample mean.

## Quick Check

1. $\text{SE}$ for $n=100$, $\sigma=20$?
2. $E[\bar{X}]$ always equals what?
3. As $n \to \infty$, what happens to $\text{Var}(\bar{X})$?

*(Answers: 2; $\mu$; → 0)*
