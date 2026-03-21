# Geometric Sequences

## Overview

A **geometric sequence** is a list of numbers in which each term is obtained by multiplying the previous term by the same fixed value, called the **common ratio** $r$. Doubling bacteria counts, halving drug concentrations, and compounding interest all follow geometric sequences. Recognizing this pattern lets you jump straight to any term without listing every one before it.

## Key Idea

$$a_n = a_1 \cdot r^{n-1}$$

Here is why the exponent is $n-1$ rather than $n$. You start at $a_1$ and multiply by $r$ once to reach $a_2$, twice to reach $a_3$, and so on. To reach the $n$th term you have multiplied by $r$ exactly $n-1$ times, giving $a_1 \cdot r^{n-1}$.

The common ratio is $r = \dfrac{a_{n+1}}{a_n}$ — any consecutive pair works because the ratio is constant throughout the sequence.

## Worked Examples

**Example 1: Find the 6th term of $2, 6, 18, 54, \ldots$**

First identify the ratio: $r = 6 \div 2 = 3$. Check: $18 \div 6 = 3$ and $54 \div 18 = 3$. Good, the ratio is constant.

Now apply the formula with $a_1 = 2$, $r = 3$, $n = 6$. The exponent is $6 - 1 = 5$:

$$a_6 = 2 \cdot 3^5 = 2 \times 243 = 486$$

You multiplied by 3 five times starting from 2, which is why you use $3^5$ not $3^6$.

---

**Example 2: The sequence is $5, 10, 20, \ldots$ Find the 8th term.**

The ratio is $r = 10 \div 5 = 2$. Each term doubles. To reach the 8th term, you double 7 times starting from $a_1 = 5$:

$$a_8 = 5 \cdot 2^7 = 5 \times 128 = 640$$

As a sanity check: $a_2 = 10$, $a_3 = 20$, $a_4 = 40$, $a_5 = 80$, $a_6 = 160$, $a_7 = 320$, $a_8 = 640$. The formula gives the same answer without listing all eight terms.

---

**Example 3: Given $a_1 = 3$ and $a_4 = 81$, find the common ratio.**

Use the formula $a_4 = a_1 \cdot r^{4-1}$ and solve for $r$:

$$81 = 3 \cdot r^3 \implies r^3 = \frac{81}{3} = 27 \implies r = \sqrt[3]{27} = 3$$

The ratio is 3. You can verify: $3, 9, 27, 81$ — the fourth term is indeed 81.

## Common Mistakes

- **Writing $r^n$ instead of $r^{n-1}$.** The first term $a_1$ has exponent $0$ — you have made zero multiplications to reach the starting point.
- **Confusing geometric with arithmetic sequences.** Arithmetic sequences add a constant; geometric sequences multiply by a constant. If terms double, triple, or halve, it is geometric.
- **Assuming $r$ must be a whole number.** $r$ can be a fraction (like $1/2$) or even negative, producing alternating signs.

## Quick Check

1. Find $a_5$ for the sequence $1, 3, 9, \ldots$
2. What is the common ratio for $100, 50, 25, \ldots$?
3. Find $a_3$ if $a_1 = 4$ and $r = -2$.

*(Answers: 81; $\frac{1}{2}$; $-16$)*
