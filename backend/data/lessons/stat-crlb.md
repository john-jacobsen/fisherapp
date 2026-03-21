# Cramér-Rao Lower Bound

## Overview

The **Cramér-Rao lower bound (CRLB)** sets a floor on how small the variance of any unbiased estimator can be. No matter how clever your estimation method, if it is unbiased, its variance cannot beat this bound. An unbiased estimator that achieves exactly this variance is called **efficient** — it extracts the maximum possible information from the data.

## Key Idea

For any unbiased estimator $\hat{\theta}$ of $\theta$, based on $n$ i.i.d. observations:

$$\text{Var}(\hat{\theta}) \geq \frac{1}{n\,I(\theta)}$$

where $I(\theta)$ is the Fisher information for a single observation. The CRLB is tight (achievable) only for certain distributions and estimators — but even when it is not achievable, it tells you how close to optimal you are.

## Worked Examples

**Example 1: Verify $\bar{X}$ achieves the CRLB for $\mu$ in the Normal distribution (known $\sigma^2$)**

From the Fisher information lesson, $I(\mu) = 1/\sigma^2$ for Normal$(\mu, \sigma^2)$.

The CRLB for any unbiased estimator of $\mu$ is therefore:

$$\text{CRLB} = \frac{1}{n \cdot 1/\sigma^2} = \frac{\sigma^2}{n}$$

Now check $\bar{X}$: it is unbiased ($E[\bar{X}] = \mu$) and $\text{Var}(\bar{X}) = \sigma^2/n$.

Since $\text{Var}(\bar{X}) = \sigma^2/n = \text{CRLB}$, the sample mean achieves the bound exactly. No unbiased estimator of $\mu$ can have smaller variance than $\sigma^2/n$, so $\bar{X}$ is efficient.

---

**Example 2: Check if $\bar{X}$ achieves the CRLB for $\lambda$ in the Poisson distribution**

For Poisson$(\lambda)$, $I(\lambda) = 1/\lambda$ (computed in the Fisher information lesson).

The CRLB is:

$$\frac{1}{n \cdot 1/\lambda} = \frac{\lambda}{n}$$

Now check $\bar{X}$: it is unbiased for $\lambda$, and for Poisson data $\text{Var}(X_i) = \lambda$, so $\text{Var}(\bar{X}) = \lambda/n$.

Again $\text{Var}(\bar{X}) = \lambda/n = \text{CRLB}$. The sample mean is the efficient unbiased estimator for the Poisson mean. Both the Normal and Poisson belong to the exponential family, which is why their natural statistics ($\bar{X}$) achieve the CRLB.

---

**Example 3: Why the CRLB is a lower bound, not an exact value**

The CRLB is derived from the Cauchy-Schwarz inequality applied to the covariance between $\hat{\theta}$ and the score function. The inequality becomes an equality only when $\hat{\theta}$ is a linear function of the score — a condition that fails for many distributions.

For example, for Uniform$(0, \theta)$, the MLE is $\hat{\theta} = X_{(n)}$ (the sample maximum). This estimator is biased, so the CRLB does not even apply to it directly. Among unbiased estimators of $\theta$, you can construct one with finite variance, but the CRLB for this family turns out to be zero (the bound is not achievable). This shows the CRLB is a benchmark — some problems admit efficient estimators, others do not.

## Common Mistakes

- **Applying the CRLB to biased estimators.** The standard CRLB applies only to unbiased estimators. A biased version exists (the generalized CRLB), but it requires knowing the bias function.
- **Concluding an estimator is optimal just because it has small variance.** Low variance is necessary but not sufficient for efficiency. You must compare $\text{Var}(\hat{\theta})$ to the CRLB specifically.
- **Forgetting the factor of $n$.** The CRLB for $n$ i.i.d. observations uses the total Fisher information $nI(\theta)$ in the denominator. Omitting the $n$ gives a bound that is $n$ times too large.

## Quick Check

Try these before using hints:

1. For Bernoulli$(p)$ with $I(p) = 1/(p(1-p))$, what is the CRLB for an unbiased estimator of $p$ based on $n$ observations?
2. If $\text{Var}(\hat{\theta}) = 2/(nI(\theta))$, does $\hat{\theta}$ achieve the CRLB?
3. What does it mean for an estimator to be "efficient"?

*(Answers: $p(1-p)/n$; no, its variance is twice the CRLB; it is unbiased and achieves exactly the CRLB)*
