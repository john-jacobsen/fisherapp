# Marginal Distributions

## Overview

The **marginal distribution** of one variable is obtained by integrating (or summing) the joint distribution over all values of the other variable. It tells you about one variable without conditioning on the other.

## Key Idea

From joint distribution $f(x,y)$ or $p(x,y)$:

$$f_X(x) = \int_{-\infty}^{\infty} f(x,y)\,dy \quad \text{(continuous)}$$

$$p_X(x) = \sum_y p(x,y) \quad \text{(discrete)}$$

## Worked Examples

**Example 1: From joint table**

| | $Y=0$ | $Y=1$ |
|---|---|---|
|$X=0$| 0.2 | 0.1 |
|$X=1$| 0.3 | 0.4 |

$p_X(0) = 0.3$, $p_X(1) = 0.7$, $p_Y(0) = 0.5$, $p_Y(1) = 0.5$.

---

**Example 2: Marginal of $X \sim N(\mu_X, \sigma_X^2)$ from bivariate normal**

The marginal of a bivariate normal is univariate normal. You "integrate out" $y$.

---

**Example 3: Marginal from $f(x,y) = e^{-(x+y)}$ on $x,y > 0$**

$f_X(x) = \int_0^\infty e^{-(x+y)}\,dy = e^{-x}$ — so $X \sim \text{Exp}(1)$.

## Common Mistakes

- **Confusing marginal with conditional.** Marginal integrates out $y$; conditional fixes $y$.
- **Wrong integration limits** when support is not the full plane.

## Quick Check

1. How do you get the marginal PMF $p_X(x)$?
2. $f_Y(y)$ for $f(x,y) = e^{-(x+y)}$ on $x,y>0$?
3. If $X$ and $Y$ are independent, do the marginals determine the joint?

*(Answers: sum over all $y$; $e^{-y}$; yes, $f(x,y)=f_Xf_Y$)*
