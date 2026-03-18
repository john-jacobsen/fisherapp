# Gamma Distribution

## Overview

The **Gamma distribution** generalizes the Exponential: it models the waiting time until the $r$-th event in a Poisson process. It is also a flexible two-parameter family used for skewed positive data.

## Key Idea

$X \sim \text{Gamma}(r, \lambda)$ (shape $r$, rate $\lambda$):

$$f(x) = \frac{\lambda^r x^{r-1} e^{-\lambda x}}{\Gamma(r)}, \quad x > 0$$

$$E[X] = \frac{r}{\lambda}, \quad \text{Var}(X) = \frac{r}{\lambda^2}$$

Gamma$(1, \lambda) = $ Exp$(\lambda)$. The sum of $r$ independent Exp$(\lambda)$ variables is Gamma$(r, \lambda)$.

## Worked Examples

**Example 1: $r=3$, $\lambda=2$. Find $E[X]$ and $\text{Var}(X)$.**

$E[X] = 3/2 = 1.5$. $\text{Var}(X) = 3/4$.

---

**Example 2: Wait for 3rd customer (rate 2/hr). Expected wait?**

$E[X] = 3/2 = 1.5$ hours.

---

**Example 3: $\Gamma(n/2, 1/2)$ is the chi-squared distribution $\chi^2(n)$.**

This connection is used in statistical testing.

## Common Mistakes

- **Confusing shape and rate parameterizations.** Some texts use scale $\theta = 1/\lambda$ instead.
- **Thinking Gamma$(r,\lambda)$ requires integer $r$.** $r$ can be any positive real number.

## Quick Check

1. What distribution is Gamma$(1, \lambda)$?
2. $E[X]$ for Gamma$(4, 2)$?
3. Sum of 5 independent Exp$(3)$ variables has what distribution?

*(Answers: Exp($\lambda$); 2; Gamma(5,3))*
