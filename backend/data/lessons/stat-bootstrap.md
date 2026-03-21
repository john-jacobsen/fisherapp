# The Bootstrap

## Overview

The **bootstrap** is a resampling method that estimates the sampling distribution of a statistic without needing a closed-form formula. The core idea: the observed data are your best approximation to the population, so you can simulate the sampling process by drawing samples from your data. It is especially valuable for complex statistics (like the median or a ratio) where analytical standard errors are hard to derive.

## Key Idea

Generate $B$ bootstrap samples by drawing $n$ observations with replacement from your original data of size $n$. Compute the statistic $\hat{\theta}^*_b$ for each bootstrap sample. Estimate the standard error of $\hat{\theta}$ by the standard deviation of these $B$ values:

$$\widehat{\text{SE}}_{boot} = \sqrt{\frac{1}{B-1}\sum_{b=1}^B (\hat{\theta}^*_b - \bar{\hat{\theta}}^*)^2}$$

where $\bar{\hat{\theta}}^* = \frac{1}{B}\sum_{b=1}^B \hat{\theta}^*_b$. A larger $B$ gives a more precise estimate of the SE; $B = 1{,}000$ to $10{,}000$ is typical.

## Worked Examples

**Example 1: Bootstrap SE of the sample median**

Suppose your data are $\{3, 7, 5, 12, 4\}$ ($n = 5$). The sample median is 5.

There is no simple closed-form formula for $\text{SE}(\text{median})$ for arbitrary distributions. The bootstrap procedure: (1) draw $n = 5$ observations with replacement from $\{3, 7, 5, 12, 4\}$, (2) compute the median of the resample, (3) repeat $B = 1{,}000$ times. The standard deviation of the 1,000 medians estimates the SE of the original sample median.

Each resample can repeat values (since you draw with replacement), so resamples like $\{3, 3, 7, 5, 5\}$ are possible. This mimics the variability of drawing a new sample of size 5 from the underlying population.

---

**Example 2: Percentile bootstrap confidence interval**

Once you have $B$ bootstrap statistics $\hat{\theta}^*_1, \ldots, \hat{\theta}^*_B$, the **percentile bootstrap CI** uses quantiles of the bootstrap distribution directly.

Sort the bootstrap statistics. A 95% CI takes the 2.5th percentile as the lower bound and the 97.5th percentile as the upper bound. For $B = 1{,}000$, this means the 25th and 975th sorted values.

Why does this work? The bootstrap distribution of $\hat{\theta}^*$ mimics the sampling distribution of $\hat{\theta}$. The region containing the central 95% of bootstrap values approximates the region where the true $\theta$ likely lies. The percentile method is attractive because it requires no normality assumption and automatically accounts for skewness in the bootstrap distribution.

---

**Example 3: Bootstrap SE versus analytical SE for $\bar{X}$**

For the sample mean, the analytical SE is $\sigma/\sqrt{n}$ (estimated as $s/\sqrt{n}$). The bootstrap should recover this.

For each bootstrap resample of size $n$, compute $\bar{X}^*_b$. The bootstrap SE is $\text{SD}(\bar{X}^*_1, \ldots, \bar{X}^*_B)$. As $B \to \infty$, this converges to $\text{SD}(\bar{X}^*) = s\sqrt{(n-1)/n^2 \cdot n} = s/\sqrt{n} \cdot \sqrt{(n-1)/n}$.

For large $n$, this is approximately $s/\sqrt{n}$ — matching the analytical formula. The bootstrap and analytical SEs agree asymptotically. For finite $B$, there is Monte Carlo error, but it shrinks as $B$ increases. This confirms the bootstrap is a valid procedure even when you already know the formula — and it generalizes to situations where no formula exists.

## Common Mistakes

- **Sampling without replacement.** Bootstrap resampling must be done with replacement. Sampling without replacement always gives back your original dataset (just reordered) and produces zero variance — completely defeating the purpose.
- **Confusing $B$ (number of bootstrap resamples) with $n$ (original sample size).** You always resample $n$ observations (to mimic the original sampling process), but you repeat this $B$ times (to approximate the bootstrap distribution). $B$ should be large; $n$ is fixed by your data.
- **Relying on the bootstrap when $n$ is very small.** The bootstrap approximates the population distribution with the empirical distribution of your data. With very small $n$ (say $n < 10$), your empirical distribution is a poor approximation to the true distribution, and bootstrap CIs can be unreliable.

## Quick Check

Try these before using hints:

1. You have $n = 100$ observations and run $B = 500$ bootstrap resamples. How many observations are in each resample?
2. The bootstrap distribution of $\hat{\theta}^*$ has mean 4.2 and standard deviation 0.6. What is $\widehat{\text{SE}}_{boot}$?
3. Why must bootstrap resampling be done with replacement rather than without replacement?

*(Answers: 100; 0.6; sampling without replacement always returns the original data — no variability is generated)*
