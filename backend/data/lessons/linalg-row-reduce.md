# Row Reduction

## Overview

**Row reduction** (Gaussian elimination) is the systematic algorithm for solving linear systems. It transforms a matrix into **reduced row echelon form (RREF)** using three legal row operations that preserve the solution set. Every linear system can be analyzed completely by bringing its augmented matrix to RREF.

## Key Idea

The three elementary row operations (all reversible, so they preserve solutions):

1. **Swap** rows $R_i \leftrightarrow R_j$
2. **Scale** a row: $R_i \leftarrow c R_i$ for $c \neq 0$
3. **Add a multiple** of one row to another: $R_i \leftarrow R_i + k R_j$

RREF requires: leading entry in each row is 1 (the **pivot**), each pivot column has zeros everywhere else, and pivots move right as you move down. Free variables correspond to non-pivot columns.

## Worked Examples

**Example 1: Solve $x + 2y = 5$, $3x - y = 4$.**

Write the augmented matrix and eliminate. The goal is to produce a 0 below the pivot in column 1:

$$\begin{pmatrix}1&2&5\\3&-1&4\end{pmatrix} \xrightarrow{R_2 \leftarrow R_2 - 3R_1} \begin{pmatrix}1&2&5\\0&-7&-11\end{pmatrix}$$

Scale $R_2$ by $-1/7$ to get a leading 1, then eliminate upward:

$$\xrightarrow{R_2 \leftarrow -R_2/7} \begin{pmatrix}1&2&5\\0&1&11/7\end{pmatrix} \xrightarrow{R_1 \leftarrow R_1 - 2R_2} \begin{pmatrix}1&0&13/7\\0&1&11/7\end{pmatrix}$$

Solution: $x = 13/7$, $y = 11/7$.

---

**Example 2: Identify free variables in RREF $\begin{pmatrix}1&2&0&3\\0&0&1&-1\end{pmatrix}$.**

Pivot columns are 1 and 3. Column 2 has no pivot, so $x_2$ is a **free variable** — it can take any value. Setting $x_2 = t$: $x_1 = 3 - 2t$, $x_3 = -1$. There are infinitely many solutions, one for each value of $t$.

---

**Example 3: Detect an inconsistent system.**

Row reduce $\begin{pmatrix}1&1&2\\2&2&5\end{pmatrix}$:

$$\xrightarrow{R_2 \leftarrow R_2 - 2R_1} \begin{pmatrix}1&1&2\\0&0&1\end{pmatrix}$$

The second row says $0x_1 + 0x_2 = 1$, which is impossible. This row means the system is **inconsistent** — no solution exists.

## Common Mistakes

- **Dividing by zero when scaling.** If the entry you want to use as a pivot is zero, first swap rows to bring a nonzero entry to the pivot position.
- **Making arithmetic errors in the add-multiple step.** Each entry in the row changes — work through every column carefully, paying attention to signs.
- **Not completing to full RREF.** Eliminating only downward gives row echelon form, not RREF. To read off solutions directly, also eliminate upward above each pivot.

## Quick Check

Try these before using hints:

1. What are the three elementary row operations?
2. What does a row $\begin{pmatrix}0 & 0 & 1\end{pmatrix}$ (in the augmented matrix) mean?
3. What does a free variable indicate about the number of solutions?

*(Answers: swap, scale, add-multiple; no solution (inconsistent); infinitely many solutions)*
