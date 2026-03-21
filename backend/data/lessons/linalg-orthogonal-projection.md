# Orthogonal Projection

## Overview

The **orthogonal projection** of a vector $\mathbf{b}$ onto a subspace $W$ is the point in $W$ that is closest to $\mathbf{b}$. It decomposes $\mathbf{b}$ into two components: one lying inside $W$ (the projection $\hat{\mathbf{b}}$) and one perpendicular to $W$ (the error $\mathbf{b} - \hat{\mathbf{b}}$). Projection is the geometric foundation of least-squares and Gram-Schmidt.

## Key Idea

**Projection onto a vector $\mathbf{a}$:**

$$\text{proj}_{\mathbf{a}}\,\mathbf{b} = \frac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{a} \cdot \mathbf{a}}\,\mathbf{a}$$

**Projection onto a subspace** with orthonormal basis $\{\mathbf{q}_1, \ldots, \mathbf{q}_k\}$:

$$\hat{\mathbf{b}} = (\mathbf{b}\cdot\mathbf{q}_1)\mathbf{q}_1 + \cdots + (\mathbf{b}\cdot\mathbf{q}_k)\mathbf{q}_k = QQ^T\mathbf{b}$$

The **projection matrix** $P = QQ^T$ satisfies $P^2 = P$ (idempotent) and $P^T = P$ (symmetric). Applying the projection twice gives the same result as applying it once.

## Worked Examples

**Example 1: Project $\mathbf{b} = (3,4)$ onto the direction $\mathbf{a} = (1,0)$.**

The scalar $\frac{\mathbf{a}\cdot\mathbf{b}}{\mathbf{a}\cdot\mathbf{a}}$ captures how far $\mathbf{b}$ extends along $\mathbf{a}$. Here $\mathbf{a}\cdot\mathbf{b} = 3$ and $\mathbf{a}\cdot\mathbf{a} = 1$:

$$\text{proj}_{\mathbf{a}}\,\mathbf{b} = \frac{3}{1}(1,0) = (3,0)$$

The projection is the "shadow" of $(3,4)$ onto the $x$-axis. The error vector is $(3,4)-(3,0) = (0,4)$, which is perpendicular to the $x$-axis ✓.

---

**Example 2: Project $\mathbf{b} = (1,1,1)^T$ onto $\mathbf{a} = (1,1,0)^T$.**

First, compute the scalar: $\mathbf{a}\cdot\mathbf{b} = 1+1+0 = 2$ and $\mathbf{a}\cdot\mathbf{a} = 1+1+0 = 2$.

$$\hat{\mathbf{b}} = \frac{2}{2}(1,1,0)^T = (1,1,0)^T$$

Check: the error is $(1,1,1)-(1,1,0) = (0,0,1)$, and $(0,0,1)\cdot(1,1,0) = 0$ ✓ — perpendicular as required.

---

**Example 3: Verify $P^2 = P$ for the projection matrix onto span$\{(1,0)\}$ in $\mathbb{R}^2$.**

The projection matrix is $P = \mathbf{a}\mathbf{a}^T/(\mathbf{a}\cdot\mathbf{a}) = \begin{pmatrix}1\\0\end{pmatrix}\begin{pmatrix}1&0\end{pmatrix} = \begin{pmatrix}1&0\\0&0\end{pmatrix}$.

Compute $P^2 = \begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}1&0\\0&0\end{pmatrix} = \begin{pmatrix}1&0\\0&0\end{pmatrix} = P$ ✓.

This makes geometric sense: projecting a point that is already in $W$ leaves it unchanged.

## Common Mistakes

- **Dividing by $\|\mathbf{a}\|$ instead of $\|\mathbf{a}\|^2$ in the projection formula.** The denominator is $\mathbf{a}\cdot\mathbf{a} = \|\mathbf{a}\|^2$, not $\|\mathbf{a}\|$. Dividing by the wrong quantity scales the projection incorrectly.
- **Projecting onto a non-unit vector without using the full formula.** If you only compute $(\mathbf{a}\cdot\mathbf{b})\mathbf{a}$, you're missing the $1/(\mathbf{a}\cdot\mathbf{a})$ factor. The full formula is correct for any nonzero $\mathbf{a}$.
- **Forgetting that the error vector must be orthogonal to the subspace.** After computing $\hat{\mathbf{b}}$, always verify that $\mathbf{b}-\hat{\mathbf{b}}$ is orthogonal to the subspace. If it's not, you made an error.

## Quick Check

Try these before using hints:

1. Project $(5,2)$ onto $(1,0)$.
2. What is $\mathbf{b} - \hat{\mathbf{b}}$ called?
3. Does $P^2 = P$ for every projection matrix?

*(Answers: $(5,0)$; the error (or residual); yes — projecting twice gives the same result as projecting once)*
