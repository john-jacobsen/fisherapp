# Properties of Estimators

## Overview

An **estimator** $\hat{\theta}$ is a function of the data that produces a guess for an unknown parameter $\theta$. Different estimators for the same parameter can behave very differently — some are systematically off (biased), some are inconsistent, and some waste information. Understanding these properties lets you choose and evaluate estimators rigorously.

## Key Idea

The three core properties are bias, consistency, and efficiency. Bias and variance together determine mean squared error:

$$\text{Bias}(\hat{\theta}) = E[\hat{\theta}] - \theta$$

$$\text{MSE}(\hat{\theta}) = \text{Var}(\hat{\theta}) + \text{Bias}^2(\hat{\theta})$$

An unbiased estimator has $\text{Bias} = 0$, so $\text{MSE} = \text{Var}$. A consistent estimator satisfies $\hat{\theta} \xrightarrow{p} \theta$ as $n \to \infty$. An efficient estimator achieves the minimum possible variance among all unbiased estimators.

## Worked Examples

**Example 1: Show $\bar{X}$ is unbiased for $\mu$**

You want to verify that $E[\bar{X}] = \mu$. Start from the definition of $\bar{X}$:

$$E[\bar{X}] = E\!\left[\frac{1}{n}\sum_{i=1}^n X_i\right] = \frac{1}{n}\sum_{i=1}^n E[X_i]$$

The second equality uses linearity of expectation, which holds always — no distributional assumptions needed. Since each $X_i$ has mean $\mu$:

$$= \frac{1}{n} \cdot n\mu = \mu$$

So $\text{Bias}(\bar{X}) = \mu - \mu = 0$: $\bar{X}$ is unbiased for $\mu$ for any sample size.

---

**Example 2: Compute $\text{MSE}(\bar{X})$ when $\sigma^2 = 4$, $n = 16$**

Since $\bar{X}$ is unbiased, $\text{Bias} = 0$ and $\text{MSE}(\bar{X}) = \text{Var}(\bar{X})$.

The variance of $\bar{X}$ for i.i.d. observations is $\sigma^2/n$, which follows from the fact that variance of independent sums adds, then dividing by $n^2$ when forming $\bar{X}$:

$$\text{MSE}(\bar{X}) = \text{Var}(\bar{X}) = \frac{\sigma^2}{n} = \frac{4}{16} = 0.25$$

The MSE shrinks with $n$, which is why $\bar{X}$ is also consistent: as $n \to \infty$, $\text{MSE} \to 0$, so $\bar{X}$ concentrates around $\mu$.

---

**Example 3: Show $S^2 = \frac{1}{n-1}\sum_{i=1}^n (X_i - \bar{X})^2$ is unbiased for $\sigma^2$**

The key identity is $\sum_{i=1}^n (X_i - \bar{X})^2 = \sum_{i=1}^n (X_i - \mu)^2 - n(\bar{X} - \mu)^2$. Taking expectations of both sides:

$$E\!\left[\sum_{i=1}^n (X_i - \bar{X})^2\right] = n\sigma^2 - n \cdot \frac{\sigma^2}{n} = (n-1)\sigma^2$$

The $n\sigma^2$ term comes from $\sum E[(X_i - \mu)^2] = n\sigma^2$, and the subtracted term uses $\text{Var}(\bar{X}) = \sigma^2/n$. Dividing both sides by $n-1$:

$$E[S^2] = \frac{(n-1)\sigma^2}{n-1} = \sigma^2$$

This is exactly why the denominator is $n-1$ rather than $n$: dividing by $n$ would give a biased (downward) estimator.

## Common Mistakes

- **Dividing by $n$ for sample variance.** Using $\frac{1}{n}\sum(X_i - \bar{X})^2$ gives a biased estimator. The $n-1$ denominator corrects for the fact that $\bar{X}$ is estimated from the same data, which "uses up" one degree of freedom.
- **Confusing low MSE with unbiasedness.** A biased estimator can have lower MSE than an unbiased one if its variance is small enough. The MSE decomposition $\text{Var} + \text{Bias}^2$ makes this tradeoff explicit.
- **Assuming consistency implies unbiasedness.** These are separate properties. An estimator can be consistent but biased for any finite $n$ (the bias just shrinks to zero as $n \to \infty$).

## Quick Check

Try these before using hints:

1. If $E[\hat{\theta}] = \theta + 2/n$, is $\hat{\theta}$ unbiased? Is it consistent?
2. An estimator has $\text{Var}(\hat{\theta}) = 3/n$ and $\text{Bias}(\hat{\theta}) = 1/\sqrt{n}$. What is $\text{MSE}(\hat{\theta})$?
3. Why does the denominator $n-1$ appear in the unbiased sample variance rather than $n$?

*(Answers: not unbiased but consistent (bias $\to 0$); $3/n + 1/n = 4/n$; because estimating $\mu$ with $\bar{X}$ costs one degree of freedom)*
