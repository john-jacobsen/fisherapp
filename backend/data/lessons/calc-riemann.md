# Riemann Sums

## Overview

A **Riemann sum** approximates the area under a curve by dividing it into $n$ rectangles and summing their areas. As $n \to \infty$, the Riemann sum converges to the definite integral.

## Key Idea

Partition $[a, b]$ into $n$ equal subintervals of width $\Delta x = (b-a)/n$. Choose a sample point $x_i^*$ in each. The Riemann sum is:

$$S_n = \sum_{i=1}^{n} f(x_i^*)\,\Delta x$$

Right, left, and midpoint rules differ in the choice of $x_i^*$.

## Worked Examples

**Example 1: Left Riemann sum for $f(x) = x^2$ on $[0,2]$ with $n=4$**

$\Delta x = 0.5$. Left endpoints: $0, 0.5, 1, 1.5$. Sum: $0.5(0 + 0.25 + 1 + 2.25) = 1.75$.

---

**Example 2: Right Riemann sum, same setup**

Right endpoints: $0.5, 1, 1.5, 2$. Sum: $0.5(0.25 + 1 + 2.25 + 4) = 3.75$.

---

**Example 3: Midpoint rule, same setup**

Midpoints: $0.25, 0.75, 1.25, 1.75$. Sum: $0.5(0.0625 + 0.5625 + 1.5625 + 3.0625) = 2.625$.

The exact integral $\int_0^2 x^2\,dx = 8/3 \approx 2.667$.

## Common Mistakes

- **Confusing left, right, and midpoint sums** — each uses different sample points.
- **Wrong $\Delta x$.** It should be the total width divided by $n$.

## Quick Check

1. $\Delta x$ for $[1,5]$ with $n=4$?
2. Left endpoints for $[0,6]$ with $n=3$?
3. Right Riemann sum for $f(x)=1$ on $[0,4]$ with $n=4$?

*(Answers: 1; $0, 2, 4$; 4)*
