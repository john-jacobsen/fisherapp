# Double Integrals

## Overview

A **double integral** $\iint_R f(x,y)\,dA$ computes volume under a surface $z = f(x,y)$ over a region $R$, or the area/mass of a 2D region. You evaluate it as an iterated integral.

## Key Idea

For a rectangular region $[a,b] \times [c,d]$ (Fubini's theorem):

$$\iint_R f(x,y)\,dA = \int_a^b \int_c^d f(x,y)\,dy\,dx = \int_c^d \int_a^b f(x,y)\,dx\,dy$$

For non-rectangular regions, the inner limits depend on the outer variable.

## Worked Examples

**Example 1: $\int_0^1 \int_0^2 (x + y)\,dy\,dx$**

Inner integral: $\int_0^2 (x+y)\,dy = [xy + y^2/2]_0^2 = 2x + 2$.

Outer: $\int_0^1 (2x+2)\,dx = [x^2 + 2x]_0^1 = 3$.

---

**Example 2: $\iint_R x y\,dA$ where $R = [0,2]\times[0,3]$**

$\int_0^2 \int_0^3 xy\,dy\,dx = \int_0^2 x \cdot \frac{9}{2}\,dx = \frac{9}{2} \cdot 2 = 9$.

---

**Example 3: Region $0 \le x \le 1$, $0 \le y \le x$**

$\int_0^1 \int_0^x (x+y)\,dy\,dx = \int_0^1 \left[xy + y^2/2\right]_0^x dx = \int_0^1 \frac{3x^2}{2}\,dx = \frac{1}{2}$.

## Common Mistakes

- **Integrating the outer limits along the inner variable.** The inner integral is a function of the outer variable.
- **Wrong order for non-rectangular regions** — draw the region and set up limits carefully.

## Quick Check

1. $\int_0^1 \int_0^1 2xy\,dy\,dx$
2. $\int_0^2 \int_0^y x\,dx\,dy$
3. Area of $R = [0,3]\times[0,2]$ via double integral of 1.

*(Answers: 1; 4/3; 6)*
