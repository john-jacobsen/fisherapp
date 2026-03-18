# Least Squares

## Overview

When $Ax = b$ has no solution (overdetermined system), the **least-squares solution** minimizes $\|Ax - b\|^2$ — the closest solution in the column space of $A$.

## Key Idea

The least-squares solution satisfies the **normal equations**:

$$A^T A \hat{x} = A^T b$$

If $A$ has full column rank, $\hat{x} = (A^T A)^{-1} A^T b$.

## Worked Examples

**Example 1: Fit a line $y = mx + c$ to $(1,1), (2,2), (3,4)$**

$A = \begin{pmatrix}1&1\\2&1\\3&1\end{pmatrix}$, $b = \begin{pmatrix}1\\2\\4\end{pmatrix}$.

$A^T A = \begin{pmatrix}14&6\\6&3\end{pmatrix}$, $A^T b = \begin{pmatrix}17\\7\end{pmatrix}$.

Normal equations give $m = 3/2$, $c = -1/3$.

---

**Example 2: Geometric meaning**

$\hat{b} = A\hat{x}$ is the projection of $b$ onto $\text{col}(A)$.

---

**Example 3: Residual is orthogonal to column space**

$A^T(b - A\hat{x}) = 0$, meaning the error is perpendicular to all columns of $A$.

## Common Mistakes

- **Solving $Ax = b$ directly when it's inconsistent.** Use normal equations instead.
- **Forgetting that $A^T A$ must be invertible** (requires $A$ to have independent columns).

## Quick Check

1. What equation do least-squares solutions satisfy?
2. Is the least-squares solution exact when $b \in \text{col}(A)$?
3. What does minimizing $\|Ax - b\|^2$ find geometrically?

*(Answers: $A^T A\hat{x} = A^T b$; yes, residual = 0; projection of $b$ onto col($A$))*
