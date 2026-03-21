# Confidence Intervals for Proportions

## Overview

When you want to estimate an unknown population proportion $p$ — for example, the fraction of voters who support a candidate — you observe $X$ successes in $n$ independent trials and compute the **normal approximation** CI. The sample proportion $\hat{p} = X/n$ is the maximum likelihood estimate of $p$. Because $\hat{p}$ is approximately normal for large $n$, you can build a CI using the standard normal distribution. The approximation is valid when $n\hat{p} \geq 5$ and $n(1-\hat{p}) \geq 5$.

## Key Idea

The Wald confidence interval for a proportion is:

$$\hat{p} \pm z_{\alpha/2}\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

The term under the square root is the estimated standard error of $\hat{p}$. It is largest when $\hat{p} = 0.5$, which is why $p = 0.5$ is used as a conservative choice when planning sample size.

## Worked Examples

**Example 1: 95% CI when $X=40$, $n=100$**

Compute $\hat{p} = 40/100 = 0.40$. Check validity: $n\hat{p} = 40 \geq 5$ and $n(1-\hat{p}) = 60 \geq 5$ — the approximation is valid.

The estimated standard error is $\sqrt{0.40 \times 0.60 / 100} = \sqrt{0.0024} \approx 0.049$. Using $z_{0.025} = 1.96$:

$$0.40 \pm 1.96 \times 0.049 \approx 0.40 \pm 0.096 \implies (0.304,\ 0.496)$$

You are 95% confident the true proportion lies between 30.4% and 49.6%.

---

**Example 2: 99% CI when $X=5$, $n=50$ — check validity**

Compute $\hat{p} = 5/50 = 0.10$. Check: $n\hat{p} = 5$ (borderline acceptable) and $n(1-\hat{p}) = 45 \geq 5$.

The standard error is $\sqrt{0.10 \times 0.90 / 50} = \sqrt{0.0018} \approx 0.042$. Using $z_{0.005} = 2.576$:

$$0.10 \pm 2.576 \times 0.042 \approx 0.10 \pm 0.108 \implies (0,\ 0.208)$$

The lower bound is truncated at 0 since a proportion cannot be negative. The validity condition is marginal here ($n\hat{p} = 5$), so this CI should be interpreted with caution. For sparse data like this, exact binomial methods (e.g., the Clopper-Pearson interval) are more reliable.

---

**Example 3: Find $n$ to estimate $p$ within $\pm 0.03$ with 95% confidence**

You want the margin of error $z_{0.025}\sqrt{\hat{p}(1-\hat{p})/n} \leq 0.03$. Because you do not yet have data, use the conservative value $\hat{p} = 0.5$, which maximizes $\hat{p}(1-\hat{p}) = 0.25$ and therefore gives the largest (most conservative) required $n$.

$$1.96\sqrt{\frac{0.25}{n}} \leq 0.03 \implies \sqrt{\frac{0.25}{n}} \leq \frac{0.03}{1.96} \approx 0.01531 \implies n \geq \frac{0.25}{(0.01531)^2} \approx 1067$$

You need at least $n = 1068$ observations. This is why large polls require thousands of respondents to achieve 3-percentage-point margins of error.

## Common Mistakes

- **Ignoring the validity condition.** If $n\hat{p} < 5$ or $n(1-\hat{p}) < 5$, the normal approximation is poor. Use the exact binomial (Clopper-Pearson) interval instead.

- **Using $p$ instead of $\hat{p}$ in the standard error.** In practice, $p$ is unknown. You must plug in $\hat{p}$ to estimate the standard error. Some students accidentally substitute a hypothesized $p_0$, which is only appropriate in a hypothesis test.

- **Forgetting to use $p = 0.5$ conservatively for sample size planning.** Any other assumed value of $p$ will underestimate $n$ if the true $p$ is actually closer to 0.5.

## Quick Check

Try these before using hints:

1. Compute a 95% CI for $p$ when $X = 60$, $n = 200$.
2. Does the validity condition hold when $X = 3$, $n = 40$?
3. How large must $n$ be to estimate $p$ within $\pm 0.05$ with 95% confidence, using $\hat{p} = 0.5$?

*(Answers: 1. $(0.233,\ 0.367)$; 2. No: $n\hat{p} = 3 < 5$; 3. $n \geq 385$)*
