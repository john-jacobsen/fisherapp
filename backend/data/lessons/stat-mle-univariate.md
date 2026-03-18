# MLE: Univariate

## Overview

**Maximum Likelihood Estimation (MLE)** finds the parameter value that makes the observed data most probable. It is the most widely used estimation method, with strong theoretical properties.

## Key Idea

The **likelihood** is $L(\theta) = \prod_{i=1}^n f(x_i;\theta)$. Maximize $\ell(\theta) = \log L(\theta)$ (the log-likelihood) by solving $\frac{d\ell}{d\theta} = 0$.

## Worked Examples

**Example 1: MLE of $\lambda$ for Poisson$(\lambda)$**

$\ell(\lambda) = \sum x_i \ln\lambda - n\lambda$. Setting $d\ell/d\lambda = \sum x_i/\lambda - n = 0$ gives $\hat{\lambda} = \bar{X}$.

---

**Example 2: MLE of $p$ for Bernoulli$(p)$**

$\ell(p) = \sum x_i \ln p + (n - \sum x_i)\ln(1-p)$. Solution: $\hat{p} = \bar{X}$.

---

**Example 3: MLE of $\mu$ for $N(\mu, \sigma_0^2)$ (known $\sigma^2$)**

Minimizing $\sum(x_i - \mu)^2$ gives $\hat{\mu} = \bar{X}$.

## Common Mistakes

- **Forgetting to take the log.** The log-likelihood is much easier to maximize.
- **Not checking the second derivative** to confirm it's a maximum.

## Quick Check

1. Why use log-likelihood instead of likelihood?
2. MLE for $\theta$ in Uniform$(0,\theta)$?
3. Is $d\ell/d\theta = 0$ always sufficient?

*(Answers: converts product to sum; $\hat{\theta}=X_{(n)}$ (max obs); no — also check 2nd derivative or boundary)*
