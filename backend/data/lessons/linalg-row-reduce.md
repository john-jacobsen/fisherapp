# Row Reduction

## Overview

**Row reduction** (Gaussian elimination) transforms a matrix into row echelon form using three elementary row operations: swap rows, scale a row, add a multiple of one row to another. It is the standard algorithm for solving linear systems.

## Key Idea

The three row operations:
1. Swap $R_i \leftrightarrow R_j$
2. Scale: $R_i \leftarrow cR_i$ ($c \ne 0$)
3. Add: $R_i \leftarrow R_i + kR_j$

These preserve the solution set. **Reduced row echelon form (RREF)** has leading 1s with zeros above and below.

## Worked Examples

**Example 1: Solve $x + 2y = 5$, $3x - y = 4$**

Augmented matrix: $\begin{pmatrix}1&2&5\\3&-1&4\end{pmatrix}$. $R_2 \leftarrow R_2 - 3R_1$: $\begin{pmatrix}1&2&5\\0&-7&-11\end{pmatrix}$. Scale: $y = 11/7$, then $x = 5 - 2(11/7) = 13/7$.

---

**Example 2: Identify a free variable**

$\begin{pmatrix}1&2&3\\0&0&1\end{pmatrix}$: pivot in columns 1 and 3; $x_2$ is free.

---

**Example 3: RREF of $\begin{pmatrix}2&4\\1&2\end{pmatrix}$**

$R_1 \leftarrow R_1/2$: $\begin{pmatrix}1&2\\1&2\end{pmatrix}$. $R_2 \leftarrow R_2 - R_1$: $\begin{pmatrix}1&2\\0&0\end{pmatrix}$. One free variable — infinitely many solutions.

## Common Mistakes

- **Dividing by zero when scaling.** Check your pivot is nonzero.
- **Arithmetic errors when adding multiples of rows.** Work carefully, sign by sign.

## Quick Check

1. What are the three elementary row operations?
2. How many solutions if RREF has a row $[0\ 0\ |\ 1]$?
3. What does a free variable in RREF indicate?

*(Answers: swap, scale, add; none (inconsistent); infinitely many solutions)*
