# U-Substitution

## Overview

**U-substitution** is the integration analogue of the chain rule. It works by substituting $u = g(x)$ to simplify an integral of the form $\int f(g(x))\,g'(x)\,dx$.

## Key Idea

Let $u = g(x)$, then $du = g'(x)\,dx$. The integral becomes:

$$\int f(g(x))\,g'(x)\,dx = \int f(u)\,du$$

Integrate in terms of $u$, then substitute back.

## Worked Examples

**Example 1: $\int 2x(x^2+1)^4\,dx$**

$u = x^2+1$, $du = 2x\,dx$. Integral: $\int u^4\,du = \frac{u^5}{5} + C = \frac{(x^2+1)^5}{5} + C$.

---

**Example 2: $\int \sin(3x)\,dx$**

$u = 3x$, $du = 3\,dx$, so $dx = du/3$. Integral: $\frac{1}{3}\int \sin u\,du = -\frac{\cos(3x)}{3} + C$.

---

**Example 3: $\int_0^1 2x e^{x^2}\,dx$**

$u = x^2$, $du = 2x\,dx$. New limits: $u(0)=0$, $u(1)=1$. Integral: $\int_0^1 e^u\,du = e-1$.

## Common Mistakes

- **Forgetting to change $dx$ (or limits for definite integrals).**
- **Choosing a $u$ that leaves leftover $x$'s you can't express in terms of $u$.**

## Quick Check

1. $\int 3(3x-1)^2\,dx$
2. $\int \frac{2x}{x^2+4}\,dx$
3. $\int_0^{\pi/2} \cos x \cdot e^{\sin x}\,dx$

*(Answers: $(3x-1)^3+C$; $\ln(x^2+4)+C$; $e-1$)*
