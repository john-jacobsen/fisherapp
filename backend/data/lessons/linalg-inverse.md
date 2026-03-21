# Matrix Inverse

## Overview

The **inverse** of a square matrix $A$ is the matrix $A^{-1}$ satisfying $A A^{-1} = A^{-1} A = I$, where $I$ is the identity matrix. The inverse exists if and only if $\det(A) \neq 0$. Geometrically, $A^{-1}$ is the transformation that exactly undoes what $A$ does.

## Key Idea

For a $2\times2$ matrix $A = \begin{pmatrix}a & b \\ c & d\end{pmatrix}$:

$$A^{-1} = \frac{1}{\det(A)}\begin{pmatrix}d & -b \\ -c & a\end{pmatrix}$$

For larger matrices, use row reduction on the augmented matrix $[A \mid I]$. When you reduce the left block to $I$, the right block becomes $A^{-1}$. This works because every row operation applied to $A$ to produce $I$ is also applied to $I$ to build $A^{-1}$.

## Worked Examples

**Example 1: Find the inverse of $A = \begin{pmatrix}2 & 1 \\ 5 & 3\end{pmatrix}$.**

First compute $\det(A) = 2(3) - 1(5) = 1$. Since $\det \neq 0$, the inverse exists. Apply the formula, swapping the diagonal and negating the off-diagonal:

$$A^{-1} = \frac{1}{1}\begin{pmatrix}3 & -1 \\ -5 & 2\end{pmatrix} = \begin{pmatrix}3 & -1 \\ -5 & 2\end{pmatrix}$$

---

**Example 2: Verify $AA^{-1} = I$.**

Multiply to confirm the inverse is correct — this is the only reliable check:

$$\begin{pmatrix}2 & 1 \\ 5 & 3\end{pmatrix}\begin{pmatrix}3 & -1 \\ -5 & 2\end{pmatrix} = \begin{pmatrix}6-5 & -2+2 \\ 15-15 & -5+6\end{pmatrix} = \begin{pmatrix}1 & 0 \\ 0 & 1\end{pmatrix} = I \checkmark$$

---

**Example 3: Solve $Ax = b$ using the inverse.**

For $b = \begin{pmatrix}4 \\ 11\end{pmatrix}$ and $A$ from Example 1, the solution is $x = A^{-1}b$ — this works because multiplying both sides of $Ax = b$ on the left by $A^{-1}$ gives $x = A^{-1}b$:

$$x = \begin{pmatrix}3 & -1 \\ -5 & 2\end{pmatrix}\begin{pmatrix}4 \\ 11\end{pmatrix} = \begin{pmatrix}12-11 \\ -20+22\end{pmatrix} = \begin{pmatrix}1 \\ 2\end{pmatrix}$$

## Common Mistakes

- **Attempting to invert a singular matrix.** If $\det(A) = 0$, no inverse exists. Trying to apply the $2\times2$ formula when $\det = 0$ causes division by zero.
- **Writing $(AB)^{-1} = A^{-1}B^{-1}$.** The correct formula is $(AB)^{-1} = B^{-1}A^{-1}$ — the order reverses, just like with transposes. This is because $(B^{-1}A^{-1})(AB) = B^{-1}(A^{-1}A)B = B^{-1}IB = I$.
- **Confusing $A^{-1}$ with $1/A$.** There is no such thing as element-wise division for matrices. The inverse is a whole matrix, found through row reduction or the formula, not by dividing entries.

## Quick Check

Try these before using hints:

1. Find the inverse of $\begin{pmatrix}1 & 2 \\ 0 & 1\end{pmatrix}$.
2. Is $\begin{pmatrix}1 & 2 \\ 2 & 4\end{pmatrix}$ invertible?
3. What is $(AB)^{-1}$?

*(Answers: $\begin{pmatrix}1 & -2 \\ 0 & 1\end{pmatrix}$; no, since $\det = 0$; $B^{-1}A^{-1}$)*
