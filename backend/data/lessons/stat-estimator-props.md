# Properties of Estimators

## Overview

An **estimator** $\hat{\theta}$ is a statistic used to estimate a population parameter $\theta$. Good estimators are unbiased, consistent, and efficient. These properties determine how reliable an estimator is.

## Key Idea

- **Unbiased:** $E[\hat{\theta}] = \theta$
- **Consistent:** $\hat{\theta} \xrightarrow{P} \theta$ as $n \to \infty$
- **Efficient:** minimum variance among all unbiased estimators (MVUE)

**MSE:** $\text{MSE}(\hat{\theta}) = \text{Var}(\hat{\theta}) + [\text{Bias}(\hat{\theta})]^2$

## Worked Examples

**Example 1: Is $\bar{X}$ unbiased for $\mu$?**

$E[\bar{X}] = \mu$ ✓ — unbiased.

---

**Example 2: Biased estimator of $\sigma^2$**

$\hat{\sigma}^2 = \frac{1}{n}\sum(X_i - \bar{X})^2$ has $E[\hat{\sigma}^2] = \frac{n-1}{n}\sigma^2$ — biased. The unbiased version uses $n-1$ in the denominator.

---

**Example 3: MSE tradeoff**

A biased estimator with smaller variance can have smaller MSE than an unbiased one. Bias-variance tradeoff is fundamental.

## Common Mistakes

- **Assuming unbiased = best.** An unbiased estimator can have high variance.
- **Confusing bias and MSE.** MSE combines both bias and variance.

## Quick Check

1. $E[\hat{\theta}] = \theta + 2$. What is the bias?
2. Does $S^2 = \frac{1}{n-1}\sum(X_i-\bar{X})^2$ overestimate or underestimate $\sigma^2$?
3. MSE formula in terms of bias and variance?

*(Answers: 2; neither (unbiased); Var + Bias²)*
