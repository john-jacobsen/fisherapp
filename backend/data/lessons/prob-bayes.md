# Bayes' Theorem

## Overview

**Bayes' theorem** inverts conditional probability: it computes $P(A|B)$ from $P(B|A)$, $P(A)$, and $P(B)$. It is the foundation of Bayesian inference.

## Key Idea

$$P(A|B) = \frac{P(B|A)\, P(A)}{P(B)}$$

Combined with the law of total probability:

$$P(A_i | B) = \frac{P(B|A_i)\,P(A_i)}{\sum_j P(B|A_j)\,P(A_j)}$$

## Worked Examples

**Example 1: Medical test. Disease prevalence 1%. Test sensitivity 99%, specificity 95%. $P(\text{disease}|\text{positive})$?**

$P(+|D)=0.99$, $P(+|D^c)=0.05$, $P(D)=0.01$.

$P(+) = 0.99(0.01) + 0.05(0.99) = 0.0594$.

$$P(D|+) = \frac{0.99 \times 0.01}{0.0594} \approx 0.167$$

---

**Example 2: Box problem (from Total Probability lesson)**

$P(B_1|\text{red}) = \frac{P(R|B_1)P(B_1)}{P(R)} = \frac{(3/5)(1/2)}{2/5} = 3/4$.

---

**Example 3: Prior vs. posterior**

$P(A)$ is the **prior** (before observing $B$). $P(A|B)$ is the **posterior** (after). Bayes' theorem updates beliefs.

## Common Mistakes

- **Confusing $P(A|B)$ with $P(B|A)$.** The classic prosecutor's fallacy.
- **Using $P(+)$ without total probability.** Compute $P(B)$ in the denominator carefully.

## Quick Check

1. $P(A)=0.3$, $P(B|A)=0.8$, $P(B)=0.5$. Find $P(A|B)$.
2. What is the denominator in Bayes' theorem?
3. If $P(B|A) = P(B)$, what does that imply about $A$ and $B$?

*(Answers: 0.48; $P(B)$; they are independent)*
