# Determinants

## Overview

The **determinant** of a square matrix is a single scalar that captures key information about the matrix. If $\det(A) = 0$, the matrix is singular and has no inverse. If $\det(A) \neq 0$, the matrix is invertible. Geometrically, $|\det(A)|$ gives the factor by which the transformation scales volumes (areas in 2D).

## Key Idea

For a $2\times2$ matrix, the determinant is:

$$\det\begin{pmatrix}a & b \\ c & d\end{pmatrix} = ad - bc$$

For a $3\times3$ matrix, expand along the first row using cofactors:

$$\det(A) = a_{11} C_{11} - a_{12} C_{12} + a_{13} C_{13}$$

where $C_{ij}$ is the determinant of the $2\times2$ submatrix obtained by deleting row $i$ and column $j$. The signs alternate: $+, -, +, \ldots$

## Worked Examples

**Example 1: Compute $\det\begin{pmatrix}3 & 1 \\ 2 & 4\end{pmatrix}$.**

Apply the $2\times2$ formula directly. Multiply along the main diagonal and subtract the product along the anti-diagonal:

$$\det = 3(4) - 1(2) = 12 - 2 = 10$$

Since $\det \neq 0$, this matrix is invertible.

---

**Example 2: Compute the determinant of a triangular matrix $\begin{pmatrix}2 & 5 & 3 \\ 0 & 4 & 1 \\ 0 & 0 & 6\end{pmatrix}$.**

For any triangular matrix (upper or lower), the determinant equals the product of the diagonal entries. This is because all off-diagonal contributions vanish in the cofactor expansion:

$$\det = 2 \cdot 4 \cdot 6 = 48$$

This shortcut saves significant computation and is worth recognizing.

---

**Example 3: Effect of row operations on the determinant.**

Start from $A = \begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}$ with $\det(A) = -2$.

- Swapping the two rows gives $\det = +2$ (sign flips).
- Scaling row 1 by 3: the new determinant is $3(-2) = -6$.
- Adding 5 times row 2 to row 1: the determinant stays $-2$ (add-multiple leaves it unchanged).

Understanding how row operations change the determinant lets you compute determinants via row reduction.

## Common Mistakes

- **Applying the $2\times2$ formula to a $3\times3$ matrix.** The $2\times2$ formula $ad - bc$ only works for $2\times2$. For $3\times3$ you must expand with cofactors.
- **Forgetting the alternating signs in cofactor expansion.** The sign pattern is $+, -, +$ along any row or column. Missing a minus sign gives a wrong answer.
- **Scaling the wrong dimension.** When expanding along a row, the sign of each term depends on the column position, not the row position.

## Quick Check

Try these before using hints:

1. Compute $\det\begin{pmatrix}2 & 0 \\ 0 & 5\end{pmatrix}$.
2. Compute $\det\begin{pmatrix}1 & 2 \\ 2 & 4\end{pmatrix}$.
3. If $\det(A) = 3$ for a $2\times2$ matrix, what is $\det(2A)$?

*(Answers: $10$; $0$ (singular); $12$ — since each row is scaled by 2, so $\det(2A) = 2^2 \det(A) = 4 \cdot 3 = 12$)*
