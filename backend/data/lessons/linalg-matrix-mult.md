# Matrix Multiplication

## Overview

**Matrix multiplication** combines two matrices to produce a third. It is not component-wise — the $(i,j)$ entry of the product is the dot product of the $i$-th row of $A$ with the $j$-th column of $B$.

## Key Idea

$(AB)_{ij} = \sum_k A_{ik} B_{kj}$. For $A$ to multiply $B$, the number of columns of $A$ must equal the number of rows of $B$. If $A$ is $m\times n$ and $B$ is $n\times p$, then $AB$ is $m\times p$.

## Worked Examples

**Example 1: $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $B = \begin{pmatrix}5&6\\7&8\end{pmatrix}$. Find $AB$.**

$AB = \begin{pmatrix}1\cdot5+2\cdot7 & 1\cdot6+2\cdot8\\3\cdot5+4\cdot7 & 3\cdot6+4\cdot8\end{pmatrix} = \begin{pmatrix}19&22\\43&50\end{pmatrix}$

---

**Example 2: $A = \begin{pmatrix}1&0\\0&1\end{pmatrix}$, $B = \begin{pmatrix}3&-1\\2&4\end{pmatrix}$. Find $AB$.**

$AB = B$ (identity matrix).

---

**Example 3: Is matrix multiplication commutative?**

No. Even when both $AB$ and $BA$ are defined and the same size, they are generally unequal.

## Common Mistakes

- **Multiplying component-wise.** That's not how matrix multiplication works.
- **Assuming $AB = BA$** — matrix multiplication is not commutative.

## Quick Check

1. Dimensions of $(3\times4)\cdot(4\times2)$?
2. Find $\begin{pmatrix}1&2\end{pmatrix} \begin{pmatrix}3\\4\end{pmatrix}$.
3. Does $AB = BA$ always?

*(Answers: $3\times2$; 11; no)*
