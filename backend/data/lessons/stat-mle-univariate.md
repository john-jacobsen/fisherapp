# Maximum Likelihood Estimation (One Parameter)

## Overview

The **maximum likelihood estimator (MLE)** $\hat{\theta}$ is the parameter value that makes your observed data most probable. Instead of matching moments, you ask: for which value of $\theta$ was this particular dataset most likely to arise? This principle produces estimators with strong theoretical properties, including consistency and asymptotic efficiency.

## Key Idea

The likelihood function is the joint density of your data viewed as a function of the parameter. You maximize the log-likelihood because logs convert products into sums, which are easier to differentiate:

$$\hat{\theta}_{MLE} = \arg\max_\theta \,\ell(\theta), \qquad \ell(\theta) = \sum_{i=1}^n \log f(x_i;\, \theta)$$

To find the maximum, differentiate $\ell(\theta)$ with respect to $\theta$, set equal to zero, and solve. Always verify you have a maximum (not a minimum) by checking the second derivative.

## Worked Examples

**Example 1: MLE for $\lambda$ in the Poisson distribution**

The Poisson PMF is $f(x;\lambda) = e^{-\lambda}\lambda^x / x!$. The log-likelihood for $n$ i.i.d. observations is:

$$\ell(\lambda) = \sum_{i=1}^n \left(-\lambda + x_i \log\lambda - \log(x_i!)\right) = -n\lambda + \log\lambda \sum_{i=1}^n x_i - \text{const}$$

Differentiate with respect to $\lambda$ and set to zero:

$$\frac{d\ell}{d\lambda} = -n + \frac{\sum x_i}{\lambda} = 0 \implies \lambda = \frac{\sum x_i}{n} = \bar{X}$$

So $\hat{\lambda}_{MLE} = \bar{X}$. The second derivative $-\sum x_i/\lambda^2 < 0$ confirms this is a maximum.

---

**Example 2: MLE for $p$ in the Bernoulli distribution**

The Bernoulli PMF is $f(x;p) = p^x(1-p)^{1-x}$. The log-likelihood is:

$$\ell(p) = \sum_{i=1}^n \left[x_i \log p + (1-x_i)\log(1-p)\right] = n\bar{x}\log p + n(1-\bar{x})\log(1-p)$$

Differentiate with respect to $p$:

$$\frac{d\ell}{dp} = \frac{n\bar{x}}{p} - \frac{n(1-\bar{x})}{1-p} = 0$$

Multiply through by $p(1-p)$ to clear denominators: $n\bar{x}(1-p) = n(1-\bar{x})p$. Expanding and collecting $p$ terms gives $p = \bar{x}$, so $\hat{p}_{MLE} = \bar{X}$.

---

**Example 3: MLE for $\mu$ in the Normal distribution (known $\sigma^2$)**

The Normal log-likelihood (dropping terms that do not involve $\mu$) is:

$$\ell(\mu) = -\frac{1}{2\sigma^2}\sum_{i=1}^n (x_i - \mu)^2$$

Differentiating with respect to $\mu$:

$$\frac{d\ell}{d\mu} = \frac{1}{\sigma^2}\sum_{i=1}^n (x_i - \mu) = \frac{1}{\sigma^2}\left(n\bar{x} - n\mu\right) = 0$$

This gives $\mu = \bar{x}$, so $\hat{\mu}_{MLE} = \bar{X}$. Because the log-likelihood is a downward-opening quadratic in $\mu$, this is clearly a maximum.

## Common Mistakes

- **Maximizing $L(\theta)$ directly instead of $\ell(\theta)$.** The log-likelihood is much easier to differentiate because products become sums. Since $\log$ is monotone increasing, the same $\theta$ maximizes both.
- **Forgetting to verify the critical point is a maximum.** Setting $d\ell/d\theta = 0$ finds a critical point. Check the second derivative is negative, or argue from the shape of the function, to confirm it is a maximum.
- **Treating constants as if they depend on $\theta$.**  Terms in $\ell(\theta)$ that do not involve $\theta$ (like $\sum \log(x_i!)$ in the Poisson case) can be dropped before differentiating. Including them clutters the algebra but does not change the MLE.

## Quick Check

Try these before using hints:

1. For Geometric$(p)$ with $P(X=k) = (1-p)^{k-1}p$, write the log-likelihood for $n$ observations and find $\hat{p}_{MLE}$.
2. If $n = 5$ Poisson observations are $\{2, 3, 1, 4, 0\}$, what is $\hat{\lambda}_{MLE}$?
3. Why is it valid to maximize $\ell(\theta) = \log L(\theta)$ instead of $L(\theta)$?

*(Answers: $\hat{p} = 1/\bar{X}$; $\hat{\lambda} = 2.0$; $\log$ is strictly increasing so $\arg\max \ell = \arg\max L$)*
