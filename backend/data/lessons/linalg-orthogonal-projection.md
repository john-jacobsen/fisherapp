# Orthogonal Projection

## Overview

The **orthogonal projection** of a vector $b$ onto a subspace $W$ is the closest point in $W$ to $b$. It decomposes $b$ into a component in $W$ and a component orthogonal to $W$.

## Key Idea

Projection onto a vector $a$:

$$\text{proj}_a b = \frac{a \cdot b}{a \cdot a}\, a$$

Projection onto a subspace with orthonormal basis $\{q_1, \ldots, q_k\}$:

$$\hat{b} = (b \cdot q_1)q_1 + \cdots + (b \cdot q_k)q_k = QQ^T b$$

## Worked Examples

**Example 1: Project $(3, 4)$ onto the direction $(1, 0)$**

$$\text{proj} = \frac{(3)(1)+(4)(0)}{1}(1,0) = (3,0)$$

---

**Example 2: Project $b = (1,1,1)^T$ onto $a = (1,1,0)^T$**

$$\hat{b} = \frac{2}{2}(1,1,0) = (1,1,0)$$

---

**Example 3: Projection matrix**

If $A$ has orthonormal columns, $P = AA^T$ is the projection matrix onto $\text{col}(A)$.

## Common Mistakes

- **Dividing by $\|a\|$ instead of $\|a\|^2$ in the scalar formula.**
- **Projecting onto a non-unit vector and forgetting to normalize.**

## Quick Check

1. Project $(5,2)$ onto $(1,0)$.
2. What is $\|b - \hat{b}\|$ called?
3. Is $P^2 = P$ for a projection matrix?

*(Answers: $(5,0)$; the error; yes (idempotent))*
