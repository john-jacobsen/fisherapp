# Cramér-Rao Lower Bound

## Overview

The **Cramér-Rao Lower Bound (CRLB)** gives a lower bound on the variance of any unbiased estimator. No unbiased estimator can do better than the CRLB, so it defines the best possible precision.

## Key Idea

For any unbiased estimator $\hat{\theta}$:

$$\text{Var}(\hat{\theta}) \ge \frac{1}{I_n(\theta)} = \frac{1}{n\,I_1(\theta)}$$

An estimator achieving the CRLB is **efficient**.

## Worked Examples

**Example 1: CRLB for $\mu$ in $N(\mu, \sigma^2)$ known $\sigma^2$**

$I_n(\mu) = n/\sigma^2$. CRLB $= \sigma^2/n$. $\bar{X}$ achieves this ✓ — efficient.

---

**Example 2: CRLB for $p$ in Binomial$(n,p)$**

$I_n(p) = n/(p(1-p))$. CRLB $= p(1-p)/n$. $\hat{p} = X/n$ achieves it.

---

**Example 3: When is the CRLB not achieved?**

Many estimators don't achieve the CRLB. The CRLB is a lower bound, not necessarily attainable.

## Common Mistakes

- **The CRLB only applies to unbiased estimators.** Biased estimators have a generalized version.
- **Assuming the minimum variance estimator always exists.** MVUE may not exist for all distributions.

## Quick Check

1. CRLB $= ?$
2. If $\text{Var}(\hat{\theta}) = 1/(nI(\theta))$, what is $\hat{\theta}$ called?
3. CRLB for Exp$(\lambda)$ given $n$ observations?

*(Answers: $1/(nI(\theta))$; efficient estimator; $\lambda^2/n$)*
