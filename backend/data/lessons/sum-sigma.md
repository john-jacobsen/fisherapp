# Sigma Notation

## Overview

**Sigma notation** uses the Greek letter $\Sigma$ (sigma) as shorthand for a sum of many terms. Instead of writing out every term explicitly, you write a formula with an index variable and specify where the index starts and stops. It is precise, compact, and universal in mathematics and statistics.

## Key Idea

The general form is:

$$\sum_{i=m}^{n} a_i = a_m + a_{m+1} + a_{m+2} + \cdots + a_n$$

Three parts control the sum: the **index variable** (here $i$) is a counter that takes each integer value in turn; the **lower bound** $m$ is where it starts; the **upper bound** $n$ is where it stops. The formula $a_i$ tells you what to compute at each value of $i$. The index is a dummy variable — the letter you use does not matter, only what role it plays.

## Worked Examples

**Example 1: Expand and evaluate $\displaystyle\sum_{i=1}^{4} i^2$**

The index $i$ runs from 1 to 4, and the formula is $i^2$. You substitute each value of $i$ and add the results. There is no shortcut here — you simply plug in $i = 1, 2, 3, 4$ one at a time:

$$1^2 + 2^2 + 3^2 + 4^2 = 1 + 4 + 9 + 16 = 30$$

---

**Example 2: Write $3 + 6 + 9 + 12 + 15$ in sigma notation**

Look for the pattern: every term is a multiple of 3. The $k$-th term equals $3k$. The first term corresponds to $k = 1$ and the last to $k = 5$. Because $3k$ generates every term exactly, the compact form is:

$$\sum_{k=1}^{5} 3k$$

You can verify: $k = 1$ gives $3$, $k = 2$ gives $6$, ..., $k = 5$ gives $15$. ✓

---

**Example 3: Evaluate $\displaystyle\sum_{k=0}^{3} 3^k$**

The lower bound is 0, not 1, so there are $3 - 0 + 1 = 4$ terms. The formula $3^k$ is a geometric sequence with ratio 3. Expand by substituting each value:

$$3^0 + 3^1 + 3^2 + 3^3 = 1 + 3 + 9 + 27 = 40$$

The reason you start at $k = 0$ is that $3^0 = 1$ is a valid and meaningful term — never skip the lower bound without thinking about it.

## Common Mistakes

- **Off-by-one errors.** The sum $\sum_{i=1}^{n}$ has exactly $n$ terms, but $\sum_{i=0}^{n}$ has $n + 1$ terms. Always count: upper bound minus lower bound plus one.
- **Confusing the index with the formula.** In $\sum_{i=1}^{5} 2i$, the formula is $2i$ — you substitute $i = 1, 2, 3, 4, 5$ into $2i$, not just count to 5.
- **Treating $\Sigma$ as multiplication.** $\sum_{i=1}^{n} c = cn$ only when $c$ does not depend on $i$. If $c$ depends on $i$, you must evaluate each term separately.

## Quick Check

1. Expand and evaluate $\displaystyle\sum_{i=1}^{3} (2i - 1)$
2. Evaluate $\displaystyle\sum_{k=1}^{4} 2^k$
3. Write $1 + 4 + 9 + 16 + 25$ in sigma notation

*(Answers: $1 + 3 + 5 = 9$; $2 + 4 + 8 + 16 = 30$; $\displaystyle\sum_{i=1}^{5} i^2$)*
