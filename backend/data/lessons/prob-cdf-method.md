# CDF Method for Transformations

## Overview

The **CDF method** finds the distribution of $Y = g(X)$ by expressing the CDF of $Y$ directly in terms of the CDF of $X$, then differentiating to get the PDF. It works for any transformation — monotone or not — because the CDF is always well defined even when the change-of-variables formula would require splitting into cases. The connection to the Fundamental Theorem of Calculus is what makes differentiation the right final step.

## Key Idea

To find the distribution of $Y = g(X)$:

$$F_Y(y) = P(Y \leq y) = P(g(X) \leq y)$$

Rewrite the inequality $g(X) \leq y$ as a condition on $X$, evaluate using $F_X$, then differentiate:

$$f_Y(y) = \frac{d}{dy} F_Y(y)$$

The Fundamental Theorem of Calculus guarantees that differentiating the CDF recovers the PDF, which is why this step always works.

## Worked Examples

**Example 1: $X \sim \text{Uniform}(0, 1)$. Find the PDF of $Y = X^2$.**

Since $X \in [0,1]$, we have $Y \in [0,1]$ as well. For $0 \leq y \leq 1$, write the CDF of $Y$ by inverting the transformation. The inequality $X^2 \leq y$ is equivalent to $X \leq \sqrt{y}$ when $X \geq 0$, so you can directly express $F_Y$ using the uniform CDF $F_X(x) = x$.

$$F_Y(y) = P(X^2 \leq y) = P(X \leq \sqrt{y}) = F_X(\sqrt{y}) = \sqrt{y}$$

Now differentiate to get the PDF — the derivative of $\sqrt{y}$ is $\frac{1}{2\sqrt{y}}$, which is the payoff of differentiating the CDF:

$$f_Y(y) = \frac{d}{dy}\sqrt{y} = \frac{1}{2\sqrt{y}}, \quad 0 < y < 1$$

This is a Beta$(1/2, 1)$ distribution — the transformation compressed the uniform distribution near zero and spread it near one.

---

**Example 2: $Y = e^X$ where $X$ has PDF $f_X$ on $\mathbb{R}$. Derive the PDF of $Y$.**

Since $e^X$ is always positive, $Y > 0$. For $y > 0$, the inequality $e^X \leq y$ is equivalent to $X \leq \ln y$ (because the natural log is an increasing function and preserves the inequality direction). This is exactly where monotonicity matters — inverting the inequality cleanly.

$$F_Y(y) = P(e^X \leq y) = P(X \leq \ln y) = F_X(\ln y)$$

Differentiate using the chain rule — the derivative of $F_X(\ln y)$ with respect to $y$ brings down a factor of $1/y$:

$$f_Y(y) = f_X(\ln y) \cdot \frac{1}{y}, \quad y > 0$$

If $X \sim N(0,1)$, this gives the log-normal PDF — a common distribution for positive data like stock prices.

---

**Example 3: Explain why differentiating the CDF gives the PDF.**

By the Fundamental Theorem of Calculus, if $F_Y(y) = \int_{-\infty}^{y} f_Y(t)\,dt$, then differentiating both sides with respect to $y$ yields $\frac{d}{dy} F_Y(y) = f_Y(y)$. This is not a trick — it is the defining relationship between the CDF and PDF. The CDF accumulates probability up to $y$; the PDF is the rate at which that accumulation happens. Differentiating undoes the integral and recovers the density. This is why the CDF method always ends with differentiation rather than some other operation.

## Common Mistakes

- **Inverting the inequality incorrectly for decreasing functions.** If $g$ is decreasing, then $g(X) \leq y$ becomes $X \geq g^{-1}(y)$, flipping the inequality. For example, $P(1/X \leq y) = P(X \geq 1/y)$ when $X > 0$ and $y > 0$.
- **Forgetting to check the support of $Y$.** Transformations change the domain. If $X \in [0, 1]$ and $Y = X^2$, then $Y \in [0, 1]$. If $X \in [-1, 1]$ and $Y = X^2$, then $Y \in [0, 1]$ but the CDF expression is different.

## Quick Check

1. $X \sim U(0,1)$. Use the CDF method to find the PDF of $Y = \sqrt{X}$.
2. $X \sim \text{Exp}(\lambda)$. Find the CDF of $Y = 2X$, then identify its distribution.
3. Why does the CDF method work for non-monotone transformations like $Y = X^2$?

*(Answers: $f_Y(y) = 2y$ on $[0,1]$; $F_Y(y) = 1 - e^{-\lambda y/2}$, so $Y \sim \text{Exp}(\lambda/2)$; inverting the inequality to a set on $X$ works even without monotonicity — you just describe the set $\{X : g(X) \leq y\}$ directly)*
