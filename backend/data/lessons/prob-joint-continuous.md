# Joint Distributions (Continuous)

## Overview

The **joint PDF** $f(x, y)$ of two continuous random variables must integrate to 1 over the entire plane, and joint probabilities are computed as double integrals over a region. The key skill is setting up integration limits correctly — especially when the support is not a rectangle, which requires careful attention to which variable's bounds depend on the other.

## Key Idea

For a valid joint PDF:

$$f(x, y) \geq 0 \quad \text{and} \quad \iint_{\mathbb{R}^2} f(x, y)\,dx\,dy = 1$$

Joint probability over a region $R$:

$$P\!\left((X, Y) \in R\right) = \iint_R f(x, y)\,dx\,dy$$

Marginals:

$$f_X(x) = \int_{-\infty}^{\infty} f(x, y)\,dy, \qquad f_Y(y) = \int_{-\infty}^{\infty} f(x, y)\,dx$$

## Worked Examples

**Example 1: Verify that $f(x, y) = c$ on the triangle $0 < x < 1$, $0 < y < x$ is a valid PDF, and find $c$.**

The triangle has $x$ ranging from 0 to 1, and for each fixed $x$, $y$ ranges from 0 to $x$. The order of integration reflects the geometry: integrate over $y$ first (inner integral, with limits that depend on $x$), then over $x$ (outer integral). Setting the total integral to 1 determines $c$.

$$\int_0^1 \int_0^x c\,dy\,dx = c \int_0^1 x\,dx = c \cdot \frac{1}{2} = 1 \implies c = 2$$

So $f(x, y) = 2$ on $\{0 < y < x < 1\}$. The area of the triangle is $1/2$, so $c = 1/\text{area} = 2$ — a useful check for uniform distributions over geometric regions.

---

**Example 2: Compute $P(X + Y < 1)$ for $f(x,y) = 1$ on the unit square $[0,1]^2$.**

This is a uniform distribution over the unit square. The event $\{X + Y < 1\}$ is the region below the diagonal line $y = 1 - x$ within the square. Geometrically this is the lower-left triangle. Set up the double integral: $x$ goes from 0 to 1, and for each $x$, $y$ goes from 0 to $\min(1-x, 1) = 1-x$ (since $1-x \leq 1$ for $x \geq 0$).

$$P(X + Y < 1) = \int_0^1 \int_0^{1-x} 1\,dy\,dx = \int_0^1 (1-x)\,dx = \left[x - \frac{x^2}{2}\right]_0^1 = \frac{1}{2}$$

The answer makes intuitive sense — the triangle $\{x + y < 1\}$ occupies exactly half the area of the unit square, and the uniform distribution assigns probability proportional to area.

---

**Example 3: Find the marginal PDF $f_X(x)$ from $f(x, y) = 2$ on $\{0 < y < x < 1\}$.**

To find the marginal of $X$, integrate out $y$. For a fixed value $x \in (0, 1)$, $y$ ranges from 0 to $x$ (the limits come from the triangular support — $y$ is bounded below by 0 and above by $x$). Integrating a constant 2 over this interval gives:

$$f_X(x) = \int_0^x 2\,dy = 2x, \quad 0 < x < 1$$

This is the marginal PDF of $X$ alone — it is a linear function that increases from 0 to 2, reflecting that larger values of $x$ correspond to a wider range of allowable $y$ values in the triangle. Verify: $\int_0^1 2x\,dx = 1$ ✓.

## Common Mistakes

- **Setting constant limits when the support is triangular.** If the support is $\{0 < y < x < 1\}$, the inner limit for $y$ is not 1 — it is $x$. Drawing the region and reading off the bounds from the picture is the most reliable approach.
- **Confusing the order of integration.** When you integrate $f_X(x) = \int f(x,y)\,dy$, you are fixing $x$ and varying $y$. The integration variable in the marginal formula must match the variable you are eliminating.

## Quick Check

1. Is $f(x,y) = 4xy$ on $[0,1]^2$ a valid joint PDF?
2. For $f(x,y) = 4xy$ on $[0,1]^2$, find the marginal PDF $f_X(x)$.
3. For $f(x,y) = 2$ on $\{0 < y < x < 1\}$, compute $P(X < 0.5)$.

*(Answers: yes, $\int_0^1\int_0^1 4xy\,dx\,dy = 4 \cdot \frac{1}{2} \cdot \frac{1}{2} = 1$; $f_X(x) = \int_0^1 4xy\,dy = 2x$; $\int_0^{0.5}\int_0^x 2\,dy\,dx = \int_0^{0.5} 2x\,dx = 0.25$)*
