# Rank-Nullity Theorem

## Overview

The **rank** of a matrix is the dimension of its column space — equivalently, the number of pivot columns in RREF. The **nullity** is the dimension of its null space (the set of solutions to $Ax = \mathbf{0}$), which equals the number of free variables. The Rank-Nullity Theorem ties these two quantities together with a clean equation.

## Key Idea

For any $m \times n$ matrix $A$:

$$\text{rank}(A) + \text{nullity}(A) = n$$

Here $n$ is the number of columns. Every column either contributes a pivot (adding to rank) or becomes a free variable (adding to nullity). There is no overlap, so rank and nullity partition all $n$ columns exactly.

## Worked Examples

**Example 1: Find the rank and nullity of $A = \begin{pmatrix}1 & 2 & 3 \\ 0 & 1 & 1\end{pmatrix}$.**

This matrix is already in row echelon form with pivots in columns 1 and 2. So rank $= 2$. By the theorem: nullity $= n - \text{rank} = 3 - 2 = 1$. There is exactly one free variable (column 3).

---

**Example 2: Find a basis for the null space of $A$ above.**

Set up $Ax = \mathbf{0}$ and row-reduce (already done). From RREF: $x_2 = -x_3$ and $x_1 = -2x_2 - 3x_3 = 2x_3 - 3x_3 = -x_3$. Set the free variable $x_3 = t$. Then the null space is:

$$x = t\begin{pmatrix}-1 \\ -1 \\ 1\end{pmatrix}$$

The null space is one-dimensional (consistent with nullity $= 1$), spanned by $(-1,-1,1)$.

---

**Example 3: A $4\times6$ matrix with rank 3. What is its nullity?**

Apply the theorem directly: nullity $= n - \text{rank} = 6 - 3 = 3$. There are 3 free variables and 3 pivot variables. Note that the number of rows ($4$) doesn't appear in the theorem — only the number of columns ($6$) matters.

## Common Mistakes

- **Confusing rank with the number of rows.** Rank is the number of pivot rows after row reduction, which can be less than either the number of rows or columns.
- **Counting nonzero rows before row reduction as the rank.** You must row-reduce first; a nonzero row before reduction might become zero after, or a pivot might not be visible until after elimination.
- **Applying rank-nullity using the number of rows instead of columns.** The theorem says rank $+$ nullity $= n$ (columns), not $m$ (rows). Check your formula before applying it.

## Quick Check

Try these before using hints:

1. A $3\times5$ matrix has rank 2. What is its nullity?
2. If $A$ is $4\times4$ with rank 4, what is its nullity?
3. What does nullity $= 0$ imply about solutions to $Ax = \mathbf{0}$?

*(Answers: $3$; $0$; only the trivial solution $x = \mathbf{0}$)*
