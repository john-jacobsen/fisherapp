# Memoryless Property

## Overview

A distribution is **memoryless** if knowing how long you have already waited tells you nothing about how much longer you still have to wait — the remaining wait is statistically identical to starting fresh. Among all distributions, only the exponential (continuous) and the geometric (discrete) are memoryless. Every other common distribution does "age": the longer you have waited, the different your remaining wait looks.

## Key Idea

For all $s, t \geq 0$, the memoryless condition is:

$$P(X > s + t \mid X > s) = P(X > t)$$

For the exponential, this follows directly from the survival function. Using the definition of conditional probability and $P(X > x) = e^{-\lambda x}$:

$$P(X > s + t \mid X > s) = \frac{P(X > s + t)}{P(X > s)} = \frac{e^{-\lambda(s+t)}}{e^{-\lambda s}} = e^{-\lambda t} = P(X > t)$$

## Worked Examples

**Example 1: Verify the exponential satisfies the memoryless property using its CDF.**

You want to confirm algebraically that conditioning on survival past time $s$ does not change the remaining distribution. Start from the definition of conditional probability — $P(A \mid B) = P(A \cap B)/P(B)$ — and note that $\{X > s + t\} \subset \{X > s\}$, so their intersection is $\{X > s + t\}$.

$$P(X > s + t \mid X > s) = \frac{P(X > s + t)}{P(X > s)} = \frac{e^{-\lambda(s+t)}}{e^{-\lambda s}} = e^{-\lambda t} = P(X > t) \checkmark$$

The exponential factors cleanly because $e^{-\lambda(s+t)} = e^{-\lambda s} \cdot e^{-\lambda t}$. The $e^{-\lambda s}$ terms cancel, leaving only the fresh-start distribution.

---

**Example 2: Apply memorylessness to a waiting-time word problem.**

A server processes requests at rate $\lambda = 0.5$ per minute, so processing times follow $\text{Exp}(0.5)$. A job has already been processing for 4 minutes. What is the probability it takes more than 2 additional minutes?

By the memoryless property, the remaining processing time is still $\text{Exp}(0.5)$, regardless of the 4 minutes already elapsed. The past gives you no information about the future. So:

$$P(\text{more than 2 more min}) = P(X > 2) = e^{-0.5 \cdot 2} = e^{-1} \approx 0.368$$

The 4 minutes already spent are irrelevant — you compute exactly as if the job were just starting.

---

**Example 3: Explain why the normal distribution is NOT memoryless.**

Suppose $X \sim N(10, 1)$ models the lifespan of a component. If a component has already survived 12 units of time (well above the mean), very little probability mass remains to the right — nearly all of the distribution has already been used up. Formally, $P(X > 14 \mid X > 12)$ is much smaller than $P(X > 2)$, because the conditional distribution shifts and tightens dramatically.

For the normal, the conditional distribution $X \mid X > s$ is a truncated normal whose shape changes with $s$. The remaining wait is not the same as starting fresh — it depends heavily on how long you have already waited. This aging behavior means the normal (and most other distributions) fail the memoryless condition.

## Common Mistakes

- **Assuming all waiting-time distributions are memoryless.** The gamma, Weibull, log-normal, and normal distributions all have aging: the longer you wait, the different the residual distribution looks.
- **Applying memorylessness in the wrong direction.** The property says past waiting time is irrelevant to future waiting time. It does NOT say that observing an event tells you nothing about future events — it only concerns the remaining time within a single inter-event gap.

## Quick Check

1. $X \sim \text{Exp}(1)$. Find $P(X > 4 \mid X > 2)$.
2. A geometric random variable $X \sim \text{Geom}(p)$ has survived $m$ trials with no success. What is $P(X > m + n \mid X > m)$?
3. Name both distributions that are memoryless.

*(Answers: $e^{-2}$; $(1-p)^n = P(X > n)$; exponential and geometric)*
