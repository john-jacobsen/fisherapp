# Combinations

## Overview

A **combination** is a selection of items from a set where order does not matter. Choosing a 3-person committee from a class of 10 is a combination problem — the group $\{$Alice, Bob, Carol$\}$ is the same committee regardless of the order you list the names. Any time you are simply choosing a subset with no ranking or arrangement, you use combinations.

## Key Idea

$$C(n, r) = \binom{n}{r} = \frac{n!}{r!\,(n-r)!}$$

Here is where this comes from. You already know that $P(n, r) = \frac{n!}{(n-r)!}$ counts ordered arrangements. But when order does not matter, every group of $r$ items gets overcounted — specifically, each group is counted once for each of its $r!$ possible orderings. Dividing by $r!$ removes that overcounting:

$$C(n, r) = \frac{P(n, r)}{r!} = \frac{n!}{r!\,(n-r)!}$$

Dividing by $r!$ is the only difference between permutations and combinations.

## Worked Examples

**Example 1: Compute $\binom{5}{2}$.**

You are choosing 2 items from 5 with no ordering. Start with the falling product for $P(5, 2)$, then divide by $2!$ because the 2 chosen items have $2! = 2$ orderings that all represent the same pair.

$$\binom{5}{2} = \frac{5 \times 4}{2!} = \frac{20}{2} = 10$$

You can verify by listing: $\{1,2\}, \{1,3\}, \{1,4\}, \{1,5\}, \{2,3\}, \{2,4\}, \{2,5\}, \{3,4\}, \{3,5\}, \{4,5\}$ — exactly 10 pairs.

---

**Example 2: A class of 10 students. How many distinct 4-person committees can be formed?**

A committee has no roles — being chosen first or fourth makes no difference. So you divide out the $4! = 24$ orderings of any 4 chosen students.

$$\binom{10}{4} = \frac{10 \times 9 \times 8 \times 7}{4!} = \frac{5{,}040}{24} = 210$$

Compare this to $P(10, 4) = 5{,}040$: committees are 24 times fewer than ranked arrangements of the same size, because every committee of 4 can be listed in $4! = 24$ orders.

---

**Example 3: How many 5-card hands can be dealt from a standard 52-card deck?**

A hand is an unordered set of cards — the order you receive them is irrelevant. You are selecting $r = 5$ from $n = 52$.

$$\binom{52}{5} = \frac{52 \times 51 \times 50 \times 49 \times 48}{5!} = \frac{311{,}875{,}200}{120} = 2{,}598{,}960$$

Over two and a half million possible hands — which is why card games feel unpredictable.

## Common Mistakes

- **Using permutations when order does not matter.** If the problem mentions a committee, a hand, a group, or a selection with no ranks, use combinations.
- **Forgetting the edge cases $\binom{n}{0} = 1$ and $\binom{n}{n} = 1$.** There is exactly one way to choose nothing, and exactly one way to choose everything.
- **Simplifying the fraction incorrectly.** Cancel factors before multiplying to keep numbers small: $\frac{10 \times 9 \times 8 \times 7}{24}$ is easier if you cancel $8 = 24/3$ first.

## Quick Check

1. Compute $\binom{6}{3}$.
2. Compute $\binom{8}{1}$.
3. How many ways can you choose 2 books from a shelf of 7?

*(Answers: 20; 8; 21)*
