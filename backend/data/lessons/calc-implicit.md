# Implicit Differentiation

## Overview

When a curve is defined by an equation involving both $x$ and $y$ (like $x^2 + y^2 = 25$), you can still find $dy/dx$ by differentiating both sides with respect to $x$ and treating $y$ as a function of $x$.

## Key Idea

Differentiate every term with respect to $x$. Whenever you differentiate a term containing $y$, multiply by $dy/dx$ (chain rule). Then isolate $dy/dx$.

## Worked Examples

**Example 1: Find $dy/dx$ for $x^2 + y^2 = 25$**

Differentiate: $2x + 2y\,\frac{dy}{dx} = 0$. Solve: $\frac{dy}{dx} = -\frac{x}{y}$.

---

**Example 2: Find $dy/dx$ for $x^3 + y^3 = 6xy$**

$3x^2 + 3y^2\,y' = 6y + 6x\,y'$. Isolate: $y'(3y^2 - 6x) = 6y - 3x^2 \Rightarrow y' = \frac{6y - 3x^2}{3y^2 - 6x}$.

---

**Example 3: Tangent line to $x^2 + y^2 = 25$ at $(3,4)$**

$dy/dx = -3/4$. Line: $y - 4 = -\frac{3}{4}(x - 3)$.

## Common Mistakes

- **Forgetting $dy/dx$ when differentiating $y$ terms.** Every $y$ term needs the chain rule.
- **Not simplifying before solving for $dy/dx$.**

## Quick Check

1. Find $dy/dx$ for $x^2 + 2y = 10$.
2. Find $dy/dx$ for $xy = 5$.
3. Find the slope of $x^2 + y^2 = 100$ at $(6, 8)$.

*(Answers: $-x$; $-y/x$; $-3/4$)*
