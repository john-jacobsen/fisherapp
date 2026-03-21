# Permutations

## Overview

A **permutation** is an ordered arrangement of items selected from a larger set. The order matters — placing Alice first and Bob second is a different outcome from placing Bob first and Alice second. Permutations count exactly how many such ordered arrangements exist when you pick $r$ items from $n$ distinct items.

## Key Idea

$$P(n, r) = \frac{n!}{(n-r)!}$$

Here is why the formula works. You have $n$ choices for the first slot. Once that slot is filled, $n-1$ items remain for the second slot. Continuing this way, you have $n-2$ choices for the third slot, down to $n-r+1$ choices for the $r$th slot. Multiply all of those together:

$$n \cdot (n-1) \cdot (n-2) \cdots (n-r+1)$$

This falling product is exactly $\frac{n!}{(n-r)!}$, because dividing $n!$ by $(n-r)!$ cancels all the factors below $n-r+1$.

## Worked Examples

**Example 1: How many ways can 3 books be arranged on a shelf if you choose from 5?**

You have 5 choices for the first position, 4 for the second, and 3 for the third. Each choice is independent, so you multiply.

$$P(5, 3) = \frac{5!}{(5-3)!} = \frac{5!}{2!} = 5 \times 4 \times 3 = 60$$

There are 60 ordered arrangements. Notice how $2!$ in the denominator cancels the factors $2 \times 1$ that you never use.

---

**Example 2: How many 4-digit codes can be formed from the digits 1–9 without repeating any digit?**

You are filling 4 slots from 9 distinct digits, and each slot must hold a different digit. The first slot has 9 options, the second has 8 (one digit is already used), the third has 7, and the fourth has 6.

$$P(9, 4) = \frac{9!}{5!} = 9 \times 8 \times 7 \times 6 = 3{,}024$$

Writing it as a falling product avoids computing all of $9! = 362{,}880$.

---

**Example 3: In a race with 8 runners, how many ways can gold, silver, and bronze be awarded?**

Three distinct medals go to three distinct runners — order matters because first place is not the same as second place. You are choosing $r = 3$ runners from $n = 8$ and assigning them to ranked positions.

$$P(8, 3) = 8 \times 7 \times 6 = 336$$

If order did not matter (say, you were just picking a three-person committee), you would divide by $3! = 6$ to get $56$ — but for medals, every ordering counts separately.

## Common Mistakes

- **Using combinations when order matters.** If the problem involves ranks, positions, passwords, or sequences, you need permutations, not combinations.
- **Computing the full factorial unnecessarily.** Write $P(n, r)$ as the falling product $n(n-1)\cdots(n-r+1)$ to keep arithmetic manageable.
- **Using $r^n$ instead of $P(n, r)$.** Exponent formulas apply when repetition is allowed; $P(n,r)$ applies when each item can only be used once.

## Quick Check

1. Compute $P(6, 2)$.
2. How many ways can 4 people stand in a line?
3. You choose and rank a first and second prize winner from 10 contestants. How many outcomes are possible?

*(Answers: 30; 24; 90)*
