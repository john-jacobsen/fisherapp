# CDF Method

## Overview

The **CDF method** (also called the distribution function method) finds the distribution of a transformed variable $Y = g(X)$ by expressing the CDF of $Y$ in terms of the CDF of $X$, then differentiating to get the PDF.

## Key Idea

To find the distribution of $Y = g(X)$:
1. Write $F_Y(y) = P(Y \le y) = P(g(X) \le y)$
2. Express as $P(X \in A)$ for some set $A$
3. Use $F_X$ to evaluate
4. Differentiate to get $f_Y(y)$

## Worked Examples

**Example 1: $X \sim \text{Uniform}(0,1)$. Find the distribution of $Y = X^2$.**

$F_Y(y) = P(X^2 \le y) = P(X \le \sqrt{y}) = \sqrt{y}$ for $0 \le y \le 1$.

$f_Y(y) = \frac{1}{2\sqrt{y}}$.

---

**Example 2: $X \sim \text{Exp}(1)$. Distribution of $Y = 2X$.**

$F_Y(y) = P(2X \le y) = P(X \le y/2) = 1 - e^{-y/2}$. So $Y \sim \text{Exp}(1/2)$.

---

**Example 3: $Y = |X|$ where $X \sim N(0,1)$**

$F_Y(y) = P(|X| \le y) = 2\Phi(y) - 1$ for $y \ge 0$. $f_Y(y) = 2\phi(y)$ (half-normal).

## Common Mistakes

- **Forgetting to account for the support** of the new variable.
- **Not checking whether $g$ is monotone** before using the change-of-variable formula.

## Quick Check

1. $X \sim U(0,1)$. CDF of $Y = \sqrt{X}$?
2. $X \sim \text{Exp}(\lambda)$. Distribution of $Y = aX$?
3. What is the CDF method used for?

*(Answers: $F_Y(y)=y^2$; Exp$(\lambda/a)$; finding distributions of transformed random variables)*
