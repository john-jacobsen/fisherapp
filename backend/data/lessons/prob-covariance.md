# Covariance and Variance of Sums

## Overview

**Covariance** measures the linear relationship between two random variables. If $X$ tends to be large when $Y$ is large, $\text{Cov}(X,Y) > 0$. Covariance is essential for computing the variance of sums.

## Key Idea

$$\text{Cov}(X,Y) = E[(X-\mu_X)(Y-\mu_Y)] = E[XY] - E[X]E[Y]$$

$$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X,Y)$$

If $X \perp Y$: $\text{Cov}(X,Y) = 0$ and $\text{Var}(X+Y) = \text{Var}(X) + \text{Var}(Y)$.

## Worked Examples

**Example 1: $E[XY] = 10$, $E[X] = 2$, $E[Y] = 4$. Find $\text{Cov}(X,Y)$.**

$\text{Cov} = 10 - 8 = 2$.

---

**Example 2: $\text{Var}(X+Y)$ if $\text{Var}(X)=4$, $\text{Var}(Y)=9$, $\text{Cov}(X,Y)=3$**

$\text{Var}(X+Y) = 4 + 9 + 6 = 19$.

---

**Example 3: Correlation**

$\text{Corr}(X,Y) = \frac{\text{Cov}(X,Y)}{\sigma_X \sigma_Y} \in [-1,1]$.

## Common Mistakes

- **Assuming $\text{Cov}=0$ implies independence.** Zero covariance does not imply independence in general.
- **Wrong sign when $X$ and $Y$ tend to go in opposite directions.**

## Quick Check

1. $\text{Cov}(X,X) = ?$
2. $\text{Var}(X-Y)$ in terms of Var and Cov?
3. If $X \perp Y$, what is $\text{Cov}(X,Y)$?

*(Answers: $\text{Var}(X)$; $\text{Var}(X)+\text{Var}(Y)-2\text{Cov}(X,Y)$; 0)*
