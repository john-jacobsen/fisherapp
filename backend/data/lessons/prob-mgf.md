# Moment Generating Functions

## Overview

The **moment generating function (MGF)** of a random variable $X$ uniquely characterizes its distribution and provides a convenient way to compute all moments. It is used to prove convergence results and derive distributions of sums.

## Key Idea

$$M_X(t) = E[e^{tX}] = \sum_x e^{tx} p(x) \quad \text{or} \quad \int e^{tx} f(x)\,dx$$

The $n$-th moment: $E[X^n] = M_X^{(n)}(0)$.

If $X \perp Y$: $M_{X+Y}(t) = M_X(t)\,M_Y(t)$.

## Worked Examples

**Example 1: MGF of Bernoulli$(p)$**

$M(t) = (1-p) + pe^t$.

---

**Example 2: MGF of $N(0,1)$**

$M(t) = e^{t^2/2}$. In general, $N(\mu,\sigma^2)$ has MGF $e^{\mu t + \sigma^2 t^2/2}$.

---

**Example 3: Sum of independent normals via MGF**

$M_{X+Y}(t) = e^{\mu_1 t + \sigma_1^2 t^2/2} \cdot e^{\mu_2 t + \sigma_2^2 t^2/2} = e^{(\mu_1+\mu_2)t + (\sigma_1^2+\sigma_2^2)t^2/2}$, which is the MGF of $N(\mu_1+\mu_2, \sigma_1^2+\sigma_2^2)$.

## Common Mistakes

- **Differentiating $M(t)$ without evaluating at $t=0$.** The $n$-th moment requires $M^{(n)}(0)$.
- **MGF may not exist for all distributions** (e.g., Cauchy has no MGF).

## Quick Check

1. $E[X] = M'(0)$ — where is this evaluated?
2. MGF of Poisson$(\lambda)$?
3. Sum of independent Exp$(1)$ variables: what is its distribution? (use MGFs)

*(Answers: at $t=0$; $e^{\lambda(e^t-1)}$; Gamma$(n,1)$)*
