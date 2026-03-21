# Covariance and Correlation

## Overview

**Covariance** measures how two random variables move together — whether large values of $X$ tend to pair with large values of $Y$ (positive covariance) or with small values of $Y$ (negative covariance). **Correlation** normalizes covariance to the interval $[-1, 1]$, making it unit-free and directly comparable across different variable scales. Both quantities summarize the linear relationship between $X$ and $Y$.

## Key Idea

The covariance shortcut formula avoids computing a double sum or integral directly:

$$\text{Cov}(X, Y) = E[XY] - E[X]\,E[Y]$$

The correlation coefficient normalizes by both standard deviations:

$$\rho = \frac{\text{Cov}(X, Y)}{\sqrt{\text{Var}(X)\,\text{Var}(Y)}}$$

Key properties: $\text{Cov}(X, X) = \text{Var}(X)$; $\rho \in [-1, 1]$; $\rho = \pm 1$ if and only if $Y = aX + b$ for some constants $a$ and $b$.

## Worked Examples

**Example 1: Compute $\text{Cov}(X, Y)$ from a joint PMF table**

Suppose $(X, Y)$ has joint PMF:

| | $Y=0$ | $Y=2$ |
|---|---|---|
| $X=1$ | 0.3 | 0.2 |
| $X=3$ | 0.1 | 0.4 |

First compute the marginal means. For $X$: $E[X] = 1(0.3 + 0.2) + 3(0.1 + 0.4) = 0.5 + 1.5 = 2.0$. For $Y$: $E[Y] = 0(0.3 + 0.1) + 2(0.2 + 0.4) = 0 + 1.2 = 1.2$.

Now compute $E[XY]$ by summing $xy \cdot p(x,y)$ over all $(x,y)$ pairs. The product $xy$ weights each pair by its joint probability:

$$E[XY] = (1)(0)(0.3) + (1)(2)(0.2) + (3)(0)(0.1) + (3)(2)(0.4) = 0 + 0.4 + 0 + 2.4 = 2.8$$

Apply the shortcut: $\text{Cov}(X, Y) = 2.8 - (2.0)(1.2) = 2.8 - 2.4 = 0.4$. The positive value confirms that larger $X$ tends to pair with larger $Y$.

---

**Example 2: Use the shortcut $E[XY] - E[X]E[Y]$**

Let $X \sim \text{Bernoulli}(0.5)$ and $Y = X^2$. Since $X \in \{0,1\}$, we have $X^2 = X$, so $Y = X$.

Compute: $E[X] = 0.5$, $E[Y] = E[X] = 0.5$, and $E[XY] = E[X \cdot X] = E[X^2] = E[X] = 0.5$ (because $X^2 = X$ for Bernoulli).

Applying the shortcut: $\text{Cov}(X, Y) = 0.5 - (0.5)(0.5) = 0.25$. This equals $\text{Var}(X)$, which makes sense because $Y = X$ means $\text{Cov}(X, Y) = \text{Cov}(X, X) = \text{Var}(X)$.

---

**Example 3: Compute and interpret $\rho$**

Using Example 1: $\text{Var}(X) = E[X^2] - (E[X])^2$. Compute $E[X^2] = 1^2(0.5) + 3^2(0.5) = 0.5 + 4.5 = 5.0$, so $\text{Var}(X) = 5.0 - 4.0 = 1.0$. Similarly, $E[Y^2] = 0^2(0.4) + 2^2(0.6) = 2.4$, so $\text{Var}(Y) = 2.4 - 1.44 = 0.96$.

$$\rho = \frac{0.4}{\sqrt{(1.0)(0.96)}} = \frac{0.4}{0.98} \approx 0.408$$

A correlation of about 0.41 indicates a moderate positive linear relationship. Note: if $X$ and $Y$ are independent, then $E[XY] = E[X]E[Y]$, so $\text{Cov}(X,Y) = 0$ and $\rho = 0$. However, $\rho = 0$ does not imply independence — it only rules out linear dependence.

## Common Mistakes

- **Confusing $\rho = 0$ with independence.** Zero correlation means no linear relationship, but $X$ and $Y$ can still be dependent in a nonlinear way. Independence implies $\rho = 0$, but the converse fails in general.
- **Forgetting the sign carries meaning.** A negative covariance means the variables move in opposite directions on average. Squaring or taking the absolute value destroys this information; do not report only $|\text{Cov}(X,Y)|$.
- **Using covariance to compare different pairs.** Because covariance depends on units, a covariance of 10 for one pair and 2 for another does not mean the first pair is more strongly related. Use $\rho$ for comparisons across different scales.

## Quick Check

1. If $E[XY] = 6$, $E[X] = 2$, $E[Y] = 4$, what is $\text{Cov}(X,Y)$?
2. If $X$ and $Y$ are independent, what is $\text{Cov}(X, Y)$?
3. If $\text{Cov}(X,Y) = -3$, $\text{Var}(X) = 4$, $\text{Var}(Y) = 9$, what is $\rho$?

*(Answers: $6 - 8 = -2$; $0$; $\rho = -3/\sqrt{36} = -0.5$)*
