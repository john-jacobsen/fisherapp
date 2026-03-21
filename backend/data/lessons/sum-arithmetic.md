# Arithmetic Series

## Overview

An **arithmetic series** is the sum of the terms of an arithmetic sequence — a sequence where each term increases (or decreases) by a fixed constant $d$ called the common difference. Because the spacing between terms is uniform, there is a clean closed-form formula for the total.

## Key Idea

The insight behind the formula is Gauss's pairing trick: pair the first term with the last, the second with the second-to-last, and so on. Each pair adds to the same value, $a_1 + a_n$. With $n$ terms, you get $n/2$ such pairs. This gives:

$$S_n = \frac{n}{2}(a_1 + a_n)$$

When you know the common difference $d$ but not the last term, substitute $a_n = a_1 + (n-1)d$:

$$S_n = \frac{n}{2}\bigl[2a_1 + (n-1)d\bigr]$$

Both forms are equivalent — choose whichever requires less computation.

## Worked Examples

**Example 1: Sum $1 + 2 + 3 + \cdots + 100$**

This is the classic example. You have $a_1 = 1$, $a_n = 100$, and $n = 100$ terms. The pairing idea: $1 + 100 = 101$, $2 + 99 = 101$, ..., there are 50 such pairs. That gives $50 \times 101$:

$$S_{100} = \frac{100}{2}(1 + 100) = 50 \times 101 = 5050$$

---

**Example 2: Sum the first 10 terms of $3, 7, 11, 15, \ldots$**

Identify the parameters: $a_1 = 3$, $d = 4$, $n = 10$. You need $a_{10}$ to use the first formula. The $n$-th term of an arithmetic sequence is $a_1 + (n-1)d$, so $a_{10} = 3 + 9 \times 4 = 39$.

Now apply the formula. Pairing the first and last: $3 + 39 = 42$, and there are $10/2 = 5$ pairs:

$$S_{10} = \frac{10}{2}(3 + 39) = 5 \times 42 = 210$$

---

**Example 3: Evaluate $\displaystyle\sum_{k=1}^{20}(2k + 1)$**

When $k = 1$: $2(1) + 1 = 3$. When $k = 20$: $2(20) + 1 = 41$. The formula $2k + 1$ is linear in $k$, so consecutive terms differ by a constant $d = 2$ — this is arithmetic with $n = 20$ terms.

Apply the formula directly:

$$S_{20} = \frac{20}{2}(3 + 41) = 10 \times 44 = 440$$

The key step is recognizing that a linear formula in the index always produces an arithmetic sequence.

## Common Mistakes

- **Miscounting the number of terms.** If a series runs from $a_1$ to $a_n$ with step $d$, the number of terms is $n = \frac{a_n - a_1}{d} + 1$, not just $\frac{a_n - a_1}{d}$.
- **Confusing arithmetic and geometric series.** An arithmetic series has a constant difference; a geometric series has a constant ratio. The formulas are completely different.
- **Using $S_n = \frac{n}{2}(a_1 + a_n)$ when $a_n$ is unknown.** You must find $a_n$ first, or switch to the $d$-based formula.

## Quick Check

1. Sum $2 + 4 + 6 + \cdots + 20$
2. Find $S_{12}$ for $a_1 = 5$, $d = 3$
3. Evaluate $\displaystyle\sum_{k=1}^{10}(3k - 1)$

*(Answers: $110$; $\frac{12}{2}(5 + 38) = 258$; $a_1 = 2$, $a_{10} = 29$, $S_{10} = 155$)*
