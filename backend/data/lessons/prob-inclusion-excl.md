# Inclusion-Exclusion

## Overview

The **inclusion-exclusion principle** computes the probability of a union of events by alternately adding and subtracting intersection probabilities. It prevents double-counting overlapping events.

## Key Idea

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

For three events:

$$P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A\cap B) - P(A\cap C) - P(B\cap C) + P(A\cap B\cap C)$$

## Worked Examples

**Example 1: $P(A) = 0.5$, $P(B) = 0.4$, $P(A\cap B) = 0.2$**

$$P(A \cup B) = 0.5 + 0.4 - 0.2 = 0.7$$

---

**Example 2: What fraction of students passed math or science if 60% passed math, 50% science, 30% both?**

$$P(M \cup S) = 0.6 + 0.5 - 0.3 = 0.8$$

---

**Example 3: Three events, all probabilities given**

$P(A)=P(B)=P(C)=0.4$, all pairwise intersections $= 0.1$, triple intersection $= 0.05$.

$P(A\cup B\cup C) = 1.2 - 0.3 + 0.05 = 0.95$.

## Common Mistakes

- **Forgetting to subtract pairwise intersections.** $P(A)+P(B)$ overcounts $P(A\cap B)$.
- **Sign errors in the three-event formula** (triple intersection is added, not subtracted).

## Quick Check

1. $P(A)=0.6$, $P(B)=0.7$, $P(A\cap B)=0.4$. Find $P(A\cup B)$.
2. If $A$ and $B$ are mutually exclusive, what is $P(A\cup B)$?
3. $P(A\cup B\cup C)$ if all three are mutually exclusive with probs 0.2, 0.3, 0.4.

*(Answers: 0.9; $P(A)+P(B)$; 0.9)*
