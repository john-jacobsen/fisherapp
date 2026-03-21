# Transpose

## Overview

The **transpose** of a matrix $A$, written $A^T$, is formed by flipping rows and columns: the $(i,j)$ entry of $A$ becomes the $(j,i)$ entry of $A^T$. If $A$ is $m \times n$, then $A^T$ is $n \times m$. A matrix is called **symmetric** if $A = A^T$, meaning it's unchanged under transposition.

## Key Idea

The transpose satisfies three key properties:

$$(A^T)^T = A, \qquad (A + B)^T = A^T + B^T, \qquad (AB)^T = B^T A^T$$

The third identity — the reversal rule — is the most important and most frequently misapplied. The order flips because transposing a product swaps the role of rows and columns in both factors.

## Worked Examples

**Example 1: Transpose $A = \begin{pmatrix}1 & 2 & 3 \\ 4 & 5 & 6\end{pmatrix}$.**

$A$ is $2 \times 3$. To transpose, write the rows of $A$ as columns of $A^T$. The first row $(1,2,3)$ becomes the first column:

$$A^T = \begin{pmatrix}1 & 4 \\ 2 & 5 \\ 3 & 6\end{pmatrix}$$

The result is $3 \times 2$, confirming that transposing swaps the dimensions.

---

**Example 2: Check whether $B = \begin{pmatrix}1 & 2 \\ 2 & 5\end{pmatrix}$ is symmetric.**

Compare $B$ to $B^T$. The $(1,2)$ entry of $B$ is 2 and the $(2,1)$ entry is also 2, so $B_{ij} = B_{ji}$ for all positions:

$$B^T = \begin{pmatrix}1 & 2 \\ 2 & 5\end{pmatrix} = B$$

Yes, $B$ is symmetric. For a matrix to be symmetric it must be square and the entries must mirror across the main diagonal.

---

**Example 3: Verify $(AB)^T = B^T A^T$ for $A = \begin{pmatrix}1 & 2\end{pmatrix}$ and $B = \begin{pmatrix}3 \\ 1\end{pmatrix}$.**

Compute $AB$ first: $AB = \begin{pmatrix}5\end{pmatrix}$ (a $1\times1$ matrix), so $(AB)^T = \begin{pmatrix}5\end{pmatrix}$.

Now compute $B^T A^T = \begin{pmatrix}3 & 1\end{pmatrix}\begin{pmatrix}1 \\ 2\end{pmatrix} = \begin{pmatrix}5\end{pmatrix}$.

Both equal $5$ — the reversal rule holds. The order must flip because when you transpose a product, the row structure and column structure of the factors swap roles.

## Common Mistakes

- **Writing $(AB)^T = A^T B^T$.** This is wrong. The correct formula is $B^T A^T$ — the order reverses. Think of it like reversing shoes when dressing: you put on socks then shoes, but you take off shoes then socks.
- **Assuming all square matrices are symmetric.** The matrix $\begin{pmatrix}1 & 3 \\ 7 & 1\end{pmatrix}$ is square but not symmetric because $3 \neq 7$.
- **Forgetting that transposing changes the dimensions.** If you need $A^T$ for a multiplication, double-check that the new dimensions are compatible.

## Quick Check

Try these before using hints:

1. Transpose $\begin{pmatrix}1 & 3 \\ 2 & 4\end{pmatrix}$.
2. Is $\begin{pmatrix}1 & 2 \\ 3 & 1\end{pmatrix}$ symmetric?
3. If $A$ is $3\times2$, what size is $A^T$?

*(Answers: $\begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}$; no (since $2 \neq 3$); $2\times3$)*
