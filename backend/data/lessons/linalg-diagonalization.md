# Diagonalization

## Overview

A matrix $A$ is **diagonalizable** if there exists an invertible $P$ such that $P^{-1}AP = D$ is diagonal. This is possible when $A$ has $n$ linearly independent eigenvectors. Diagonalization simplifies powers and functions of matrices.

## Key Idea

$A = PDP^{-1}$ where $D = \text{diag}(\lambda_1, \ldots, \lambda_n)$ and the columns of $P$ are the corresponding eigenvectors.

Then $A^k = PD^kP^{-1}$, and $D^k$ is just diagonal entries raised to the $k$-th power.

## Worked Examples

**Example 1: Diagonalize $A = \begin{pmatrix}3&1\\0&2\end{pmatrix}$**

Eigenvalues $\lambda_1=3$, $\lambda_2=2$; eigenvectors $(1,0)$, $(-1,1)$.

$P = \begin{pmatrix}1&-1\\0&1\end{pmatrix}$, $D = \begin{pmatrix}3&0\\0&2\end{pmatrix}$.

---

**Example 2: Compute $A^3$ via diagonalization**

$A^3 = PD^3P^{-1}$, where $D^3 = \begin{pmatrix}27&0\\0&8\end{pmatrix}$.

---

**Example 3: When is a matrix not diagonalizable?**

If it doesn't have $n$ independent eigenvectors. Example: $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ has only one independent eigenvector for $\lambda=1$.

## Common Mistakes

- **Assuming symmetric matrices can have complex eigenvalues.** Real symmetric matrices always have real eigenvalues.
- **Mixing up column order in $P$ vs. diagonal order in $D$.**

## Quick Check

1. A matrix has eigenvalues 2 and 5. What is $D$?
2. Is the identity matrix diagonalizable?
3. If $A = PDP^{-1}$, what is $A^2$?

*(Answers: $\text{diag}(2,5)$; yes ($A=I=ID I^{-1}$); $PD^2P^{-1}$)*
