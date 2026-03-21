# Fundamental Counting Principle

## Overview

The **Fundamental Counting Principle** says that when you make a series of independent choices, the total number of possible outcomes is the product of the number of options at each step. It is the foundation for all combinatorics — permutations, combinations, and beyond all rest on this idea.

## Key Idea

If one task can be completed in $m$ ways and a second independent task can be completed in $n$ ways, then both tasks together can be completed in:

$$m \times n \text{ ways}$$

This extends to any number of steps. If there are $k$ steps with $n_1, n_2, \ldots, n_k$ options respectively:

$$\text{Total outcomes} = n_1 \times n_2 \times \cdots \times n_k$$

Why multiplication and not addition? Because for each of the $m$ choices in the first task, every one of the $n$ choices in the second task is still available. Draw a tree: $m$ branches at the first level, each sprouting $n$ branches — giving $m \times n$ leaf nodes total.

## Worked Examples

**Example 1: How many 2-character codes can you form using letters A–D followed by digits 1–3?**

The first character is a letter: 4 options (A, B, C, D). The second character is a digit: 3 options (1, 2, 3). These choices are independent — whichever letter you pick, all 3 digits are still available. So the total is:

$$4 \times 3 = 12$$

You can verify by listing: A1, A2, A3, B1, B2, B3, C1, C2, C3, D1, D2, D3 — exactly 12.

---

**Example 2: A restaurant offers 3 soups, 5 entrees, and 2 desserts. How many distinct 3-course meals are possible?**

Each course is chosen independently. The number of options at each step does not shrink based on earlier choices. Apply the principle across all three steps:

$$3 \times 5 \times 2 = 30$$

The reason you multiply: for each of the 3 soups, all 5 entrees are available (giving $3 \times 5 = 15$ soup-entree combinations), and for each of those 15, both desserts are available — yielding $15 \times 2 = 30$.

---

**Example 3: How many 7-character license plates consist of 3 letters (A–Z) followed by 4 digits (0–9), with repetition allowed?**

Each of the 3 letter slots has 26 options, and each of the 4 digit slots has 10 options. Because repetition is allowed, picking one letter does not reduce options for the next:

$$26 \times 26 \times 26 \times 10 \times 10 \times 10 \times 10 = 26^3 \times 10^4 = 17{,}576{,}000$$

If repetition were not allowed, the second letter slot would have only 25 options and the third only 24. Always read carefully whether repetition is permitted.

## Common Mistakes

- **Adding instead of multiplying.** Adding $m + n$ counts the options for task A or task B independently. Multiplying $m \times n$ counts the combinations when you do both. Sequential choices require multiplication.
- **Not accounting for whether repetition is allowed.** If repetition is forbidden, the number of options decreases with each step. If allowed, it stays the same. The problem statement always specifies which case applies.
- **Applying the principle to dependent events.** The principle assumes independence — your choice at step 1 does not eliminate options at step 2. If choices are linked (e.g., picking without replacement), you must track the shrinking pool at each step.

## Quick Check

1. You flip a coin and roll a standard 6-sided die. How many outcomes are possible?
2. A store sells 4 colors of shirt, 3 sizes, and 2 fabric types. How many distinct shirts are there?
3. How many 3-digit PINs can you form from digits 0–9 with repetition allowed?

*(Answers: $2 \times 6 = 12$; $4 \times 3 \times 2 = 24$; $10^3 = 1000$)*
