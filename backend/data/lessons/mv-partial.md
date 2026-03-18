# Partial Derivatives

## Overview

A **partial derivative** measures how a function of several variables changes with respect to one variable, while holding all others constant. They are written $\partial f/\partial x$ or $f_x$.

## Key Idea

$$f_x(x, y) = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}$$

To compute $\partial f/\partial x$: differentiate with respect to $x$, treating $y$ as a constant.

## Worked Examples

**Example 1: $f(x,y) = x^3 y + 2xy^2$. Find $f_x$ and $f_y$.**

$f_x = 3x^2 y + 2y^2$; $f_y = x^3 + 4xy$.

---

**Example 2: $g(x,y) = e^{xy}$. Find $g_x$.**

Treat $y$ as constant: $g_x = y e^{xy}$.

---

**Example 3: Find all second-order partial derivatives of $f(x,y) = x^2 y^3$.**

$f_x = 2xy^3$, $f_{xx} = 2y^3$. $f_y = 3x^2y^2$, $f_{yy} = 6x^2 y$. $f_{xy} = 6xy^2 = f_{yx}$.

## Common Mistakes

- **Differentiating the "constant" variable.** When computing $f_x$, treat $y$ as a number.
- **Mixing up $f_{xy}$ and $f_{yx}$.** By Clairaut's theorem, they're equal for smooth functions.

## Quick Check

1. $f_x$ for $f = 3x^2 + xy - y^3$?
2. $f_y$ for $f = \sin(xy)$?
3. $f_{xx}$ for $f = x^3 + y^3$?

*(Answers: $6x+y$; $x\cos(xy)$; $6x$)*
