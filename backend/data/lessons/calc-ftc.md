# Fundamental Theorem of Calculus

## Overview

The **Fundamental Theorem of Calculus (FTC)** connects differentiation and integration. It has two parts: Part 1 says an integral with a variable upper limit is an antiderivative; Part 2 gives a formula for computing definite integrals.

## Key Idea

**FTC Part 1:** If $F(x) = \int_a^x f(t)\,dt$, then $F'(x) = f(x)$.

**FTC Part 2:** If $F$ is an antiderivative of $f$, then:

$$\int_a^b f(x)\,dx = F(b) - F(a)$$

## Worked Examples

**Example 1: $\int_1^3 (2x + 1)\,dx$**

Antiderivative: $F(x) = x^2 + x$. Result: $F(3) - F(1) = 12 - 2 = 10$.

---

**Example 2: $\int_0^{\pi} \sin x\,dx$**

$F(x) = -\cos x$. Result: $-\cos\pi - (-\cos 0) = 1 + 1 = 2$.

---

**Example 3: $\frac{d}{dx}\int_0^{x^2} \sin t\,dt$**

By FTC Part 1 + chain rule: $\sin(x^2) \cdot 2x = 2x\sin(x^2)$.

## Common Mistakes

- **Not applying FTC Part 1 with the chain rule** when the upper limit is a function of $x$.
- **Forgetting to subtract $F(a)$** — it's $F(b) - F(a)$, not just $F(b)$.

## Quick Check

1. $\int_0^2 3x^2\,dx$
2. $\int_1^4 \sqrt{x}\,dx$
3. $\frac{d}{dx}\int_0^x e^t\,dt$

*(Answers: 8; $14/3$; $e^x$)*
