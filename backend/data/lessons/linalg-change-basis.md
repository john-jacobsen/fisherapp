# Change of Basis

## Overview

**Change of basis** converts the representation of a vector (or transformation) from one basis to another. This is useful when a different basis makes a problem simpler — especially for diagonalization.

## Key Idea

If $B = \{b_1, \ldots, b_n\}$ is a basis and $P = [b_1 \mid \cdots \mid b_n]$ is the change-of-basis matrix (columns are basis vectors), then:

$$[x]_B = P^{-1} x, \quad x = P[x]_B$$

For a transformation $T$ with matrix $A$ (standard) and new basis $P$: the matrix in the new basis is $P^{-1}AP$.

## Worked Examples

**Example 1: Express $(3, 1)$ in the basis $\{(1,1),(1,-1)\}$**

$P = \begin{pmatrix}1&1\\1&-1\end{pmatrix}$. $P^{-1} = \frac{1}{-2}\begin{pmatrix}-1&-1\\-1&1\end{pmatrix}$. $(3,1)$ in new basis: $P^{-1}\begin{pmatrix}3\\1\end{pmatrix} = \begin{pmatrix}2\\1\end{pmatrix}$ (up to scaling).

---

**Example 2: Verify by reconstruction**

$2(1,1) + 1(1,-1) = (2,2) + (1,-1) = (3,1)$ ✓

---

**Example 3: New basis matrix for $A = \begin{pmatrix}3&0\\0&1\end{pmatrix}$ in eigenbasis**

If $A$ is already diagonal, the eigenbasis is the standard basis.

## Common Mistakes

- **Using $P$ instead of $P^{-1}$.** Converting to the new basis uses $P^{-1}$; converting back uses $P$.

## Quick Check

1. $P = \begin{pmatrix}1&0\\0&2\end{pmatrix}$. What is $P^{-1}(2,4)^T$?
2. What does $P^{-1}AP$ represent geometrically?
3. Is change of basis a linear operation?

*(Answers: $(2,2)^T$; $A$ in the new basis; yes)*
