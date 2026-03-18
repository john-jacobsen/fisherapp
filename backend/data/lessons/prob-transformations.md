# Transformations of Random Variables

## Overview

When you apply a function to a random variable, the **change-of-variables formula** gives the PDF of the result directly for monotone transformations — a shortcut vs. the full CDF method.

## Key Idea

If $Y = g(X)$ and $g$ is monotone and differentiable:

$$f_Y(y) = f_X(g^{-1}(y)) \cdot \left|\frac{d}{dy}g^{-1}(y)\right|$$

For multivariate: include the absolute Jacobian determinant.

## Worked Examples

**Example 1: $X \sim \text{Exp}(1)$. PDF of $Y = \ln X$.**

$g^{-1}(y) = e^y$, $|dg^{-1}/dy| = e^y$. $f_Y(y) = f_X(e^y) \cdot e^y = e^{-e^y} \cdot e^y$ for $y \in \mathbb{R}$.

---

**Example 2: $X \sim N(0,1)$. PDF of $Y = X^2$ (chi-squared with 1 df).**

$g^{-1}(y) = \pm\sqrt{y}$. For $y > 0$: $f_Y(y) = \frac{1}{\sqrt{2\pi y}} e^{-y/2}$.

---

**Example 3: $X \sim U(0,1)$. PDF of $Y = -\ln X$.**

$g^{-1}(y) = e^{-y}$, $|d/dy| = e^{-y}$. $f_Y(y) = 1 \cdot e^{-y} = e^{-y}$ — so $Y \sim \text{Exp}(1)$.

## Common Mistakes

- **Forgetting the absolute value of the derivative.** Sign errors change the PDF.
- **Using the formula for non-monotone $g$.** Split the domain or use the CDF method instead.

## Quick Check

1. What is the Jacobian for a 1D monotone transformation?
2. If $X \sim U(0,1)$, what is the distribution of $-\ln X$?
3. Why do we need $|dg^{-1}/dy|$?

*(Answers: $|dg^{-1}/dy|$; Exp(1); to account for stretching/squishing of the density)*
