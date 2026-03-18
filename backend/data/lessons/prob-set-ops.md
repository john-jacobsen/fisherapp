# Set Operations

## Overview

Probability events are sets, and the fundamental operations — **union**, **intersection**, and **complement** — correspond to "or", "and", and "not". Mastering these is essential for computing probabilities of compound events.

## Key Idea

For events $A$ and $B$:
- **Union** $A \cup B$: $A$ or $B$ (or both) occurs
- **Intersection** $A \cap B$: both $A$ and $B$ occur
- **Complement** $A^c$: $A$ does not occur

De Morgan's laws: $(A \cup B)^c = A^c \cap B^c$ and $(A \cap B)^c = A^c \cup B^c$.

## Worked Examples

**Example 1: Roll a die. $A = \{\text{even}\}$, $B = \{\text{>3}\}$. Find $A \cup B$ and $A \cap B$.**

$A = \{2,4,6\}$, $B = \{4,5,6\}$. $A \cup B = \{2,4,5,6\}$, $A \cap B = \{4,6\}$.

---

**Example 2: $A^c$ when $A = \{2,4,6\}$ on a die**

$A^c = \{1,3,5\}$ (odd numbers).

---

**Example 3: De Morgan on $A \cup B = \{2,4,5,6\}$**

$(A \cup B)^c = \{1,3\} = \{1,3,5\} \cap \{1,2,3\} = A^c \cap B^c$ ✓

## Common Mistakes

- **Confusing $A \cup B$ with $A \cap B$.** Union is "or"; intersection is "and".
- **Forgetting that $P(A \cup B) \ne P(A) + P(B)$ when they overlap.**

## Quick Check

1. $A = \{1,2\}$, $B = \{2,3\}$. Find $A \cup B$ and $A \cap B$.
2. $A^c$ if $\Omega = \{1,2,3,4\}$ and $A = \{1,2\}$?
3. $(A \cap B)^c = ?$

*(Answers: $\{1,2,3\}$, $\{2\}$; $\{3,4\}$; $A^c \cup B^c$)*
