# Bayesian Posterior

## Overview

In **Bayesian statistics**, the parameter $\theta$ is treated as a random variable. The **posterior distribution** $p(\theta | \text{data})$ combines the prior $p(\theta)$ with the likelihood via Bayes' theorem to give updated beliefs about $\theta$.

## Key Idea

$$p(\theta | x) \propto L(\theta; x) \cdot p(\theta)$$

**Posterior $\propto$ Likelihood $\times$ Prior**

A **conjugate prior** is one where the posterior has the same family as the prior (e.g., Beta prior for Binomial likelihood gives Beta posterior).

## Worked Examples

**Example 1: Binomial likelihood, Beta prior**

$X|p \sim \text{Bin}(n,p)$, $p \sim \text{Beta}(\alpha, \beta)$.

Posterior: $p|X \sim \text{Beta}(\alpha + X, \beta + n - X)$.

---

**Example 2: Posterior mean**

With $n=10$, $X=7$, prior Beta$(1,1)$ (uniform): posterior Beta$(8,4)$, mean $= 8/12 = 2/3$.

---

**Example 3: Credible interval**

A 95% **credible interval** $[a,b]$ satisfies $P(a \le \theta \le b | \text{data}) = 0.95$. Direct probability statement about $\theta$ — not the same as frequentist CI.

## Common Mistakes

- **Interpreting frequentist CI as Bayesian credible interval.** Only the Bayesian CI makes a direct probability statement about $\theta$.
- **Choosing an informative prior without justification.**

## Quick Check

1. Posterior formula?
2. What is a conjugate prior?
3. Difference between 95% CI and 95% credible interval?

*(Answers: $p(\theta|x) \propto L(\theta;x)p(\theta)$; prior where posterior has same distributional form; CI is about procedure; credible interval is about $\theta$ given data)*
