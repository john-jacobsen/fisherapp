# Chain Rule

## Overview

The **chain rule** differentiates composite functions $f(g(x))$. It says: differentiate the outer function (keeping the inner function intact), then multiply by the derivative of the inner function.

## Key Idea

$$\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)$$

Think of it as: (derivative of outer at inner) × (derivative of inner).

## Worked Examples

**Example 1: Differentiate $h(x) = (3x + 1)^5$**

Outer: $u^5$, inner: $3x+1$. $h'(x) = 5(3x+1)^4 \cdot 3 = 15(3x+1)^4$.

---

**Example 2: Differentiate $f(x) = \sin(x^2)$**

$f'(x) = \cos(x^2) \cdot 2x = 2x\cos(x^2)$.

---

**Example 3: Differentiate $g(x) = e^{-x^2}$**

$g'(x) = e^{-x^2} \cdot (-2x) = -2x e^{-x^2}$.

## Common Mistakes

- **Forgetting the chain rule entirely** when differentiating a composite.
- **Applying chain rule when it's not needed** (e.g., $f(x) = x^3$ is not a composition).

## Quick Check

1. $\frac{d}{dx}(\sqrt{2x+3})$
2. $\frac{d}{dx}(\cos(5x))$
3. $\frac{d}{dx}((x^2+1)^4)$

*(Answers: $\frac{1}{\sqrt{2x+3}}$; $-5\sin(5x)$; $8x(x^2+1)^3$)*
