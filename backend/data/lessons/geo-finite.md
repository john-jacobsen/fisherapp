# Finite Geometric Series

## Overview

A **finite geometric series** is the sum of the first $n$ terms of a geometric sequence. Adding every term by hand gets tedious fast — imagine summing 20 terms of a sequence that triples each time. The closed-form formula lets you compute that sum in one step.

## Key Idea

For $n$ terms with first term $a_1$ and common ratio $r \ne 1$:

$$S_n = a_1 \cdot \frac{1 - r^n}{1 - r}$$

If $r = 1$, every term equals $a_1$, so $S_n = n \cdot a_1$.

**Derivation (why it works).** Write the sum twice — the second time multiplied by $r$:

$$S_n = a_1 + a_1 r + a_1 r^2 + \cdots + a_1 r^{n-1}$$
$$r S_n = a_1 r + a_1 r^2 + \cdots + a_1 r^{n-1} + a_1 r^n$$

Subtract the second from the first. Every middle term cancels:

$$S_n - r S_n = a_1 - a_1 r^n$$
$$S_n(1 - r) = a_1(1 - r^n)$$
$$S_n = a_1 \cdot \frac{1 - r^n}{1 - r}$$

This subtraction trick works because the two sums share almost all the same terms, offset by one position.

## Worked Examples

**Example 1: Find the sum of the first 5 terms of $2, 6, 18, 54, \ldots$**

Here $a_1 = 2$, $r = 3$, and $n = 5$. Plug into the formula:

$$S_5 = 2 \cdot \frac{1 - 3^5}{1 - 3} = 2 \cdot \frac{1 - 243}{-2} = 2 \cdot \frac{-242}{-2} = 2 \times 121 = 242$$

The two negatives in the fraction cancel, giving a positive result. You can verify: $2 + 6 + 18 + 54 + 162 = 242$.

---

**Example 2: Sum the series $1 + 2 + 4 + \cdots + 512$.**

First find $n$. The terms are $2^0, 2^1, \ldots, 2^9$, so the last term is $2^9 = 512$ and there are $n = 10$ terms. Here $a_1 = 1$ and $r = 2$:

$$S_{10} = 1 \cdot \frac{1 - 2^{10}}{1 - 2} = \frac{1 - 1{,}024}{-1} = \frac{-1{,}023}{-1} = 1{,}023$$

Counting the number of terms carefully is the key step — go from exponent 0 to exponent 9, which is 10 terms total.

---

**Example 3: Compute $\displaystyle\sum_{k=0}^{4} 3 \cdot (0.5)^k$.**

The sum starts at $k = 0$ with value $3 \cdot (0.5)^0 = 3$, so $a_1 = 3$. The ratio is $r = 0.5$ and there are $n = 5$ terms (from $k = 0$ through $k = 4$):

$$S_5 = 3 \cdot \frac{1 - (0.5)^5}{1 - 0.5} = 3 \cdot \frac{1 - \tfrac{1}{32}}{\tfrac{1}{2}} = 3 \cdot \frac{\tfrac{31}{32}}{\tfrac{1}{2}} = 3 \cdot \frac{31}{16} = \frac{93}{16}$$

Dividing by $\tfrac{1}{2}$ is the same as multiplying by 2, which is why $\tfrac{31}{32} \div \tfrac{1}{2} = \tfrac{31}{16}$.

## Common Mistakes

- **Misidentifying $n$.** Count terms, not the highest index. The sum from $k = 0$ to $k = 4$ has 5 terms, not 4.
- **Applying the infinite series formula when the series is finite.** The formula $\frac{a_1}{1-r}$ is only valid when $n \to \infty$ and $|r| < 1$.
- **Sign errors when $r$ is negative or greater than 1.** Keep the numerator and denominator of $\frac{1-r^n}{1-r}$ together; the formula handles any $r \ne 1$.

## Quick Check

1. Sum the first 4 terms of $1, 2, 4, 8, \ldots$
2. Find $S_6$ for $a_1 = 1$, $r = -1$.
3. Sum $3 + 1.5 + 0.75 + 0.375$.

*(Answers: 15; 0; $\frac{45}{8}$)*
