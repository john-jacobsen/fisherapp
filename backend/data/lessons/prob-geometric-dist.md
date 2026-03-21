# Geometric Distribution

## Overview

The **geometric distribution** models the number of trials needed until the first success, where each trial is independent and has the same success probability $p$. It answers the question: "How long do you have to wait?" Whether waiting for a machine to fail, a customer to convert, or a die to show a 6, the geometric distribution is the natural model whenever you repeat independent trials until something happens for the first time.

## Key Idea

If $X$ is the trial number on which the first success occurs ($X = 1, 2, 3, \ldots$), then:

$$P(X = k) = (1-p)^{k-1}\, p \quad \text{for } k = 1, 2, 3, \ldots$$

The factor $(1-p)^{k-1}$ is the probability of failing the first $k-1$ trials; the final $p$ is the probability that trial $k$ succeeds. The mean and variance are:

$$E[X] = \frac{1}{p} \qquad \text{Var}(X) = \frac{1-p}{p^2}$$

The geometric distribution also has the **memoryless property**: given that the first success has not occurred in $m$ trials, the remaining wait is distributed as if you are starting fresh.

## Worked Examples

**Example 1: Expected number of rolls until the first 6**

A fair die shows a 6 with probability $p = 1/6$. The expected number of rolls to get the first 6 uses the mean formula directly — you expect to wait $1/p$ trials on average because each trial independently has a $p$ chance of ending your wait:

$$E[X] = \frac{1}{p} = \frac{1}{1/6} = 6$$

You expect to roll the die 6 times before seeing the first 6. This makes intuitive sense: one out of every 6 faces is a 6, so on average every 6 rolls produces one.

---

**Example 2: Computing $P(X > 3)$**

Still with $p = 1/6$, find the probability that the first 6 does not appear in the first 3 rolls: $P(X > 3)$.

$P(X > 3)$ means all of the first 3 trials failed. Since the trials are independent, you multiply the failure probabilities:

$$P(X > 3) = (1 - p)^3 = \left(\frac{5}{6}\right)^3 = \frac{125}{216} \approx 0.579$$

This tail formula generalizes: $P(X > m) = (1-p)^m$. It is a direct consequence of the memoryless property — the event $\{X > m\}$ is exactly the event that the first $m$ trials all fail.

---

**Example 3: Variance for $p = 0.4$**

Suppose each trial succeeds with probability $p = 0.4$. The variance measures the spread of waiting times around the mean.

First note the mean: $E[X] = 1/0.4 = 2.5$. Then apply the variance formula — the numerator is the failure probability, the denominator is $p^2$:

$$\text{Var}(X) = \frac{1-p}{p^2} = \frac{0.6}{(0.4)^2} = \frac{0.6}{0.16} = 3.75$$

The standard deviation is $\sqrt{3.75} \approx 1.94$. Notice that as $p$ decreases (rarer successes), both the mean and the variance grow — waiting longer also means more uncertainty about how long you will wait.

## Common Mistakes

- **Off-by-one: confusing the number-of-trials and number-of-failures versions.** Some textbooks define $X$ as the number of failures before the first success. In that version, $P(X = k) = (1-p)^k p$ for $k = 0, 1, 2, \ldots$ and $E[X] = (1-p)/p$. Always check which convention is being used.
- **Assuming the geometric applies when trials are not independent.** The geometric distribution requires that each trial's outcome does not affect the others. If past failures change the probability of future success, the model breaks down.
- **Using $P(X \geq k)$ when the problem asks for $P(X > k)$.** These differ by one term: $P(X \geq k) = (1-p)^{k-1}$, while $P(X > k) = (1-p)^k$. The exponent shifts by 1.

## Quick Check

1. A basketball player makes free throws with probability 0.7. Find the expected number of shots until the first make.
2. For the same player, find $P(X > 2)$.
3. Find $\text{Var}(X)$ for $p = 0.5$.

*(Answers: $1/0.7 \approx 1.43$; $(0.3)^2 = 0.09$; $(0.5)/(0.5)^2 = 2$)*
