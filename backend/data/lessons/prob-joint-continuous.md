# Joint Continuous Distributions

## Overview

The **joint density** $f(x,y)$ of two continuous random variables satisfies $P(X \in A, Y \in B) = \iint_{A\times B} f(x,y)\,dx\,dy$. Joint continuous distributions generalize everything from the discrete case.

## Key Idea

Valid joint PDF: $f(x,y) \ge 0$ and $\int\int f(x,y)\,dx\,dy = 1$.

Marginals: $f_X(x) = \int_{-\infty}^{\infty} f(x,y)\,dy$ and $f_Y(y) = \int_{-\infty}^{\infty} f(x,y)\,dx$.

Independence: $f(x,y) = f_X(x)\,f_Y(y)$.

## Worked Examples

**Example 1: $f(x,y) = 6xy^2$ on $0 \le x \le 1$, $0 \le y \le 1$. Valid PDF?**

$\int_0^1\int_0^1 6xy^2\,dy\,dx = 6 \cdot (1/2)(1/3) = 1$ ✓.

---

**Example 2: Find the marginal $f_X(x)$ for Example 1.**

$f_X(x) = \int_0^1 6xy^2\,dy = 6x(1/3) = 2x$.

---

**Example 3: $P(X > Y)$ for $f(x,y) = 2$ on $0<y<x<1$.**

$\int_0^1\int_0^x 2\,dy\,dx = \int_0^1 2x\,dx = 1$.

## Common Mistakes

- **Integrating over the wrong region when the joint PDF has a triangular or non-rectangular support.**
- **Forgetting to find the correct marginal limits.**

## Quick Check

1. $\int\int f(x,y)\,dx\,dy = ?$ for a valid PDF?
2. If $f(x,y) = f_X(x)f_Y(y)$, are $X$ and $Y$ independent?
3. $f_Y(y)$ for $f(x,y) = 6xy^2$ on $[0,1]^2$?

*(Answers: 1; yes; $3y^2$)*
