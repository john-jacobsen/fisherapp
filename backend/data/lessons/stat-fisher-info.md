# Fisher Information

## Overview

**Fisher information** $I(\theta)$ quantifies how much information a random variable (or sample) carries about an unknown parameter. Higher Fisher information means the parameter can be estimated more precisely.

## Key Idea

$$I(\theta) = E\left[\left(\frac{\partial}{\partial\theta} \ln f(X;\theta)\right)^2\right] = -E\left[\frac{\partial^2}{\partial\theta^2} \ln f(X;\theta)\right]$$

For $n$ iid observations: $I_n(\theta) = n \cdot I_1(\theta)$.

## Worked Examples

**Example 1: Fisher information for Bernoulli$(p)$**

$\ln f = x\ln p + (1-x)\ln(1-p)$. Score: $x/p - (1-x)/(1-p)$. $I(p) = 1/(p(1-p))$.

---

**Example 2: Fisher information for $N(\mu, \sigma^2)$ (known $\sigma^2$)**

$I(\mu) = 1/\sigma^2$. More variance = less information.

---

**Example 3: Information and sample size**

For $n$ iid observations from Bernoulli$(p)$: $I_n(p) = n/(p(1-p))$.

## Common Mistakes

- **Fisher information is not the same as the observed information.** Observed information is $-d^2\ell/d\theta^2$ at $\hat{\theta}$.
- **I(θ) can depend on θ.** It is generally a function of the true parameter.

## Quick Check

1. $I(\lambda)$ for Poisson$(\lambda)$?
2. What does high $I(\theta)$ imply about estimation?
3. $I_n(\theta) = ?$ for $n$ iid observations?

*(Answers: $1/\lambda$; can estimate $\theta$ precisely; $nI_1(\theta)$)*
