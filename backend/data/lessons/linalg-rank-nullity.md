# Rank-Nullity Theorem

## Overview

The **rank** of a matrix $A$ is the dimension of its column space (= number of pivot columns). The **nullity** is the dimension of the null space (solutions to $Ax = 0$). The Rank-Nullity Theorem links the two.

## Key Idea

For an $m \times n$ matrix $A$:

$$\text{rank}(A) + \text{nullity}(A) = n$$

The null space (kernel) is the set of all $x$ with $Ax = 0$; its dimension is the number of free variables.

## Worked Examples

**Example 1: $A = \begin{pmatrix}1&2&3\\0&1&1\end{pmatrix}$. Find rank and nullity.**

Two pivot columns → rank = 2. $n = 3$. Nullity = 1 (one free variable).

---

**Example 2: Find a basis for the null space of $A$ above.**

From RREF: $x_1 = -x_3$, $x_2 = -x_3$. Free variable $x_3 = t$. Null space = span$\{(-1,-1,1)\}$.

---

**Example 3: $A$ is $4\times6$ with rank 3. What is its nullity?**

$6 - 3 = 3$.

## Common Mistakes

- **Confusing rank with the number of rows.** Rank is the number of pivot rows, which may be less.
- **Computing rank as the number of nonzero rows before row reduction.**

## Quick Check

1. A $3\times5$ matrix has rank 2. What is its nullity?
2. If $A$ is $4\times4$ and has rank 4, what is the nullity?
3. What does nullity 0 imply about $Ax=0$?

*(Answers: 3; 0; only the trivial solution)*
