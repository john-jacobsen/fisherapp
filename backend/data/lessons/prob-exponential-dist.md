# Exponential Distribution

## Overview

The **exponential distribution** models waiting times between events in a Poisson process — for example, the time until the next customer arrives, the next server request lands, or a radioactive atom decays. It has a single rate parameter $\lambda > 0$, which is the average number of events per unit time. The higher $\lambda$ is, the faster events arrive and the shorter the expected wait.

## Key Idea

For $X \sim \text{Exp}(\lambda)$ with $x \geq 0$:

$$f(x) = \lambda e^{-\lambda x} \qquad \text{(PDF)}$$

$$F(x) = 1 - e^{-\lambda x} \qquad \text{(CDF)}$$

$$E[X] = \frac{1}{\lambda}, \qquad \text{Var}(X) = \frac{1}{\lambda^2}$$

The survival function $P(X > x) = e^{-\lambda x}$ comes up constantly — it is simply $1 - F(x)$.

## Worked Examples

**Example 1: Calls arrive at rate 2 per minute. Find $P(\text{wait} > 1 \text{ min})$.**

Here $\lambda = 2$ and you want the probability the next call takes more than 1 minute. Use the survival function rather than the CDF — the CDF gives $P(X \leq x)$, so its complement gives $P(X > x)$ directly. This avoids an extra subtraction step.

$$P(X > 1) = e^{-2 \cdot 1} = e^{-2} \approx 0.135$$

There is about a 13.5% chance you wait more than 1 minute. When $\lambda$ is large (events arrive fast), the exponential decay is steep and the probability of a long wait drops quickly.

---

**Example 2: Find the median waiting time for $X \sim \text{Exp}(2)$.**

The median $m$ satisfies $F(m) = 0.5$ — exactly half the distribution lies below $m$, half above. Because the CDF is strictly increasing, there is exactly one solution. Set $F(m) = 0.5$ and solve algebraically.

$$1 - e^{-2m} = 0.5 \implies e^{-2m} = 0.5 \implies -2m = \ln(0.5) \implies m = \frac{\ln 2}{2} \approx 0.347 \text{ min}$$

The median (about 20.8 seconds) is less than the mean ($1/\lambda = 0.5$ min). The exponential is right-skewed: a small number of very long waits pull the mean above the median.

---

**Example 3: Compute $E[X]$ and $\text{Var}(X)$ for $\lambda = 0.5$.**

With $\lambda = 0.5$ events per minute, events arrive slowly — roughly one every 2 minutes. The mean and variance formulas come from integrating $x \cdot f(x)$ and $x^2 \cdot f(x)$ against the PDF; here you plug directly into the results.

$$E[X] = \frac{1}{\lambda} = \frac{1}{0.5} = 2 \text{ min}$$

$$\text{Var}(X) = \frac{1}{\lambda^2} = \frac{1}{0.25} = 4 \text{ min}^2, \qquad \text{SD}(X) = 2 \text{ min}$$

The standard deviation equals the mean — this is always true for the exponential. A coefficient of variation of exactly 1 is a distinguishing signature of this distribution.

## Common Mistakes

- **Plugging into $f(x)$ to get a probability.** $f(x)$ is a density, not a probability. To find $P(a \leq X \leq b)$, compute $F(b) - F(a)$ or integrate the PDF over $[a, b]$.
- **Confusing $\lambda$ (rate) with mean.** If the average wait is 5 minutes, then $E[X] = 5$ and $\lambda = 1/5 = 0.2$. The rate parameter enters every formula — not the mean.
- **Forgetting the domain $x \geq 0$.** The exponential is defined only for non-negative values. Setting an integral lower bound below zero is an error.

## Quick Check

1. If $X \sim \text{Exp}(3)$, find $P(X > 2)$.
2. Find the median of $\text{Exp}(\lambda)$ in terms of $\lambda$.
3. If the average time between failures is 10 hours, what is $\lambda$ and $\text{Var}(X)$?

*(Answers: $e^{-6} \approx 0.0025$; $\dfrac{\ln 2}{\lambda}$; $\lambda = 0.1$, $\text{Var}(X) = 100 \text{ hr}^2$)*
