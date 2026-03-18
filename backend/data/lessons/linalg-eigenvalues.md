# Eigenvalues and Eigenvectors

## Overview

An **eigenvector** of $A$ is a nonzero vector $v$ such that $Av = \lambda v$ for some scalar $\lambda$ (the **eigenvalue**). Eigenvectors point in directions that the transformation scales but doesn't rotate.

## Key Idea

Find eigenvalues by solving the **characteristic equation**:

$$\det(A - \lambda I) = 0$$

For each $\lambda$, find eigenvectors by solving $(A - \lambda I)v = 0$.

## Worked Examples

**Example 1: Find eigenvalues of $A = \begin{pmatrix}3&1\\0&2\end{pmatrix}$**

$\det(A - \lambda I) = (3-\lambda)(2-\lambda) = 0$. Eigenvalues: $\lambda = 3$ and $\lambda = 2$.

---

**Example 2: Eigenvector for $\lambda = 3$**

$(A - 3I)v = \begin{pmatrix}0&1\\0&-1\end{pmatrix}v = 0 \Rightarrow v = \begin{pmatrix}1\\0\end{pmatrix}$.

---

**Example 3: Eigenvalues of $A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$**

$\det(A-\lambda I) = (2-\lambda)^2 - 1 = 0 \Rightarrow \lambda = 3$ or $\lambda = 1$.

## Common Mistakes

- **Setting $Av = \lambda v$ to find $\lambda$ before finding eigenvectors.** You need the characteristic equation first.
- **Thinking eigenvectors are unique.** Any nonzero multiple of an eigenvector is also an eigenvector.

## Quick Check

1. Find eigenvalues of $\begin{pmatrix}4&0\\0&-1\end{pmatrix}$.
2. Eigenvector for $\lambda = 4$ above?
3. What does $\lambda = 0$ imply?

*(Answers: 4, −1; $(1,0)$; $A$ is singular)*
