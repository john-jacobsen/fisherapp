# Poisson Process

## Overview

A **Poisson process** models the occurrence of random events in continuous time — phone calls arriving at a call center, radioactive decays, or customers entering a store. The defining feature is a constant rate $\lambda > 0$: events arrive at rate $\lambda$ per unit time, independently of each other and independently of the time since the last event. This memoryless, independent-increments structure makes the Poisson process mathematically tractable and widely applicable.

## Key Idea

Three equivalent characterizations of a Poisson process with rate $\lambda$:

**Count in an interval:** The number of arrivals in any interval of length $t$ is:

$$N(t) \sim \text{Poisson}(\lambda t), \qquad P(N(t) = k) = \frac{e^{-\lambda t}(\lambda t)^k}{k!}$$

**Inter-arrival times:** The waiting time between consecutive arrivals is:

$$T_k \sim \text{Exp}(\lambda) \text{ i.i.d.}, \qquad P(T_k > t) = e^{-\lambda t}$$

**$k$-th arrival time:** The time until the $k$-th arrival is:

$$S_k = T_1 + T_2 + \cdots + T_k \sim \text{Gamma}(k, \lambda), \qquad E[S_k] = \frac{k}{\lambda}$$

## Worked Examples

**Example 1: Find $P(\text{3 arrivals in 2 hours})$ with $\lambda = 1$/hour**

The number of arrivals in 2 hours follows $N(2) \sim \text{Poisson}(\lambda \cdot 2) = \text{Poisson}(2)$. The rate parameter of the Poisson distribution is $\lambda t$, not $\lambda$ alone — you scale by the interval length because more time means proportionally more expected arrivals.

$$P(N(2) = 3) = \frac{e^{-2} \cdot 2^3}{3!} = \frac{e^{-2} \cdot 8}{6} = \frac{4e^{-2}}{3} \approx \frac{4(0.1353)}{3} \approx 0.180$$

There is about an 18% chance of seeing exactly 3 arrivals in a 2-hour window.

---

**Example 2: Find $P(\text{wait} > 30 \text{ min for first arrival})$**

The first inter-arrival time is $T_1 \sim \text{Exp}(\lambda)$. With $\lambda = 1$ arrival/hour, 30 minutes is $t = 0.5$ hours. The exponential distribution's survival function gives the probability of waiting more than $t$ time units directly:

$$P(T_1 > 0.5) = e^{-\lambda \cdot 0.5} = e^{-1 \cdot 0.5} = e^{-0.5} \approx 0.607$$

There is about a 61% chance of waiting more than 30 minutes for the first arrival. The exponential distribution is the unique continuous distribution with the memoryless property: $P(T > s + t \mid T > s) = P(T > t)$. How long you have already waited does not affect the distribution of the remaining wait.

---

**Example 3: Expected time until the 5th arrival**

The 5th arrival time is $S_5 = T_1 + T_2 + T_3 + T_4 + T_5$, where each $T_k \sim \text{Exp}(\lambda)$ independently. The sum of $k$ independent Exp$(\lambda)$ random variables follows a Gamma$(k, \lambda)$ distribution, and the expected value of a Gamma$(k, \lambda)$ is $k/\lambda$.

$$E[S_5] = \frac{5}{\lambda} = \frac{5}{1} = 5 \text{ hours}$$

This makes intuitive sense: if one arrival happens on average every $1/\lambda = 1$ hour, then 5 arrivals take an average of 5 hours. The Gamma structure generalizes the exponential: waiting for the $k$-th event is just waiting for $k$ independent exponential events in sequence.

## Common Mistakes

- **Using $\lambda$ instead of $\lambda t$ in the Poisson PMF.** The mean of $N(t)$ is $\lambda t$, not $\lambda$. Forgetting to multiply by $t$ gives the wrong distribution for any interval other than $[0,1]$.
- **Confusing $N(t)$ (a count) with $S_k$ (a time).** $N(t)$ is a discrete random variable counting events in $[0,t]$; $S_k$ is a continuous random variable measuring when the $k$-th event occurs. They are related but not the same.
- **Assuming the Poisson process applies when events are not independent.** If one arrival makes another more or less likely (clustering or inhibition), the Poisson process model is wrong. The independence of increments assumption must be verified.

## Quick Check

1. If $\lambda = 4$ calls/hour, what is the expected number of calls in 45 minutes?
2. With $\lambda = 2$/hour, what is $P(T_1 > 1)$ (probability of waiting more than 1 hour for the first arrival)?
3. With $\lambda = 3$/hour, what is $E[S_4]$ (expected time until the 4th arrival)?

*(Answers: $\lambda t = 4 \times 0.75 = 3$; $e^{-2} \approx 0.135$; $4/3$ hours $\approx 80$ minutes)*
