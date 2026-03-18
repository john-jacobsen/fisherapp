# Joint Discrete Distributions

## Overview

The **joint distribution** of two discrete random variables $X$ and $Y$ specifies $P(X=x, Y=y)$ for all $(x,y)$ pairs. From it, you can recover marginal distributions, check independence, and compute joint expectations.

## Key Idea

Joint PMF: $p(x,y) = P(X=x, Y=y)$.

Marginals: $p_X(x) = \sum_y p(x,y)$ and $p_Y(y) = \sum_x p(x,y)$.

Independence: $X \perp Y$ iff $p(x,y) = p_X(x)\,p_Y(y)$ for all $(x,y)$.

## Worked Examples

**Example 1: Roll two dice. Joint PMF of $(X,Y)$.**

$P(X=i, Y=j) = 1/36$ for $i,j \in \{1,\ldots,6\}$. Independent and uniform.

---

**Example 2: Marginal of $X$ from the table below**

| $p(x,y)$ | $y=0$ | $y=1$ |
|---|---|---|
| $x=0$ | 0.1 | 0.2 |
| $x=1$ | 0.3 | 0.4 |

$p_X(0) = 0.3$, $p_X(1) = 0.7$.

---

**Example 3: Check independence**

$p_X(0)\,p_Y(0) = 0.3 \times 0.4 = 0.12 \ne 0.1 = p(0,0)$. Not independent.

## Common Mistakes

- **Confusing joint PMF with conditional PMF.** $p(x|y) = p(x,y)/p_Y(y)$.
- **Forgetting to verify $\sum_{x,y} p(x,y) = 1$.**

## Quick Check

1. How do you get $p_Y(y)$ from the joint PMF?
2. If $X \perp Y$, how does the joint PMF factor?
3. Can $p(x,y) > p_X(x)$?

*(Answers: sum over all $x$; $p_X(x)p_Y(y)$; no)*
