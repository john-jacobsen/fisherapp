# Continuous Random Variables

## Overview

A **continuous random variable** $X$ takes values on a continuum. Its distribution is specified by a **probability density function (PDF)** $f(x)$, where $P(a \le X \le b) = \int_a^b f(x)\,dx$.

## Key Idea

Properties of a valid PDF:
1. $f(x) \ge 0$ for all $x$
2. $\int_{-\infty}^{\infty} f(x)\,dx = 1$

$P(X = c) = 0$ for any single point — continuous RVs have zero probability at individual values.

## Worked Examples

**Example 1: $f(x) = 2x$ on $[0,1]$. Verify it is a PDF.**

$\int_0^1 2x\,dx = [x^2]_0^1 = 1$ ✓. $f(x) \ge 0$ on $[0,1]$ ✓.

---

**Example 2: $P(0.5 \le X \le 1)$ for $f(x) = 2x$**

$$\int_{0.5}^1 2x\,dx = [x^2]_{0.5}^1 = 1 - 0.25 = 0.75$$

---

**Example 3: CDF $F(x)$ for $f(x) = 2x$ on $[0,1]$**

$$F(x) = \int_0^x 2t\,dt = x^2 \quad (0 \le x \le 1)$$

## Common Mistakes

- **Thinking $f(x) = P(X=x)$.** For continuous RVs, $P(X=x)=0$. The PDF is a density, not a probability.
- **$f(x)$ can exceed 1** (it's a density, not a probability).

## Quick Check

1. $f(x) = 3x^2$ on $[0,1]$. Is it a valid PDF?
2. Find $P(X \le 0.5)$ for $f(x) = 2x$ on $[0,1]$.
3. What is $P(X = 0.7)$ for any continuous RV?

*(Answers: yes; 0.25; 0)*
