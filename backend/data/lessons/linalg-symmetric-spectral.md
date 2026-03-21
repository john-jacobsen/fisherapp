# Symmetric Matrices and the Spectral Theorem

## Overview

A **symmetric matrix** satisfies $A = A^T$ — its entries mirror across the main diagonal. Symmetric matrices arise throughout statistics, physics, and optimization. The **Spectral Theorem** guarantees that every real symmetric matrix is orthogonally diagonalizable, giving it a decomposition $A = Q\Lambda Q^T$ where $Q$ is orthogonal and $\Lambda$ is diagonal.

## Key Idea

**Spectral Theorem:** If $A$ is a real $n\times n$ symmetric matrix, then:

1. All eigenvalues of $A$ are **real**.
2. Eigenvectors corresponding to distinct eigenvalues are **orthogonal**.
3. $A = Q\Lambda Q^T$, where $\Lambda$ is diagonal (eigenvalues) and $Q$ is orthogonal ($Q^TQ = I$, columns are orthonormal eigenvectors).

This is stronger than ordinary diagonalization ($A = PDP^{-1}$) because $Q^{-1} = Q^T$ — you don't need to invert anything.

## Worked Examples

**Example 1: Find eigenvalues and verify orthogonality for $A = \begin{pmatrix}2 & 1 \\ 1 & 2\end{pmatrix}$.**

The characteristic polynomial is $(2-\lambda)^2 - 1 = 0$, giving $\lambda_1 = 3$ and $\lambda_2 = 1$.

For $\lambda_1 = 3$: solve $(A-3I)\mathbf{v} = 0$; eigenvector is $(1,1)$.
For $\lambda_2 = 1$: solve $(A-I)\mathbf{v} = 0$; eigenvector is $(1,-1)$.

Check orthogonality: $(1,1)\cdot(1,-1) = 1-1 = 0$ ✓. Distinct eigenvalues guarantee orthogonal eigenvectors — the Spectral Theorem predicted this.

---

**Example 2: Construct $Q$ and $\Lambda$ for $A$ above.**

Normalize the eigenvectors to get orthonormal columns for $Q$:

$$Q = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1 \\ 1 & -1\end{pmatrix}, \quad \Lambda = \begin{pmatrix}3 & 0 \\ 0 & 1\end{pmatrix}$$

Then $A = Q\Lambda Q^T$. You can verify: since $Q$ is orthogonal, $Q^T = Q^{-1}$, so $Q\Lambda Q^T$ is valid without computing an inverse.

---

**Example 3: Write $A$ as a sum of rank-1 matrices (spectral decomposition).**

The Spectral Theorem also says $A = \lambda_1 \mathbf{q}_1\mathbf{q}_1^T + \lambda_2 \mathbf{q}_2\mathbf{q}_2^T$, where $\mathbf{q}_i$ are unit eigenvectors. Each term is a projection onto the $i$-th eigenspace, scaled by $\lambda_i$. This **outer product form** reveals the structure of $A$ as a weighted combination of directions:

$$A = 3 \cdot \frac{1}{2}\begin{pmatrix}1\\1\end{pmatrix}\begin{pmatrix}1&1\end{pmatrix} + 1 \cdot \frac{1}{2}\begin{pmatrix}1\\-1\end{pmatrix}\begin{pmatrix}1&-1\end{pmatrix}$$

## Common Mistakes

- **Forgetting to normalize eigenvectors when building $Q$.** The Spectral Theorem requires orthonormal columns (unit vectors), not just orthogonal ones. Skipping normalization means $Q^T \neq Q^{-1}$ and the decomposition fails.
- **Applying the Spectral Theorem to non-symmetric matrices.** The theorem holds only for symmetric matrices. A non-symmetric real matrix can have complex eigenvalues and may not be orthogonally diagonalizable.
- **Confusing $Q\Lambda Q^T$ with $Q\Lambda Q^{-1}$.** For orthogonal $Q$, these are the same thing ($Q^T = Q^{-1}$), but writing $Q^T$ signals that you know you're working with an orthogonal matrix and can avoid computing an inverse.

## Quick Check

Try these before using hints:

1. Are eigenvalues of a real symmetric matrix always real?
2. Are eigenvectors for distinct eigenvalues of a symmetric matrix always orthogonal?
3. What does the decomposition $A = Q\Lambda Q^T$ mean geometrically?

*(Answers: yes; yes — Spectral Theorem guarantees it; rotate to eigenbasis, scale by eigenvalues, rotate back)*
