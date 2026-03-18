# Orthogonality

## Overview

Two vectors are **orthogonal** if their dot product is zero. A set of vectors is **orthonormal** if they are pairwise orthogonal and each has unit length. Orthogonality is the generalization of perpendicularity.

## Key Idea

$\mathbf{u}$ and $\mathbf{v}$ are orthogonal iff $\mathbf{u} \cdot \mathbf{v} = 0$.

A matrix $Q$ is **orthogonal** if its columns form an orthonormal set: $Q^T Q = I$, so $Q^{-1} = Q^T$.

## Worked Examples

**Example 1: Are $(1,2,-1)$ and $(3,0,3)$ orthogonal?**

$1(3) + 2(0) + (-1)(3) = 0$. Yes.

---

**Example 2: Normalize $v = (3,4)$**

$\|v\| = 5$. Unit vector: $(3/5, 4/5)$.

---

**Example 3: Verify $Q = \frac{1}{\sqrt{2}}\begin{pmatrix}1&-1\\1&1\end{pmatrix}$ is orthogonal**

$Q^T Q = \frac{1}{2}\begin{pmatrix}1&1\\-1&1\end{pmatrix}\begin{pmatrix}1&-1\\1&1\end{pmatrix} = \frac{1}{2}\begin{pmatrix}2&0\\0&2\end{pmatrix} = I$ ✓

## Common Mistakes

- **Confusing orthogonal (dot product = 0) with parallel (one is a scalar multiple of the other).**
- **Thinking $Q^T = Q^{-1}$ holds for all matrices.** Only for orthogonal matrices.

## Quick Check

1. Are $(1,0,0)$ and $(0,1,0)$ orthogonal?
2. Normalize $(0,0,5)$.
3. If $Q$ is orthogonal, what is $Q^{-1}$?

*(Answers: yes; $(0,0,1)$; $Q^T$)*
