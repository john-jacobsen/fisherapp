# Method of Moments

## Overview

The **Method of Moments (MOM)** estimates parameters by equating population moments (expressed in terms of parameters) to sample moments. It is simple and often provides consistent estimators.

## Key Idea

Set the $k$-th population moment $\mu_k' = E[X^k]$ equal to the sample moment $m_k' = \frac{1}{n}\sum X_i^k$, and solve for the parameters.

## Worked Examples

**Example 1: MOM estimator of $\lambda$ for Poisson$(\lambda)$**

$E[X] = \lambda$. Set $\lambda = \bar{X}$. So $\hat{\lambda}_{MOM} = \bar{X}$.

---

**Example 2: MOM for Normal$(\mu, \sigma^2)$**

First moment: $\hat{\mu} = \bar{X}$.

Second central moment: $\hat{\sigma}^2 = \frac{1}{n}\sum(X_i - \bar{X})^2$.

---

**Example 3: MOM for Uniform$(0, \theta)$**

$E[X] = \theta/2$. Set $\bar{X} = \hat{\theta}/2$. So $\hat{\theta} = 2\bar{X}$.

## Common Mistakes

- **MOM estimators can be outside the parameter space.** For example, $2\bar{X}$ could be less than the observed maximum.
- **MOM may not be efficient** — it doesn't always minimize MSE.

## Quick Check

1. MOM estimator of $p$ for Bernoulli$(p)$?
2. MOM for Exp$(\lambda)$?
3. MOM requires solving what kind of equations?

*(Answers: $\bar{X}$; $\hat{\lambda}=1/\bar{X}$; setting population moments equal to sample moments)*
