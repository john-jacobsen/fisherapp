# Matrix Addition and Scalar Multiplication

## Overview

A **matrix** is a rectangular array of numbers arranged in rows and columns, written as $m \times n$ (rows by columns). Matrix addition and scalar multiplication are the entry-level operations: they extend familiar arithmetic to arrays. Every more complex matrix operation builds on these two.

## Key Idea

For matrices $A$ and $B$ of the same dimensions, and scalar $c$:

$$(A + B)_{ij} = A_{ij} + B_{ij}, \qquad (cA)_{ij} = c \cdot A_{ij}$$

You can only add matrices of the same dimensions — the size must match exactly. Scalar multiplication scales every entry without exception, which geometrically stretches or compresses the linear transformation that the matrix represents.

## Worked Examples

**Example 1: Add $A = \begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}$ and $B = \begin{pmatrix}5 & -1 \\ 0 & 2\end{pmatrix}$.**

Both matrices are $2 \times 2$, so addition is defined. Add corresponding entries — position $(i,j)$ in the sum comes from positions $(i,j)$ in each matrix:

$$A + B = \begin{pmatrix}1+5 & 2+(-1) \\ 3+0 & 4+2\end{pmatrix} = \begin{pmatrix}6 & 1 \\ 3 & 6\end{pmatrix}$$

The result is still $2 \times 2$.

---

**Example 2: Compute $3A$ for $A = \begin{pmatrix}2 & -1 \\ 0 & 4\end{pmatrix}$.**

Multiply every entry by 3. The scalar distributes across all entries because scalar multiplication represents a uniform stretch of the entire transformation — no entry is exempt:

$$3A = \begin{pmatrix}3(2) & 3(-1) \\ 3(0) & 3(4)\end{pmatrix} = \begin{pmatrix}6 & -3 \\ 0 & 12\end{pmatrix}$$

Note that $3(0) = 0$; zero entries stay zero but the scalar still applies.

---

**Example 3: Compute $2A - B$ for $A = \begin{pmatrix}1 & 3 \\ 2 & 0\end{pmatrix}$ and $B = \begin{pmatrix}4 & 1 \\ -1 & 5\end{pmatrix}$.**

First scale $A$ by 2, then subtract $B$ entry by entry. Subtraction is just addition of $-1$ times $B$, so the same rule applies:

$$2A - B = \begin{pmatrix}2(1)-4 & 2(3)-1 \\ 2(2)-(-1) & 2(0)-5\end{pmatrix} = \begin{pmatrix}-2 & 5 \\ 5 & -5\end{pmatrix}$$

## Common Mistakes

- **Adding matrices of different sizes.** A $2 \times 3$ matrix cannot be added to a $3 \times 2$ matrix even though both contain 6 entries — the dimensions must match exactly.
- **Applying scalar multiplication to only some entries.** The scalar multiplies every entry, including zeros. Students sometimes skip the zero entries, but $c \cdot 0 = 0$ is still required for the operation to be well-defined.
- **Confusing subtraction with absolute value.** $A - B$ subtracts each entry, so the result can be negative. Negative entries in matrices are normal.

## Quick Check

Try these before using hints:

1. Add $\begin{pmatrix}1 & 0 \\ 2 & 3\end{pmatrix} + \begin{pmatrix}0 & 4 \\ -1 & 1\end{pmatrix}$.
2. Compute $-2\begin{pmatrix}3 & -1 \\ 0 & 5\end{pmatrix}$.
3. Can you add a $2\times3$ matrix to a $3\times2$ matrix?

*(Answers: $\begin{pmatrix}1 & 4 \\ 1 & 4\end{pmatrix}$; $\begin{pmatrix}-6 & 2 \\ 0 & -10\end{pmatrix}$; no — dimensions don't match)*
