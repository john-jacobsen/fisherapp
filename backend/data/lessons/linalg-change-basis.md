# Change of Basis

## Overview

Vectors and matrices look different depending on which **basis** you use to describe them. **Change of basis** is the process of converting a vector's coordinates from one basis to another. This is essential for diagonalization, where we change to the eigenbasis to make the transformation look simpler.

## Key Idea

Let $\mathcal{B} = \{\mathbf{b}_1, \ldots, \mathbf{b}_n\}$ be a basis and $P = [\mathbf{b}_1 \mid \cdots \mid \mathbf{b}_n]$ the matrix whose columns are the basis vectors. Then:

$$[\mathbf{x}]_{\mathcal{B}} = P^{-1}\mathbf{x}, \qquad \mathbf{x} = P[\mathbf{x}]_{\mathcal{B}}$$

$P$ converts from $\mathcal{B}$-coordinates to standard coordinates; $P^{-1}$ converts the other way. For a linear transformation with standard matrix $A$, its matrix in the basis $\mathcal{B}$ is $P^{-1}AP$.

## Worked Examples

**Example 1: Express $\mathbf{x} = (3,1)$ in the basis $\mathcal{B} = \{(1,1),(1,-1)\}$.**

Form $P$ with the basis vectors as columns, then solve $P[\mathbf{x}]_{\mathcal{B}} = \mathbf{x}$:

$$P = \begin{pmatrix}1&1\\1&-1\end{pmatrix}, \quad \det(P) = -2, \quad P^{-1} = \frac{1}{-2}\begin{pmatrix}-1&-1\\-1&1\end{pmatrix} = \begin{pmatrix}1/2&1/2\\1/2&-1/2\end{pmatrix}$$

$$[\mathbf{x}]_{\mathcal{B}} = P^{-1}\begin{pmatrix}3\\1\end{pmatrix} = \begin{pmatrix}2\\1\end{pmatrix}$$

This means $\mathbf{x} = 2\mathbf{b}_1 + 1\mathbf{b}_2$.

---

**Example 2: Verify the coordinates from Example 1.**

Reconstruct $\mathbf{x}$ from its $\mathcal{B}$-coordinates. If the answer is right, $2(1,1) + 1(1,-1)$ should equal $(3,1)$:

$$2\begin{pmatrix}1\\1\end{pmatrix} + 1\begin{pmatrix}1\\-1\end{pmatrix} = \begin{pmatrix}2\\2\end{pmatrix} + \begin{pmatrix}1\\-1\end{pmatrix} = \begin{pmatrix}3\\1\end{pmatrix} \checkmark$$

This reconstruction check ($\mathbf{x} = P[\mathbf{x}]_{\mathcal{B}}$) is always a good way to verify change-of-basis computations.

---

**Example 3: Find the matrix of $A = \begin{pmatrix}4&1\\2&3\end{pmatrix}$ in the basis of its eigenvectors.**

The eigenvalues of $A$ are $\lambda_1 = 5$ and $\lambda_2 = 2$, with eigenvectors $(1,1)$ and $(-1,2)$. Set $P = \begin{pmatrix}1&-1\\1&2\end{pmatrix}$. In the eigenbasis, the matrix is diagonal:

$$P^{-1}AP = \begin{pmatrix}5&0\\0&2\end{pmatrix}$$

Diagonal matrices are far easier to work with — this is exactly why change of basis matters.

## Common Mistakes

- **Mixing up $P$ and $P^{-1}$.** To go from standard coordinates to $\mathcal{B}$-coordinates, multiply by $P^{-1}$. To go from $\mathcal{B}$-coordinates back to standard, multiply by $P$. Getting these backwards is the most common error.
- **Putting basis vectors in rows instead of columns.** The change-of-basis matrix $P$ has the basis vectors as its columns, not rows.
- **Forgetting to reverse order for transformations.** The matrix of $T$ in basis $\mathcal{B}$ is $P^{-1}AP$, not $PAP^{-1}$. The $P^{-1}$ goes on the left because it converts input coordinates first.

## Quick Check

Try these before using hints:

1. If $P = \begin{pmatrix}1&0\\0&2\end{pmatrix}$, find $P^{-1}\begin{pmatrix}2\\4\end{pmatrix}$.
2. What does $P^{-1}AP$ represent geometrically?
3. If the columns of $P$ are eigenvectors of $A$, what is $P^{-1}AP$?

*(Answers: $(2,2)^T$; the matrix of $A$ expressed in the basis given by columns of $P$; a diagonal matrix with eigenvalues on the diagonal)*
