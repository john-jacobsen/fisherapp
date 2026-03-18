# Singular Value Decomposition

## Overview

The **Singular Value Decomposition (SVD)** decomposes any $m\times n$ matrix $A$ as $A = U\Sigma V^T$, where $U$ and $V$ are orthogonal and $\Sigma$ is diagonal with non-negative entries. It is the most informative matrix factorization.

## Key Idea

$$A = U \Sigma V^T$$

- $U$: $m\times m$ orthogonal (left singular vectors)
- $\Sigma$: $m\times n$ diagonal ($\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$ are singular values)
- $V$: $n\times n$ orthogonal (right singular vectors)

Singular values $\sigma_i = \sqrt{\lambda_i(A^T A)}$.

## Worked Examples

**Example 1: SVD of $A = \begin{pmatrix}3&0\\0&2\end{pmatrix}$ (diagonal)**

$\Sigma = A$, $U = V = I$. Singular values: 3 and 2.

---

**Example 2: Geometric interpretation**

$A = U\Sigma V^T$: $V^T$ rotates, $\Sigma$ scales axes, $U$ rotates again. Every linear map is "rotate–scale–rotate."

---

**Example 3: Low-rank approximation**

Rank-$k$ approximation: $A_k = \sum_{i=1}^k \sigma_i u_i v_i^T$. Best rank-$k$ approximation in 2-norm.

## Common Mistakes

- **Confusing singular values with eigenvalues.** For symmetric $A$, they coincide, but not in general.
- **Thinking $U$ and $V$ must be the same matrix.** They are different orthogonal matrices.

## Quick Check

1. What is the rank of $A$ in terms of its singular values?
2. If $A$ is symmetric positive definite, how do singular values relate to eigenvalues?
3. What does a near-zero singular value indicate?

*(Answers: number of nonzero $\sigma_i$; they are equal; near-linear dependence)*
