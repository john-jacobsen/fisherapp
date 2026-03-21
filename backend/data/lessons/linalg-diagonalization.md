# Diagonalization

## Overview

A matrix $A$ is **diagonalizable** if it can be written as $A = PDP^{-1}$, where $D$ is diagonal and $P$ is invertible. Diagonalization is possible exactly when $A$ has $n$ linearly independent eigenvectors. It matters because diagonal matrices are easy to work with: powers, exponentials, and other functions become trivial.

## Key Idea

Form $D$ with eigenvalues on the diagonal and $P$ with corresponding eigenvectors as columns (in matching order):

$$A = PDP^{-1}, \qquad D = \begin{pmatrix}\lambda_1 & & \\ & \ddots & \\ & & \lambda_n\end{pmatrix}$$

Then $A^k = PD^kP^{-1}$, and $D^k$ is simply the diagonal entries raised to the $k$-th power — a massive simplification compared to multiplying $A$ by itself $k$ times.

## Worked Examples

**Example 1: Diagonalize $A = \begin{pmatrix}3 & 1 \\ 0 & 2\end{pmatrix}$.**

From the eigenvalue lesson, $\lambda_1 = 3$ with eigenvector $\mathbf{v}_1 = (1,0)$, and $\lambda_2 = 2$ with eigenvector: solve $(A-2I)\mathbf{v} = 0$, giving $\mathbf{v}_2 = (-1,1)$. Place eigenvectors as columns of $P$ in the same order as eigenvalues in $D$:

$$P = \begin{pmatrix}1 & -1 \\ 0 & 1\end{pmatrix}, \quad D = \begin{pmatrix}3 & 0 \\ 0 & 2\end{pmatrix}$$

---

**Example 2: Compute $A^3$ using diagonalization.**

Rather than multiplying $A \cdot A \cdot A$ (tedious), use $A^3 = PD^3P^{-1}$. Since $D$ is diagonal, $D^3$ just cubes each entry:

$$D^3 = \begin{pmatrix}27 & 0 \\ 0 & 8\end{pmatrix}$$

Then multiply $PD^3P^{-1}$. This technique is especially powerful for large powers like $A^{100}$.

---

**Example 3: When is a matrix not diagonalizable?**

$A = \begin{pmatrix}1 & 1 \\ 0 & 1\end{pmatrix}$ has only one eigenvalue $\lambda = 1$ (repeated). Solving $(A - I)\mathbf{v} = 0$ gives only one independent eigenvector $(1,0)$. With only one independent eigenvector for a $2\times2$ matrix, we cannot form an invertible $P$ — the matrix is not diagonalizable. This is a **defective** matrix.

## Common Mistakes

- **Putting eigenvectors as rows of $P$ instead of columns.** The formula requires eigenvectors as columns. Using rows gives a different (wrong) matrix.
- **Mismatching the column order in $P$ with the diagonal order in $D$.** If $\mathbf{v}_1$ corresponds to $\lambda_1$, then $\mathbf{v}_1$ must appear in the column of $P$ that aligns with $\lambda_1$'s position in $D$. Swapping the order makes $PDP^{-1} \neq A$.
- **Assuming a matrix with repeated eigenvalues is not diagonalizable.** Repeated eigenvalues don't automatically prevent diagonalization. The identity matrix $I = I \cdot I \cdot I^{-1}$ is already diagonal, and all its eigenvalues are 1. What matters is whether there are enough independent eigenvectors.

## Quick Check

Try these before using hints:

1. A matrix has distinct eigenvalues 2 and 5. What is $D$?
2. Is the identity matrix $I$ diagonalizable?
3. If $A = PDP^{-1}$, what is $A^2$ in terms of $P$, $D$?

*(Answers: $\text{diag}(2,5)$; yes — $I = I \cdot I \cdot I^{-1}$; $PD^2P^{-1}$)*
