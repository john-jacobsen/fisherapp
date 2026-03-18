# Linear Transformations

## Overview

A **linear transformation** $T: \mathbb{R}^n \to \mathbb{R}^m$ satisfies additivity and homogeneity: $T(u+v) = T(u)+T(v)$ and $T(cu) = cT(u)$. Every linear transformation can be represented by a matrix.

## Key Idea

Every linear $T: \mathbb{R}^n \to \mathbb{R}^m$ has a unique matrix $A$ (the **standard matrix**) such that $T(x) = Ax$ for all $x$. The columns of $A$ are the images of the standard basis vectors.

## Worked Examples

**Example 1: $T(x_1, x_2) = (2x_1 + x_2, x_1 - 3x_2)$. Find the matrix.**

$T(e_1) = (2,1)$, $T(e_2) = (1,-3)$. Matrix: $\begin{pmatrix}2&1\\1&-3\end{pmatrix}$.

---

**Example 2: Is $T(x,y) = (x+1, y)$ linear?**

$T(0,0) = (1,0) \ne (0,0)$. Not linear (fails $T(\mathbf{0}) = \mathbf{0}$).

---

**Example 3: Rotation by $\theta$ in $\mathbb{R}^2$**

$$A = \begin{pmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{pmatrix}$$

## Common Mistakes

- **Thinking any transformation can be written as $Ax$.** Only linear ones can.
- **Not checking $T(\mathbf{0}) = \mathbf{0}$** as a quick linearity test.

## Quick Check

1. Is $T(x,y) = (3x, y)$ linear?
2. Find the standard matrix of $T(x,y) = (y,x)$.
3. Image of $(1,2)$ under the $90°$ rotation matrix?

*(Answers: yes; $\begin{pmatrix}0&1\\1&0\end{pmatrix}$; $(-2,1)$)*
