# Optimization

## Overview

**Optimization** uses the derivative to find where a function reaches its maximum or minimum value. The key insight is that at a smooth peak or valley, the function is momentarily flat — the slope is zero. Those points are candidates for extrema. You find them by solving $f'(x) = 0$, then test to determine whether each candidate is a max, a min, or neither.

## Key Idea

A **critical point** of $f$ occurs where $f'(x) = 0$ or $f'(x)$ is undefined.

On a **closed interval $[a, b]$**: the global maximum and minimum must occur either at a critical point in $(a, b)$ or at an endpoint. Evaluate $f$ at all of these and compare.

**Second derivative test:** At a critical point $c$ where $f'(c) = 0$:
- $f''(c) > 0 \Rightarrow$ local minimum (concave up, like a bowl)
- $f''(c) < 0 \Rightarrow$ local maximum (concave down, like a hill)
- $f''(c) = 0 \Rightarrow$ inconclusive

$$f'(c) = 0 \text{ and } f''(c) > 0 \implies \text{local min at } c$$

## Worked Examples

**Example 1: Find the maximum of $f(x) = -x^2 + 4x$ on $[0, 4]$**

Find critical points: $f'(x) = -2x + 4 = 0 \Rightarrow x = 2$. This is inside the interval.

On a closed interval, also check the endpoints. Evaluate $f$ at all candidates:

- $f(0) = 0$
- $f(2) = -(4) + 8 = 4$
- $f(4) = -(16) + 16 = 0$

The global maximum is $4$ at $x = 2$, and the global minimum is $0$ at both endpoints.

---

**Example 2: Find local extrema of $f(x) = x^3 - 3x$**

Find critical points: $f'(x) = 3x^2 - 3 = 0 \Rightarrow x^2 = 1 \Rightarrow x = \pm 1$.

Apply the second derivative test: $f''(x) = 6x$.

- At $x = 1$: $f''(1) = 6 > 0$ → local minimum. $f(1) = 1 - 3 = -2$.
- At $x = -1$: $f''(-1) = -6 < 0$ → local maximum. $f(-1) = -1 + 3 = 2$.

The function rises to a local max of 2, dips to a local min of $-2$, then rises again — typical cubic behavior.

---

**Example 3: Minimize surface area of an open-top box with volume 32**

Let the square base have side $s$ and height $h$. The volume constraint gives $s^2 h = 32$, so $h = 32/s^2$.

Express surface area in terms of $s$ alone (substitute the constraint to eliminate $h$):

$$S = s^2 + 4sh = s^2 + 4s \cdot \frac{32}{s^2} = s^2 + \frac{128}{s}$$

Differentiate and set equal to zero:

$$S'(s) = 2s - \frac{128}{s^2} = 0 \implies 2s^3 = 128 \implies s = 4$$

Then $h = 32/16 = 2$. Verify with $S'' = 2 + 256/s^3 > 0$ (minimum confirmed).

## Common Mistakes

- **Forgetting to check endpoints on a closed interval.** On $[a,b]$, the global extremum can occur at the boundary even if $f' \ne 0$ there. Always evaluate $f$ at endpoints alongside critical points.
- **Assuming every critical point is an extremum.** Inflection points also satisfy $f'(c) = 0$. Use the second derivative test (or first derivative sign chart) to classify each critical point.
- **Forgetting to substitute the constraint before differentiating.** In applied optimization, express the objective function in terms of a single variable before differentiating. Trying to differentiate a two-variable expression directly doesn't work.

## Quick Check

1. Critical points of $f(x) = x^3 - 6x^2$?
2. Classify the critical point at $x = 2$ if $f''(2) = 5$.
3. Global max of $f(x) = 4x - x^2$ on $[0, 3]$?

*(Answers: $x = 0, 4$; local minimum; $f(2) = 4$)*
