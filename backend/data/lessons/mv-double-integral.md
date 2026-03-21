# Double Integrals

## Overview

A **double integral** $\iint_R f(x,y)\,dA$ extends single-variable integration to functions of two variables. Geometrically, it computes the volume under the surface $z = f(x,y)$ above a region $R$ in the $xy$-plane. Computationally, you evaluate it as an **iterated integral** — integrate with respect to one variable while holding the other fixed, then integrate the result with respect to the other variable.

## Key Idea

For a rectangular region $R = [a,b] \times [c,d]$, **Fubini's theorem** guarantees you can integrate in either order:

$$\iint_R f(x,y)\,dA = \int_a^b\int_c^d f(x,y)\,dy\,dx = \int_c^d\int_a^b f(x,y)\,dx\,dy$$

For non-rectangular regions, the inner limits of integration become functions of the outer variable. The inner integral is always performed first and produces a function of the outer variable, which the outer integral then finishes.

## Worked Examples

**Example 1: $\int_0^1\int_0^2(x + y)\,dy\,dx$**

Work from the inside out. Integrate the inner integral with respect to $y$, treating $x$ as a constant.

$$\int_0^2(x + y)\,dy = \left[xy + \frac{y^2}{2}\right]_0^2 = \left(2x + 2\right) - 0 = 2x + 2$$

Now integrate the result with respect to $x$:

$$\int_0^1(2x + 2)\,dx = \left[x^2 + 2x\right]_0^1 = (1 + 2) - 0 = 3$$

---

**Example 2: $\iint_R xy\,dA$ where $R = [0,2] \times [0,3]$**

On a rectangular region, $x$ and $y$ integrate independently. Factor the integrand: $\iint xy\,dA = \left(\int_0^2 x\,dx\right)\!\left(\int_0^3 y\,dy\right)$.

$$\int_0^2 x\,dx = \left[\frac{x^2}{2}\right]_0^2 = 2 \qquad \int_0^3 y\,dy = \left[\frac{y^2}{2}\right]_0^3 = \frac{9}{2}$$

$$\iint_R xy\,dA = 2 \cdot \frac{9}{2} = 9$$

---

**Example 3: Region bounded by $0 \le x \le 1$, $0 \le y \le x$**

This is a triangular region — the upper limit on $y$ depends on $x$. Set up with $y$ on the inside (varying up to $x$) and $x$ on the outside.

$$\int_0^1\int_0^x(x + y)\,dy\,dx$$

Inner integral (with respect to $y$, treating $x$ as constant):

$$\int_0^x(x + y)\,dy = \left[xy + \frac{y^2}{2}\right]_0^x = x^2 + \frac{x^2}{2} = \frac{3x^2}{2}$$

Outer integral:

$$\int_0^1 \frac{3x^2}{2}\,dx = \left[\frac{x^3}{2}\right]_0^1 = \frac{1}{2}$$

## Common Mistakes

- **Treating the inner limits as constants when they depend on the outer variable.** For the region $0 \le y \le x$, the inner limit on $y$ is $x$ — it's a function of the outer variable, not a number. Treating it as a fixed number changes the region of integration.
- **Applying the outer integral before finishing the inner one.** The inner integral must be fully evaluated (as a function of the outer variable) before the outer integral begins. Do not mix the two.
- **Confusing which variable is inner vs. outer.** In $\int dx\int dy$, $dy$ is inner and its limits can depend on $x$. In $\int dy\int dx$, the roles reverse. Always draw the region and check which setup gives variable limits on the inner integral.

## Quick Check

1. $\int_0^1\int_0^1 2xy\,dy\,dx$
2. $\int_0^2\int_0^y x\,dx\,dy$
3. Area of $R = [0,3] \times [0,2]$ via $\iint_R 1\,dA$.

*(Answers: 1; $\dfrac{4}{3}$; 6)*
