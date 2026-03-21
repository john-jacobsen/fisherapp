# Singular Value Decomposition

## Overview

The **Singular Value Decomposition (SVD)** factors any $m\times n$ matrix $A$ — regardless of whether it's square — as $A = U\Sigma V^T$. It is the most complete and informative matrix factorization. SVD reveals the true geometry of a linear transformation: every matrix is equivalent to a rotate–scale–rotate sequence. It underlies dimensionality reduction, image compression, and numerically stable least-squares solvers.

## Key Idea

$$A = U\Sigma V^T$$

- $U$ is $m\times m$ orthogonal — columns are **left singular vectors** (orthonormal basis for $\mathbb{R}^m$)
- $\Sigma$ is $m\times n$ diagonal — diagonal entries $\sigma_1 \geq \sigma_2 \geq \cdots \geq 0$ are **singular values**
- $V$ is $n\times n$ orthogonal — columns are **right singular vectors** (orthonormal basis for $\mathbb{R}^n$)

The singular values are $\sigma_i = \sqrt{\lambda_i(A^T A)}$, and the rank of $A$ equals the number of nonzero singular values.

## Worked Examples

**Example 1: SVD of a diagonal matrix $A = \begin{pmatrix}3 & 0 \\ 0 & 2\end{pmatrix}$.**

A diagonal matrix with non-negative entries is already in SVD form. $U = I$, $V = I$, and $\Sigma = A$. The singular values are 3 and 2. This case makes the structure clear: no rotation needed, just scaling.

---

**Example 2: Geometric interpretation of $A = U\Sigma V^T$.**

Applying $A$ to a vector $\mathbf{x}$ proceeds in three stages. First, $V^T\mathbf{x}$ rotates (or reflects) $\mathbf{x}$ — $V^T$ is orthogonal, so it preserves lengths. Second, $\Sigma(V^T\mathbf{x})$ scales along each coordinate axis by $\sigma_1, \sigma_2, \ldots$. Third, $U(\Sigma V^T\mathbf{x})$ rotates again. Every linear map on any spaces decomposes this way: it's always "rotate, scale, rotate back."

---

**Example 3: Best rank-1 approximation of $A$.**

The best rank-$k$ approximation to $A$ (in the sense of minimizing $\|A - A_k\|$) is:

$$A_k = \sum_{i=1}^k \sigma_i\, \mathbf{u}_i\, \mathbf{v}_i^T$$

For rank 1, this is $\sigma_1 \mathbf{u}_1 \mathbf{v}_1^T$. If $A$ is a $1000\times1000$ image matrix with many small singular values, keeping only the top $k$ singular values and vectors compresses the image with minimal visual loss. This is the basis of image compression via SVD.

## Common Mistakes

- **Confusing singular values with eigenvalues.** For a symmetric positive definite matrix, they coincide, but in general they are different. Eigenvalues can be negative or complex; singular values are always real and non-negative.
- **Thinking $U = V$.** These are two different orthogonal matrices — $U$ is $m\times m$ and $V$ is $n\times n$. For non-square $A$, they can't even be the same matrix.
- **Forgetting that $\Sigma$ is $m\times n$, not square.** The diagonal of $\Sigma$ has $\min(m,n)$ entries. If $A$ is $3\times5$, then $\Sigma$ is $3\times5$ with at most 3 singular values.

## Quick Check

Try these before using hints:

1. How many nonzero singular values does a rank-2 matrix have?
2. For a symmetric positive definite matrix, how do singular values relate to eigenvalues?
3. What does a near-zero singular value indicate about the matrix?

*(Answers: exactly 2; they are equal; near-linear dependence among columns — the matrix is nearly singular)*
