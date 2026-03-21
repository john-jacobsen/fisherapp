# Bernoulli and Binomial Distributions

## Overview

A **Bernoulli** trial is a single success/failure experiment with success probability $p$. A **Binomial** random variable counts the number of successes in $n$ independent, identical Bernoulli trials. The binomial is the go-to model whenever you have a fixed number of trials, each with the same two outcomes and the same probability, and the trials do not affect each other.

## Key Idea

If $X \sim \text{Bin}(n, p)$, the probability of exactly $k$ successes is:

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \ldots, n$$

The $\binom{n}{k}$ counts the number of ways to arrange $k$ successes among $n$ trials; $p^k(1-p)^{n-k}$ is the probability of any one such arrangement. The mean and variance are:

$$E[X] = np \qquad \text{Var}(X) = np(1-p)$$

## Worked Examples

**Example 1: Probability of exactly 3 heads in 5 fair coin flips**

You have $n = 5$ flips, each with $p = 1/2$, and you want $k = 3$ heads. The $\binom{5}{3} = 10$ counts the number of distinct sequences with exactly 3 heads among 5 positions. Each such sequence has probability $(1/2)^3 (1/2)^2$ because heads and tails are equally likely.

$$P(X = 3) = \binom{5}{3}\left(\frac{1}{2}\right)^3\!\left(\frac{1}{2}\right)^2 = 10 \cdot \frac{1}{32} = \frac{10}{32} = \frac{5}{16} \approx 0.313$$

The probability is about 31.3%.

---

**Example 2: Finding $P(X \geq 2)$ using the complement**

Let $X \sim \text{Bin}(5, 1/2)$. Computing $P(X \geq 2)$ directly requires summing four terms ($k = 2, 3, 4, 5$). The complement approach is cleaner: $P(X \geq 2) = 1 - P(X \leq 1) = 1 - P(X=0) - P(X=1)$.

Each tail probability is computed with the same formula:

$$P(X = 0) = \binom{5}{0}(1/2)^0(1/2)^5 = \frac{1}{32}$$

$$P(X = 1) = \binom{5}{1}(1/2)^1(1/2)^4 = \frac{5}{32}$$

Subtracting from 1 gives the answer — you are removing all outcomes where fewer than 2 heads occur:

$$P(X \geq 2) = 1 - \frac{1}{32} - \frac{5}{32} = 1 - \frac{6}{32} = \frac{26}{32} = \frac{13}{16} \approx 0.813$$

---

**Example 3: Mean and variance for $X \sim \text{Bin}(20, 0.3)$**

You have $n = 20$ trials with success probability $p = 0.3$. Rather than summing over all 21 possible values, use the closed-form expressions derived from the indicator representation of the binomial.

$$E[X] = np = 20 \cdot 0.3 = 6$$

$$\text{Var}(X) = np(1-p) = 20 \cdot 0.3 \cdot 0.7 = 4.2$$

$$\text{SD}(X) = \sqrt{4.2} \approx 2.05$$

On average you expect 6 successes, and most outcomes fall within roughly 2 of that value. The variance is largest when $p = 0.5$ and shrinks as $p$ approaches 0 or 1.

## Common Mistakes

- **Using the binomial when trials are not independent.** If sampling without replacement from a small population, the correct model is hypergeometric, not binomial. Use binomial only when each trial's outcome does not change the probability for the next.
- **Forgetting that $\binom{n}{k}$ is about positions, not outcomes.** The combination counts the number of arrangements of successes, not the number of ways the experiment can turn out. Each arrangement has the same probability $p^k(1-p)^{n-k}$.
- **Computing $P(X > k)$ when you mean $P(X \geq k)$.** These differ by exactly one term: $P(X = k)$. Always check whether the inequality is strict or non-strict before using the complement.

## Quick Check

1. Let $X \sim \text{Bin}(4, 0.5)$. Find $P(X = 2)$.
2. Find $P(X \geq 1)$ for $X \sim \text{Bin}(3, 0.4)$ using the complement.
3. For $X \sim \text{Bin}(10, 0.6)$, find $E[X]$ and $\text{Var}(X)$.

*(Answers: $\binom{4}{2}(0.5)^4 = 6/16 = 3/8$; $1 - (0.6)^3 = 1 - 0.216 = 0.784$; $E[X]=6$, $\text{Var}(X)=2.4$)*
