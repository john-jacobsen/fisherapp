# Antiderivatives

## Overview

An **antiderivative** of $f(x)$ is any function $F(x)$ with $F'(x) = f(x)$. The general antiderivative includes an arbitrary constant $C$ because derivatives of constants vanish.

## Key Idea

$$\int f(x)\,dx = F(x) + C \quad\text{where}\quad F'(x) = f(x)$$

Power rule for integration:

$$\int x^n\,dx = \frac{x^{n+1}}{n+1} + C \quad (n \ne -1)$$

## Worked Examples

**Example 1: $\int x^3\,dx$**

$$\frac{x^4}{4} + C$$

---

**Example 2: $\int (3x^2 - 2x + 5)\,dx$**

$$x^3 - x^2 + 5x + C$$

---

**Example 3: $\int \sqrt{x}\,dx$**

Rewrite: $\int x^{1/2}\,dx = \frac{x^{3/2}}{3/2} + C = \frac{2}{3}x^{3/2} + C$.

## Common Mistakes

- **Forgetting $+C$.** The constant is essential; without it you have only one function, not the family.
- **Using the power rule for $n = -1$.** $\int x^{-1}\,dx = \ln|x| + C$, not $x^0/0$.

## Quick Check

1. $\int 4x^3\,dx$
2. $\int (2x + 3)\,dx$
3. $\int x^{-2}\,dx$

*(Answers: $x^4+C$; $x^2+3x+C$; $-x^{-1}+C$)*
