# Central Limit Theorem

## Overview

The **central limit theorem** (CLT) says that the standardized sample mean converges in distribution to $N(0,1)$ as the sample size grows, regardless of the shape of the population distribution. This is remarkable: whether you are averaging exponential, uniform, Bernoulli, or any other finite-variance distribution, the sample mean becomes approximately normal for large $n$. The CLT is the foundation for confidence intervals, hypothesis tests, and nearly all classical statistical inference.

## Key Idea

If $X_1, X_2, \ldots, X_n$ are i.i.d. with mean $\mu$ and variance $\sigma^2 < \infty$, then:

$$\frac{\bar{X}_n - \mu}{\sigma / \sqrt{n}} \xrightarrow{d} N(0,1) \quad \text{as } n \to \infty$$

Equivalently, for large $n$, the sample mean is approximately:

$$\bar{X}_n \approx N\!\left(\mu,\; \frac{\sigma^2}{n}\right)$$

The standard deviation of $\bar{X}_n$ is $\sigma/\sqrt{n}$ — it shrinks as $n$ grows, which is why larger samples give more precise estimates. The CLT quantifies the shape of the fluctuations; the law of large numbers says only that those fluctuations shrink.

## Worked Examples

**Example 1: Approximate $P(\bar{X}_{50} > 5.2)$ from a non-normal population**

Suppose $X_i \sim \text{Exp}(1)$, so $\mu = 1$ and $\sigma^2 = 1$ — but wait, $\mu = 1$ for Exp$(1)$. Let us instead use $X_i$ with $\mu = 5$ and $\sigma^2 = 4$ (say, a shifted distribution). With $n = 50$:

$$\bar{X}_{50} \approx N\!\left(5, \frac{4}{50}\right) = N(5,\; 0.08)$$

To find $P(\bar{X}_{50} > 5.2)$, standardize. The standardization works because it converts the question into a $N(0,1)$ probability, which you can look up:

$$P\!\left(\bar{X}_{50} > 5.2\right) = P\!\left(Z > \frac{5.2 - 5}{\sqrt{0.08}}\right) = P\!\left(Z > \frac{0.2}{0.283}\right) = P(Z > 0.707) \approx 1 - 0.760 = 0.240$$

The key step is forming the $z$-score by subtracting the mean and dividing by $\sigma/\sqrt{n}$, not $\sigma$ alone.

---

**Example 2: Find minimum $n$ so that $P(|\bar{X}_n - \mu| < 0.5) \geq 0.95$**

Let $\sigma^2 = 9$. You want the sample mean to be within 0.5 of $\mu$ with probability at least 95%. By the CLT, $\bar{X}_n \approx N(\mu, 9/n)$, so:

$$P(|\bar{X}_n - \mu| < 0.5) = P\!\left(|Z| < \frac{0.5}{\sqrt{9/n}}\right) = P\!\left(|Z| < \frac{0.5\sqrt{n}}{3}\right)$$

For this probability to equal 0.95, you need the argument to equal the 97.5th percentile of $N(0,1)$, which is $z_{0.025} = 1.96$. This is because $P(|Z| < c) = 0.95$ when $c = 1.96$:

$$\frac{0.5\sqrt{n}}{3} = 1.96 \implies \sqrt{n} = \frac{3 \times 1.96}{0.5} = 11.76 \implies n \geq 138.3$$

Round up: $n \geq 139$. The $1.96$ comes from the standard normal table — it is the value such that 95% of the normal distribution lies within $\pm 1.96$ standard deviations of the mean.

---

**Example 3: The CLT applies to the sample mean, not individual observations**

A common misreading of the CLT: students sometimes believe it says that individual $X_i$ values become normally distributed as $n$ grows. This is false. Each $X_i$ is still drawn from the original population — if the population is Uniform$(0,1)$, every observation is still uniform, no matter how many you collect.

What the CLT says is that the sample mean $\bar{X}_n = \frac{1}{n}\sum X_i$ — a function of all $n$ observations — becomes approximately normal. The averaging is essential. A single observation $X_i$ never becomes normal by itself; it is the aggregation of many independent values that produces the normal shape through cancellation of asymmetries.

## Common Mistakes

- **Dividing by $\sigma$ instead of $\sigma/\sqrt{n}$ when standardizing $\bar{X}_n$.** The standard deviation of $\bar{X}_n$ is $\sigma/\sqrt{n}$, not $\sigma$. Using $\sigma$ alone ignores the variance reduction from averaging.
- **Applying the CLT for very small $n$.** The CLT is asymptotic. For skewed or heavy-tailed populations, $n = 5$ or $n = 10$ may not be large enough. A common rule of thumb is $n \geq 30$, but this depends heavily on the population's skewness.
- **Confusing the CLT with the LLN.** The LLN says $\bar{X}_n \to \mu$ (it stabilizes). The CLT says $(\bar{X}_n - \mu)/(\sigma/\sqrt{n})$ is approximately normal (it describes the distribution of the fluctuations). Both concern $\bar{X}_n$, but they answer different questions.

## Quick Check

1. If $\mu = 10$, $\sigma^2 = 16$, $n = 64$, what is the approximate distribution of $\bar{X}_{64}$?
2. Using that distribution, find $P(\bar{X}_{64} < 9)$
3. Does the CLT require the population to be symmetric?

*(Answers: $N(10, 16/64) = N(10, 0.25)$; $P(Z < (9-10)/0.5) = P(Z < -2) \approx 0.023$; no — the CLT applies to any distribution with finite variance, regardless of shape)*
