# MLE with Multiple Parameters

## Overview

When a distribution has two or more unknown parameters, the MLE is found by solving a system of equations — one equation per parameter. You cannot optimize each parameter separately while ignoring the others, because the parameters often interact in the log-likelihood. This lesson covers how to set up and solve the **score equations** for multiparameter models.

## Key Idea

For a parameter vector $\theta = (\theta_1, \theta_2, \ldots)$, the MLE solves the score equations simultaneously — set all partial derivatives of the log-likelihood to zero at once:

$$\nabla_\theta \,\ell(\theta) = \mathbf{0}$$

That is, $\partial \ell / \partial \theta_j = 0$ for each $j$. Solving these equations jointly gives the MLE $\hat{\theta}$.

## Worked Examples

**Example 1: Normal distribution with unknown $\mu$ and $\sigma^2$**

The Normal log-likelihood (up to an additive constant) is:

$$\ell(\mu, \sigma^2) = -\frac{n}{2}\log\sigma^2 - \frac{1}{2\sigma^2}\sum_{i=1}^n (x_i - \mu)^2$$

**Score equation for $\mu$:** Differentiating with respect to $\mu$:

$$\frac{\partial \ell}{\partial \mu} = \frac{1}{\sigma^2}\sum_{i=1}^n(x_i - \mu) = 0 \implies \hat{\mu} = \bar{x}$$

**Score equation for $\sigma^2$:** Let $v = \sigma^2$. Differentiating with respect to $v$:

$$\frac{\partial \ell}{\partial v} = -\frac{n}{2v} + \frac{1}{2v^2}\sum_{i=1}^n(x_i - \mu)^2 = 0 \implies \hat{\sigma}^2 = \frac{1}{n}\sum_{i=1}^n(x_i - \bar{x})^2$$

The first equation gave us $\hat{\mu} = \bar{x}$, which we then substituted into the second. This is why the equations must be solved jointly — the solution for $\sigma^2$ depends on $\mu$.

---

**Example 2: Exponential distribution with rate $\lambda$**

The Exponential$(\lambda)$ density is $f(x;\lambda) = \lambda e^{-\lambda x}$ for $x > 0$. The log-likelihood is:

$$\ell(\lambda) = n\log\lambda - \lambda\sum_{i=1}^n x_i$$

Differentiating and setting to zero:

$$\frac{d\ell}{d\lambda} = \frac{n}{\lambda} - \sum_{i=1}^n x_i = 0 \implies \hat{\lambda} = \frac{n}{\sum x_i} = \frac{1}{\bar{X}}$$

So $\hat{\lambda}_{MLE} = 1/\bar{X}$. This is a single-parameter problem, but it illustrates that the MLE of a function of the mean is the function applied to $\bar{X}$ — a consequence of the **invariance property** of MLEs.

---

**Example 3: Why you must solve partial derivatives simultaneously**

Consider a two-parameter log-likelihood $\ell(\theta_1, \theta_2)$. If you try to optimize over $\theta_1$ alone while treating $\theta_2$ as a free constant, you get a function of $\theta_2$, not a number. The "best" $\theta_1$ depends on what $\theta_2$ is. You can only finalize the solution by imposing both score equations at once.

Geometrically, the log-likelihood surface is a function of two variables. The MLE is the peak of this surface. Each score equation describes the curve where the surface is flat in one direction. The MLE is their intersection — the single point where the surface is simultaneously flat in all directions.

## Common Mistakes

- **Solving score equations one at a time and ignoring the coupling.** For the Normal, solving $\partial\ell/\partial\mu = 0$ gives $\hat{\mu} = \bar{x}$ regardless of $\sigma^2$. But solving $\partial\ell/\partial\sigma^2 = 0$ requires substituting $\hat{\mu} = \bar{x}$ first — the equations are coupled even if the coupling is mild.
- **Confusing the MLE $\hat{\sigma}^2 = \frac{1}{n}\sum(x_i-\bar{x})^2$ with the unbiased $S^2 = \frac{1}{n-1}\sum(x_i-\bar{x})^2$.** The MLE uses $1/n$ and is slightly biased downward. The unbiased estimator uses $n-1$.
- **Forgetting to check the second-order conditions.** Setting partial derivatives to zero finds a critical point. For log-likelihoods that are strictly concave (like the Normal and Poisson), any critical point is a global maximum.

## Quick Check

Try these before using hints:

1. For the Gamma$(\alpha, \beta)$ distribution, how many score equations do you need?
2. What is $\hat{\lambda}_{MLE}$ for Exponential$(\lambda)$ if $n = 4$ and $\bar{x} = 5$?
3. What is the MLE invariance property, and why is it useful for the Exponential example?

*(Answers: two (one per parameter); $1/5 = 0.2$; $\widehat{g(\theta)} = g(\hat{\theta})$, so the MLE of the mean $1/\lambda$ is $1/\hat{\lambda} = \bar{X}$)*
