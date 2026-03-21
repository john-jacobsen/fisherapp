# Poisson Approximation to Binomial

## Overview

When $n$ is large and $p$ is small, $\text{Bin}(n, p)$ is well approximated by $\text{Poisson}(\lambda)$ with $\lambda = np$. The approximation works because the binomial PMF converges to the Poisson PMF as $n \to \infty$ and $p \to 0$ with $np$ held fixed. In practice, the approximation is excellent when $n \geq 20$ and $p \leq 0.05$. This is useful because the Poisson PMF is often much easier to compute than the binomial when $n$ is large.

## Key Idea

The approximation rule is:

$$\text{Bin}(n, p) \approx \text{Poisson}(\lambda), \quad \lambda = np, \quad \text{when } n \geq 20 \text{ and } p \leq 0.05$$

In terms of probabilities, you replace:

$$\binom{n}{k} p^k (1-p)^{n-k} \approx \frac{e^{-\lambda} \lambda^k}{k!}$$

Both distributions have mean $\lambda = np$. The binomial variance is $np(1-p) \approx np = \lambda$ when $p$ is small, so the variances also approximately match — this is why the approximation is so accurate in the small-$p$ regime.

## Worked Examples

**Example 1: Factory components — finding $P(X = 0)$**

A factory produces 1000 components. Each component independently fails during quality testing with probability 0.002. Let $X$ count the number of failures. Here $n = 1000$ is large and $p = 0.002$ is small, so the binomial is unwieldy but the Poisson approximation is excellent.

Set $\lambda = np = 1000 \times 0.002 = 2$. The probability that no components fail is:

$$P(X = 0) \approx e^{-\lambda} = e^{-2} \approx 0.135$$

Compare: the exact binomial gives $P(X=0) = (0.998)^{1000} \approx 0.135$ — they agree to three decimal places.

---

**Example 2: Comparing exact binomial vs. Poisson for small $k$**

Using the same setup ($n = 1000$, $p = 0.002$, $\lambda = 2$), compare $P(X = 1)$ under both models.

Exact binomial:

$$P(X = 1) = \binom{1000}{1}(0.002)^1(0.998)^{999} = 1000 \cdot 0.002 \cdot (0.998)^{999}$$

$(0.998)^{999}$ is painful to compute by hand. The Poisson approximation gives it immediately:

$$P(X = 1) \approx \frac{e^{-2} \cdot 2^1}{1!} = 2e^{-2} \approx 0.271$$

The exact binomial answer is also approximately $0.271$. The Poisson approximation saves all the computation while giving a result indistinguishable from the exact answer at this precision.

---

**Example 3: Identifying when the approximation is appropriate**

Consider three scenarios: (A) $n = 10$, $p = 0.3$; (B) $n = 200$, $p = 0.01$; (C) $n = 50$, $p = 0.4$.

Scenario A: $n = 10$ is too small. The approximation requires $n \geq 20$.

Scenario B: $n = 200 \geq 20$ and $p = 0.01 \leq 0.05$. Both conditions are met — use $\text{Poisson}(2)$.

Scenario C: $p = 0.4$ is much too large. With $p$ near 0.5, the binomial is symmetric and bell-shaped, not resembling the Poisson at all. Use the exact binomial or a normal approximation instead.

The check is simple: both $n$ large and $p$ small must hold simultaneously.

## Common Mistakes

- **Setting $\lambda$ incorrectly.** You must use $\lambda = np$, not just $n$ or $p$ alone. The Poisson parameter is the expected number of successes, which you must compute from the binomial parameters.
- **Applying the approximation when $p$ is not small.** Large $n$ alone is not enough. If $p = 0.5$ and $n = 1000$, the normal approximation is correct, not the Poisson. The Poisson approximation specifically requires $p \to 0$.
- **Forgetting that the approximation only works for small $k$.** The Poisson PMF matches the binomial PMF most closely near $k = 0, 1, 2, \ldots$ When $k$ is close to $n$, both are near zero anyway — but always sanity-check that $k \ll n$.

## Quick Check

1. $n = 500$, $p = 0.004$. What $\lambda$ do you use for the Poisson approximation?
2. For the same setup, find $P(X = 0)$ using the approximation.
3. Is the Poisson approximation appropriate for $n = 30$, $p = 0.3$? Explain.

*(Answers: $\lambda = 500 \times 0.004 = 2$; $e^{-2} \approx 0.135$; No — $p = 0.3 > 0.05$, so $p$ is not small enough for the approximation to be valid)*
