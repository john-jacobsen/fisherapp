# Indicator Random Variables

## Overview

An **indicator random variable** $\mathbf{1}_A$ equals 1 if event $A$ occurs and 0 otherwise. This deceptively simple idea is one of the most powerful techniques in probability: it converts counting problems into expectation problems. The key fact is that $E[\mathbf{1}_A] = P(A)$, which means expectation and probability are the same thing when you use indicators correctly.

## Key Idea

The indicator for event $A$ is defined as:

$$\mathbf{1}_A = \begin{cases}1 & \text{if } A \text{ occurs}\0 & \text{otherwise}\end{cases}$$

Its expected value equals the probability of the event:

$$E[\mathbf{1}_A] = 1 \cdot P(A) + 0 \cdot P(A^c) = P(A)$$

The real power comes from decomposing a count $X$ as a sum of indicators, then applying linearity of expectation:

$$X = \mathbf{1}_{A_1} + \mathbf{1}_{A_2} + \cdots + \mathbf{1}_{A_n} \implies E[X] = P(A_1) + P(A_2) + \cdots + P(A_n)$$

This works even when the indicator variables are dependent on each other.

## Worked Examples

**Example 1: Total heads in $n$ flips as a sum of indicators**

Let $X$ be the total number of heads in $n$ fair coin flips. Define $\mathbf{1}_i$ as the indicator that flip $i$ lands heads. Then $X = \mathbf{1}_1 + \mathbf{1}_2 + \cdots + \mathbf{1}_n$.

By linearity of expectation, you can sum the individual expectations even though the flips are independent:

$$E[X] = E[\mathbf{1}_1] + \cdots + E[\mathbf{1}_n] = P(\text{head}) + \cdots + P(\text{head}) = n \cdot \frac{1}{2} = \frac{n}{2}$$

Each indicator contributes exactly $P(\text{head}) = 1/2$. This is why $E[X] = np$ for a binomial — indicators make the derivation transparent.

---

**Example 2: Expected number of matches in a matching problem**

You have $n$ letters and $n$ envelopes; the letters are placed randomly. Let $X$ be the number of letters placed in the correct envelope. Define $\mathbf{1}_i$ as the indicator that letter $i$ goes into the correct envelope.

By symmetry, each letter has probability $1/n$ of landing in the right envelope — there are $n$ envelopes and the assignment is random:

$$P(\mathbf{1}_i = 1) = \frac{1}{n}$$

Even though the indicators are dependent (if one letter is correct, it affects the others), linearity still applies:

$$E[X] = \sum_{i=1}^{n} E[\mathbf{1}_i] = \sum_{i=1}^{n} \frac{1}{n} = 1$$

No matter how many letters there are, the expected number of matches is exactly 1. This is a striking result that would be painful to derive by summing the full distribution.

---

**Example 3: Expected number of sixes in 10 rolls**

Roll a fair die 10 times. Let $X$ count the number of sixes. Define $\mathbf{1}_i = 1$ if roll $i$ shows a 6.

Each roll shows a 6 with probability $1/6$, so $E[\mathbf{1}_i] = 1/6$. Apply linearity:

$$E[X] = \sum_{i=1}^{10} E[\mathbf{1}_i] = 10 \cdot \frac{1}{6} = \frac{10}{6} \approx 1.67$$

The indicator approach sidesteps enumerating the distribution entirely. You just identify one probability per indicator, multiply by how many indicators there are, and sum.

## Common Mistakes

- **Thinking dependence breaks linearity.** $E[X+Y] = E[X]+E[Y]$ always — no independence required. Dependence matters for variance but not for expectation.
- **Using $E[\mathbf{1}_A \mathbf{1}_B] = P(A)P(B)$ when $A$ and $B$ are dependent.** The product of two indicators is itself an indicator: $\mathbf{1}_A \mathbf{1}_B = \mathbf{1}_{A \cap B}$, so $E[\mathbf{1}_A \mathbf{1}_B] = P(A \cap B)$, which only equals $P(A)P(B)$ when $A$ and $B$ are independent.
- **Defining indicators for the wrong event.** Make sure $\mathbf{1}_i$ captures exactly the event you want to count. If you want to count pairs, each indicator should represent one pair, not one element.

## Quick Check

1. You draw 5 cards from a standard deck. Using indicators, find the expected number of aces.
2. Define $\mathbf{1}_A$ for the event that a fair die shows an even number. What is $E[\mathbf{1}_A]$?
3. Letters 1 through 4 are placed randomly in envelopes 1 through 4. What is $E[X]$ where $X$ counts correct placements?

*(Answers: $5 \cdot \frac{4}{52} = \frac{5}{13}$; $E[\mathbf{1}_A] = P(\text{even}) = \frac{1}{2}$; $E[X] = 1$)*
