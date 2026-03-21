# Nested Sums

## Overview

A **nested sum** (also called a double summation) is a sum inside another sum — one $\Sigma$ appears within the expression being summed by an outer $\Sigma$. They arise naturally when summing over a grid of values, such as all pairs $(i, j)$. The rule for evaluating them is simple: work from the inside out.

## Key Idea

$$\sum_{i=1}^{m}\sum_{j=1}^{n} a_{ij} = \sum_{i=1}^{m}\left(\sum_{j=1}^{n} a_{ij}\right)$$

For each fixed value of $i$, compute the inner sum over all values of $j$. This produces a single number that may depend on $i$. Then the outer sum adds those numbers across all values of $i$.

The reason this works: the inner sum treats $i$ as a constant, so $j$ is the only moving part. Once that sum is finished, $j$ disappears entirely and you are left with a quantity in $i$ alone — which the outer sum then consumes.

## Worked Examples

**Example 1: $\displaystyle\sum_{i=1}^{2}\sum_{j=1}^{3} i$**

The inner sum runs $j$ from 1 to 3, but the formula $i$ does not involve $j$ at all. Adding a constant $i$ exactly 3 times gives $3i$:

$$\sum_{j=1}^{3} i = i + i + i = 3i$$

Now substitute into the outer sum:

$$\sum_{i=1}^{2} 3i = 3(1) + 3(2) = 3 + 6 = 9$$

---

**Example 2: $\displaystyle\sum_{i=1}^{3}\sum_{j=1}^{i} 1$**

Here the upper bound of the inner sum depends on $i$. For each value of $i$, the inner sum adds the constant 1 exactly $i$ times, giving $i$:

$$\sum_{j=1}^{i} 1 = \underbrace{1 + 1 + \cdots + 1}_{i \text{ times}} = i$$

The outer sum is then:

$$\sum_{i=1}^{3} i = 1 + 2 + 3 = 6$$

This example shows why you must evaluate the inner sum for each value of $i$ separately when the bounds are linked — the inner sum produces different results for different $i$.

---

**Example 3: $\displaystyle\sum_{i=1}^{2}\sum_{j=1}^{2} ij$**

This time the formula $ij$ involves both variables. Fix $i$ first and sum over $j$:

- $i = 1$: $\displaystyle\sum_{j=1}^{2} 1 \cdot j = 1 + 2 = 3$
- $i = 2$: $\displaystyle\sum_{j=1}^{2} 2 \cdot j = 2 + 4 = 6$

Add the results across $i$:

$$S = 3 + 6 = 9$$

Notice that $\sum_{j=1}^{2} ij = i \cdot \sum_{j=1}^{2} j = i \cdot 3$, so the outer sum becomes $\sum_{i=1}^{2} 3i = 9$ — same answer, faster work.

## Common Mistakes

- **Evaluating the sums in the wrong order.** Always start with the innermost sum. The outer sum cannot begin until the inner sum has been computed and reduced.
- **Swapping limits when bounds depend on each other.** In Example 2, swapping $i$ and $j$ is not valid because the inner limit $j \leq i$ is not symmetric. You can freely swap independent limits, but linked limits require care.
- **Leaving both indices free.** After the inner sum is evaluated, the index $j$ must disappear. If $j$ still appears in your expression, you have not finished the inner sum.

## Quick Check

1. $\displaystyle\sum_{i=1}^{3}\sum_{j=1}^{2} 1$
2. $\displaystyle\sum_{i=1}^{2}\sum_{j=1}^{3} j$
3. $\displaystyle\sum_{i=1}^{3}\sum_{j=1}^{i} j$

*(Answers: $6$; inner sum $= 1+2+3 = 6$ for each $i$, so $2 \times 6 = 12$; $i=1$: $1$, $i=2$: $3$, $i=3$: $6$, total $= 10$)*
