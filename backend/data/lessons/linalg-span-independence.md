# Span and Linear Independence

## Overview

The **span** of a set of vectors is the collection of all possible linear combinations of those vectors — it describes every point you can reach by stretching and adding them. A set is **linearly independent** if no vector in it can be expressed as a combination of the others. Independence tells you that no vector is "redundant."

## Key Idea

The set $\{\mathbf{v}_1, \ldots, \mathbf{v}_k\}$ is **linearly independent** if and only if the equation

$$c_1 \mathbf{v}_1 + c_2 \mathbf{v}_2 + \cdots + c_k \mathbf{v}_k = \mathbf{0}$$

has only the **trivial solution** $c_1 = c_2 = \cdots = c_k = 0$. If any nontrivial solution exists, the set is **linearly dependent** and at least one vector is redundant. Equivalently, form the matrix with these vectors as columns — if RREF has a free variable, the set is dependent.

## Worked Examples

**Example 1: Are $(1,0)$ and $(0,1)$ linearly independent?**

Set up $c_1(1,0) + c_2(0,1) = (0,0)$. This gives the system $c_1 = 0$ and $c_2 = 0$ directly — the only solution is the trivial one. These vectors are independent because neither is a multiple of the other; they point in genuinely different directions.

---

**Example 2: Are $(1,2)$ and $(2,4)$ linearly independent?**

Notice that $(2,4) = 2(1,2)$. So $2(1,2) - 1(2,4) = (0,0)$ is a nontrivial solution with $c_1 = 2$, $c_2 = -1$. The set is **linearly dependent** — the second vector carries no new directional information beyond the first.

---

**Example 3: Does $(3,1)$ lie in $\text{span}\{(1,0),(0,1)\}$?**

Ask whether scalars $c_1, c_2$ exist with $c_1(1,0) + c_2(0,1) = (3,1)$. This gives $c_1 = 3$ and $c_2 = 1$ immediately. Yes — $(3,1) = 3(1,0) + 1(0,1)$. Since $(1,0)$ and $(0,1)$ span all of $\mathbb{R}^2$, every vector in $\mathbb{R}^2$ is in their span.

## Common Mistakes

- **Confusing span with independence.** A large set of vectors can span a space even while being dependent — the span tells you what you can reach, independence tells you whether any vectors are wasteful. These are separate questions.
- **Testing only one pair of vectors.** In a set of three or more vectors, you must check whether any vector is a combination of all the others, not just pairwise.
- **Forgetting that more vectors than dimensions always means dependence.** You cannot have more than $n$ linearly independent vectors in $\mathbb{R}^n$. If $k > n$, the set is automatically dependent.

## Quick Check

Try these before using hints:

1. Is $\{(1,2),(3,6)\}$ linearly independent?
2. Does $(5,3)$ lie in $\text{span}\{(1,0),(0,1)\}$?
3. Can 4 vectors in $\mathbb{R}^3$ be linearly independent?

*(Answers: no — $(3,6) = 3(1,2)$; yes — $5(1,0)+3(0,1)$; no — at most 3 independent vectors in $\mathbb{R}^3$)*
