# Nested Sums

## Overview

A **nested sum** is a double (or higher) summation where one sigma appears inside another. Evaluate the inner sum first for each value of the outer index, then sum those results.

## Key Idea

$$\sum_{i=1}^{m}\sum_{j=1}^{n} a_{ij} = \sum_{i=1}^{m}\left(\sum_{j=1}^{n} a_{ij}\right)$$

You can also exchange the order of summation when limits are independent.

## Worked Examples

**Example 1: $\sum_{i=1}^{2}\sum_{j=1}^{3} i$**

Inner sum (fixed $i$): $\sum_{j=1}^{3} i = 3i$. Outer sum: $3(1) + 3(2) = 9$.

---

**Example 2: $\sum_{i=1}^{3}\sum_{j=1}^{i} 1$**

The inner sum goes to $i$, so it equals $i$. Outer: $1 + 2 + 3 = 6$.

---

**Example 3: $\sum_{i=1}^{2}\sum_{j=1}^{2} ij$**

$i=1$: $1\cdot1 + 1\cdot2 = 3$. $i=2$: $2\cdot1 + 2\cdot2 = 6$. Total: $3 + 6 = 9$.

## Common Mistakes

- **Treating the outer index as constant when evaluating the outer sum.** After evaluating the inner sum, $i$ is free again.
- **Swapping limits incorrectly when bounds depend on each other.**

## Quick Check

1. $\sum_{i=1}^{3}\sum_{j=1}^{2} 1$
2. $\sum_{i=1}^{2}\sum_{j=1}^{3} j$
3. $\sum_{i=1}^{3}\sum_{j=1}^{i} j$

*(Answers: 6; 12; 10)*
