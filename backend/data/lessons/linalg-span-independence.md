# Span and Linear Independence

## Overview

The **span** of a set of vectors is the set of all linear combinations. Vectors are **linearly independent** if no vector in the set can be written as a linear combination of the others.

## Key Idea

$\{\mathbf{v}_1, \ldots, \mathbf{v}_k\}$ is linearly independent iff the only solution to $c_1 \mathbf{v}_1 + \cdots + c_k \mathbf{v}_k = \mathbf{0}$ is $c_1 = \cdots = c_k = 0$.

Equivalently, they are independent iff the matrix with these as columns has full column rank.

## Worked Examples

**Example 1: Are $(1,0)$ and $(0,1)$ linearly independent?**

$c_1(1,0) + c_2(0,1) = (0,0) \Rightarrow c_1 = c_2 = 0$. Yes.

---

**Example 2: Are $(1,2)$ and $(2,4)$ linearly independent?**

$(2,4) = 2(1,2)$, so they are **dependent**.

---

**Example 3: Does $(3,1)$ lie in span$\{(1,0),(0,1)\}$?**

$(3,1) = 3(1,0) + 1(0,1)$. Yes.

## Common Mistakes

- **Confusing span with independence.** A large set can span a space but still contain dependent vectors.
- **Testing only one combination.** Linear independence requires the zero combination to be the only one.

## Quick Check

1. Is $\{(1,2),(3,6)\}$ linearly independent?
2. Does $(5,3)$ lie in span$\{(1,0),(0,1)\}$?
3. If $k > n$, can $k$ vectors in $\mathbb{R}^n$ be independent?

*(Answers: no; yes; no)*
