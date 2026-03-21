# Minimum Variance Unbiased Estimation

## Overview

A **minimum variance unbiased estimator (MVUE)** is the best you can do among unbiased estimators: it is unbiased and has the smallest possible variance. The theory for finding MVUEs rests on two ideas — the Rao-Blackwell theorem, which tells you how to improve estimators, and completeness, which guarantees uniqueness.

## Key Idea

The **Rao-Blackwell theorem** says: if $\hat{\theta}$ is unbiased and $T$ is a sufficient statistic, then $\tilde{\theta} = E[\hat{\theta} \mid T]$ is also unbiased and satisfies $\text{Var}(\tilde{\theta}) \leq \text{Var}(\hat{\theta})$. Conditioning on a sufficient statistic cannot increase variance. If $T$ is also **complete**, then $\tilde{\theta}$ is the unique MVUE:

$$\text{MVUE} = E[\hat{\theta} \mid T], \quad T \text{ complete sufficient}$$

## Worked Examples

**Example 1: MVUE for $p$ in the Bernoulli distribution**

You know $T = \sum_{i=1}^n X_i$ is sufficient for $p$ (from the Sufficiency lesson). It is also complete — this means the only function of $T$ with expectation zero for all $p$ is the zero function.

The estimator $\hat{p} = \bar{X} = T/n$ is unbiased: $E[\bar{X}] = p$. Since $\bar{X}$ is a function of the complete sufficient statistic $T$, the Lehmann-Scheffé theorem guarantees $\bar{X}$ is the MVUE for $p$.

There is no need to apply Rao-Blackwell here because $\bar{X}$ is already a function of $T$. The key insight: if an unbiased estimator is already a function of a complete sufficient statistic, it is the MVUE.

---

**Example 2: Rao-Blackwell improvement for the Poisson mean**

Suppose you start with the crude estimator $\hat{\lambda} = X_1$ (just the first observation). This is unbiased: $E[X_1] = \lambda$. But it wastes observations $X_2, \ldots, X_n$.

The complete sufficient statistic for $\lambda$ is $T = \sum_{i=1}^n X_i$. Apply Rao-Blackwell: compute $E[X_1 \mid T = t]$.

By symmetry, $E[X_1 \mid T = t] = t/n$ — given the total, each observation has the same conditional expectation by exchangeability of i.i.d. variables. Therefore:

$$\tilde{\lambda} = E[X_1 \mid T] = \frac{T}{n} = \bar{X}$$

The Rao-Blackwell improvement of $X_1$ is $\bar{X}$. This is unbiased and has variance $\lambda/n$ instead of $\lambda$: a factor of $n$ improvement. Since $\bar{X}$ is a function of the complete sufficient statistic, it is the MVUE.

---

**Example 3: Uniqueness of the MVUE with a complete sufficient statistic**

When a complete sufficient statistic $T$ exists, the MVUE is unique. Here is why: suppose $\tilde{\theta}_1$ and $\tilde{\theta}_2$ are both MVUEs (both unbiased, both functions of $T$, both with the same minimum variance). Then $\tilde{\theta}_1 - \tilde{\theta}_2$ is a function of $T$ with $E[\tilde{\theta}_1 - \tilde{\theta}_2] = 0$ for all $\theta$. By the definition of completeness, the only such function is zero almost surely, so $\tilde{\theta}_1 = \tilde{\theta}_2$.

Completeness is the key: without it, two different functions of $T$ could both have expectation zero, allowing multiple MVUEs (or none at all). The exponential family distributions — Normal, Poisson, Bernoulli, Exponential — all have complete sufficient statistics, which is one reason they are so tractable.

## Common Mistakes

- **Applying Rao-Blackwell with an insufficient statistic.** Conditioning on a non-sufficient statistic can produce an estimator that is still unbiased but is no longer the MVUE. The theorem requires $T$ to be sufficient.
- **Assuming the MVUE always exists.** If no complete sufficient statistic exists, you cannot guarantee a unique MVUE. In some problems, no estimator simultaneously achieves minimum variance at every $\theta$.
- **Thinking the MVUE is necessarily efficient in the CRLB sense.** The MVUE minimizes variance among unbiased estimators, but for small $n$ the minimum achievable variance might still exceed the CRLB (if the CRLB is not achievable for that model).

## Quick Check

Try these before using hints:

1. For Normal$(\mu, \sigma^2)$ with $\sigma^2$ known, what is the MVUE for $\mu$?
2. If $\hat{\theta} = X_1^2$ is an unbiased estimator and $T = \sum X_i$ is complete sufficient, how do you improve it?
3. Why does the Rao-Blackwell theorem guarantee $\text{Var}(E[\hat{\theta}|T]) \leq \text{Var}(\hat{\theta})$?

*(Answers: $\bar{X}$; compute $E[X_1^2 \mid T]$; by the law of total variance: $\text{Var}(\hat{\theta}) = E[\text{Var}(\hat{\theta}|T)] + \text{Var}(E[\hat{\theta}|T]) \geq \text{Var}(E[\hat{\theta}|T])$)*
