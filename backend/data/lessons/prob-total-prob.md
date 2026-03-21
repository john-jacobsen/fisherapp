# Law of Total Probability

## Overview

The **Law of Total Probability** computes $P(B)$ by breaking the sample space into disjoint cases, computing the probability of $B$ within each case, and weighting those conditional probabilities by how likely each case is. It is the systematic way to handle situations where you know probabilities within subgroups but need an overall probability. The law is also the engine behind Bayes' theorem — the denominator in Bayes' formula is always computed via total probability.

## Key Idea

If events $A_1, A_2, \ldots, A_n$ form a **partition** of $\Omega$ — mutually exclusive ($A_i \cap A_j = \emptyset$ for $i \neq j$) and exhaustive ($\bigcup_i A_i = \Omega$) — then for any event $B$:

$$P(B) = \sum_{i=1}^{n} P(B \mid A_i)\, P(A_i)$$

Each term $P(B \mid A_i) \cdot P(A_i)$ is the probability that $B$ occurs via the route through $A_i$. Summing over all routes gives the total probability of $B$.

## Worked Examples

**Example 1: Two factories — find the overall defective rate**

A company has two factories. Factory 1 produces 60% of all parts and has a 2% defect rate. Factory 2 produces 40% of parts and has a 5% defect rate. What is the overall probability that a randomly selected part is defective?

The partition is $\{F_1, F_2\}$ — every part comes from exactly one factory. Set up the law:

$$P(D) = P(D \mid F_1)\,P(F_1) + P(D \mid F_2)\,P(F_2)$$

$$P(D) = (0.02)(0.60) + (0.05)(0.40) = 0.012 + 0.020 = 0.032$$

The overall defect rate is 3.2%. This is a weighted average of the two factory rates, weighted by how much each factory contributes. Factory 2's higher defect rate pulls the total above Factory 1's rate alone.

---

**Example 2: Partition into three cases**

A student picks a study strategy at random: 50% of the time they read notes ($R$), 30% of the time they do practice problems ($P$), and 20% of the time they watch videos ($V$). Given each strategy, the probability they pass the quiz is $P(\text{pass} \mid R) = 0.7$, $P(\text{pass} \mid P) = 0.9$, $P(\text{pass} \mid V) = 0.5$. Find $P(\text{pass})$.

The three strategies partition the sample space. Apply the law with three terms:

$$P(\text{pass}) = (0.7)(0.5) + (0.9)(0.3) + (0.5)(0.2)$$

$$= 0.35 + 0.27 + 0.10 = 0.72$$

The student passes 72% of the time overall. Note that the weights $0.5$, $0.3$, and $0.2$ sum to 1 — this is required for a valid partition.

---

**Example 3: Setting up the partition from a word problem**

A bag contains coins of three types: 40% are pennies (1 cent), 35% are nickels (5 cents), and 25% are dimes (10 cents). If you draw a coin at random and flip it (all coins are fair), what is the probability you get heads?

This seems trivial since all coins are fair, but the law of total probability makes the setup explicit. The partition is $\{$penny, nickel, dime$\}$. Since all coins are fair, $P(H \mid \text{any coin}) = 0.5$:

$$P(H) = (0.5)(0.40) + (0.5)(0.35) + (0.5)(0.25) = 0.5(0.40 + 0.35 + 0.25) = 0.5(1) = 0.5$$

As expected, the coin type does not affect the result since all coins are fair. The law correctly reduces to 0.5. This illustrates how the law handles even cases where conditioning doesn't matter.

## Common Mistakes

- **Using a partition that is not exhaustive.** If $A_1, \ldots, A_n$ do not cover all of $\Omega$, the sum $\sum P(B \mid A_i) P(A_i)$ will be less than $P(B)$. Always verify that the partition weights $P(A_i)$ sum to 1.
- **Confusing $P(B \mid A_i)$ with $P(A_i \mid B)$.** These are different. $P(B \mid A_i)$ is the input to the total probability formula; $P(A_i \mid B)$ is what Bayes' theorem computes as output.
- **Creating overlapping cases.** If two partition events can occur simultaneously, the formula double-counts. The $A_i$ must be mutually exclusive — every outcome belongs to exactly one $A_i$.

## Quick Check

1. $P(A_1) = 0.3$, $P(A_2) = 0.7$, $P(B \mid A_1) = 0.4$, $P(B \mid A_2) = 0.8$. Find $P(B)$.
2. The partition weights are $0.2$, $0.5$, and $0.3$. Do they form a valid partition?
3. If $P(B \mid A_i) = c$ (a constant) for all $i$, what is $P(B)$?

*(Answers: $(0.4)(0.3) + (0.8)(0.7) = 0.12 + 0.56 = 0.68$; yes, they sum to 1.0; $P(B) = c$)*
