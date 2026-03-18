# Conditional Probability

## Overview

**Conditional probability** $P(A|B)$ is the probability of $A$ given that $B$ has occurred. It updates probability based on new information by restricting the sample space to $B$.

## Key Idea

$$P(A|B) = \frac{P(A \cap B)}{P(B)} \quad (P(B) > 0)$$

## Worked Examples

**Example 1: Roll a die. $P(\text{even} | \text{>3})$?**

$B = \{4,5,6\}$, $A \cap B = \{4,6\}$. $P = (2/6)/(3/6) = 2/3$.

---

**Example 2: Deck of cards. $P(\text{ace} | \text{red})$?**

$P(\text{ace} \cap \text{red}) = 2/52$. $P(\text{red}) = 26/52$. $P = 2/26 = 1/13$.

---

**Example 3: From a table: $P(A \cap B) = 0.3$, $P(B) = 0.6$. Find $P(A|B)$.**

$P(A|B) = 0.3/0.6 = 0.5$.

## Common Mistakes

- **Confusing $P(A|B)$ with $P(B|A)$.** These are generally different (Bayes' theorem relates them).
- **Applying conditional probability when $P(B) = 0$** — it's undefined.

## Quick Check

1. $P(B|A)$ if $P(A\cap B) = 0.1$ and $P(A) = 0.4$.
2. Two cards drawn. $P(\text{2nd is ace} | \text{1st is ace})$?
3. $P(A|B)$ if $A$ and $B$ are mutually exclusive?

*(Answers: 0.25; 3/51; 0)*
