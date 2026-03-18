# Combinations

## Overview

A **combination** is a selection of items where order does **not** matter. Choosing a committee of 3 from 10 people is a combination problem — the group $\{A, B, C\}$ is the same regardless of the order you list them.

## Key Idea

$$C(n, r) = \binom{n}{r} = \frac{n!}{r!\,(n-r)!}$$

Combinations equal permutations divided by $r!$ (the number of orderings of $r$ items we don't care about).

## Worked Examples

**Example 1: $\binom{5}{2}$**

$$\binom{5}{2} = \frac{5!}{2! \cdot 3!} = \frac{20}{2} = 10$$

---

**Example 2: A class of 10. How many committees of 4?**

$$\binom{10}{4} = \frac{10 \cdot 9 \cdot 8 \cdot 7}{4!} = \frac{5040}{24} = 210$$

---

**Example 3: 52-card deck. How many 5-card hands?**

$$\binom{52}{5} = \frac{52 \cdot 51 \cdot 50 \cdot 49 \cdot 48}{120} = 2{,}598{,}960$$

## Common Mistakes

- **Using permutations when order doesn't matter.** Committees and hands use combinations.
- **Forgetting $\binom{n}{0} = \binom{n}{n} = 1$.**

## Quick Check

1. $\binom{6}{3}$
2. $\binom{8}{1}$
3. How many ways to choose 2 from 7?

*(Answers: 20; 8; 21)*
