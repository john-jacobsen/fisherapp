# Conditional Probability

## Overview

**Conditional probability** $P(A \mid B)$ is the probability that $A$ occurs given that $B$ has already occurred. When you learn that $B$ happened, you restrict your sample space to outcomes inside $B$ — only those matter now. Within that restricted space, you ask how much of it is also covered by $A$. The result is a probability that reflects the updated information. Conditional probability is the mathematical mechanism for incorporating evidence.

## Key Idea

The conditional probability of $A$ given $B$ is defined as:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(B) > 0$$

Rearranged, this gives the **multiplication rule**:

$$P(A \cap B) = P(A \mid B) \cdot P(B)$$

The multiplication rule is how you compute joint probabilities when you know a conditional probability and a marginal probability.

## Worked Examples

**Example 1: Drawing cards without replacement**

You draw two cards from a standard 52-card deck without replacement. Find the probability that the second card is an ace given that the first card is an ace.

After drawing one ace, 51 cards remain. Of those, 3 are aces (one was already removed). Conditioning on "first card is an ace" restricts your sample space to the 51 remaining cards — that is the new universe. Within it, 3 outcomes are favorable:

$$P(\text{2nd is ace} \mid \text{1st is ace}) = \frac{3}{51} = \frac{1}{17}$$

The conditioning shrank the denominator from 52 to 51 and the numerator from 4 aces to 3. This is exactly what restricting the sample space means: you replace $|\Omega|$ with the count of outcomes consistent with the given information.

---

**Example 2: Reading a 2×2 table**

A survey recorded whether 200 people exercise regularly and whether they report good health:

|  | Good health | Not good health | Total |
|---|---|---|---|
| Exercises | 90 | 30 | 120 |
| Does not exercise | 40 | 40 | 80 |
| **Total** | 130 | 70 | 200 |

Find $P(\text{good health} \mid \text{exercises})$.

The condition "exercises" restricts you to the top row: 120 people. Of those, 90 report good health. Dividing:

$$P(\text{good health} \mid \text{exercises}) = \frac{90}{120} = 0.75$$

In formula terms: $P(G \cap E) = 90/200 = 0.45$ and $P(E) = 120/200 = 0.60$, so $P(G \mid E) = 0.45/0.60 = 0.75$. Both routes give the same answer.

---

**Example 3: Rearranging the formula to find $P(A \cap B)$**

Suppose $P(\text{rain tomorrow} \mid \text{cloudy today}) = 0.8$ and $P(\text{cloudy today}) = 0.3$. Find $P(\text{rain tomorrow and cloudy today})$.

Use the multiplication rule — rearrange the definition of conditional probability to isolate the joint probability:

$$P(A \cap B) = P(A \mid B) \cdot P(B) = 0.8 \times 0.3 = 0.24$$

The multiplication rule is the inverse direction of the conditional probability formula. Whenever you know how likely one event is given another, and you know the second event's probability, you can find their joint probability directly.

## Common Mistakes

- **Reversing $P(A \mid B)$ and $P(B \mid A)$.** These are generally different quantities. $P(\text{disease} \mid \text{positive test})$ and $P(\text{positive test} \mid \text{disease})$ answer entirely different questions. Confusing them is one of the most common errors in applied probability.
- **Using conditional probability when the events are given as already independent.** If $A$ and $B$ are independent, $P(A \mid B) = P(A)$ — conditioning changes nothing. Applying the full formula still works, but recognizing independence first simplifies the calculation.
- **Leaving $P(B) = 0$ in the denominator.** Conditional probability $P(A \mid B)$ is undefined when $P(B) = 0$. If the conditioning event has zero probability, you cannot condition on it.

## Quick Check

1. $P(A \cap B) = 0.12$ and $P(B) = 0.4$. Find $P(A \mid B)$.
2. A bag has 3 red and 5 blue balls. You draw one ball and it is red. Without replacement, what is $P(\text{2nd ball is red} \mid \text{1st is red})$?
3. $P(B \mid A) = 0.6$ and $P(A) = 0.5$. Find $P(A \cap B)$.

*(Answers: $0.3$; $2/7$; $0.3$)*
