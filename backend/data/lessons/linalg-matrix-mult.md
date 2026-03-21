# Matrix Multiplication

## Overview

**Matrix multiplication** is the core operation of linear algebra. Unlike addition, it is not entry-wise — the $(i,j)$ entry of the product $AB$ comes from the dot product of the $i$-th row of $A$ with the $j$-th column of $B$. This rule encodes the composition of two linear transformations.

## Key Idea

If $A$ is $m \times n$ and $B$ is $n \times p$, then $AB$ is $m \times p$, with:

$$(AB)_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$$

The inner dimensions must match: the number of columns of $A$ must equal the number of rows of $B$. The outer dimensions give the size of the result. Matrix multiplication is associative but **not** commutative — $AB \neq BA$ in general.

## Worked Examples

**Example 1: Multiply $A = \begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}$ and $B = \begin{pmatrix}5 & 6 \\ 7 & 8\end{pmatrix}$.**

Each entry of $AB$ is computed as a row-times-column dot product. For position $(1,1)$: row 1 of $A$ is $(1,2)$, column 1 of $B$ is $(5,7)$, so the product is $1(5)+2(7)=19$:

$$AB = \begin{pmatrix}1(5)+2(7) & 1(6)+2(8) \\ 3(5)+4(7) & 3(6)+4(8)\end{pmatrix} = \begin{pmatrix}19 & 22 \\ 43 & 50\end{pmatrix}$$

---

**Example 2: Multiply a $1\times2$ matrix by a $2\times1$ matrix.**

$A = \begin{pmatrix}1 & 2\end{pmatrix}$ (size $1\times2$) and $B = \begin{pmatrix}3 \\ 4\end{pmatrix}$ (size $2\times1$). Inner dimensions match ($2=2$), so $AB$ is $1\times1$:

$$AB = \begin{pmatrix}1(3) + 2(4)\end{pmatrix} = \begin{pmatrix}11\end{pmatrix}$$

This is exactly the dot product, confirming that matrix multiplication generalizes the dot product.

---

**Example 3: Show that $AB \neq BA$ in general.**

Using $A = \begin{pmatrix}1 & 0 \\ 0 & 0\end{pmatrix}$ and $B = \begin{pmatrix}0 & 1 \\ 0 & 0\end{pmatrix}$:

$$AB = \begin{pmatrix}0 & 1 \\ 0 & 0\end{pmatrix}, \quad BA = \begin{pmatrix}0 & 0 \\ 0 & 0\end{pmatrix}$$

$AB \neq BA$. This matters because it means the order you multiply matrices cannot be swapped arbitrarily.

## Common Mistakes

- **Multiplying entry-wise.** That's Hadamard product, not matrix multiplication. The standard product is row-times-column, not position-times-position.
- **Checking the wrong dimensions.** The condition is columns of $A$ = rows of $B$ (inner dimensions), not rows of $A$ = rows of $B$. A $3\times4$ matrix times a $4\times2$ matrix works; the result is $3\times2$.
- **Assuming $AB = BA$.** Matrix multiplication is not commutative. Even when both products are defined and the same size, they are usually different.

## Quick Check

Try these before using hints:

1. What are the dimensions of $(3\times4) \cdot (4\times2)$?
2. Compute $\begin{pmatrix}1 & 2\end{pmatrix}\begin{pmatrix}3 \\ 4\end{pmatrix}$.
3. Does $AB = BA$ always hold?

*(Answers: $3\times2$; $11$; no — multiplication is not commutative)*
