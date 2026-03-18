# Gram-Schmidt Process

## Overview

The **Gram-Schmidt process** converts a set of linearly independent vectors into an orthonormal basis for the same span. It works by successive projection and subtraction.

## Key Idea

Given $\{v_1, v_2, \ldots\}$, construct orthogonal vectors $\{u_1, u_2, \ldots\}$:

$$u_1 = v_1, \quad u_k = v_k - \sum_{j=1}^{k-1} \frac{v_k \cdot u_j}{u_j \cdot u_j}\, u_j$$

Normalize each $u_i$ to get the orthonormal basis $e_i = u_i/\|u_i\|$.

## Worked Examples

**Example 1: $v_1 = (1,1)$, $v_2 = (1,0)$. Apply Gram-Schmidt.**

$u_1 = (1,1)$. Projection of $v_2$ onto $u_1$: $\frac{(1)(1)+(0)(1)}{2}(1,1) = (1/2, 1/2)$.

$u_2 = (1,0) - (1/2,1/2) = (1/2,-1/2)$.

Normalize: $e_1 = (1,1)/\sqrt{2}$, $e_2 = (1,-1)/\sqrt{2}$.

---

**Example 2: Verify orthogonality of result**

$e_1 \cdot e_2 = \frac{1}{2}(1)(1) + \frac{1}{2}(1)(-1) = 0$ ✓

---

**Example 3: Use of QR decomposition**

Gram-Schmidt produces $Q$ (orthonormal columns) and implicitly $R$ (upper triangular), giving $A = QR$.

## Common Mistakes

- **Subtracting projections from the normalized vectors** instead of the unnormalized ones.
- **Normalizing before completing all Gram-Schmidt steps.**

## Quick Check

1. What does Gram-Schmidt produce from a set of independent vectors?
2. After Gram-Schmidt, are the result vectors orthonormal?
3. What is QR decomposition used for?

*(Answers: orthonormal basis for the same span; yes (after normalizing); solving least-squares, numerics)*
