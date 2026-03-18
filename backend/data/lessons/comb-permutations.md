# Permutations

## Overview

A **permutation** is an ordered arrangement of items. The order matters — "ABC" and "BAC" are different permutations. Permutations count the number of ways to select and arrange $r$ items from $n$ distinct items.

## Key Idea

$$P(n, r) = \frac{n!}{(n-r)!}$$

If you arrange all $n$ items, the count is simply $n!$ (n factorial).

## Worked Examples

**Example 1: How many ways to arrange 3 books chosen from 5?**

$$P(5, 3) = \frac{5!}{2!} = \frac{120}{2} = 60$$

---

**Example 2: How many 4-digit codes using digits 1–9 without repetition?**

$$P(9, 4) = \frac{9!}{5!} = 9 \times 8 \times 7 \times 6 = 3024$$

---

**Example 3: A race with 8 runners. In how many ways can 1st, 2nd, 3rd be assigned?**

$$P(8, 3) = 8 \times 7 \times 6 = 336$$

## Common Mistakes

- **Using combinations when order matters.** Gold/Silver/Bronze is not the same as a committee.
- **Computing $n!$ when you only need $n!/(n-r)!$.** Write it as a falling product: $n(n-1)\cdots(n-r+1)$.

## Quick Check

1. $P(6, 2)$
2. Arrange 4 people in a line: how many ways?
3. Choose and rank 2 winners from 10 contestants.

*(Answers: 30; 24; 90)*
