# The Delta Method

## Overview

The **delta method** extends the Central Limit Theorem to smooth functions of estimators. If you know the asymptotic distribution of $\hat{\theta}$, you can derive the asymptotic distribution of $g(\hat{\theta})$ for any differentiable function $g$. This is essential when your quantity of interest is a nonlinear transformation of a parameter you can estimate directly.

## Key Idea

If $\sqrt{n}(\hat{\theta} - \theta) \xrightarrow{d} N(0, \sigma^2)$, then for a differentiable function $g$ with $g'(\theta) \neq 0$:

$$\sqrt{n}(g(\hat{\theta}) - g(\theta)) \xrightarrow{d} N\!\left(0,\, \sigma^2 [g'(\theta)]^2\right)$$

The result comes from a first-order Taylor expansion: $g(\hat{\theta}) \approx g(\theta) + g'(\theta)(\hat{\theta} - \theta)$. Multiplying by $\sqrt{n}$ and applying the CLT gives the result. The asymptotic variance of $g(\hat{\theta})$ is the variance of $\hat{\theta}$ scaled by the square of $g'$.

## Worked Examples

**Example 1: Asymptotic distribution of $1/\bar{X}$ when $X_i \sim \text{Poisson}(\lambda)$**

For Poisson$(\lambda)$, $\text{Var}(X_i) = \lambda$, so by the CLT: $\sqrt{n}(\bar{X} - \lambda) \xrightarrow{d} N(0, \lambda)$.

Let $g(x) = 1/x$, so $g'(x) = -1/x^2$ and $g'(\lambda) = -1/\lambda^2$.

Apply the delta method:

$$\sqrt{n}\!\left(\frac{1}{\bar{X}} - \frac{1}{\lambda}\right) \xrightarrow{d} N\!\left(0,\; \lambda \cdot \frac{1}{\lambda^4}\right) = N\!\left(0,\; \frac{1}{\lambda^3}\right)$$

So $1/\bar{X}$ is asymptotically normal with variance $1/(n\lambda^3)$. You estimate this variance by substituting $\hat{\lambda} = \bar{X}$: $\widehat{\text{Var}}(1/\bar{X}) \approx 1/(n\bar{X}^3)$.

---

**Example 2: Asymptotic variance of $\hat{p}^2$ from Bernoulli data**

For Bernoulli$(p)$, $\text{Var}(X_i) = p(1-p)$, so the CLT gives: $\sqrt{n}(\hat{p} - p) \xrightarrow{d} N(0, p(1-p))$.

Let $g(p) = p^2$, so $g'(p) = 2p$.

By the delta method:

$$\sqrt{n}(\hat{p}^2 - p^2) \xrightarrow{d} N\!\left(0,\; p(1-p) \cdot (2p)^2\right) = N\!\left(0,\; 4p^3(1-p)\right)$$

The asymptotic variance of $\hat{p}^2$ is $4p^3(1-p)/n$. Estimate this in practice by replacing $p$ with $\hat{p}$: $4\hat{p}^3(1-\hat{p})/n$.

---

**Example 3: Construct a 95% CI for $g(\theta)$ using the delta method**

Suppose $\sqrt{n}(\hat{\theta} - \theta) \xrightarrow{d} N(0, \sigma^2)$ and you want a CI for $g(\theta)$.

By the delta method, $g(\hat{\theta})$ is approximately $N(g(\theta),\; \sigma^2[g'(\theta)]^2/n)$. Standardizing and using the normal table, an approximate 95% CI is:

$$g(\hat{\theta}) \pm 1.96 \cdot \frac{|g'(\hat{\theta})|\,\hat{\sigma}}{\sqrt{n}}$$

where $\hat{\sigma}$ estimates $\sigma$. For Example 1, a 95% CI for $1/\lambda$ would be $1/\bar{X} \pm 1.96/(\bar{X}^2\sqrt{n} \cdot \sqrt{1/\bar{X}}) = 1/\bar{X} \pm 1.96/(\bar{X}^{3/2}\sqrt{n})$. The CI is asymmetric on the original $\lambda$ scale — which the delta method handles automatically.

## Common Mistakes

- **Forgetting to square $g'(\theta)$ in the variance.** The variance formula involves $[g'(\theta)]^2$, not $g'(\theta)$. This ensures the variance is always non-negative regardless of the sign of $g'$.
- **Using the delta method when $g'(\theta) = 0$.** If $g'(\theta) = 0$, the first-order approximation is exact zero and the delta method breaks down. The correct asymptotic distribution is then determined by the second derivative of $g$ and involves a chi-squared distribution, not a normal.
- **Applying the delta method to discrete estimators.** The delta method requires $\hat{\theta}$ to be asymptotically normal (continuous) and $g$ to be differentiable. For count-valued statistics or non-smooth $g$, alternative methods are needed.

## Quick Check

Try these before using hints:

1. If $\sqrt{n}(\hat{\theta} - \theta) \xrightarrow{d} N(0, 4)$ and $g(\theta) = e^\theta$, what is the asymptotic variance of $e^{\hat{\theta}}$?
2. For $\hat{p} \approx N(p, p(1-p)/n)$, use the delta method to find the asymptotic variance of $\log(\hat{p}/(1-\hat{p}))$ (the log-odds).
3. Why does the delta method use a first-order Taylor expansion rather than a higher-order one?

*(Answers: $4e^{2\theta}/n$; $1/(np(1-p))$; because higher-order terms vanish faster than $1/\sqrt{n}$ and do not affect the limiting distribution)*
