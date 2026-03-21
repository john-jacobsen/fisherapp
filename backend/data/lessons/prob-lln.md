# Law of Large Numbers

## Overview

The **law of large numbers** (LLN) is the formal statement that the sample mean $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$ converges to the population mean $\mu$ as the sample size $n$ grows. There are two versions: the **weak LLN** says $\bar{X}_n$ converges to $\mu$ in probability (for any fixed tolerance, the chance of being outside that tolerance goes to zero); the **strong LLN** says $\bar{X}_n \to \mu$ almost surely (the convergence happens with probability 1 on every sample path). Both require finite mean; the weak LLN also requires finite variance when proved via Chebyshev's inequality.

## Key Idea

The weak LLN states:

$$\bar{X}_n \xrightarrow{p} \mu \quad \text{as } n \to \infty$$

The standard proof uses Chebyshev's inequality applied to $\bar{X}_n$. Since $E[\bar{X}_n] = \mu$ and $\text{Var}(\bar{X}_n) = \sigma^2/n$:

$$P(|\bar{X}_n - \mu| \geq \epsilon) \leq \frac{\text{Var}(\bar{X}_n)}{\epsilon^2} = \frac{\sigma^2}{n\epsilon^2}$$

The right side goes to 0 as $n \to \infty$ for any fixed $\epsilon > 0$, proving convergence in probability.

## Worked Examples

**Example 1: Bound $P(|\bar{X}_{100} - \mu| > 0.1)$ using Chebyshev**

Suppose $X_1, X_2, \ldots$ are i.i.d. with mean $\mu$ and variance $\sigma^2 = 1$. After $n = 100$ observations, apply the Chebyshev bound with $\epsilon = 0.1$.

The key insight is that averaging $n$ observations reduces the variance by a factor of $n$ — the variance of the sample mean is $\sigma^2/n$, not $\sigma^2$. This variance reduction is exactly why more data gives a better estimate of $\mu$:

$$P(|\bar{X}_{100} - \mu| > 0.1) \leq \frac{\sigma^2}{n\epsilon^2} = \frac{1}{100 \cdot 0.01} = \frac{1}{1} = 1$$

With $n = 100$ and $\epsilon = 0.1$, the Chebyshev bound equals 1 — it is not informative here. The bound becomes useful when $n$ is large relative to $\sigma^2/\epsilon^2$. Try $n = 1000$: the bound becomes $1/(1000 \cdot 0.01) = 0.1$.

---

**Example 2: The bound tightens as $n$ increases**

Continuing with $\sigma^2 = 1$ and $\epsilon = 0.1$, the Chebyshev bound is $1/(n \cdot 0.01) = 100/n$. As $n$ grows:

| $n$ | Upper bound on $P(\|\bar{X}_n - \mu\| > 0.1)$ |
|---|---|
| 100 | 1.00 (uninformative) |
| 1000 | 0.10 |
| 10000 | 0.01 |
| 100000 | 0.001 |

The bound shrinks as $1/n$ because Var$(\bar{X}_n) = \sigma^2/n$. Every factor of 10 in sample size buys another factor of 10 reduction in the Chebyshev bound. This is a direct quantitative expression of what the LLN states qualitatively: more data makes the sample mean concentrate closer to $\mu$.

---

**Example 3: Distinguish the LLN from the CLT**

The LLN and the Central Limit Theorem both concern $\bar{X}_n$, but they answer different questions. The LLN says that $\bar{X}_n$ stabilizes at $\mu$ — the value it converges to. The CLT says how the fluctuations around $\mu$ are distributed while $n$ is large but finite.

Concretely: after $n$ observations, $\bar{X}_n$ is close to $\mu$ (LLN), and the deviation $\bar{X}_n - \mu$ is approximately normal with mean 0 and standard deviation $\sigma/\sqrt{n}$ (CLT). The LLN tells you the destination; the CLT describes the shape of the spread around that destination. You need both to make probability statements about how far $\bar{X}_n$ is from $\mu$ for a specific $n$.

## Common Mistakes

- **Applying the LLN to individual observations.** The LLN says the sample mean converges to $\mu$, not that individual $X_i$ values become closer to $\mu$. Each new observation is still drawn from the original distribution — the averaging is what drives convergence.
- **Invoking the LLN for small $n$.** The LLN is an asymptotic statement about $n \to \infty$. For small or moderate $n$, you cannot conclude that $\bar{X}_n \approx \mu$ without additional calculations (e.g., a Chebyshev bound or CLT approximation).
- **Confusing weak and strong convergence.** Convergence in probability (weak LLN) means $P(|\bar{X}_n - \mu| > \epsilon) \to 0$ for each $\epsilon$; almost sure convergence (strong LLN) is a stronger statement about entire sample paths. For practical purposes the distinction rarely matters, but it is important to state which version you are using.

## Quick Check

1. If $\sigma^2 = 9$ and $n = 900$, give the Chebyshev upper bound on $P(|\bar{X}_n - \mu| \geq 0.1)$
2. Does the LLN say anything about how $\bar{X}_n - \mu$ is distributed, or only about its size?
3. Can the LLN be applied when $\sigma^2 = \infty$? (Assume finite $\mu$ exists)

*(Answers: $9/(900 \times 0.01) = 1$ — uninformative; only about its size (it converges to 0); the weak LLN proved via Chebyshev requires finite variance, but the strong LLN holds under finite mean alone)*
