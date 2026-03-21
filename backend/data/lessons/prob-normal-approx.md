# Normal Approximation to Binomial

## Overview

For large $n$, the binomial distribution is approximately normal — this follows from the Central Limit Theorem applied to a sum of independent Bernoulli trials. The **continuity correction** improves the approximation by accounting for the fact that you are approximating a discrete distribution with a continuous one: a discrete value $k$ corresponds to the continuous interval $[k - 0.5, k + 0.5]$, so shifting the boundary by 0.5 makes the approximation more accurate.

## Key Idea

If $X \sim \text{Bin}(n, p)$, then for large $n$:

$$X \approx N\!\left(np,\; np(1-p)\right)$$

To standardize, subtract the mean and divide by the standard deviation:

$$Z = \frac{X - np}{\sqrt{np(1-p)}} \approx N(0,1)$$

With continuity correction:

$$P(X \leq k) \approx P\!\left(Z \leq \frac{k + 0.5 - np}{\sqrt{np(1-p)}}\right)$$

The approximation is reliable when $np \geq 5$ and $n(1-p) \geq 5$.

## Worked Examples

**Example 1: 100 fair coin flips. Estimate $P(X \leq 55)$ without continuity correction.**

Here $X \sim \text{Bin}(100, 0.5)$, so $\mu = np = 50$ and $\sigma = \sqrt{np(1-p)} = \sqrt{25} = 5$. Standardize $X = 55$ directly: you are measuring how many standard deviations 55 is above the mean, which tells you where it falls in the standard normal table.

$$P(X \leq 55) \approx P\!\left(Z \leq \frac{55 - 50}{5}\right) = P(Z \leq 1.0) \approx 0.8413$$

---

**Example 2: Repeat with continuity correction.**

When approximating a discrete distribution with a continuous one, the event $\{X \leq 55\}$ in the discrete world corresponds to $\{X < 55.5\}$ in the continuous world — because any continuous value between 55 and 55.5 would round down to 55. Adding 0.5 to the boundary before standardizing corrects for this mismatch and brings the approximation closer to the true binomial value.

$$P(X \leq 55) \approx P\!\left(Z \leq \frac{55 + 0.5 - 50}{5}\right) = P(Z \leq 1.1) \approx 0.8643$$

The true binomial value is approximately 0.8644, so the continuity-corrected answer is nearly exact, while the uncorrected answer in Example 1 has a meaningful error.

---

**Example 3: Identify when the approximation is appropriate.**

The rule of thumb — $np \geq 5$ and $n(1-p) \geq 5$ — ensures that both tails of the binomial have enough mass that the distribution looks roughly bell-shaped. When $p$ is near 0 or 1, the binomial is heavily skewed, and no matter how large $n$ is, the normal is a poor fit near the extreme tail. Check both conditions before applying the approximation.

For $X \sim \text{Bin}(20, 0.1)$: $np = 2 < 5$, so the approximation is **not** valid — the Poisson approximation is better here. For $X \sim \text{Bin}(50, 0.4)$: $np = 20 \geq 5$ and $n(1-p) = 30 \geq 5$, so the normal approximation is appropriate.

## Common Mistakes

- **Forgetting the continuity correction for $P(X = k)$.** For a single value, $P(X = k) \approx P(k - 0.5 \leq Z_{\text{rescaled}} \leq k + 0.5)$. Without this correction, $P(X = k)$ would be approximately zero under the continuous normal.
- **Using the approximation when $np < 5$ or $n(1-p) < 5$.** When either condition fails, the binomial is too skewed for the normal to capture accurately. Use exact binomial calculations or the Poisson approximation instead.

## Quick Check

1. $X \sim \text{Bin}(100, 0.5)$. Use continuity correction to approximate $P(X \leq 45)$.
2. Is the normal approximation appropriate for $\text{Bin}(30, 0.9)$?
3. What are $\mu$ and $\sigma$ for $\text{Bin}(200, 0.3)$?

*(Answers: $P(Z \leq -0.9) \approx 0.184$; no, $n(1-p) = 3 < 5$; $\mu = 60$, $\sigma = \sqrt{42} \approx 6.48$)*
