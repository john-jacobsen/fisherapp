# Implicit Differentiation

## Overview

Most curves you've seen are defined by $y = f(x)$ — output $y$ expressed explicitly in terms of $x$. But many important curves, like circles and ellipses, are defined by equations such as $x^2 + y^2 = 25$ where you can't easily solve for $y$. **Implicit differentiation** lets you find $dy/dx$ directly from the equation without isolating $y$ first, by treating $y$ as an unknown function of $x$ and applying the chain rule to every $y$ term.

## Key Idea

Differentiate both sides of the equation with respect to $x$. Whenever you differentiate a term containing $y$, apply the chain rule: treat $y$ as a function of $x$ and multiply by $\dfrac{dy}{dx}$.

$$\frac{d}{dx}[y^n] = n y^{n-1} \cdot \frac{dy}{dx}$$

After differentiating, collect all $dy/dx$ terms on one side and solve algebraically.

## Worked Examples

**Example 1: Find $dy/dx$ for $x^2 + y^2 = 25$**

This is a circle of radius 5. Differentiate both sides with respect to $x$. The left side has two terms; the right side (constant) has derivative 0.

$$\frac{d}{dx}[x^2] + \frac{d}{dx}[y^2] = 0$$

Differentiate $x^2$ normally to get $2x$. Differentiate $y^2$ using the chain rule — the outer derivative gives $2y$, and the inner derivative (treating $y$ as a function of $x$) gives $\frac{dy}{dx}$.

$$2x + 2y\,\frac{dy}{dx} = 0$$

Solve for $\frac{dy}{dx}$: subtract $2x$, then divide by $2y$:

$$\frac{dy}{dx} = -\frac{x}{y}$$

The slope depends on both $x$ and $y$ — this is expected for a curve where multiple $y$ values correspond to one $x$.

---

**Example 2: Find $dy/dx$ for $x^3 + y^3 = 6xy$**

Differentiate every term. For $x^3$: get $3x^2$. For $y^3$: chain rule gives $3y^2 \frac{dy}{dx}$. For the right side, $6xy$ is a product of $x$ and $y$, so use the product rule — differentiate $x$ to get $6y$, then differentiate $y$ to get $6x \frac{dy}{dx}$.

$$3x^2 + 3y^2\,\frac{dy}{dx} = 6y + 6x\,\frac{dy}{dx}$$

Collect all $\frac{dy}{dx}$ terms on the left:

$$3y^2\,\frac{dy}{dx} - 6x\,\frac{dy}{dx} = 6y - 3x^2$$

Factor out $\frac{dy}{dx}$ and divide:

$$\frac{dy}{dx} = \frac{6y - 3x^2}{3y^2 - 6x} = \frac{2y - x^2}{y^2 - 2x}$$

---

**Example 3: Tangent line to $x^2 + y^2 = 25$ at $(3, 4)$**

From Example 1, $\frac{dy}{dx} = -\frac{x}{y}$. Substitute the point $(3, 4)$:

$$\frac{dy}{dx}\bigg|_{(3,4)} = -\frac{3}{4}$$

Use point-slope form: $y - 4 = -\frac{3}{4}(x - 3)$.

## Common Mistakes

- **Forgetting to attach $dy/dx$ when differentiating any $y$ term.** Every $y$ is a function of $x$, so every $y$ derivative gets a chain rule factor. $\frac{d}{dx}[y^3] = 3y^2 \cdot \frac{dy}{dx}$, not just $3y^2$.
- **Applying the product rule to mixed $xy$ terms but dropping one part.** $\frac{d}{dx}[xy] = y + x\,\frac{dy}{dx}$ — both the term where $x$ is differentiated and the term where $y$ is differentiated must appear.
- **Trying to solve for $\frac{dy}{dx}$ before collecting all terms.** First, differentiate everything; second, move all $\frac{dy}{dx}$ terms to one side; third, factor and divide.

## Quick Check

1. Find $dy/dx$ for $x^2 + 2y = 10$.
2. Find $dy/dx$ for $xy = 5$.
3. Find the slope of $x^2 + y^2 = 100$ at $(6, 8)$.

*(Answers: $-x$; $-y/x$; $-3/4$)*
