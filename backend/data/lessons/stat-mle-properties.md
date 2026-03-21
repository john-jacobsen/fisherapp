# Asymptotic Properties of MLE

## Overview

The MLE has three key large-sample properties that hold under mild regularity conditions. It is **consistent** (converges to the true parameter), **asymptotically normal** (approximately normal for large $n$), and **asymptotically efficient** (achieves the minimum possible variance among consistent, asymptotically normal estimators). These properties justify using the MLE in practice and make it easy to construct confidence intervals.

## Key Idea

Under regularity conditions, the MLE $\hat{\theta}_{MLE}$ satisfies:

$$\hat{\theta}_{MLE} \overset{d}{\approx} N\!\left(\theta_0,\, \frac{1}{n\,I(\theta_0)}\right)$$

where $I(\theta_0)$ is the Fisher information for a single observation evaluated at the true parameter $\theta_0$. The asymptotic variance $1/(nI(\theta_0))$ is exactly the Cramér-Rao lower bound, which means no consistent estimator can beat the MLE asymptotically.

## Worked Examples

**Example 1: Asymptotic distribution of the Poisson MLE**

For Poisson$(\lambda)$, the Fisher information for one observation is $I(\lambda) = 1/\lambda$ (derived by computing $-E[\partial^2 \log f/\partial\lambda^2]$). The MLE is $\hat{\lambda} = \bar{X}$.

By the asymptotic normality result, for large $n$:

$$\hat{\lambda} \approx N\!\left(\lambda,\, \frac{1}{n \cdot (1/\lambda)}\right) = N\!\left(\lambda,\, \frac{\lambda}{n}\right)$$

This matches the exact result $\text{Var}(\bar{X}) = \lambda/n$ for Poisson data, confirming that $\hat{\lambda} = \bar{X}$ achieves the asymptotic efficiency bound exactly.

---

**Example 2: Asymptotic distribution of the Bernoulli MLE**

For Bernoulli$(p)$, the Fisher information is $I(p) = 1/(p(1-p))$. The MLE is $\hat{p} = \bar{X}$.

The asymptotic normality result gives:

$$\hat{p} \approx N\!\left(p,\, \frac{1}{n \cdot 1/(p(1-p))}\right) = N\!\left(p,\, \frac{p(1-p)}{n}\right)$$

Again this matches the exact variance of $\bar{X}$ for Bernoulli data: $\text{Var}(\bar{X}) = p(1-p)/n$. The asymptotic standard error is $\sqrt{p(1-p)/n}$; in practice you estimate this as $\sqrt{\hat{p}(1-\hat{p})/n}$.

---

**Example 3: Approximate 95% CI for $\lambda$ using asymptotic normality**

From Example 1, $\hat{\lambda} \approx N(\lambda, \lambda/n)$. The standard error is $\sqrt{\hat{\lambda}/n}$ (plugging in the MLE for the unknown $\lambda$). A 95% confidence interval is:

$$\hat{\lambda} \pm 1.96\,\sqrt{\frac{\hat{\lambda}}{n}}$$

For example, if $n = 100$ and $\hat{\lambda} = 4$:

$$4 \pm 1.96\sqrt{0.04} = 4 \pm 1.96 \times 0.2 = 4 \pm 0.392$$

The interval $(3.61,\, 4.39)$ is an approximate 95% CI for $\lambda$. This approach works for any MLE with a known Fisher information formula.

## Common Mistakes

- **Applying asymptotic results to small samples.** The normal approximation for $\hat{\theta}_{MLE}$ requires large $n$. For small samples, the exact distribution may be far from normal, making asymptotic CIs unreliable.
- **Forgetting to estimate $I(\theta_0)$.** The asymptotic variance involves the true $\theta_0$, which is unknown. In practice, substitute $\hat{\theta}_{MLE}$ for $\theta_0$ to get a feasible standard error. This is called the **observed Fisher information** approach.
- **Confusing asymptotic efficiency with finite-sample efficiency.** The MLE achieves the Cramér-Rao bound asymptotically, but for small $n$ another estimator might have lower MSE.

## Quick Check

Try these before using hints:

1. For Normal$(\mu, \sigma^2)$ with known $\sigma^2$, $I(\mu) = 1/\sigma^2$. What is the asymptotic variance of $\hat{\mu}_{MLE}$?
2. Why do we plug $\hat{\theta}$ into the asymptotic variance formula rather than using the true $\theta_0$?
3. If $n = 100$, $\hat{p} = 0.4$, construct an approximate 95% CI for $p$.

*(Answers: $\sigma^2/n$; because $\theta_0$ is unknown — using $\hat{\theta}$ is consistent; $0.4 \pm 1.96\sqrt{0.24/100} \approx 0.4 \pm 0.096$)*
