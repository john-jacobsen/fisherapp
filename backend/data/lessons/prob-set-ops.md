# Set Operations on Events

## Overview

Events are sets, and the three fundamental set operations — **union** ($A \cup B$), **intersection** ($A \cap B$), and **complement** ($A^c$) — translate directly into everyday probability language: "or," "and," and "not." Being fluent with set operations is essential because every compound probability statement is built from these three building blocks. De Morgan's laws connect the operations to each other, letting you rewrite one form in terms of another.

## Key Idea

For events $A$ and $B$ in sample space $\Omega$:

$$A \cup B = \{\omega \in \Omega : \omega \in A \text{ or } \omega \in B\} \qquad \text{("A or B")}$$

$$A \cap B = \{\omega \in \Omega : \omega \in A \text{ and } \omega \in B\} \qquad \text{("A and B")}$$

$$A^c = \{\omega \in \Omega : \omega \notin A\} \qquad \text{("not A")}$$

**De Morgan's laws** (apply complement to a union or intersection by flipping the operation):

$$(A \cup B)^c = A^c \cap B^c \qquad \text{and} \qquad (A \cap B)^c = A^c \cup B^c$$

## Worked Examples

**Example 1: Describe $A \cup B$ in words for a die-roll scenario**

Roll a six-sided die. Let $A$ = "result is even" $= \{2, 4, 6\}$ and $B$ = "result is greater than 3" $= \{4, 5, 6\}$.

The union $A \cup B$ means the outcome is in $A$ or in $B$ or both. You collect all outcomes that appear in either set:

$$A \cup B = \{2, 4, 5, 6\}$$

In words: "the result is even or greater than 3." The outcome 4 and 6 appear in both sets, but you list each outcome only once in the union — a set never has duplicate elements. The outcome 1 appears in neither set, so it is excluded.

---

**Example 2: Find $A \cap B$ for two events on a die**

Using the same $A = \{2, 4, 6\}$ and $B = \{4, 5, 6\}$, the intersection $A \cap B$ contains only outcomes that satisfy both conditions simultaneously — even and greater than 3:

$$A \cap B = \{4, 6\}$$

This makes sense intuitively: 4 and 6 are the only outcomes that are both even and larger than 3. The outcome 2 is even but not greater than 3, so it fails the $B$ condition and is excluded. The outcome 5 is greater than 3 but odd, so it fails the $A$ condition and is also excluded.

---

**Example 3: Apply De Morgan's law to simplify $(A \cap B)^c$**

Continuing with $A = \{2, 4, 6\}$, $B = \{4, 5, 6\}$, and $\Omega = \{1, 2, 3, 4, 5, 6\}$.

De Morgan's second law states $(A \cap B)^c = A^c \cup B^c$. This says "not (both A and B)" is the same as "not A, or not B." To verify:

- $A \cap B = \{4, 6\}$, so $(A \cap B)^c = \{1, 2, 3, 5\}$
- $A^c = \{1, 3, 5\}$ and $B^c = \{1, 2, 3\}$
- $A^c \cup B^c = \{1, 2, 3, 5\}$ ✓

De Morgan's laws are useful when the complement of a union or intersection is easier to compute than the original event, or when you need to push a complement inside a compound expression.

## Common Mistakes

- **Confusing $A \cup B$ with $A \cap B$.** Union ($\cup$) is "or" — an outcome qualifies if it satisfies at least one condition. Intersection ($\cap$) is "and" — an outcome must satisfy both. Mixing them up reverses the condition.
- **Applying De Morgan's law with the wrong operation flip.** The complement of a union becomes an intersection of complements, and vice versa: $(A \cup B)^c = A^c \cap B^c$, not $A^c \cup B^c$. The operation always switches when you distribute the complement.
- **Assuming $P(A \cup B) = P(A) + P(B)$.** This is only true when $A$ and $B$ are mutually exclusive (no overlap). In general you must subtract $P(A \cap B)$ to avoid double-counting outcomes in both sets.

## Quick Check

1. Let $\Omega = \{1, 2, 3, 4, 5, 6\}$, $A = \{1, 2, 3\}$, $B = \{3, 4, 5\}$. Find $A \cup B$ and $A \cap B$.
2. Using the same $A$ and $\Omega$, find $A^c$.
3. Use De Morgan's law to rewrite $(A \cup B)^c$ without the union symbol.

*(Answers: $A \cup B = \{1,2,3,4,5\}$, $A \cap B = \{3\}$; $A^c = \{4,5,6\}$; $(A \cup B)^c = A^c \cap B^c$)*
