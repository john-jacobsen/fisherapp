# Gram-Schmidt Process

## Overview

The **Gram-Schmidt process** converts any set of linearly independent vectors into an **orthonormal basis** for the same span. The idea is sequential: at each step, subtract off the component of the new vector that is parallel to all previous ones, leaving only the perpendicular part. This produces an orthogonal set, which you then normalize.

## Key Idea

Given linearly independent vectors $\{\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_k\}$, construct orthogonal vectors $\{\mathbf{u}_1, \mathbf{u}_2, \ldots, \mathbf{u}_k\}$ by:

$$\mathbf{u}_1 = \mathbf{v}_1, \qquad \mathbf{u}_j = \mathbf{v}_j - \sum_{i=1}^{j-1} \frac{\mathbf{v}_j \cdot \mathbf{u}_i}{\mathbf{u}_i \cdot \mathbf{u}_i}\,\mathbf{u}_i$$

Each term in the sum is the projection of $\mathbf{v}_j$ onto $\mathbf{u}_i$. Subtracting all these projections removes everything parallel to the earlier vectors. Normalize at the end: $\mathbf{e}_j = \mathbf{u}_j / \|\mathbf{u}_j\|$.

## Worked Examples

**Example 1: Apply Gram-Schmidt to $\mathbf{v}_1 = (1,1)$ and $\mathbf{v}_2 = (1,0)$.**

Start: $\mathbf{u}_1 = \mathbf{v}_1 = (1,1)$.

For $\mathbf{u}_2$, subtract the projection of $\mathbf{v}_2$ onto $\mathbf{u}_1$. The projection scalar is $\frac{\mathbf{v}_2 \cdot \mathbf{u}_1}{\mathbf{u}_1 \cdot \mathbf{u}_1} = \frac{1}{2}$:

$$\mathbf{u}_2 = (1,0) - \frac{1}{2}(1,1) = \left(\frac{1}{2}, -\frac{1}{2}\right)$$

Normalize: $\mathbf{e}_1 = \frac{1}{\sqrt{2}}(1,1)$, $\mathbf{e}_2 = \frac{1}{\sqrt{2}}(1,-1)$.

---

**Example 2: Verify orthogonality of the result.**

Two vectors are orthogonal iff their dot product is zero. Check $\mathbf{e}_1 \cdot \mathbf{e}_2$:

$$\mathbf{e}_1 \cdot \mathbf{e}_2 = \frac{1}{\sqrt{2}} \cdot \frac{1}{\sqrt{2}}\bigl[(1)(1)+(1)(-1)\bigr] = \frac{1}{2}(0) = 0 \checkmark$$

Also verify unit length: $\|\mathbf{e}_1\|^2 = \frac{1}{2}(1+1) = 1$ ✓

---

**Example 3: Gram-Schmidt gives QR decomposition.**

When you apply Gram-Schmidt to the columns of a matrix $A$, you implicitly produce $A = QR$, where $Q$ has the orthonormal basis vectors as columns and $R$ is upper triangular. $R$ records the projection coefficients used in each step. The $QR$ decomposition is used for numerically stable least-squares solving and eigenvalue algorithms.

## Common Mistakes

- **Subtracting projections from the already-normalized vectors instead of the intermediate $\mathbf{u}_j$.** Do all Gram-Schmidt steps using the unnormalized vectors, then normalize at the end. Normalizing mid-process can be done but changes the projection formula.
- **Computing the projection scalar as $\mathbf{v}\cdot\mathbf{u}$ instead of $\frac{\mathbf{v}\cdot\mathbf{u}}{\mathbf{u}\cdot\mathbf{u}}$.** You must divide by $\|\mathbf{u}\|^2$ to get the correct scalar for projecting onto a non-unit vector.
- **Applying Gram-Schmidt to a linearly dependent set.** If the set is dependent, one step will produce $\mathbf{u}_j = \mathbf{0}$, which cannot be normalized. Gram-Schmidt requires linear independence as input.

## Quick Check

Try these before using hints:

1. What does Gram-Schmidt produce from linearly independent vectors?
2. After normalizing the outputs, what property do they have?
3. What matrix factorization does Gram-Schmidt produce?

*(Answers: an orthogonal set spanning the same space; orthonormal — pairwise orthogonal with unit length; QR decomposition)*
