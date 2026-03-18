# MVUE

## Overview

The **Minimum Variance Unbiased Estimator (MVUE)** is the unique unbiased estimator with the smallest possible variance among all unbiased estimators. It is the gold standard for point estimation.

## Key Idea

**Lehmann-Scheffé theorem:** If $T$ is a complete sufficient statistic and $\hat{\theta} = g(T)$ is unbiased, then $\hat{\theta}$ is the MVUE.

**Rao-Blackwell:** Conditioning an unbiased estimator on a sufficient statistic always improves (or maintains) it.

## Worked Examples

**Example 1: MVUE of $\mu$ for $N(\mu,\sigma^2)$ known $\sigma^2$**

$\bar{X}$ is unbiased and a function of the complete sufficient statistic. It is the MVUE.

---

**Example 2: Rao-Blackwellization**

If $\hat{\theta}$ is unbiased and $T$ is sufficient, then $\hat{\theta}_{RB} = E[\hat{\theta}|T]$ is at least as good (lower or equal MSE).

---

**Example 3: Poisson MVUE**

For Poisson$(\lambda)$, $\bar{X}$ is the MVUE of $\lambda$. But the MVUE of $e^{-\lambda}$ (probability of 0 events) requires more work.

## Common Mistakes

- **MVUE requires the estimator to be based on the complete sufficient statistic.** Regular sufficient is not enough.
- **Assuming MVUE always exists.** For some problems there is no MVUE.

## Quick Check

1. What theorem guarantees the MVUE from a complete sufficient statistic?
2. Rao-Blackwell improves what property?
3. Is $\bar{X}$ the MVUE of $\mu$ for any distribution?

*(Answers: Lehmann-Scheffé; variance (reduces or maintains it); no — only when it's the complete suff. stat.)*
