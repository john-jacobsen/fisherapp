# Sufficient Statistics

## Overview

A **sufficient statistic** $T(X)$ captures all the information in the data about the parameter $\theta$: once you know $T$, the conditional distribution of the data given $T$ does not depend on $\theta$.

## Key Idea

**Factorization theorem (Neyman-Fisher):** $T(X)$ is sufficient for $\theta$ iff the joint density factors as:

$$f(x_1,\ldots,x_n; \theta) = g(T(x), \theta) \cdot h(x_1,\ldots,x_n)$$

## Worked Examples

**Example 1: $X_i \sim \text{Bernoulli}(p)$. Show $T = \sum X_i$ is sufficient.**

$L(p) = p^{\sum x_i}(1-p)^{n-\sum x_i} = g(\sum x_i, p) \cdot 1$. Factorization confirms sufficiency.

---

**Example 2: $X_i \sim N(\mu, 1)$. Sufficient statistic?**

$L(\mu) \propto \exp\left(-\frac{1}{2}\sum(x_i-\mu)^2\right) \propto \exp\left(\mu\bar{x} - n\mu^2/2\right)$. So $T = \bar{X}$ is sufficient.

---

**Example 3: Complete sufficient statistic**

A sufficient statistic is **complete** if $E[g(T)] = 0$ for all $\theta$ implies $g(T) = 0$ a.s. Complete sufficient statistics lead to UMVUEs.

## Common Mistakes

- **Sufficient ≠ minimal sufficient.** Minimal sufficient contains the least information needed.
- **$T$ sufficient doesn't mean it's unbiased or efficient alone.**

## Quick Check

1. Factorization theorem: what does $g$ depend on?
2. For Poisson$(\lambda)$, is $\sum X_i$ sufficient?
3. What is a complete sufficient statistic used for?

*(Answers: $T(x)$ and $\theta$; yes; constructing UMVUEs via Lehmann-Scheffé)*
