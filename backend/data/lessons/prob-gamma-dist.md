# Gamma Distribution

## Overview

The **Gamma distribution** generalizes the exponential — where the exponential models the wait until the 1st event in a Poisson process, the Gamma$(r, \lambda)$ distribution models the wait until the $r$-th event. It has a shape parameter $r > 0$ and a rate parameter $\lambda > 0$. Because it can take on a wide variety of shapes (ranging from exponential to approximately normal as $r$ grows), it is one of the most flexible distributions for modeling positive, right-skewed data.

## Key Idea

For $X \sim \text{Gamma}(r, \lambda)$ with $x > 0$:

$$f(x) = \frac{\lambda^r x^{r-1} e^{-\lambda x}}{\Gamma(r)}$$

$$E[X] = \frac{r}{\lambda}, \qquad \text{Var}(X) = \frac{r}{\lambda^2}$$

The special case $r = 1$ recovers the exponential: $\text{Gamma}(1, \lambda) = \text{Exp}(\lambda)$. The function $\Gamma(r)$ is the gamma function; for positive integers, $\Gamma(r) = (r-1)!$.

## Worked Examples

**Example 1: $X \sim \text{Gamma}(3, 2)$ — identify what $r$ and $\lambda$ mean in context.**

In a Poisson process with rate $\lambda = 2$ events per minute, $X$ represents the waiting time until the 3rd event arrives. The shape parameter $r = 3$ counts how many events you are waiting for; the rate parameter $\lambda = 2$ controls how fast those events arrive. This interpretation connects the Gamma directly to the Poisson process: you are stacking $r$ independent exponential waiting times on top of each other.

The PDF has $r = 3$ and $\lambda = 2$, so $f(x) = \frac{2^3 x^2 e^{-2x}}{\Gamma(3)} = \frac{8x^2 e^{-2x}}{2} = 4x^2 e^{-2x}$ for $x > 0$.

---

**Example 2: Find $E[X]$ and $\text{Var}(X)$ for $X \sim \text{Gamma}(3, 2)$.**

Plug $r = 3$ and $\lambda = 2$ into the formulas. The mean $r/\lambda$ makes intuitive sense: you are waiting for 3 events and each takes $1/\lambda$ time on average, so the total expected wait is $r$ times that.

$$E[X] = \frac{r}{\lambda} = \frac{3}{2} = 1.5 \text{ min}$$

$$\text{Var}(X) = \frac{r}{\lambda^2} = \frac{3}{4} = 0.75 \text{ min}^2$$

As $r$ increases (waiting for more events), the mean grows and the distribution spreads — but it also becomes more symmetric and bell-shaped, which is why the Gamma converges to a normal distribution for large $r$ by the Central Limit Theorem.

---

**Example 3: The sum of independent exponentials is Gamma.**

Suppose $X_1, X_2, \ldots, X_r$ are independent and each $X_i \sim \text{Exp}(\lambda)$. Then their sum $S = X_1 + X_2 + \cdots + X_r$ follows $\text{Gamma}(r, \lambda)$.

This is why the Gamma models the wait for the $r$-th event: you add up $r$ independent inter-event gaps, each exponentially distributed. The mean confirms the intuition — $E[S] = r \cdot E[X_i] = r/\lambda$. For example, if 5 independent jobs each take $\text{Exp}(3)$ time, the total processing time follows $\text{Gamma}(5, 3)$ with mean $5/3$ minutes.

## Common Mistakes

- **Mixing up rate and scale parameterizations.** Some textbooks parameterize by scale $\theta = 1/\lambda$ instead of rate $\lambda$, giving $E[X] = r\theta$. Always confirm which convention is in use before applying formulas.
- **Assuming $r$ must be a positive integer.** The Gamma distribution is defined for any $r > 0$ via the gamma function $\Gamma(r)$. Integer $r$ just makes the PDF formula simplify because $\Gamma(r) = (r-1)!$.

## Quick Check

1. What distribution is $\text{Gamma}(1, \lambda)$?
2. Find $E[X]$ and $\text{Var}(X)$ for $\text{Gamma}(4, 2)$.
3. The sum of 5 independent $\text{Exp}(3)$ random variables has what distribution?

*(Answers: $\text{Exp}(\lambda)$; $E[X] = 2$, $\text{Var}(X) = 1$; $\text{Gamma}(5, 3)$)*
