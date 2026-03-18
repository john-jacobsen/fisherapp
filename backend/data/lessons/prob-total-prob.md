# Law of Total Probability

## Overview

The **Law of Total Probability** computes $P(B)$ by partitioning the sample space into mutually exclusive events $A_1, \ldots, A_n$ and summing conditional probabilities.

## Key Idea

If $A_1, \ldots, A_n$ partition $\Omega$ (mutually exclusive and exhaustive):

$$P(B) = \sum_{i=1}^n P(B | A_i)\, P(A_i)$$

## Worked Examples

**Example 1: Two boxes. Box 1 has 3 red, 2 blue. Box 2 has 1 red, 4 blue. Pick a box at random, then a ball. $P(\text{red})$?**

$P(R|B_1) = 3/5$, $P(R|B_2) = 1/5$, $P(B_1) = P(B_2) = 1/2$.

$$P(R) = (3/5)(1/2) + (1/5)(1/2) = 3/10 + 1/10 = 2/5$$

---

**Example 2: Factory defects**

Machine A produces 60% of parts (1% defective). Machine B produces 40% (2% defective). $P(\text{defective}) = 0.01(0.6) + 0.02(0.4) = 0.014$.

---

**Example 3: Weather model**

$P(\text{rain}|\text{cloudy}) = 0.7$, $P(\text{rain}|\text{clear}) = 0.1$. $P(\text{cloudy}) = 0.4$. $P(\text{rain}) = 0.7(0.4) + 0.1(0.6) = 0.34$.

## Common Mistakes

- **Partition not exhaustive or not mutually exclusive.** The $A_i$ must cover all cases exactly once.
- **Mixing up $P(B|A_i)$ and $P(A_i|B)$.**

## Quick Check

1. $P(A_1)=0.4$, $P(A_2)=0.6$, $P(B|A_1)=0.3$, $P(B|A_2)=0.7$. Find $P(B)$.
2. Is the law needed when all $A_i$ have equal probability?
3. How many terms if the partition has 3 events?

*(Answers: 0.54; yes (it still applies); 3)*
