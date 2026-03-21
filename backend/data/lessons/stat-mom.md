# Method of Moments Estimation

## Overview

The **method of moments (MOM)** is a systematic way to construct estimators: set population moments (which depend on unknown parameters) equal to sample moments (which you compute from your data), then solve for the parameters. It is often the simplest estimation strategy, and the resulting estimators are usually consistent, though not always efficient.

## Key Idea

The $k$-th population moment is $\mu_k = E[X^k]$. The corresponding sample moment is $\hat{\mu}_k = \frac{1}{n}\sum_{i=1}^n X_i^k$. Set them equal and solve:

$$E[X^k] = \frac{1}{n}\sum_{i=1}^n X_i^k$$

With one unknown parameter, you typically only need $k = 1$ (the mean). With two unknown parameters, you set up two equations using $k = 1$ and $k = 2$ (or the variance).

## Worked Examples

**Example 1: MOM estimator for $\lambda$ in the Poisson distribution**

For a Poisson$(\lambda)$ random variable, $E[X] = \lambda$. There is one unknown parameter, so you need one equation. Set the first population moment equal to the first sample moment:

$$E[X] = \lambda \quad \Longrightarrow \quad \lambda = \frac{1}{n}\sum_{i=1}^n X_i = \bar{X}$$

Therefore $\hat{\lambda}_{MOM} = \bar{X}$. This makes intuitive sense: the Poisson mean equals $\lambda$, so estimate $\lambda$ with the sample mean. You can verify this estimator is unbiased because $E[\bar{X}] = E[X] = \lambda$.

---

**Example 2: MOM estimator for $p$ in the Bernoulli distribution**

For a Bernoulli$(p)$ random variable, $E[X] = p$. Again one unknown parameter, one equation:

$$E[X] = p \quad \Longrightarrow \quad p = \frac{1}{n}\sum_{i=1}^n X_i = \bar{X}$$

So $\hat{p}_{MOM} = \bar{X}$, the sample proportion of ones. This is unbiased since $E[\bar{X}] = p$, and it is consistent by the Law of Large Numbers: $\bar{X} \xrightarrow{p} E[X] = p$ as $n \to \infty$.

---

**Example 3: MOM estimators for $\mu$ and $\sigma^2$ in the Normal distribution**

The Normal$(\mu, \sigma^2)$ has two unknown parameters, so you need two equations. Use the first and second moments.

First moment: $E[X] = \mu$, so set $\mu = \bar{X}$, giving $\hat{\mu}_{MOM} = \bar{X}$.

Second moment: $E[X^2] = \text{Var}(X) + (E[X])^2 = \sigma^2 + \mu^2$. Set equal to the sample second moment:

$$\sigma^2 + \mu^2 = \frac{1}{n}\sum_{i=1}^n X_i^2$$

Substitute $\hat{\mu} = \bar{X}$ and solve for $\sigma^2$:

$$\hat{\sigma}^2_{MOM} = \frac{1}{n}\sum_{i=1}^n X_i^2 - \bar{X}^2 = \frac{1}{n}\sum_{i=1}^n (X_i - \bar{X})^2$$

Notice this uses $1/n$ rather than $1/(n-1)$, so the MOM estimator for $\sigma^2$ is slightly biased — but it is consistent.

## Common Mistakes

- **Using the wrong number of equations.** You need exactly as many moment equations as unknown parameters. With two parameters, setting only the first moment equal to $\bar{X}$ gives you one equation with two unknowns — the system is underdetermined.
- **Forgetting that MOM variance uses $1/n$, not $1/(n-1)$.** The unbiased sample variance $S^2$ uses $n-1$. The MOM estimator $\hat{\sigma}^2_{MOM}$ uses $n$, because it comes directly from matching moments, not from correcting for bias.
- **Assuming MOM estimators are always unbiased.** The Poisson and Bernoulli MOM estimators are unbiased, but the Normal MOM estimator for $\sigma^2$ is not. Always check by taking expectations.

## Quick Check

Try these before using hints:

1. For an Exponential$(\lambda)$ distribution with $E[X] = 1/\lambda$, what is $\hat{\lambda}_{MOM}$?
2. If you observe $n = 10$ Bernoulli trials and get 7 successes, what is $\hat{p}_{MOM}$?
3. For a Uniform$(0, \theta)$ distribution with $E[X] = \theta/2$, what is $\hat{\theta}_{MOM}$?

*(Answers: $1/\bar{X}$; $0.7$; $2\bar{X}$)*
