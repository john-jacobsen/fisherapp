# Confidence Intervals Using the Z-Distribution

## Overview

A **confidence interval (CI)** is a range of values constructed so that the interval contains the true parameter with probability $1-\alpha$ in repeated sampling. In other words, if you repeated your experiment many times and built a CI each time, $(1-\alpha) \times 100\%$ of those intervals would contain the true mean $\mu$. This frequentist guarantee is about the procedure, not about any single interval. You use the Z-distribution when the population standard deviation $\sigma$ is known.

## Key Idea

When $\sigma$ is known, the sample mean $\bar{X}$ follows a normal distribution (exactly if the population is normal, approximately by the Central Limit Theorem for large $n$). The standard error $\sigma/\sqrt{n}$ measures how much $\bar{X}$ varies across samples. The CI is:

$$\bar{X} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$$

The critical value $z_{\alpha/2}$ comes from the standard normal: for 95% confidence, $z_{0.025} = 1.96$; for 99% confidence, $z_{0.005} = 2.576$.

## Worked Examples

**Example 1: 95% CI for $\mu$ with $n=36$, $\bar{x}=50$, $\sigma=12$**

First, compute the standard error: $\sigma/\sqrt{n} = 12/\sqrt{36} = 12/6 = 2$. For 95% confidence, $\alpha = 0.05$, so you use $z_{0.025} = 1.96$. The margin of error is $1.96 \times 2 = 3.92$.

$$50 \pm 3.92 \implies (46.08,\ 53.92)$$

You are 95% confident the true mean lies in this interval. The interval is symmetric around $\bar{x}$ because the normal distribution is symmetric.

---

**Example 2: 99% CI for $\mu$ with $n=36$, $\bar{x}=50$, $\sigma=12$**

Now $\alpha = 0.01$, so you use $z_{0.005} = 2.576$. The margin of error grows to $2.576 \times 2 = 5.152$.

$$50 \pm 5.152 \implies (44.848,\ 55.152)$$

This interval is wider than the 95% CI. That makes intuitive sense: to be more confident you have captured $\mu$, you must cast a wider net. Higher confidence always comes at the cost of precision.

---

**Example 3: Find minimum $n$ so that a 95% CI has width $\leq 2$, given $\sigma=10$**

The total width of the CI equals $2 \times z_{\alpha/2} \times \sigma/\sqrt{n}$. Setting this $\leq 2$ and solving for $n$:

$$2 \times 1.96 \times \frac{10}{\sqrt{n}} \leq 2 \implies \frac{19.6}{\sqrt{n}} \leq 1 \implies \sqrt{n} \geq 19.6 \implies n \geq 384.16$$

Round up to $n = 385$. You always round up when solving for sample size because rounding down would violate the width requirement. This example shows that high precision demands a substantially large sample.

## Common Mistakes

- **Using $z_{\alpha}$ instead of $z_{\alpha/2}$.** For a two-sided 95% CI, you split $\alpha = 0.05$ equally between both tails, giving $z_{0.025} = 1.96$, not $z_{0.05} = 1.645$. Using the wrong critical value yields an interval with incorrect coverage.

- **Interpreting the CI as a probability about $\mu$.** Once data are collected, $\mu$ is a fixed unknown number. You cannot say "there is a 95% probability that $\mu$ is in this interval." The correct statement is that the procedure produces intervals covering $\mu$ in 95% of repetitions.

- **Dividing by $n$ instead of $\sqrt{n}$.** The standard error is $\sigma/\sqrt{n}$. Forgetting the square root makes the interval far too narrow, drastically undercovering the true mean.

## Quick Check

Try these before using hints:

1. Compute a 95% CI for $\mu$ when $\bar{x} = 80$, $\sigma = 5$, $n = 25$.
2. A 95% CI has width 10. How wide would a 99% CI be for the same data?
3. Find the minimum $n$ so that a 95% CI has width at most 4, given $\sigma = 8$.

*(Answers: 1. $(78.04,\ 81.96)$; 2. width $= 10 \times (2.576/1.96) \approx 13.14$; 3. $n \geq \lceil(1.96 \times 8/2)^2\rceil = \lceil 61.47 \rceil = 62$)*
