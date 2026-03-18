# Finite Geometric Series

## Overview

A **finite geometric series** is the sum of a finite number of terms from a geometric sequence. There is a closed-form formula that avoids adding every term individually.

## Key Idea

For $n$ terms with first term $a_1$ and ratio $r \ne 1$:

$$S_n = a_1 \cdot \frac{1 - r^n}{1 - r}$$

If $r = 1$, then $S_n = n \cdot a_1$.

## Worked Examples

**Example 1: Sum the first 5 terms of $2, 6, 18, 54, \ldots$**

$a_1 = 2$, $r = 3$, $n = 5$:

$$S_5 = 2 \cdot \frac{1 - 3^5}{1 - 3} = 2 \cdot \frac{-242}{-2} = 2 \times 121 = 242$$

---

**Example 2: Sum $1 + 2 + 4 + \cdots + 512$**

$r = 2$, $a_1 = 1$. Last term $512 = 2^9$, so $n = 10$:

$$S_{10} = \frac{1 - 2^{10}}{1 - 2} = \frac{-1023}{-1} = 1023$$

---

**Example 3: Find $\sum_{k=0}^{4} 3 \cdot (0.5)^k$**

$a_1 = 3$, $r = 0.5$, $n = 5$:

$$S_5 = 3 \cdot \frac{1 - (0.5)^5}{1 - 0.5} = 3 \cdot \frac{1 - 1/32}{0.5} = 3 \cdot \frac{31/32}{1/2} = 3 \cdot \frac{31}{16} = \frac{93}{16}$$

## Common Mistakes

- **Using the infinite series formula when $|r| \ge 1$.** The infinite formula only converges for $|r| < 1$.
- **Off-by-one in $n$.** Count terms carefully.

## Quick Check

1. Sum the first 4 terms of $1, 2, 4, 8, \ldots$
2. $S_6$ for $a_1=1$, $r=-1$.
3. Sum $3 + 3(0.5) + 3(0.25) + 3(0.125)$.

*(Answers: 15; 0; $45/8$)*
