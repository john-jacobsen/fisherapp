# Subspaces and Column Space

## Overview

A **subspace** of $\mathbb{R}^n$ is a subset that is closed under addition and scalar multiplication and contains the zero vector. Subspaces are the "linear" structures inside $\mathbb{R}^n$ — lines, planes, and hyperplanes through the origin. The **column space** of a matrix is the span of its columns, and is one of the most important subspaces you'll encounter.

## Key Idea

A subset $V \subseteq \mathbb{R}^n$ is a subspace if and only if all three conditions hold:

1. $\mathbf{0} \in V$
2. $\mathbf{u}, \mathbf{v} \in V \Rightarrow \mathbf{u} + \mathbf{v} \in V$ (closed under addition)
3. $\mathbf{u} \in V,\ c \in \mathbb{R} \Rightarrow c\mathbf{u} \in V$ (closed under scalar multiplication)

The **column space** $\text{col}(A)$ is the set of all vectors $b$ for which $Ax = b$ has a solution — it equals the span of the columns of $A$.

## Worked Examples

**Example 1: Is $V = \{(x,y) : y = 2x\}$ a subspace of $\mathbb{R}^2$?**

Check all three conditions. First, $(0,0)$ satisfies $y = 2x$ since $0 = 2(0)$. Second, if $(x_1,2x_1)$ and $(x_2,2x_2)$ are in $V$, their sum is $(x_1+x_2, 2(x_1+x_2))$, which also satisfies $y = 2x$. Third, $c(x,2x) = (cx, 2cx)$ satisfies $y = 2x$. All three hold — $V$ is a subspace (a line through the origin).

---

**Example 2: Find the column space of $A = \begin{pmatrix}1 & 2 \\ 3 & 6\end{pmatrix}$.**

The columns are $(1,3)$ and $(2,6)$. But $(2,6) = 2(1,3)$, so the second column adds no new direction. The column space is $\text{span}\{(1,3)\}$ — a single line through the origin. The system $Ax = b$ is solvable only when $b$ lies on this line.

---

**Example 3: Is $W = \{(x,y) : y = 2x + 1\}$ a subspace?**

Check the first condition: does $\mathbf{0} = (0,0)$ belong to $W$? We need $0 = 2(0)+1 = 1$, which is false. The zero vector is not in $W$, so $W$ fails immediately — it is an affine line (translated line) but not a subspace.

## Common Mistakes

- **Forgetting to check that $\mathbf{0}$ is in the set.** This is the quickest test. Any set that doesn't contain the zero vector cannot be a subspace. Planes and lines not passing through the origin fail here.
- **Checking only one closure condition.** You must verify all three. A set can contain zero and be closed under addition but fail under scalar multiplication (e.g., vectors with integer entries).
- **Thinking the column space is just the set of columns.** The column space is the **span** of the columns — all linear combinations, not just the columns themselves.

## Quick Check

Try these before using hints:

1. Is $\{\mathbf{0}\}$ a subspace?
2. Is the set of all vectors in $\mathbb{R}^2$ with non-negative entries a subspace?
3. What is the column space of the $2\times2$ identity matrix?

*(Answers: yes — the trivial subspace; no — not closed under scaling by $-1$; all of $\mathbb{R}^2$)*
