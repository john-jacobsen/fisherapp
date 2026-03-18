# Axioms of Probability

## Overview

The **Kolmogorov axioms** provide the mathematical foundation for probability. They define what it means for a function $P$ to be a valid probability measure, and all probability rules follow from them.

## Key Idea

The three axioms:
1. $P(A) \ge 0$ for all events $A$
2. $P(\Omega) = 1$
3. For mutually exclusive events $A_1, A_2, \ldots$: $P(A_1 \cup A_2 \cup \cdots) = \sum P(A_i)$

From these: $P(\emptyset) = 0$, $P(A^c) = 1 - P(A)$, and $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.

## Worked Examples

**Example 1: $P(A^c)$ when $P(A) = 0.3$**

$P(A^c) = 1 - 0.3 = 0.7$.

---

**Example 2: $P(A \cup B)$ when $P(A) = 0.4$, $P(B) = 0.5$, $P(A \cap B) = 0.2$**

$$P(A \cup B) = 0.4 + 0.5 - 0.2 = 0.7$$

---

**Example 3: Verify axiom 3 for a die**

$P(\text{odd or even}) = P(\{1,3,5\}) + P(\{2,4,6\}) = 1/2 + 1/2 = 1 = P(\Omega)$ ✓

## Common Mistakes

- **Adding probabilities without checking mutual exclusivity.** Use inclusion-exclusion when events overlap.
- **Assigning negative probabilities.** Axiom 1 forbids this.

## Quick Check

1. $P(A) = 0.6$. Find $P(A^c)$.
2. $P(A) = 0.3$, $P(B) = 0.5$, disjoint. Find $P(A \cup B)$.
3. Can $P(A) = 1.2$?

*(Answers: 0.4; 0.8; no)*
