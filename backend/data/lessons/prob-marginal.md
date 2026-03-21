# Marginal Distributions

## Overview

A **marginal distribution** is what you get when you "integrate out" (or sum out) one variable from a joint distribution — it describes one variable alone, without reference to the other. The name comes from the practice of writing totals in the margins of a joint probability table: the row and column totals are the marginals. Marginals let you study each variable individually even when you started with a model for both together.

## Key Idea

Given a joint distribution, marginals are obtained by:

$$\text{Discrete:} \quad p_X(x) = \sum_y p(x, y), \qquad p_Y(y) = \sum_x p(x, y)$$

$$\text{Continuous:} \quad f_X(x) = \int_{-\infty}^{\infty} f(x, y)\,dy, \qquad f_Y(y) = \int_{-\infty}^{\infty} f(x, y)\,dx$$

Summing or integrating over all values of $y$ uses the law of total probability: it adds up the probability of $\{X = x\}$ across every possible value $Y$ can take.

## Worked Examples

**Example 1: Find both marginals from a $3 \times 3$ joint PMF table.**

| $p(x,y)$ | $Y=1$ | $Y=2$ | $Y=3$ |
|---|---|---|---|
| $X=1$ | 0.05 | 0.10 | 0.05 |
| $X=2$ | 0.10 | 0.30 | 0.10 |
| $X=3$ | 0.05 | 0.15 | 0.10 |

To find $p_X$, sum each row — you add up the joint probabilities across all values of $Y$, leaving only the marginal behavior of $X$.

$$p_X(1) = 0.05+0.10+0.05 = 0.20, \quad p_X(2) = 0.50, \quad p_X(3) = 0.30$$

To find $p_Y$, sum each column — adding down each column collapses $X$ and leaves the distribution of $Y$ alone.

$$p_Y(1) = 0.20, \quad p_Y(2) = 0.55, \quad p_Y(3) = 0.25$$

Both marginals sum to 1 — a useful check.

---

**Example 2: Find the marginal PDF $f_X(x)$ from a joint PDF on a rectangle.**

Let $f(x, y) = 6x^2 y$ on $0 \leq x \leq 1$, $0 \leq y \leq 1$ (verify it integrates to 1: $\int_0^1\int_0^1 6x^2y\,dy\,dx = 6 \cdot \frac{1}{3} \cdot \frac{1}{2} = 1$ ✓). To find $f_X(x)$, integrate out $y$ over its full range $[0, 1]$. Because the support is a rectangle, the $y$-limits do not depend on $x$, making this straightforward.

$$f_X(x) = \int_0^1 6x^2 y\,dy = 6x^2 \left[\frac{y^2}{2}\right]_0^1 = 3x^2, \quad 0 \leq x \leq 1$$

Check: $\int_0^1 3x^2\,dx = 1$ ✓. The $y$ variable has been integrated away entirely; $f_X$ depends only on $x$.

---

**Example 3: Find $f_Y(y)$ from a joint PDF on a triangular region.**

Let $f(x, y) = 2$ on $\{0 < y < x < 1\}$. To find $f_Y(y)$, fix $y$ and integrate over all $x$ compatible with that $y$. On the triangle, for a fixed $y \in (0, 1)$, $x$ must satisfy $y < x < 1$ — because the region requires $y < x$. The lower limit is $y$ (not 0), which is where triangular supports differ from rectangular ones.

$$f_Y(y) = \int_y^1 2\,dx = 2(1 - y), \quad 0 < y < 1$$

The lower integration limit $y$ (rather than 0) is the key step that trips people up. Sketch the triangle: for a horizontal slice at height $y$, $x$ ranges from the diagonal boundary $x = y$ on the left to $x = 1$ on the right. Verify: $\int_0^1 2(1-y)\,dy = 2 \cdot \frac{1}{2} = 1$ ✓.

## Common Mistakes

- **Using constant limits when the support is not rectangular.** For a triangular region, the limits of integration for the inner variable depend on the outer variable. Always draw the support region and read off limits from the geometry.
- **Confusing marginal with conditional.** The marginal $f_X(x)$ gives the distribution of $X$ alone, averaging over all values of $Y$. The conditional $f_{X|Y}(x|y) = f(x,y)/f_Y(y)$ gives the distribution of $X$ given that $Y = y$. They are different objects.

## Quick Check

1. From the table in Example 1, what is $p_X(2)$?
2. $f(x, y) = 2e^{-(x+2y)}$ on $x, y > 0$. Find $f_X(x)$.
3. For $f(x, y) = 2$ on $\{0 < y < x < 1\}$, set up (but do not evaluate) the integral for $f_X(x)$.

*(Answers: 0.50; $f_X(x) = \int_0^\infty 2e^{-(x+2y)}\,dy = e^{-x}$, so $X \sim \text{Exp}(1)$; $f_X(x) = \int_0^x 2\,dy = 2x$)*
