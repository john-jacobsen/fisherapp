# Linear Transformations

## Overview

A **linear transformation** $T: \mathbb{R}^n \to \mathbb{R}^m$ is a function between vector spaces that preserves addition and scalar multiplication. Every rotation, reflection, projection, and shear in geometry is a linear transformation. Every linear transformation can be represented by a matrix, making matrix operations the computational engine of linear algebra.

## Key Idea

$T$ is linear if and only if for all vectors $\mathbf{u}, \mathbf{v}$ and scalar $c$:

$$T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}), \qquad T(c\mathbf{u}) = c\,T(\mathbf{u})$$

Every linear $T: \mathbb{R}^n \to \mathbb{R}^m$ has a unique **standard matrix** $A$ such that $T(\mathbf{x}) = A\mathbf{x}$. The $j$-th column of $A$ is $T(\mathbf{e}_j)$ — the image of the $j$-th standard basis vector.

## Worked Examples

**Example 1: Find the standard matrix of $T(x_1, x_2) = (2x_1 + x_2,\ x_1 - 3x_2)$.**

Apply $T$ to each standard basis vector separately. $T(\mathbf{e}_1) = T(1,0) = (2,1)$ and $T(\mathbf{e}_2) = T(0,1) = (1,-3)$. These become the columns of $A$:

$$A = \begin{pmatrix}2 & 1 \\ 1 & -3\end{pmatrix}$$

You can verify: $A\begin{pmatrix}x_1\\x_2\end{pmatrix} = \begin{pmatrix}2x_1+x_2\\x_1-3x_2\end{pmatrix}$ matches the formula for $T$.

---

**Example 2: Is $T(x,y) = (x+1, y)$ a linear transformation?**

Test the necessary condition $T(\mathbf{0}) = \mathbf{0}$. Here $T(0,0) = (0+1, 0) = (1,0) \neq (0,0)$. This fails immediately — a linear transformation must always send the zero vector to the zero vector. The translation by 1 in the first coordinate breaks linearity.

---

**Example 3: The rotation by angle $\theta$ in $\mathbb{R}^2$.**

Rotating $\mathbf{e}_1 = (1,0)$ by $\theta$ gives $(\cos\theta, \sin\theta)$; rotating $\mathbf{e}_2 = (0,1)$ by $\theta$ gives $(-\sin\theta, \cos\theta)$. These are the columns of the rotation matrix:

$$A = \begin{pmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{pmatrix}$$

For $\theta = 90°$: $A = \begin{pmatrix}0 & -1 \\ 1 & 0\end{pmatrix}$, which sends $(1,0)$ to $(0,1)$ and $(0,1)$ to $(-1,0)$ — a quarter turn.

## Common Mistakes

- **Assuming any function between vector spaces is linear.** Functions like $T(x) = x^2$ or $T(x,y) = (x+1,y)$ are not linear. Always check both conditions, or at minimum check $T(\mathbf{0}) = \mathbf{0}$.
- **Building the standard matrix in the wrong order.** The $j$-th column is $T(\mathbf{e}_j)$, not $T(\mathbf{e}_j)$ as a row. If your columns and rows are swapped, you get the transpose of the correct matrix.
- **Forgetting that composition of linear maps corresponds to matrix multiplication.** If $T_1$ has matrix $A_1$ and $T_2$ has matrix $A_2$, then $T_2 \circ T_1$ has matrix $A_2 A_1$ (apply $T_1$ first, so $A_1$ goes on the right).

## Quick Check

Try these before using hints:

1. Is $T(x,y) = (3x, y)$ a linear transformation?
2. Find the standard matrix of $T(x,y) = (y, x)$.
3. What is the image of $(1,2)$ under the $90°$ counterclockwise rotation?

*(Answers: yes; $\begin{pmatrix}0 & 1 \\ 1 & 0\end{pmatrix}$; $(-2,1)$)*
