# Bivariate Normal Distribution

## Overview

The **bivariate normal distribution** is the joint normal distribution of two random variables $(X,Y)$. It is fully characterized by the means, variances, and correlation $\rho$ of $X$ and $Y$.

## Key Idea

$(X,Y) \sim N_2(\mu_X, \mu_Y, \sigma_X^2, \sigma_Y^2, \rho)$.

Key facts:
- Marginals: $X \sim N(\mu_X, \sigma_X^2)$, $Y \sim N(\mu_Y, \sigma_Y^2)$
- Conditional: $Y|X=x \sim N\!\left(\mu_Y + \rho\frac{\sigma_Y}{\sigma_X}(x-\mu_X),\; \sigma_Y^2(1-\rho^2)\right)$
- $X \perp Y \iff \rho = 0$ (unique to the normal family!)

## Worked Examples

**Example 1: $X, Y$ bivariate normal with $\rho = 0$. Are they independent?**

Yes — for bivariate normals, zero correlation implies independence.

---

**Example 2: $X \sim N(0,1)$, $Y \sim N(0,1)$, $\rho = 0.8$. $E[Y|X=2]$?**

$E[Y|X=2] = 0 + 0.8(1/1)(2-0) = 1.6$.

---

**Example 3: Conditional variance**

$\text{Var}(Y|X=2) = 1(1 - 0.64) = 0.36$.

## Common Mistakes

- **Assuming zero correlation implies independence in general.** This only holds for the normal family.
- **Confusing the conditional distribution's mean and variance with the unconditional ones.**

## Quick Check

1. $(X,Y)$ bivariate normal with $\rho=0$. Are they independent?
2. Marginal of $X$ from bivariate normal?
3. $\text{Var}(Y|X=x)$ depends on $x$?

*(Answers: yes; $N(\mu_X,\sigma_X^2)$; no — it's constant $\sigma_Y^2(1-\rho^2)$)*
