# Least Squares

## Overview

When a linear system $A\mathbf{x} = \mathbf{b}$ has no exact solution (too many equations, not enough freedom), the **least-squares solution** is the $\hat{\mathbf{x}}$ that gets as close as possible — it minimizes the squared error $\|A\hat{\mathbf{x}} - \mathbf{b}\|^2$. This is the mathematical foundation of linear regression and data fitting.

## Key Idea

The least-squares solution satisfies the **normal equations**:

$$A^T A\,\hat{\mathbf{x}} = A^T \mathbf{b}$$

When $A$ has full column rank, $A^T A$ is invertible and $\hat{\mathbf{x}} = (A^T A)^{-1} A^T \mathbf{b}$. Geometrically, $A\hat{\mathbf{x}} = \hat{\mathbf{b}}$ is the orthogonal projection of $\mathbf{b}$ onto the column space of $A$ — the closest point in col$(A)$ to $\mathbf{b}$.

## Worked Examples

**Example 1: Fit a line $y = mx + c$ to the points $(1,1)$, $(2,2)$, $(3,4)$.**

Set up $Ax = b$ where each row is one data point:

$$A = \begin{pmatrix}1&1\\2&1\\3&1\end{pmatrix}, \quad \mathbf{b} = \begin{pmatrix}1\\2\\4\end{pmatrix}, \quad \mathbf{x} = \begin{pmatrix}m\\c\end{pmatrix}$$

The system is overdetermined (3 equations, 2 unknowns), so form the normal equations. Compute $A^T A$ and $A^T \mathbf{b}$:

$$A^T A = \begin{pmatrix}14&6\\6&3\end{pmatrix}, \quad A^T\mathbf{b} = \begin{pmatrix}17\\7\end{pmatrix}$$

Solving $A^T A\,\hat{\mathbf{x}} = A^T\mathbf{b}$ gives $m = 3/2$, $c = -1/3$.

---

**Example 2: Geometric interpretation — why does this work?**

The residual $\mathbf{b} - A\hat{\mathbf{x}}$ is the error vector. The normal equations require $A^T(\mathbf{b} - A\hat{\mathbf{x}}) = \mathbf{0}$, which means the error is orthogonal to every column of $A$. In other words, $A\hat{\mathbf{x}}$ is the closest point in col$(A)$ to $\mathbf{b}$ — the orthogonal projection. No other choice of $\mathbf{x}$ produces a smaller error.

---

**Example 3: What if $b$ is already in col$(A)$?**

If $\mathbf{b} \in \text{col}(A)$, then $Ax = \mathbf{b}$ has an exact solution. The least-squares solution $\hat{\mathbf{x}}$ is that exact solution — the residual $\mathbf{b}-A\hat{\mathbf{x}} = \mathbf{0}$. Least-squares reduces to ordinary solving when an exact solution exists.

## Common Mistakes

- **Trying to solve $Ax = b$ directly when the system is overdetermined.** The system likely has no solution; you must form the normal equations $A^T A\hat{x} = A^T b$ and solve those instead.
- **Forgetting that $A^T A$ must be invertible.** The formula $(A^T A)^{-1}A^T\mathbf{b}$ requires $A^T A$ to be invertible, which happens when $A$ has linearly independent columns (full column rank). If the columns are dependent, $A^T A$ is singular and you need another approach (such as the pseudoinverse).
- **Confusing the least-squares solution with the exact solution.** The vector $A\hat{\mathbf{x}}$ is the projection of $\mathbf{b}$ onto col$(A)$, not necessarily equal to $\mathbf{b}$. The error $\mathbf{b} - A\hat{\mathbf{x}}$ is generally nonzero.

## Quick Check

Try these before using hints:

1. What equation does the least-squares solution satisfy?
2. What is the geometric meaning of $A\hat{\mathbf{x}}$?
3. If $\mathbf{b}$ is exactly in col$(A)$, what is the residual?

*(Answers: $A^T A\hat{\mathbf{x}} = A^T\mathbf{b}$; the orthogonal projection of $\mathbf{b}$ onto col$(A)$; zero)*
