# Moment Generating Functions

## Overview

The **moment generating function** (MGF) $M_X(t) = E[e^{tX}]$ encodes all moments of $X$ in a single function. Differentiating $M_X$ at $t = 0$ pulls out moments: the $k$-th derivative evaluated at zero gives $E[X^k]$. Beyond moments, the MGF has a uniqueness property — if two distributions share the same MGF (on an open interval containing 0), they are identical. This makes the MGF a powerful tool for identifying distributions and proving results about sums of independent random variables.

## Key Idea

The MGF and its moment-extraction rule:

$$M_X(t) = E[e^{tX}], \qquad E[X^k] = M_X^{(k)}(0) = \left.\frac{d^k}{dt^k} M_X(t)\right|_{t=0}$$

For independent $X$ and $Y$, the MGF of their sum factors:

$$M_{X+Y}(t) = M_X(t) \cdot M_Y(t) \qquad (X \perp Y)$$

This factoring works because $E[e^{t(X+Y)}] = E[e^{tX} e^{tY}] = E[e^{tX}]E[e^{tY}]$ by independence.

## Worked Examples

**Example 1: Derive the MGF of Bernoulli$(p)$**

Let $X \sim \text{Bernoulli}(p)$, so $P(X=1) = p$ and $P(X=0) = 1-p$. To compute $M_X(t) = E[e^{tX}]$, substitute each value of $X$ and weight by its probability. The expectation of $e^{tX}$ is a weighted sum over all possible values:

$$M_X(t) = e^{t \cdot 0}(1-p) + e^{t \cdot 1}(p) = (1-p) + pe^t$$

This is valid for all $t \in \mathbb{R}$. Notice that $M_X(0) = (1-p) + p = 1$, as required — every MGF equals 1 at $t = 0$ because $e^{0 \cdot X} = 1$ always.

---

**Example 2: Use derivatives to find $E[X]$ and $E[X^2]$**

Using the Bernoulli MGF $M_X(t) = (1-p) + pe^t$, differentiate to extract moments. The reason derivatives at 0 give moments is the Taylor expansion $e^{tX} = 1 + tX + \frac{t^2 X^2}{2!} + \cdots$, so $E[e^{tX}] = 1 + tE[X] + \frac{t^2}{2}E[X^2] + \cdots$ and the $k$-th coefficient is $E[X^k]/k!$.

First derivative: $M_X'(t) = pe^t$. Evaluate at $t=0$:

$$E[X] = M_X'(0) = pe^0 = p$$

Second derivative: $M_X''(t) = pe^t$. Evaluate at $t=0$:

$$E[X^2] = M_X''(0) = p$$

From these: $\text{Var}(X) = E[X^2] - (E[X])^2 = p - p^2 = p(1-p)$, the standard Bernoulli variance.

---

**Example 3: Identify a distribution from its MGF**

Suppose you are told that $M_X(t) = e^{\mu t + \frac{1}{2}\sigma^2 t^2}$ for some $\mu$ and $\sigma^2 > 0$. You need to identify the distribution of $X$.

The MGF of $N(\mu, \sigma^2)$ is exactly $e^{\mu t + \frac{1}{2}\sigma^2 t^2}$. By the uniqueness property of MGFs — if two random variables have the same MGF on an open interval containing 0, they have the same distribution — you can conclude:

$$X \sim N(\mu, \sigma^2)$$

This is how MGFs are used to prove the CLT and to show that sums of independent normals are normal: compute the MGF of the sum, recognize its form, and invoke uniqueness. No integration or convolution is needed.

## Common Mistakes

- **Confusing $M_X(t) = E[e^{tX}]$ with the characteristic function $E[e^{itX}]$.** The MGF uses a real argument $t$; the characteristic function uses an imaginary argument. MGFs may not exist for all distributions (e.g., heavy-tailed ones), while characteristic functions always exist.
- **Differentiating with respect to $X$ instead of $t$.** The moments come from derivatives with respect to $t$, the auxiliary variable, not with respect to $X$.
- **Forgetting to evaluate at $t = 0$ after differentiating.** The derivative $M_X^{(k)}(t)$ gives a function of $t$; you must plug in $t = 0$ to get $E[X^k]$.

## Quick Check

1. What is $M_X(0)$ for any random variable $X$?
2. If $M_X(t) = e^{3t + 2t^2}$, what are $E[X]$ and $\text{Var}(X)$?
3. If $X$ and $Y$ are independent with MGFs $M_X(t)$ and $M_Y(t)$, what is the MGF of $X + Y$?

*(Answers: 1; $E[X] = M_X'(0) = 3$, $\text{Var}(X) = 4$ since $E[X^2]=M_X''(0)=9+4=13$ so $\text{Var}=13-9=4$; $M_X(t) \cdot M_Y(t)$)*
