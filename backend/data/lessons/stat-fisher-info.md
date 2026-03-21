# Fisher Information

## Overview

**Fisher information** $I(\theta)$ quantifies how much a single observation tells you about an unknown parameter $\theta$. High Fisher information means the data vary strongly with $\theta$, so small changes in $\theta$ produce noticeable changes in the distribution — making $\theta$ easier to estimate. Low Fisher information means the distribution is nearly insensitive to $\theta$, making estimation hard.

## Key Idea

Fisher information is the expected squared score (the score is the derivative of the log-likelihood). Under regularity conditions this equals the negative expected second derivative of the log-likelihood:

$$I(\theta) = -E\!\left[\frac{\partial^2}{\partial\theta^2}\log f(X;\theta)\right]$$

For $n$ i.i.d. observations, the total Fisher information is $n$ times the single-observation Fisher information: $I_n(\theta) = n\,I(\theta)$. More data means more information — linearly.

## Worked Examples

**Example 1: Compute $I(\lambda)$ for the Poisson distribution**

The Poisson PMF is $f(x;\lambda) = e^{-\lambda}\lambda^x/x!$, so:

$$\log f(x;\lambda) = -\lambda + x\log\lambda - \log(x!)$$

First derivative (the score): $\frac{\partial}{\partial\lambda}\log f = -1 + x/\lambda$.

Second derivative: $\frac{\partial^2}{\partial\lambda^2}\log f = -x/\lambda^2$.

Take the negative expectation. Since $E[X] = \lambda$ for Poisson:

$$I(\lambda) = -E\!\left[-\frac{X}{\lambda^2}\right] = \frac{E[X]}{\lambda^2} = \frac{\lambda}{\lambda^2} = \frac{1}{\lambda}$$

Higher $\lambda$ means less information per observation — this makes sense because Poisson distributions with large $\lambda$ are more spread out, making $\lambda$ harder to pin down precisely.

---

**Example 2: Compute $I(p)$ for the Bernoulli distribution**

The Bernoulli log-likelihood is $\log f(x;p) = x\log p + (1-x)\log(1-p)$.

Second derivative: $\frac{\partial^2}{\partial p^2}\log f = -x/p^2 - (1-x)/(1-p)^2$.

Take the negative expectation, using $E[X] = p$:

$$I(p) = -E\!\left[-\frac{X}{p^2} - \frac{1-X}{(1-p)^2}\right] = \frac{p}{p^2} + \frac{1-p}{(1-p)^2} = \frac{1}{p} + \frac{1}{1-p} = \frac{1}{p(1-p)}$$

Fisher information is highest when $p$ is near 0 or 1 (extreme, informative outcomes) and lowest when $p = 1/2$ (maximum uncertainty about the outcome).

---

**Example 3: Compute $I(\mu)$ for the Normal distribution (known $\sigma^2$)**

The Normal log-likelihood is $\log f(x;\mu) = -\frac{(x-\mu)^2}{2\sigma^2} + \text{const}$.

Second derivative: $\frac{\partial^2}{\partial\mu^2}\log f = -\frac{1}{\sigma^2}$.

This is a constant (does not depend on $X$), so taking the negative expectation is immediate:

$$I(\mu) = -E\!\left[-\frac{1}{\sigma^2}\right] = \frac{1}{\sigma^2}$$

Larger variance $\sigma^2$ means less information about $\mu$ — intuitively, noisy data make it harder to estimate the center of the distribution.

## Common Mistakes

- **Forgetting to take the expectation.** The second derivative $\frac{\partial^2}{\partial\theta^2}\log f(X;\theta)$ is a random variable (it depends on $X$). Fisher information is its negative expected value — you must integrate (or take $E$) before you have $I(\theta)$.
- **Using $n\,I(\theta)$ when only one observation is present.** The formula $I_n(\theta) = n\,I(\theta)$ applies to the total Fisher information from $n$ i.i.d. observations. For a single observation, use $I(\theta)$ alone.
- **Confusing Fisher information with variance.** Fisher information is a property of the distribution (the model), not of a specific estimator. The Cramér-Rao bound then links $I(\theta)$ to the minimum achievable variance of an estimator.

## Quick Check

Try these before using hints:

1. For Exponential$(\lambda)$ with log-likelihood $\log\lambda - \lambda x$, find $I(\lambda)$.
2. If $I(\theta) = 5$ for one observation, what is the total Fisher information for $n = 20$ i.i.d. observations?
3. For Bernoulli, at what value of $p$ is $I(p)$ minimized? What does that mean?

*(Answers: $1/\lambda^2$; 100; $p = 1/2$, meaning equal proportions give the least information per trial about $p$)*
