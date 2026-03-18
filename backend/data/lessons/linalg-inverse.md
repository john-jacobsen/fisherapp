# Matrix Inverse

## Overview

The **inverse** of a square matrix $A$ is the matrix $A^{-1}$ satisfying $AA^{-1} = A^{-1}A = I$. A matrix is invertible if and only if $\det A \ne 0$. The inverse undoes the linear transformation.

## Key Idea

For $2\times2$: $A^{-1} = \frac{1}{\det A}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$ when $A = \begin{pmatrix}a&b\\c&d\end{pmatrix}$.

For larger matrices: row-reduce the augmented matrix $[A | I]$ until the left block becomes $I$; the right block is $A^{-1}$.

## Worked Examples

**Example 1: Find the inverse of $A = \begin{pmatrix}2&1\\5&3\end{pmatrix}$**

$\det A = 1$. $A^{-1} = \begin{pmatrix}3&-1\\-5&2\end{pmatrix}$.

---

**Example 2: Verify: $AA^{-1} = I$**

$\begin{pmatrix}2&1\\5&3\end{pmatrix}\begin{pmatrix}3&-1\\-5&2\end{pmatrix} = \begin{pmatrix}1&0\\0&1\end{pmatrix}$ ✓

---

**Example 3: Use inverse to solve $Ax = b$**

If $A^{-1}$ exists, then $x = A^{-1}b$. For $A$ above and $b = \begin{pmatrix}4\\11\end{pmatrix}$: $x = \begin{pmatrix}3&-1\\-5&2\end{pmatrix}\begin{pmatrix}4\\11\end{pmatrix} = \begin{pmatrix}1\\2\end{pmatrix}$.

## Common Mistakes

- **Inverting a singular matrix.** If $\det A = 0$, no inverse exists.
- **$(AB)^{-1} = A^{-1}B^{-1}$.** Wrong — it's $B^{-1}A^{-1}$ (reverse order).

## Quick Check

1. Find the inverse of $\begin{pmatrix}1&2\\0&1\end{pmatrix}$.
2. Is $\begin{pmatrix}1&2\\2&4\end{pmatrix}$ invertible?
3. $(AB)^{-1} = ?$

*(Answers: $\begin{pmatrix}1&-2\\0&1\end{pmatrix}$; no (det=0); $B^{-1}A^{-1}$)*
