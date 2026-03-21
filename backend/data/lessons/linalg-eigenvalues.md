# Eigenvalues and Eigenvectors

## Overview

An **eigenvector** of a matrix $A$ is a nonzero vector $\mathbf{v}$ that $A$ only scales — not rotates. The scale factor is the corresponding **eigenvalue** $\lambda$. Together they satisfy $A\mathbf{v} = \lambda\mathbf{v}$. Eigenvalues reveal the fundamental behavior of a linear transformation: which directions are preserved and by how much.

## Key Idea

Find eigenvalues by solving the **characteristic equation**:

$$\det(A - \lambda I) = 0$$

This is a polynomial in $\lambda$ whose roots are the eigenvalues. For each eigenvalue $\lambda$, find its eigenvectors by solving the homogeneous system $(A - \lambda I)\mathbf{v} = \mathbf{0}$. The set of all solutions (excluding $\mathbf{0}$) forms the **eigenspace** for $\lambda$.

## Worked Examples

**Example 1: Find the eigenvalues of $A = \begin{pmatrix}3 & 1 \\ 0 & 2\end{pmatrix}$.**

Compute $\det(A - \lambda I)$. Subtracting $\lambda$ from the diagonal gives a triangular matrix, so the determinant is the product of the diagonal entries:

$$\det\begin{pmatrix}3-\lambda & 1 \\ 0 & 2-\lambda\end{pmatrix} = (3-\lambda)(2-\lambda) = 0$$

Eigenvalues: $\lambda_1 = 3$ and $\lambda_2 = 2$. For triangular matrices, the eigenvalues are always the diagonal entries.

---

**Example 2: Find the eigenvector for $\lambda_1 = 3$.**

Substitute $\lambda = 3$ and solve $(A - 3I)\mathbf{v} = \mathbf{0}$:

$$A - 3I = \begin{pmatrix}0 & 1 \\ 0 & -1\end{pmatrix} \rightarrow \text{RREF:} \begin{pmatrix}0 & 1 \\ 0 & 0\end{pmatrix}$$

The second equation gives $v_2 = 0$; $v_1$ is free. Setting $v_1 = 1$: eigenvector is $(1,0)$. Check: $A(1,0)^T = (3,0)^T = 3(1,0)^T$ ✓

---

**Example 3: Find eigenvalues of $A = \begin{pmatrix}2 & 1 \\ 1 & 2\end{pmatrix}$.**

Compute the characteristic polynomial:

$$\det\begin{pmatrix}2-\lambda & 1 \\ 1 & 2-\lambda\end{pmatrix} = (2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = (\lambda-3)(\lambda-1) = 0$$

Eigenvalues: $\lambda = 3$ and $\lambda = 1$. For $\lambda = 3$: eigenvector $(1,1)/\sqrt{2}$. For $\lambda = 1$: eigenvector $(1,-1)/\sqrt{2}$. Note that $A$ is symmetric, so these eigenvectors are orthogonal — as expected.

## Common Mistakes

- **Trying to find $\lambda$ from $A\mathbf{v} = \lambda\mathbf{v}$ without first using the characteristic equation.** The equation $A\mathbf{v} = \lambda\mathbf{v}$ only makes sense after you know $\lambda$. Always solve $\det(A-\lambda I)=0$ first to find eigenvalues, then find eigenvectors.
- **Assuming eigenvectors are unique.** Any nonzero scalar multiple of an eigenvector is also an eigenvector for the same eigenvalue. The eigenspace can be multi-dimensional.
- **Forgetting to subtract $\lambda$ from every diagonal entry.** In $A - \lambda I$, every diagonal entry decreases by $\lambda$. Students sometimes subtract only from one entry, especially for larger matrices.

## Quick Check

Try these before using hints:

1. Find the eigenvalues of $\begin{pmatrix}4 & 0 \\ 0 & -1\end{pmatrix}$.
2. What is an eigenvector for $\lambda = 4$ above?
3. What does $\lambda = 0$ imply about $A$?

*(Answers: $4$ and $-1$; any nonzero multiple of $(1,0)$; $A$ is singular — $Av = 0$ for some nonzero $v$)*
