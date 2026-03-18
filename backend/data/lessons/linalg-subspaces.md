# Subspaces and Column Space

## Overview

A **subspace** of $\mathbb{R}^n$ is a subset closed under addition and scalar multiplication that contains the zero vector. The **column space** (or range) of a matrix $A$ is the span of its columns.

## Key Idea

A set $V$ is a subspace iff:
1. $\mathbf{0} \in V$
2. $\mathbf{u}, \mathbf{v} \in V \Rightarrow \mathbf{u} + \mathbf{v} \in V$
3. $\mathbf{u} \in V$, $c \in \mathbb{R} \Rightarrow c\mathbf{u} \in V$

The column space of $A$ is the set of all $b$ for which $Ax = b$ has a solution.

## Worked Examples

**Example 1: Is $V = \{(x,y): y = 2x\}$ a subspace of $\mathbb{R}^2$?**

$\mathbf{0} = (0,0)$ satisfies $y=2x$ ✓. Sum of two elements: $(x_1,2x_1)+(x_2,2x_2) = (x_1+x_2, 2(x_1+x_2))$ ✓. Subspace.

---

**Example 2: Column space of $\begin{pmatrix}1&2\\3&6\end{pmatrix}$**

Columns are $(1,3)$ and $(2,6)=2(1,3)$. Column space = span$\{(1,3)\}$, a line through the origin.

---

**Example 3: Is $W = \{(x,y): y = 2x + 1\}$ a subspace?**

$\mathbf{0}$ does not satisfy $y = 2x+1$ ($0 \ne 1$). Not a subspace.

## Common Mistakes

- **Forgetting to check that $\mathbf{0}$ is in the set.** Affine subsets (like planes not through the origin) are not subspaces.

## Quick Check

1. Is $\{\mathbf{0}\}$ a subspace?
2. Is the set of all vectors with non-negative entries a subspace?
3. What is the column space of the identity matrix?

*(Answers: yes; no (not closed under scalar mult by $-1$); all of $\mathbb{R}^n$)*
