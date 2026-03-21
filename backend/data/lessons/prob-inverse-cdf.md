# Inverse CDF Method

## Overview

The **inverse CDF method** (also called the quantile transform) lets you generate a random variable with any target distribution $F$ using only a Uniform$(0,1)$ random variable. It works because $F^{-1}(U)$ has exactly the CDF $F$ — a fact that follows directly from the definition of the CDF and the uniform distribution. This technique is the backbone of random number generation in simulation software.

## Key Idea

If $U \sim \text{Uniform}(0,1)$ and $F$ is any CDF with inverse $F^{-1}$, then:

$$X = F^{-1}(U) \quad \text{has CDF } F$$

Why it works: $P(X \leq x) = P(F^{-1}(U) \leq x) = P(U \leq F(x)) = F(x)$, since $F(x) \in [0,1]$ and $U$ is uniform on $[0,1]$. The last step uses the fact that $P(U \leq t) = t$ for any $t \in [0,1]$.

## Worked Examples

**Example 1: Generate $\text{Exp}(\lambda)$ samples from a Uniform$(0,1)$ variable.**

Start from the CDF of the exponential: $F(x) = 1 - e^{-\lambda x}$. To find $F^{-1}$, set $u = 1 - e^{-\lambda x}$ and solve for $x$ — you want to express $x$ as a function of the uniform probability $u$.

$$u = 1 - e^{-\lambda x} \implies e^{-\lambda x} = 1 - u \implies x = -\frac{1}{\lambda}\ln(1-u)$$

So $X = -\frac{1}{\lambda}\ln(1-U) \sim \text{Exp}(\lambda)$. In practice, since $1-U$ has the same distribution as $U$ when $U \sim \text{Uniform}(0,1)$, you can simplify to $X = -\frac{1}{\lambda}\ln(U)$ without changing the distribution of the output.

---

**Example 2: Find the quantile function for a simple piecewise PDF.**

Suppose $f(x) = 2x$ on $[0,1]$. First find the CDF by integrating: $F(x) = x^2$ on $[0,1]$. To find $F^{-1}$, set $u = x^2$ and solve for $x$: since $x \geq 0$, $x = \sqrt{u}$.

Therefore $F^{-1}(u) = \sqrt{u}$. To generate a random variable with PDF $f(x) = 2x$, compute $X = \sqrt{U}$ where $U \sim \text{Uniform}(0,1)$. You can verify: the change-of-variables formula applied to $X = \sqrt{U}$ gives $f_X(x) = f_U(x^2) \cdot 2x = 1 \cdot 2x = 2x$, confirming the result.

---

**Example 3: Use the method to identify the median from the CDF.**

The median is the value $m$ where $F(m) = 0.5$ — which is exactly $F^{-1}(0.5)$. Setting $U = 0.5$ (a fixed probability, not a random variable) in the inverse CDF formula gives the median directly.

For $\text{Exp}(\lambda)$: $F^{-1}(0.5) = -\frac{1}{\lambda}\ln(1 - 0.5) = \frac{\ln 2}{\lambda}$. For the distribution with CDF $F(x) = x^2$ on $[0,1]$: $F^{-1}(0.5) = \sqrt{0.5} = \frac{1}{\sqrt{2}} \approx 0.707$. The inverse CDF method unifies random number generation and quantile computation — both use exactly the same formula.

## Common Mistakes

- **Inverting $F$ algebraically without checking monotonicity.** The inverse $F^{-1}$ exists as a function only when $F$ is strictly increasing. For discrete distributions, $F$ has flat steps, so you use the generalized inverse $F^{-1}(u) = \inf\{x : F(x) \geq u\}$ instead.
- **Confusing $F^{-1}$ (inverse CDF) with $1/F$.** The notation $F^{-1}$ means the functional inverse — the value $x$ such that $F(x) = u$ — not the reciprocal $1/F(u)$.

## Quick Check

1. $F(x) = 1 - e^{-3x}$ for $x \geq 0$. Find $F^{-1}(u)$ and use it to generate $\text{Exp}(3)$ samples.
2. What does $F^{-1}(0.25)$ represent?
3. Why does $P(F^{-1}(U) \leq x) = F(x)$?

*(Answers: $F^{-1}(u) = -\frac{1}{3}\ln(1-u)$, so use $X = -\frac{1}{3}\ln(1-U)$; the 25th percentile (first quartile); because $F^{-1}(U) \leq x \iff U \leq F(x)$, and $P(U \leq F(x)) = F(x)$ for $U \sim \text{Uniform}(0,1)$)*
