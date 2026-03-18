# Transpose

## Overview

The **transpose** of a matrix $A$, denoted $A^T$, flips rows and columns: the $(i,j)$ entry of $A^T$ is the $(j,i)$ entry of $A$. A matrix is **symmetric** if $A = A^T$.

## Key Idea

$$(A^T)_{ij} = A_{ji}, \quad (AB)^T = B^T A^T, \quad (A^T)^T = A$$

## Worked Examples

**Example 1: Transpose of $A = \begin{pmatrix}1&2&3\\4&5&6\end{pmatrix}$**

$$A^T = \begin{pmatrix}1&4\\2&5\\3&6\end{pmatrix}$$

---

**Example 2: Is $B = \begin{pmatrix}1&2\\2&3\end{pmatrix}$ symmetric?**

$B^T = B$, so yes.

---

**Example 3: Verify $(AB)^T = B^T A^T$ for simple matrices**

$A = \begin{pmatrix}1&0\\0&2\end{pmatrix}$, $B = \begin{pmatrix}3\\1\end{pmatrix}$. $AB = \begin{pmatrix}3\\2\end{pmatrix}$, $(AB)^T = \begin{pmatrix}3&2\end{pmatrix}$. $B^T A^T = \begin{pmatrix}3&1\end{pmatrix}\begin{pmatrix}1&0\\0&2\end{pmatrix} = \begin{pmatrix}3&2\end{pmatrix}$ ✓

## Common Mistakes

- **Reversing the order in $(AB)^T$:** it is $B^T A^T$, not $A^T B^T$.
- **Thinking all matrices are symmetric.**

## Quick Check

1. Transpose $\begin{pmatrix}1&3\\2&4\end{pmatrix}$.
2. Is $\begin{pmatrix}1&2\\3&1\end{pmatrix}$ symmetric?
3. $(AB)^T = ?$

*(Answers: $\begin{pmatrix}1&2\\3&4\end{pmatrix}$; no ($2\ne3$); $B^T A^T$)*
