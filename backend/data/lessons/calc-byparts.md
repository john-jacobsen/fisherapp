# Integration by Parts

## Overview

**Integration by parts** handles integrals of products where $u$-substitution doesn't apply. The rule comes from integrating the product rule.

## Key Idea

$$\int u\,dv = uv - \int v\,du$$

Choose $u$ and $dv$ using the LIATE priority: Logarithm, Inverse trig, Algebraic, Trigonometric, Exponential — pick the first type in this list as $u$.

## Worked Examples

**Example 1: $\int x e^x\,dx$**

$u = x$, $dv = e^x\,dx$. Then $du = dx$, $v = e^x$.

$$\int x e^x\,dx = x e^x - \int e^x\,dx = xe^x - e^x + C = e^x(x-1) + C$$

---

**Example 2: $\int x \ln x\,dx$**

$u = \ln x$, $dv = x\,dx$. Then $du = dx/x$, $v = x^2/2$.

$$\frac{x^2}{2}\ln x - \int \frac{x}{2}\,dx = \frac{x^2}{2}\ln x - \frac{x^2}{4} + C$$

---

**Example 3: $\int e^x \sin x\,dx$**

Apply integration by parts twice (both times $u = \sin x$ or $u = \cos x$, keeping exponential as $dv$). After two steps, the original integral appears on both sides — solve algebraically.

$$\int e^x \sin x\,dx = \frac{e^x(\sin x - \cos x)}{2} + C$$

## Common Mistakes

- **Bad choice of $u$ and $dv$** — if $v$ is harder to integrate than the original, switch the assignment.
- **Forgetting to subtract the whole $\int v\,du$, not just $v$.**

## Quick Check

1. $\int x \cos x\,dx$
2. $\int \ln x\,dx$
3. $\int x^2 e^x\,dx$

*(Answers: $x\sin x + \cos x + C$; $x\ln x - x + C$; $e^x(x^2-2x+2)+C$)*
