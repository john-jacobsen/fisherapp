# Delta Method

## Overview

The **delta method** gives the asymptotic distribution of a transformed estimator. If $\sqrt{n}(\hat{\theta} - \theta) \xrightarrow{d} N(0, \sigma^2)$, then you can find the asymptotic distribution of $g(\hat{\theta})$.

## Key Idea

If $\sqrt{n}(\hat{\theta} - \theta) \xrightarrow{d} N(0,\sigma^2)$ and $g$ is differentiable at $\theta$:

$$\sqrt{n}(g(\hat{\theta}) - g(\theta)) \xrightarrow{d} N(0, [g'(\theta)]^2 \sigma^2)$$

## Worked Examples

**Example 1: Distribution of $\log\hat{p}$ where $\hat{p} = X/n \sim N(p, p(1-p)/n)$**

$g(p) = \log p$, $g'(p) = 1/p$.

$$\sqrt{n}(\log\hat{p} - \log p) \xrightarrow{d} N\!\left(0, \frac{1-p}{p}\right)$$

---

**Example 2: Variance-stabilizing transformation**

Choose $g$ so that $[g'(\theta)]^2 \sigma^2(\theta) = \text{const}$. For Binomial, $g(p) = \arcsin(\sqrt{p})$ works.

---

**Example 3: Multivariate delta method**

For vector-valued $\hat{\theta}$: asymptotic variance of $g(\hat{\theta})$ is $\nabla g^T \Sigma \nabla g$.

## Common Mistakes

- **Forgetting to square $g'(\theta)$.** The variance transforms by $[g'(\theta)]^2$.
- **Using delta method when $g'(\theta) = 0$.** The first-order approximation fails; you need the second-order delta method.

## Quick Check

1. If $\sqrt{n}(\hat{\theta}-\theta)\to N(0,4)$, asymptotic variance of $g(\hat{\theta})$?
2. $g(x) = x^2$. $g'(\theta) = ?$
3. What assumption on $g$ does the delta method require?

*(Answers: $4[g'(\theta)]^2$; $2\theta$; differentiability at $\theta$)*
