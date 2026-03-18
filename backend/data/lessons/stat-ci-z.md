# Z Confidence Intervals

## Overview

A **Z confidence interval** for $\mu$ uses the standard normal distribution and requires either known $\sigma$ or large $n$ (where $s \approx \sigma$ by LLN). It gives a range likely to contain the true mean.

## Key Idea

$$\bar{X} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$$

For 95% CI: $z_{0.025} = 1.96$. Interpretation: 95% of intervals constructed this way contain $\mu$.

## Worked Examples

**Example 1: $n=100$, $\bar{x}=50$, $\sigma=10$. 95% CI.**

$$50 \pm 1.96(10/10) = 50 \pm 1.96 = (48.04, 51.96)$$

---

**Example 2: 99% CI for the same data**

$z_{0.005} = 2.576$. $(50-2.576, 50+2.576) = (47.42, 52.58)$.

---

**Example 3: Effect of sample size**

Doubling $n$ reduces margin of error by $\sqrt{2}$. To halve margin of error, quadruple $n$.

## Common Mistakes

- **"95% probability that $\mu$ is in the interval."** Wrong. $\mu$ is fixed; the interval is random. 95% of such intervals contain $\mu$.
- **Using $Z$ CI when $\sigma$ is unknown and $n$ is small.** Use $t$ CI instead.

## Quick Check

1. Margin of error for $n=64$, $\sigma=8$, 95%?
2. $z_{0.025} = ?$
3. How does CI width change if $n$ quadruples?

*(Answers: 1.96; 1.96; halves)*
