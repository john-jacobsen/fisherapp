# Orthogonality

## Overview

Two vectors are **orthogonal** if their dot product is zero — this generalizes perpendicularity to any number of dimensions. A set of vectors is **orthonormal** if they are pairwise orthogonal and each has unit length (magnitude 1). A square matrix $Q$ is called an **orthogonal matrix** if its columns form an orthonormal set.

## Key Idea

$\mathbf{u}$ and $\mathbf{v}$ are orthogonal iff $\mathbf{u} \cdot \mathbf{v} = 0$.

For a matrix $Q$ with orthonormal columns:

$$Q^T Q = I \implies Q^{-1} = Q^T$$

This is the defining property: orthogonal matrices are invertible and their inverse is simply their transpose — no row reduction needed. Orthogonal matrices also preserve lengths: $\|Q\mathbf{x}\| = \|\mathbf{x}\|$ for all $\mathbf{x}$.

## Worked Examples

**Example 1: Are $(1, 2, -1)$ and $(3, 0, 3)$ orthogonal?**

Compute the dot product. If it equals zero, the vectors are orthogonal regardless of their magnitudes:

$$\mathbf{u} \cdot \mathbf{v} = 1(3) + 2(0) + (-1)(3) = 3 + 0 - 3 = 0$$

Yes — they are orthogonal. The magnitudes are $\|\mathbf{u}\| = \sqrt{6}$ and $\|\mathbf{v}\| = 3\sqrt{2}$, but magnitude does not affect orthogonality.

---

**Example 2: Normalize $\mathbf{v} = (3, 4)$ to get a unit vector.**

A unit vector points in the same direction but has magnitude 1. Divide each component by the magnitude:

$$\|\mathbf{v}\| = \sqrt{3^2 + 4^2} = \sqrt{25} = 5, \qquad \hat{\mathbf{v}} = \frac{1}{5}(3,4) = \left(\frac{3}{5}, \frac{4}{5}\right)$$

Verify: $\left(\frac{3}{5}\right)^2 + \left(\frac{4}{5}\right)^2 = \frac{9}{25}+\frac{16}{25} = 1$ ✓

---

**Example 3: Verify $Q = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & -1 \\ 1 & 1\end{pmatrix}$ is an orthogonal matrix.**

Compute $Q^T Q$. For this to equal $I$, the column dot products must produce 1s on the diagonal and 0s off it:

$$Q^T Q = \frac{1}{2}\begin{pmatrix}1 & 1 \\ -1 & 1\end{pmatrix}\begin{pmatrix}1 & -1 \\ 1 & 1\end{pmatrix} = \frac{1}{2}\begin{pmatrix}2 & 0 \\ 0 & 2\end{pmatrix} = I \checkmark$$

The columns are orthonormal, confirming $Q^{-1} = Q^T$.

## Common Mistakes

- **Confusing orthogonal vectors with parallel vectors.** Orthogonal means dot product equals zero. Parallel means one is a scalar multiple of the other. These are opposite concepts.
- **Thinking $Q^T = Q^{-1}$ for all matrices.** This holds only when $Q$ has orthonormal columns. For a general matrix, the inverse requires row reduction.
- **Normalizing before checking orthogonality.** Orthogonality ($\mathbf{u}\cdot\mathbf{v}=0$) is independent of length. Check the dot product directly — don't normalize first.

## Quick Check

Try these before using hints:

1. Are $(1,0,0)$ and $(0,1,0)$ orthogonal?
2. Normalize the vector $(0, 0, 5)$.
3. If $Q$ is an orthogonal matrix, what is $Q^{-1}$?

*(Answers: yes, since the dot product is 0; $(0,0,1)$; $Q^T$)*
