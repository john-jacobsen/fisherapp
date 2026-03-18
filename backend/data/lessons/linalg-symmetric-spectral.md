# Symmetric Matrices and Spectral Theorem

## Overview

A **symmetric matrix** satisfies $A = A^T$. The **Spectral Theorem** guarantees that every real symmetric matrix is orthogonally diagonalizable: $A = Q\Lambda Q^T$, where $Q$ has orthonormal eigenvectors as columns.

## Key Idea

**Spectral Theorem:** If $A$ is real symmetric ($n\times n$), then:
1. All eigenvalues are real.
2. Eigenvectors for distinct eigenvalues are orthogonal.
3. $A = Q\Lambda Q^T$ where $Q$ is orthogonal ($Q^T = Q^{-1}$).

## Worked Examples

**Example 1: Eigenvalues of $A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$**

$\lambda_1 = 3$ (eigenvector $(1,1)/\sqrt{2}$), $\lambda_2 = 1$ (eigenvector $(1,-1)/\sqrt{2}$). Note: orthogonal ✓

---

**Example 2: Spectral decomposition of $A$ above**

$A = 3 \cdot v_1 v_1^T + 1 \cdot v_2 v_2^T$ where $v_i$ are the unit eigenvectors.

---

**Example 3: Verify $Q^T Q = I$**

Columns of $Q$ are orthonormal by construction, so $Q^T Q = I$.

## Common Mistakes

- **Forgetting to normalize eigenvectors** when constructing $Q$.
- **Applying the Spectral Theorem to non-symmetric matrices.**

## Quick Check

1. Are eigenvalues of a real symmetric matrix always real?
2. Are eigenvectors for distinct eigenvalues always orthogonal (symmetric case)?
3. What does $A = Q\Lambda Q^T$ mean geometrically?

*(Answers: yes; yes; rotate, scale, rotate back)*
