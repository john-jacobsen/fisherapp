# Two-Sample t-Test (Independent Samples)

## Overview

The **two-sample independent t-test** compares the means of two independent groups to test $H_0: \mu_1 = \mu_2$. "Independent" means the subjects in Group 1 have no connection to those in Group 2 — this is the key assumption separating this test from the paired t-test. When the two groups may have different population variances, you use Welch's version, which does not assume $\sigma_1^2 = \sigma_2^2$.

## Key Idea

Under $H_0: \mu_1 = \mu_2$, the Welch t-statistic is:

$$T = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}}}$$

The denominator estimates the standard error of the difference $\bar{X}_1 - \bar{X}_2$. Each term $s_i^2/n_i$ is the variance of one sample mean; you add them because the two groups are independent. The degrees of freedom are approximated by the Welch-Satterthwaite formula:

$$df \approx \frac{\left(\dfrac{s_1^2}{n_1} + \dfrac{s_2^2}{n_2}\right)^2}{\dfrac{(s_1^2/n_1)^2}{n_1-1} + \dfrac{(s_2^2/n_2)^2}{n_2-1}}$$

This is generally non-integer and must be rounded down.

## Worked Examples

**Example 1: Compute the test statistic**

Group 1 (new curriculum): $n_1 = 20$, $\bar{x}_1 = 75$, $s_1 = 8$.
Group 2 (standard curriculum): $n_2 = 18$, $\bar{x}_2 = 70$, $s_2 = 10$.
Test $H_0: \mu_1 = \mu_2$ vs $H_1: \mu_1 \neq \mu_2$ at $\alpha = 0.05$.

First compute the standard error of the difference:

$$SE = \sqrt{\frac{64}{20} + \frac{100}{18}} = \sqrt{3.2 + 5.556} = \sqrt{8.756} \approx 2.959$$

Each term $s_i^2/n_i$ measures how precisely one sample mean estimates its group mean. You add them because variances of independent quantities add.

$$T = \frac{75 - 70}{2.959} = \frac{5}{2.959} \approx 1.69$$

---

**Example 2: Interpret the result and make a decision**

Using the Welch-Satterthwaite formula for Example 1 gives approximately $df \approx 32$. The two-sided critical value at $\alpha = 0.05$ with $df = 32$ is approximately $t_{0.025, 32} \approx 2.037$.

Since $|T| = 1.69 < 2.037$, you **fail to reject $H_0$**. There is not sufficient evidence at the 5% level to conclude the curricula produce different mean scores. The observed 5-point gap could plausibly arise from sampling variability alone, given the within-group standard deviations of 8 and 10.

---

**Example 3: Why use Welch's test by default**

Suppose instead you assumed $\sigma_1 = \sigma_2$ and used the pooled t-test. The pooled estimate would blend the two sample variances into a single number, which is only appropriate if the true variances are equal. When the true variances differ — which you rarely know in advance — the pooled test can give incorrect p-values and test sizes that don't match the stated $\alpha$.

Welch's test performs well whether or not the variances are equal. When variances are actually equal, Welch's test is only slightly less powerful than the pooled test. The cost of being wrong about equal variances far exceeds the cost of using Welch's by default.

## Common Mistakes

- **Using the paired t-test for independent groups.** If the two groups have different subjects, pairing is wrong — it changes the degrees of freedom and the test statistic in ways that invalidate the result.
- **Assuming equal variances without checking.** The pooled t-test requires $\sigma_1^2 = \sigma_2^2$. Welch's test does not, and is the safer default choice.
- **Forgetting that "independent samples" means the groups, not the observations within a group.** Observations within a group can be dependent; what matters is that Group 1 and Group 2 are sampled independently of each other.

## Quick Check

Try these before using hints:

1. $\bar{x}_1 = 40$, $\bar{x}_2 = 35$, $s_1^2 = 25$, $s_2^2 = 36$, $n_1 = n_2 = 10$. Compute the standard error of $\bar{X}_1 - \bar{X}_2$.
2. If $T = 2.5$ and $df = 20$, is the two-sided test significant at $\alpha = 0.05$ (critical value $\approx 2.086$)?
3. Why do you add $s_1^2/n_1 + s_2^2/n_2$ under the square root, rather than $(s_1^2 + s_2^2)/(n_1 + n_2)$?

*(Answers: 1. $SE = \sqrt{2.5 + 3.6} = \sqrt{6.1} \approx 2.47$; 2. Yes, reject ($2.5 > 2.086$); 3. Because each $s_i^2/n_i$ is the variance of a sample mean, and the variance of a difference of independent quantities is the sum of their variances)*
