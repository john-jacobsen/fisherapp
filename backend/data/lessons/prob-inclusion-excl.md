# Inclusion-Exclusion

## Overview

The **inclusion-exclusion principle** corrects for double-counting when you add probabilities of overlapping events. When two events share outcomes, simply adding $P(A) + P(B)$ counts the outcomes in $A \cap B$ twice. You fix this by subtracting $P(A \cap B)$ once. The same logic extends to three or more events: you add all singletons, subtract all pairwise intersections, add back all triple intersections, and so on — alternating signs to achieve an exact count.

## Key Idea

For two events:

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

For three events:

$$P(A \cup B \cup C) = P(A)+P(B)+P(C) - P(A\cap B) - P(A\cap C) - P(B\cap C) + P(A\cap B\cap C)$$

When $A$ and $B$ are **mutually exclusive** (disjoint), $P(A \cap B) = 0$ and the formula reduces to $P(A \cup B) = P(A) + P(B)$, which is just Axiom 3.

## Worked Examples

**Example 1: Two overlapping events**

Suppose $P(A) = 0.5$, $P(B) = 0.4$, and $P(A \cap B) = 0.2$. Find $P(A \cup B)$.

The overlap region $A \cap B$ gets counted once when you add $P(A)$ and again when you add $P(B)$. Subtracting $P(A \cap B)$ removes that extra count, leaving each outcome counted exactly once:

$$P(A \cup B) = 0.5 + 0.4 - 0.2 = 0.7$$

You can verify this makes sense: the union cannot be larger than 1, and it must be at least as large as either individual event, so $0.7$ is plausible.

---

**Example 2: Find $P(A \cap B)$ given the union and marginals**

Suppose you know $P(A) = 0.6$, $P(B) = 0.5$, and $P(A \cup B) = 0.8$. Find $P(A \cap B)$.

Rearrange the inclusion-exclusion formula to isolate the intersection:

$$P(A \cap B) = P(A) + P(B) - P(A \cup B) = 0.6 + 0.5 - 0.8 = 0.3$$

This shows that inclusion-exclusion is not just a one-directional formula. Whenever three of the four quantities $P(A)$, $P(B)$, $P(A \cap B)$, $P(A \cup B)$ are known, you can solve for the fourth by rearranging.

---

**Example 3: Three events**

Three events $A$, $B$, $C$ have $P(A) = P(B) = P(C) = 0.4$, all pairwise intersections equal $0.1$, and the triple intersection $P(A \cap B \cap C) = 0.02$. Find $P(A \cup B \cup C)$.

Apply the three-event formula, grouping the terms by sign:

$$P(A \cup B \cup C) = (0.4 + 0.4 + 0.4) - (0.1 + 0.1 + 0.1) + 0.02$$

$$= 1.2 - 0.3 + 0.02 = 0.92$$

The triple intersection is added back because it was subtracted three times (once in each pairwise term) but should be counted exactly once, so two of those subtractions must be undone — adding it back once achieves that.

## Common Mistakes

- **Forgetting to subtract the intersection.** Writing $P(A \cup B) = P(A) + P(B)$ when $A$ and $B$ overlap counts the shared outcomes twice. Always check whether the events can occur simultaneously before deciding $P(A \cap B) = 0$.
- **Getting the sign wrong on the triple intersection.** In the three-event formula, the triple intersection $P(A \cap B \cap C)$ is added (positive sign), not subtracted. A sign error here will push the result above 1 or below 0, which is an immediate signal something is wrong.
- **Applying inclusion-exclusion to conditional probabilities without care.** The formula holds for ordinary probabilities. When working with conditional probabilities, each term must be conditioned on the same event.

## Quick Check

1. $P(A) = 0.7$, $P(B) = 0.6$, $P(A \cap B) = 0.4$. Find $P(A \cup B)$.
2. $P(A) = 0.5$, $P(B) = 0.4$, $P(A \cup B) = 0.7$. Find $P(A \cap B)$.
3. Events $A$, $B$, $C$ are mutually exclusive with $P(A) = 0.2$, $P(B) = 0.3$, $P(C) = 0.4$. Find $P(A \cup B \cup C)$.

*(Answers: $0.9$; $0.2$; $0.9$)*
