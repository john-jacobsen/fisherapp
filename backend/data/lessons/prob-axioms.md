# The Axioms of Probability

## Overview

The three **Kolmogorov axioms** define what any valid probability measure must satisfy. Rather than describing probability as a vague intuition about chance, the axioms pin down exactly which functions $P$ from events to numbers are permissible. Every rule you use in probability — complementation, inclusion-exclusion, conditional probability — is a theorem that follows logically from these three axioms alone. You never need to appeal to intuition to justify a probability identity; you derive it.

## Key Idea

Let $\Omega$ be a sample space and $A, B$ be events (subsets of $\Omega$). A function $P$ is a valid probability measure if and only if it satisfies:

$$\text{Axiom 1:} \quad P(A) \geq 0 \quad \text{for every event } A$$

$$\text{Axiom 2:} \quad P(\Omega) = 1$$

$$\text{Axiom 3:} \quad P(A \cup B) = P(A) + P(B) \quad \text{whenever } A \cap B = \emptyset$$

Axiom 3 extends to any finite (or countably infinite) collection of mutually exclusive events: $P\!\left(\bigcup_i A_i\right) = \sum_i P(A_i)$.

## Worked Examples

**Example 1: Verify a given probability assignment is valid**

Suppose $\Omega = \{a, b, c\}$ and you assign $P(\{a\}) = 0.5$, $P(\{b\}) = 0.3$, $P(\{c\}) = 0.2$.

Check Axiom 1: all three values are non-negative. Check Axiom 2: since $\{a\}$, $\{b\}$, $\{c\}$ are mutually exclusive and their union is $\Omega$, Axiom 3 gives $P(\Omega) = 0.5 + 0.3 + 0.2 = 1.0$ ✓. All three axioms are satisfied, so this is a valid probability measure. Notice that any assignment with non-negative values summing to 1 over the individual outcomes will pass — the axioms do not dictate which specific numbers to use, only what constraints they must obey.

---

**Example 2: Use the axioms to derive $P(\emptyset) = 0$**

The empty set $\emptyset$ and the full sample space $\Omega$ are mutually exclusive: $\emptyset \cap \Omega = \emptyset$. Their union is $\Omega$: $\emptyset \cup \Omega = \Omega$.

Apply Axiom 3 (they are disjoint) and then Axiom 2:

$$P(\Omega) = P(\emptyset \cup \Omega) = P(\emptyset) + P(\Omega) = P(\emptyset) + 1$$

Since $P(\Omega) = 1$ by Axiom 2, subtracting 1 from both sides gives $P(\emptyset) = 0$. This result was not assumed — it was derived. The impossible event has probability zero because the axioms force it.

---

**Example 3: Find $P(A^c)$ given $P(A) = 0.7$**

The event $A$ and its complement $A^c$ are mutually exclusive ($A \cap A^c = \emptyset$) and their union is $\Omega$ ($A \cup A^c = \Omega$). Apply Axiom 3 then Axiom 2:

$$P(A \cup A^c) = P(A) + P(A^c) \implies P(\Omega) = P(A) + P(A^c) \implies 1 = 0.7 + P(A^c)$$

$$P(A^c) = 1 - 0.7 = 0.3$$

The complement rule $P(A^c) = 1 - P(A)$ is not a separate axiom — it is a direct consequence of Axioms 2 and 3. This is the right way to think about every named probability rule: as a derived result, not as something memorized in isolation.

## Common Mistakes

- **Assigning negative probabilities.** Axiom 1 forbids this absolutely. Negative values are mathematically invalid, even if they might seem to "cancel out" in a calculation.
- **Making individual event probabilities sum to something other than 1.** If $\Omega$ is finite with equally likely outcomes and you assign each outcome a probability, those probabilities must sum to exactly 1 by Axioms 2 and 3 together. A common error is using rounded values like $1/3 \approx 0.33$ for three outcomes and ending up with a sum of 0.99.
- **Adding probabilities of overlapping events using Axiom 3 directly.** Axiom 3 only applies to mutually exclusive events. For events that can occur simultaneously, you need inclusion-exclusion.

## Quick Check

1. $P(A) = 0.45$. Find $P(A^c)$.
2. Events $A$ and $B$ are mutually exclusive with $P(A) = 0.3$ and $P(B) = 0.5$. Find $P(A \cup B)$.
3. Is the assignment $P(\{x\}) = 0.6$, $P(\{y\}) = 0.5$ valid for $\Omega = \{x, y\}$? Why or why not?

*(Answers: $0.55$; $0.8$; no — the probabilities sum to $1.1 \neq 1$, violating Axiom 2)*
