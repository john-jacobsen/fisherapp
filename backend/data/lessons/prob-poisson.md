# Poisson Distribution

## Overview

The **Poisson distribution** models the count of rare events in a fixed interval when events occur at a constant rate $\lambda$ and independently of one another. Classic examples include the number of phone calls arriving at a call center per hour, the number of typos per page, or the number of radioactive decays per second. Whenever you are counting how many times something happens in a fixed window — not the number of trials — the Poisson distribution is often the right model.

## Key Idea

If $X \sim \text{Poisson}(\lambda)$, where $\lambda > 0$ is the average number of events per interval:

$$P(X = k) = \frac{e^{-\lambda}\, \lambda^k}{k!}, \quad k = 0, 1, 2, \ldots$$

A remarkable feature of the Poisson is that its mean and variance are both equal to $\lambda$:

$$E[X] = \lambda \qquad \text{Var}(X) = \lambda$$

If you observe that the variance of a count is roughly equal to its mean, that is a signal the Poisson may be an appropriate model.

## Worked Examples

**Example 1: Calls arrive at rate 3 per hour — find $P(X = 2)$**

Calls arrive at a rate of $\lambda = 3$ per hour. You want the probability that exactly 2 calls arrive in a one-hour window. Plug directly into the PMF — the $e^{-\lambda}$ factor accounts for the probability of any given configuration, and $\lambda^k / k!$ distributes that weight across the count $k$:

$$P(X = 2) = \frac{e^{-3} \cdot 3^2}{2!} = \frac{e^{-3} \cdot 9}{2} = \frac{9}{2e^3} \approx \frac{9}{2 \cdot 20.086} \approx 0.224$$

There is about a 22.4% chance exactly 2 calls arrive in that hour.

---

**Example 2: Finding $P(X = 0)$**

Still with $\lambda = 3$, find the probability of no calls in one hour.

Setting $k = 0$: $\lambda^0 = 1$ and $0! = 1$, so the formula simplifies entirely to the exponential term:

$$P(X = 0) = \frac{e^{-3} \cdot 1}{1} = e^{-3} \approx 0.0498$$

There is about a 5% chance of a completely quiet hour. The $e^{-\lambda}$ term always gives $P(X = 0)$ — it represents the probability that no events occur given the rate $\lambda$.

---

**Example 3: Finding $P(X \geq 2)$ using the complement**

With $\lambda = 3$, find $P(X \geq 2)$. Summing from $k = 2$ to infinity is impractical. The complement is much cleaner: $P(X \geq 2) = 1 - P(X = 0) - P(X = 1)$.

You already know $P(X = 0) = e^{-3}$. Compute $P(X = 1)$:

$$P(X = 1) = \frac{e^{-3} \cdot 3}{1} = 3e^{-3} \approx 3 \cdot 0.0498 = 0.1494$$

Now subtract both from 1:

$$P(X \geq 2) = 1 - e^{-3} - 3e^{-3} = 1 - 4e^{-3} \approx 1 - 0.1991 = 0.801$$

There is about an 80.1% chance of 2 or more calls in an hour. The complement collapses an infinite sum into just two terms.

## Common Mistakes

- **Misidentifying the interval.** The rate $\lambda$ must match the interval you are computing over. If calls arrive at 3 per hour and you want the count over 30 minutes, use $\lambda = 1.5$, not $\lambda = 3$.
- **Applying Poisson to counts that are not rare or independent.** The Poisson requires that events do not cluster and that knowing one event occurred does not change the probability of another. For highly bursty or correlated arrivals, the Poisson is a poor fit.
- **Using $P(X \geq k)$ when you mean $P(X > k)$.** These differ by $P(X = k)$. Always re-read whether the threshold is included.

## Quick Check

1. Typos occur at a rate of 2 per page. Find $P(X = 0)$ on a given page.
2. For the same rate, find $P(X = 3)$.
3. If $X \sim \text{Poisson}(5)$, what are $E[X]$ and $\text{Var}(X)$?

*(Answers: $e^{-2} \approx 0.135$; $\frac{e^{-2} \cdot 8}{6} \approx 0.180$; $E[X] = 5$, $\text{Var}(X) = 5$)*
