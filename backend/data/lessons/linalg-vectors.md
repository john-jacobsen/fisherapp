# Vectors: Dot Product and Magnitude

## Overview

A **vector** in $\mathbb{R}^n$ is an ordered list of $n$ real numbers that encodes both direction and magnitude. Two essential operations on vectors are the **dot product** (which measures alignment between vectors) and the **magnitude** (which measures length). These tools appear throughout linear algebra, physics, and machine learning.

## Key Idea

For vectors $\mathbf{u} = (u_1, \ldots, u_n)$ and $\mathbf{v} = (v_1, \ldots, v_n)$:

$$\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^n u_i v_i, \qquad \|\mathbf{u}\| = \sqrt{\mathbf{u} \cdot \mathbf{u}} = \sqrt{u_1^2 + \cdots + u_n^2}$$

The dot product is also related to the angle $\theta$ between two vectors: $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\|\|\mathbf{v}\|\cos\theta$. When $\mathbf{u} \cdot \mathbf{v} = 0$, the vectors are **orthogonal** (perpendicular), because $\cos(90°) = 0$.

## Worked Examples

**Example 1: Compute $\mathbf{u} \cdot \mathbf{v}$ for $\mathbf{u} = (1, 2, 3)$ and $\mathbf{v} = (4, -1, 2)$.**

Multiply corresponding components and sum. This works because the dot product is defined as a component-wise product sum — each pair contributes how much the two vectors "agree" in that direction:

$$\mathbf{u} \cdot \mathbf{v} = 1(4) + 2(-1) + 3(2) = 4 - 2 + 6 = 8$$

The result is a scalar, not a vector.

---

**Example 2: Find $\|\mathbf{u}\|$ for $\mathbf{u} = (3, 4)$.**

The magnitude is the length of the vector, computed via the Pythagorean theorem generalized to $n$ dimensions. Square each component, sum them, then take the square root:

$$\|\mathbf{u}\| = \sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5$$

This is a 3-4-5 right triangle, confirming the answer is 5.

---

**Example 3: Are $\mathbf{u} = (2, -1)$ and $\mathbf{v} = (1, 2)$ orthogonal?**

Two vectors are orthogonal if and only if their dot product equals zero. Compute:

$$\mathbf{u} \cdot \mathbf{v} = 2(1) + (-1)(2) = 2 - 2 = 0$$

Yes, they are orthogonal. You can verify geometrically: $\mathbf{u}$ goes right-and-down while $\mathbf{v}$ goes right-and-up at exactly 90°.

## Common Mistakes

- **Returning a vector instead of a scalar.** The dot product always produces a single number. If you're getting a vector, you've computed something else (perhaps component-wise multiplication without summing).
- **Confusing $\|\mathbf{u}\|^2$ with $\|\mathbf{u}\|$.** The squared magnitude is $\mathbf{u} \cdot \mathbf{u}$; the magnitude requires taking the square root. Forgetting the root gives the wrong units and wrong answer.
- **Assuming equal magnitudes means orthogonal.** Orthogonality is about direction (dot product = 0), not length. Two unit vectors can be parallel or perpendicular regardless of having the same magnitude.

## Quick Check

Try these before using hints:

1. Compute $(2, 1) \cdot (3, 4)$.
2. Find $\|(1, 2, 2)\|$.
3. Are $(1, 0)$ and $(0, 1)$ orthogonal?

*(Answers: $10$; $3$; yes, since $(1)(0)+(0)(1)=0$)*
