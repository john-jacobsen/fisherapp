# Determinants

## Overview

The **determinant** of a square matrix is a scalar that encodes important geometric and algebraic information. If $\det A = 0$, the matrix is singular (not invertible). Geometrically, $|\det A|$ is the volume scaling factor of the linear transformation.

## Key Idea

For $2\times2$: $\det\begin{pmatrix}a&b\\c&d\end{pmatrix} = ad - bc$.

For $3\times3$ (cofactor expansion along first row):

$$\det A = a_{11}M_{11} - a_{12}M_{12} + a_{13}M_{13}$$

where $M_{ij}$ is the minor (determinant of the submatrix with row $i$, column $j$ deleted).

## Worked Examples

**Example 1: $\det\begin{pmatrix}3&1\\2&4\end{pmatrix}$**

$$3(4) - 1(2) = 10$$

---

**Example 2: $\det\begin{pmatrix}1&0&0\\2&3&0\\4&5&6\end{pmatrix}$**

Lower triangular — determinant = product of diagonal = $1 \cdot 3 \cdot 6 = 18$.

---

**Example 3: Effect of row operations on determinant**

Swapping rows changes sign. Scaling row $i$ by $c$ multiplies $\det$ by $c$. Adding a multiple of one row to another leaves $\det$ unchanged.

## Common Mistakes

- **Using $2\times2$ formula for $3\times3$ matrices.**
- **Forgetting the alternating signs** in cofactor expansion.

## Quick Check

1. $\det\begin{pmatrix}2&0\\0&5\end{pmatrix}$
2. $\det\begin{pmatrix}1&2\\2&4\end{pmatrix}$
3. If $\det A = 3$, what is $\det(2A)$ for a $2\times2$ matrix?

*(Answers: 10; 0; 12)*
