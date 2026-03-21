# Partial Derivatives

## Overview

A **partial derivative** measures how a multivariable function changes with respect to one input variable while all other inputs are held fixed. For a function $f(x, y)$, the partial derivative $f_x$ (or $\partial f/\partial x$) treats $y$ as a constant and differentiates with respect to $x$ using the usual single-variable rules. This extends differentiation to functions of several variables and is the foundation of multivariable calculus.

## Key Idea

$$f_x(x, y) = \frac{\partial f}{\partial x} = \lim_{h \to 0}\frac{f(x+h,\, y) - f(x,\, y)}{h}$$

In practice: to compute $\partial f/\partial x$, treat every variable other than $x$ as a constant and differentiate with respect to $x$ normally. Second-order mixed partials satisfy **Clairaut's theorem**: for smooth functions, $f_{xy} = f_{yx}$.

## Worked Examples

**Example 1: $f(x,y) = x^3 y + 2xy^2$. Find $f_x$ and $f_y$.**

For $f_x$: treat $y$ as a constant. The term $x^3 y$ differentiates as $y \cdot 3x^2 = 3x^2 y$ (the $y$ is just a multiplying constant). The term $2xy^2$ differentiates as $2y^2$ (since $y^2$ is constant).

$$f_x = 3x^2 y + 2y^2$$

For $f_y$: treat $x$ as a constant. The term $x^3 y$ differentiates as $x^3$ (since $x^3$ is a constant multiplying $y$). The term $2xy^2$ differentiates as $2x \cdot 2y = 4xy$.

$$f_y = x^3 + 4xy$$

---

**Example 2: $g(x,y) = e^{xy}$. Find $g_x$.**

Treat $y$ as a constant — so $xy$ is a linear function of $x$ with constant coefficient $y$. Apply the chain rule: derivative of $e^{(\cdot)}$ is $e^{(\cdot)}$, times the derivative of the exponent with respect to $x$.

$$g_x = e^{xy} \cdot \frac{\partial}{\partial x}(xy) = e^{xy} \cdot y = y e^{xy}$$

The $y$ factor out front is the chain rule correction from differentiating the exponent $xy$ with respect to $x$.

---

**Example 3: Find all second-order partial derivatives of $f(x,y) = x^2 y^3$.**

Compute the first-order partials:

$f_x = 2xy^3$ (treat $y^3$ as a constant coefficient).
$f_y = 3x^2 y^2$ (treat $x^2$ as a constant coefficient).

Differentiate again for second-order:

$f_{xx} = \frac{\partial}{\partial x}[2xy^3] = 2y^3$ (treat $y^3$ as constant).

$f_{yy} = \frac{\partial}{\partial y}[3x^2 y^2] = 6x^2 y$.

$f_{xy} = \frac{\partial}{\partial y}[2xy^3] = 6xy^2$.

$f_{yx} = \frac{\partial}{\partial x}[3x^2 y^2] = 6xy^2$.

As Clairaut's theorem predicts, $f_{xy} = f_{yx} = 6xy^2$.

## Common Mistakes

- **Differentiating the "held-constant" variable.** When computing $f_x$, $y$ is a constant — it does not get differentiated. $\frac{\partial}{\partial x}[xy^2] = y^2$, not $2y$ or $2xy$.
- **Forgetting the chain rule for composite expressions.** $\frac{\partial}{\partial x}[e^{xy}] = y e^{xy}$, not $e^{xy}$ alone. The chain rule still applies — the multiplying factor is the partial derivative of the exponent.
- **Assuming $f_{xy} \ne f_{yx}$ by default.** For smooth functions (which is essentially everything in this course), the mixed partials are equal. You can compute whichever order is more convenient.

## Quick Check

1. $f_x$ for $f(x,y) = 3x^2 + xy - y^3$?
2. $f_y$ for $f(x,y) = \sin(xy)$?
3. $f_{xx}$ for $f(x,y) = x^3 + y^3$?

*(Answers: $6x + y$; $x\cos(xy)$; $6x$)*
