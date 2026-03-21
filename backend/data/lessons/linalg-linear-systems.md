# Linear Systems

## Overview

A **linear system** is a collection of linear equations sharing the same unknowns. Depending on how the equations relate to each other, a system can have exactly one solution, infinitely many, or none at all. Row reduction on the augmented matrix is the standard method for finding and classifying solutions.

## Key Idea

Write the system as an augmented matrix $[A \mid b]$ and row-reduce to RREF. Three outcomes are possible:

- **Unique solution**: every variable has a pivot column — RREF produces exact values.
- **Infinitely many solutions**: at least one free variable (a column with no pivot).
- **No solution (inconsistent)**: RREF produces a row of the form $\begin{pmatrix}0 & \cdots & 0 & c\end{pmatrix}$ with $c \neq 0$.

## Worked Examples

**Example 1: Unique solution — $x + y = 3$ and $x - y = 1$.**

Form the augmented matrix and row-reduce:

$$\begin{pmatrix}1&1&3\\1&-1&1\end{pmatrix} \xrightarrow{R_2 \leftarrow R_2 - R_1} \begin{pmatrix}1&1&3\\0&-2&-2\end{pmatrix} \xrightarrow{R_2 \leftarrow -R_2/2} \begin{pmatrix}1&1&3\\0&1&1\end{pmatrix}$$

Back-substitute: $y = 1$, then $x = 3 - 1 = 2$. There is exactly one solution because both variables have pivot columns.

---

**Example 2: Infinitely many solutions — $x + 2y = 4$ and $2x + 4y = 8$.**

The second equation is twice the first, so row reduction zeroes it out:

$$\begin{pmatrix}1&2&4\\2&4&8\end{pmatrix} \xrightarrow{R_2 \leftarrow R_2 - 2R_1} \begin{pmatrix}1&2&4\\0&0&0\end{pmatrix}$$

Column 2 has no pivot, so $y$ is free. Set $y = t$. Then $x = 4 - 2t$. For every real number $t$ there is a different solution — infinitely many.

---

**Example 3: No solution — $x + y = 3$ and $x + y = 5$.**

Both equations constrain $x + y$ to different values simultaneously, which is impossible:

$$\begin{pmatrix}1&1&3\\1&1&5\end{pmatrix} \xrightarrow{R_2 \leftarrow R_2 - R_1} \begin{pmatrix}1&1&3\\0&0&2\end{pmatrix}$$

The second row says $0 = 2$, which is false. The system is **inconsistent** — there is no solution.

## Common Mistakes

- **Stopping at row echelon form instead of RREF.** Row echelon form has zeros below pivots; RREF also has zeros above. Only RREF lets you read off values directly without back-substitution.
- **Missing free variables.** When a column in RREF has no pivot, the corresponding variable is free. Skipping it produces an incomplete answer.
- **Declaring a system inconsistent without checking for the $[0 \cdots 0 \mid c]$ pattern.** A row of all zeros on the left side is not inconsistent — it just means a redundant equation.

## Quick Check

Try these before using hints:

1. How many solutions can a linear system have?
2. What does a row $\begin{pmatrix}0 & 0 & 5\end{pmatrix}$ in the augmented RREF mean?
3. Classify: $x + y = 2$, $2x + 2y = 5$.

*(Answers: 0, 1, or infinitely many; inconsistent — no solution; inconsistent since $2(x+y)=4 \neq 5$)*
