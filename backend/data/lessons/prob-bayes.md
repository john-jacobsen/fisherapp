# Bayes' Theorem

## Overview

**Bayes' theorem** inverts a conditional probability. You know $P(B \mid A)$ — how likely you are to observe $B$ if $A$ is true — and you want $P(A \mid B)$ — how likely $A$ is given that you observed $B$. The theorem combines this "forward" probability with a **prior** $P(A)$ (your initial probability for $A$ before seeing any evidence) and a normalizing denominator to produce a **posterior** $P(A \mid B)$ (the updated probability after accounting for the evidence $B$). This update mechanism is the foundation of Bayesian reasoning.

## Key Idea

$$P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}$$

The denominator is computed via the Law of Total Probability. If $A_1, \ldots, A_n$ partition $\Omega$, the full form is:

$$P(A_i \mid B) = \frac{P(B \mid A_i)\,P(A_i)}{\displaystyle\sum_{j=1}^{n} P(B \mid A_j)\,P(A_j)}$$

## Worked Examples

**Example 1: Medical test — find $P(\text{disease} \mid \text{positive})$**

A disease affects 1% of the population. A diagnostic test has 95% sensitivity (it correctly detects disease 95% of the time) and 90% specificity (it correctly gives a negative result 90% of the time in healthy individuals). A randomly selected person tests positive. Find the probability they actually have the disease.

Identify the quantities: $P(D) = 0.01$, $P(D^c) = 0.99$, $P(+ \mid D) = 0.95$, $P(+ \mid D^c) = 1 - 0.90 = 0.10$.

Compute the denominator using total probability:

$$P(+) = P(+ \mid D)\,P(D) + P(+ \mid D^c)\,P(D^c) = (0.95)(0.01) + (0.10)(0.99) = 0.0095 + 0.099 = 0.1085$$

Apply Bayes' theorem:

$$P(D \mid +) = \frac{(0.95)(0.01)}{0.1085} = \frac{0.0095}{0.1085} \approx 0.088$$

Only about 8.8% of positive testers actually have the disease. The low prevalence (1%) means that even with a good test, most positives come from the large pool of healthy people. This counterintuitive result is why understanding the denominator $P(B)$ is critical.

---

**Example 2: Two-box problem**

Box 1 contains 3 red and 2 blue balls. Box 2 contains 1 red and 4 blue balls. You choose a box uniformly at random, then draw one ball. The ball is red. What is the probability it came from Box 1?

From the Law of Total Probability lesson: $P(R) = (3/5)(1/2) + (1/5)(1/2) = 2/5$.

Now apply Bayes' theorem with $A = B_1$ and $B = R$:

$$P(B_1 \mid R) = \frac{P(R \mid B_1)\,P(B_1)}{P(R)} = \frac{(3/5)(1/2)}{2/5} = \frac{3/10}{2/5} = \frac{3}{10} \cdot \frac{5}{2} = \frac{3}{4}$$

Given that the ball is red, there is a 75% chance it came from Box 1. This makes sense: Box 1 has a much higher proportion of red balls, so drawing red is strong evidence for Box 1.

---

**Example 3: Bayes with three hypotheses**

An email is classified as spam, ham, or newsletter with prior probabilities $P(S) = 0.5$, $P(H) = 0.3$, $P(N) = 0.2$. The word "deal" appears with conditional probabilities $P(\text{deal} \mid S) = 0.8$, $P(\text{deal} \mid H) = 0.1$, $P(\text{deal} \mid N) = 0.4$. Given that the email contains "deal," find $P(S \mid \text{deal})$.

Denominator via total probability:

$$P(\text{deal}) = (0.8)(0.5) + (0.1)(0.3) + (0.4)(0.2) = 0.40 + 0.03 + 0.08 = 0.51$$

Apply Bayes':

$$P(S \mid \text{deal}) = \frac{(0.8)(0.5)}{0.51} = \frac{0.40}{0.51} \approx 0.784$$

Seeing the word "deal" pushes the spam probability from 50% to 78%. Each hypothesis gets updated by how well it predicts the observed evidence, scaled by its prior.

## Common Mistakes

- **Confusing $P(A \mid B)$ with $P(B \mid A)$.** This is the classic "prosecutor's fallacy": confusing the probability of a guilty person leaving evidence with the probability of someone who left evidence being guilty. These quantities can differ dramatically.
- **Forgetting to compute $P(B)$ using total probability.** The denominator is not simply $P(B \mid A)$ or $P(A)$. You must sum over all hypotheses: $P(B) = \sum_j P(B \mid A_j) P(A_j)$.
- **Neglecting the prior.** Bayes' theorem requires a prior $P(A)$. If you omit it and treat $P(A \mid B) \approx P(B \mid A)$, you will get wrong answers whenever the prior differs substantially from $1/2$.

## Quick Check

1. $P(A) = 0.4$, $P(B \mid A) = 0.7$, $P(B \mid A^c) = 0.2$. Find $P(A \mid B)$.
2. In the medical test example, what happens to $P(D \mid +)$ if prevalence increases to 10%? (Just describe the direction.)
3. If $P(B \mid A) = P(B)$, what does Bayes' theorem give for $P(A \mid B)$?

*(Answers: $P(B) = 0.7(0.4)+0.2(0.6) = 0.40$, so $P(A|B) = 0.28/0.40 = 0.70$; it increases — higher prevalence means fewer false positives dominate; $P(A \mid B) = P(A)$, i.e., the posterior equals the prior when $A$ and $B$ are independent)*
