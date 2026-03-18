# Independence

## Overview

Events $A$ and $B$ are **independent** if knowing that $B$ occurred does not change the probability of $A$. Independence is a specific mathematical condition, not just intuitive lack of connection.

## Key Idea

$A$ and $B$ are independent iff:

$$P(A \cap B) = P(A) \cdot P(B)$$

Equivalently, $P(A|B) = P(A)$ (when $P(B) > 0$). For multiple events, pairwise independence does NOT imply mutual independence.

## Worked Examples

**Example 1: Flip two fair coins. Are "first is H" and "second is H" independent?**

$P(\text{both H}) = 1/4 = (1/2)(1/2)$. Yes, independent.

---

**Example 2: Roll a die. $A = \{\text{even}\}$, $B = \{1,2,3,4\}$. Independent?**

$P(A) = 1/2$, $P(B) = 2/3$, $P(A\cap B) = P(\{2,4\}) = 1/3 = (1/2)(2/3)$. Yes.

---

**Example 3: $P(A) = 0.6$, $P(B) = 0.4$, $P(A\cap B) = 0.3$. Independent?**

$P(A)P(B) = 0.24 \ne 0.3$. Not independent.

## Common Mistakes

- **Confusing mutually exclusive with independent.** If $P(A),P(B)>0$, they can't be both mutually exclusive AND independent.
- **Assuming independence from context** without verification.

## Quick Check

1. $P(A)=0.3$, $P(B)=0.5$. If independent, $P(A\cap B)$?
2. Are mutually exclusive events (with positive probability) independent?
3. $P(A\cap B) = P(A)P(B)$ is the definition of what?

*(Answers: 0.15; no; independence)*
