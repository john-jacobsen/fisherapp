# Conditional Distributions

## Overview

The **conditional distribution** of $Y$ given $X = x$ describes how $Y$ behaves when you know $X$. It is computed by dividing the joint by the marginal.

## Key Idea

$$f_{Y|X}(y|x) = \frac{f(x,y)}{f_X(x)}, \quad f_X(x) > 0$$

The conditional expectation $E[Y|X=x] = \int y\, f_{Y|X}(y|x)\,dy$ is a function of $x$.

## Worked Examples

**Example 1: $f(x,y) = 6xy^2$ on $[0,1]^2$. Find $f_{Y|X}(y|x)$.**

$f_X(x) = 2x$. $f_{Y|X}(y|x) = \frac{6xy^2}{2x} = 3y^2$ — uniform in $y$ regardless of $x$.

---

**Example 2: $E[Y|X=x]$ for Example 1**

$E[Y|X=x] = \int_0^1 y \cdot 3y^2\,dy = 3/4$.

---

**Example 3: Discrete case**

$P(Y=1|X=0) = p(0,1)/p_X(0) = 0.1/0.3 = 1/3$.

## Common Mistakes

- **Forgetting to normalize** by the marginal.
- **Treating conditional distribution as the same as the marginal** when variables are not independent.

## Quick Check

1. $f_{Y|X}(y|x)$ vs. $f_Y(y)$: when are they equal?
2. $P(Y=0|X=1)$ from Example 1 table in marginal lesson?
3. $E[Y|X=x]$ is a function of what?

*(Answers: when $X \perp Y$; $0.3/0.7\approx0.43$; $x$)*
