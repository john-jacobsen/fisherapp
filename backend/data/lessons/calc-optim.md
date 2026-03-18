# Optimization

## Overview

**Optimization** uses calculus to find the maximum or minimum value of a function on a domain. You find critical points (where $f'(x) = 0$ or is undefined) and test them using the first or second derivative test.

## Key Idea

Critical points occur where $f'(x) = 0$ or $f'(x)$ is undefined. On a closed interval $[a,b]$, also check the endpoints. Use the second derivative to classify: $f''(c) > 0$ → local min; $f''(c) < 0$ → local max.

## Worked Examples

**Example 1: Find the maximum of $f(x) = -x^2 + 4x$ on $[0, 4]$**

$f'(x) = -2x + 4 = 0 \Rightarrow x = 2$. $f(0)=0$, $f(2)=4$, $f(4)=0$. Maximum = 4 at $x=2$.

---

**Example 2: A box with square base and open top has volume 32. Minimize surface area.**

Let side $= s$, height $= h$. Volume: $s^2 h = 32$, so $h = 32/s^2$. Surface: $S = s^2 + 4sh = s^2 + 128/s$. $S' = 2s - 128/s^2 = 0 \Rightarrow s = 4$, $h = 2$.

---

**Example 3: Find local extrema of $f(x) = x^3 - 3x$**

$f'(x) = 3x^2 - 3 = 0 \Rightarrow x = \pm 1$. $f''(1) = 6 > 0$ (min), $f''(-1) = -6 < 0$ (max).

## Common Mistakes

- **Forgetting to check endpoints** on closed intervals.
- **Assuming a critical point is always an extremum.** Inflection points are also critical points.

## Quick Check

1. Critical points of $f(x) = x^3 - 6x^2$?
2. Classify $f'(x) = 0$ at $x=2$ if $f''(2) = 5$.
3. Max of $f(x) = 4x - x^2$?

*(Answers: $x=0, 4$; local min; 4 at $x=2$)*
