# Matrix Addition and Scalar Multiplication

## Overview

**Matrix addition** and **scalar multiplication** are the building blocks of linear algebra. Matrices must have the same dimensions to be added; scalar multiplication scales every entry.

## Key Idea

For matrices $A$ and $B$ of the same size, and scalar $c$:

$$(A + B)_{ij} = A_{ij} + B_{ij}, \quad (cA)_{ij} = c \cdot A_{ij}$$

## Worked Examples

**Example 1: Add $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$ and $B = \begin{pmatrix}5&-1\\0&2\end{pmatrix}$**

$$A + B = \begin{pmatrix}6&1\\3&6\end{pmatrix}$$

---

**Example 2: Compute $3A$ for $A = \begin{pmatrix}1&-1\\2&0\end{pmatrix}$**

$$3A = \begin{pmatrix}3&-3\\6&0\end{pmatrix}$$

---

**Example 3: Compute $2A - B$**

$2A = \begin{pmatrix}2&4\\6&8\end{pmatrix}$. Then $2A - B = \begin{pmatrix}-3&5\\6&6\end{pmatrix}$.

## Common Mistakes

- **Adding matrices of different sizes.** Not defined.
- **Misapplying scalar multiplication** — every single entry gets multiplied.

## Quick Check

1. $\begin{pmatrix}1&2\\3&4\end{pmatrix} + \begin{pmatrix}-1&0\\2&1\end{pmatrix}$
2. $5 \cdot \begin{pmatrix}1&0\\0&1\end{pmatrix}$
3. Can you add a $2\times3$ matrix to a $3\times2$ matrix?

*(Answers: $\begin{pmatrix}0&2\\5&5\end{pmatrix}$; $5I_2$; no)*
