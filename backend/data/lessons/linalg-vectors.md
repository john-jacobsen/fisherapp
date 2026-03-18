# Vectors: Dot Product and Magnitude

## Overview

A **vector** in $\mathbb{R}^n$ is an ordered list of $n$ numbers representing direction and magnitude. The **dot product** and **magnitude** are fundamental operations used throughout linear algebra and physics.

## Key Idea

For vectors $\mathbf{u} = (u_1, \ldots, u_n)$ and $\mathbf{v} = (v_1, \ldots, v_n)$:

$$\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^n u_i v_i, \quad \|\mathbf{u}\| = \sqrt{\mathbf{u} \cdot \mathbf{u}}$$

The dot product also satisfies $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\|\|\mathbf{v}\|\cos\theta$, where $\theta$ is the angle between them.

## Worked Examples

**Example 1: $\mathbf{u} = (1, 2, 3)$, $\mathbf{v} = (4, -1, 2)$. Find $\mathbf{u} \cdot \mathbf{v}$.**

$$1(4) + 2(-1) + 3(2) = 4 - 2 + 6 = 8$$

---

**Example 2: Find $\|\mathbf{u}\|$ for $\mathbf{u} = (3, 4)$.**

$$\|\mathbf{u}\| = \sqrt{9 + 16} = 5$$

---

**Example 3: Are $\mathbf{u} = (1, -1)$ and $\mathbf{v} = (1, 1)$ orthogonal?**

$\mathbf{u} \cdot \mathbf{v} = 1 - 1 = 0$. Yes, they are orthogonal.

## Common Mistakes

- **Confusing dot product with cross product.** Dot product is a scalar; cross product is a vector.
- **Forgetting that orthogonal means dot product = 0, not equal magnitudes.**

## Quick Check

1. $\mathbf{u} = (2,1)$, $\mathbf{v} = (3,4)$. Find $\mathbf{u} \cdot \mathbf{v}$.
2. $\|(1,2,2)\|$?
3. Are $(1,0)$ and $(0,1)$ orthogonal?

*(Answers: 10; 3; yes)*
