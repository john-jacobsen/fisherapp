# Riemann Sums

## Overview

A **Riemann sum** approximates the area under a curve $y = f(x)$ over $[a, b]$ by dividing the region into $n$ thin rectangles and summing their areas. Each rectangle has width $\Delta x$ and height determined by the function value at a chosen sample point. As you use more and narrower rectangles ($n \to \infty$), the approximation converges to the exact area — the definite integral. This is the geometric foundation of integration.

## Key Idea

Partition $[a, b]$ into $n$ equal subintervals of width:

$$\Delta x = \frac{b - a}{n}$$

Choose a sample point $x_i^*$ in each subinterval $[x_{i-1}, x_i]$. The Riemann sum is:

$$S_n = \sum_{i=1}^{n} f(x_i^*)\,\Delta x$$

The three standard choices of sample point: **left endpoints** ($x_i^* = x_{i-1}$), **right endpoints** ($x_i^* = x_i$), **midpoints** ($x_i^* = \frac{x_{i-1}+x_i}{2}$).

## Worked Examples

**Example 1: Left Riemann sum for $f(x) = x^2$ on $[0, 2]$, $n = 4$**

Compute $\Delta x = \frac{2-0}{4} = 0.5$. The four subintervals are $[0, 0.5]$, $[0.5, 1]$, $[1, 1.5]$, $[1.5, 2]$.

Left endpoints are the left edges of each rectangle: $x = 0, 0.5, 1, 1.5$.

Evaluate $f$ at each left endpoint and sum:

$$S_4 = 0.5\left[f(0) + f(0.5) + f(1) + f(1.5)\right] = 0.5\left[0 + 0.25 + 1 + 2.25\right] = 0.5 \cdot 3.5 = 1.75$$

The left sum underestimates here because $f$ is increasing — the left endpoint of each rectangle is below the curve.

---

**Example 2: Right Riemann sum, same setup**

Right endpoints are the right edges: $x = 0.5, 1, 1.5, 2$.

$$S_4 = 0.5\left[f(0.5) + f(1) + f(1.5) + f(2)\right] = 0.5\left[0.25 + 1 + 2.25 + 4\right] = 0.5 \cdot 7.5 = 3.75$$

The right sum overestimates for the same reason — each rectangle's height is the function value at the upper end of the interval.

---

**Example 3: Midpoint rule, same setup**

Midpoints of the four intervals: $x = 0.25, 0.75, 1.25, 1.75$.

$$S_4 = 0.5\left[(0.25)^2 + (0.75)^2 + (1.25)^2 + (1.75)^2\right] = 0.5\left[0.0625 + 0.5625 + 1.5625 + 3.0625\right] = 2.625$$

The exact integral $\int_0^2 x^2\,dx = \frac{8}{3} \approx 2.667$. The midpoint rule is the closest of the three — it tends to be the most accurate Riemann sum for smooth functions.

## Common Mistakes

- **Using the wrong sample points.** Left sums use $x_{i-1}$ (the left edge), right sums use $x_i$ (the right edge), and midpoint sums use the center. Mixing them up produces values corresponding to a different rule.
- **Computing $\Delta x$ as $n/(b-a)$ instead of $(b-a)/n$.** The width is the total interval length divided by the number of subintervals, not the other way around.
- **Forgetting to multiply each function value by $\Delta x$.** Each term in the sum is an area (height times width). Writing $\sum f(x_i^*)$ without the $\Delta x$ gives a sum of heights, not areas.

## Quick Check

1. $\Delta x$ for $[1, 5]$ with $n = 4$?
2. List the left endpoints for $[0, 6]$ with $n = 3$.
3. Right Riemann sum for $f(x) = 1$ on $[0, 4]$ with $n = 4$?

*(Answers: 1; $x = 0, 2, 4$; 4)*
