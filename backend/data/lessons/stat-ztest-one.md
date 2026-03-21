# One-Sample Z-Test

## Overview

The **one-sample z-test** tests a hypothesis about a population mean when the population standard deviation $\sigma$ is known. You compare your sample mean $\bar{X}$ to a hypothesized value $\mu_0$ and determine whether the observed difference is too large to attribute to random chance. Because $\sigma$ is known, the test statistic follows a standard normal distribution exactly under $H_0$.

## Key Idea

Under $H_0: \mu = \mu_0$, the test statistic is:

$$Z = \frac{\bar{X} - \mu_0}{\sigma/\sqrt{n}}$$

The denominator $\sigma/\sqrt{n}$ is the standard error of the mean — it measures how much $\bar{X}$ varies from sample to sample. Dividing by it converts the raw difference into standard-deviation units, which you can compare directly to the standard normal distribution.

- **Two-sided test** ($H_1: \mu \neq \mu_0$): reject if $|Z| > z_{\alpha/2}$
- **One-sided test** ($H_1: \mu < \mu_0$): reject if $Z < -z_\alpha$
- At $\alpha = 0.05$: critical values are $\pm 1.96$ (two-sided) or $-1.645$ (left-tailed)

## Worked Examples

**Example 1: Two-sided test**

A machine fills bags with a target weight of $\mu_0 = 50$ g. You know $\sigma = 10$ g. A sample of $n = 25$ bags gives $\bar{x} = 52.3$ g. Test $H_0: \mu = 50$ vs $H_1: \mu \neq 50$ at $\alpha = 0.05$.

The standard error is $\sigma/\sqrt{n} = 10/\sqrt{25} = 10/5 = 2$. This tells you how much the sample mean typically varies from the true mean when drawing samples of size 25.

$$Z = \frac{52.3 - 50}{2} = \frac{2.3}{2} = 1.15$$

The critical value for a two-sided test at $\alpha = 0.05$ is $z_{0.025} = 1.96$. Since $|1.15| = 1.15 < 1.96$, you **fail to reject $H_0$**. The sample mean is only 1.15 standard errors above the target — not unusual enough to conclude the machine is miscalibrated.

---

**Example 2: One-sided test**

A company claims its product lasts $\mu_0 = 100$ hours. You suspect it lasts less. You sample $n = 36$ units and find $\bar{x} = 97$, with known $\sigma = 15$. Test $H_0: \mu = 100$ vs $H_1: \mu < 100$ at $\alpha = 0.05$.

Standard error: $15/\sqrt{36} = 15/6 = 2.5$. A smaller standard error means more precision — larger samples pin down the mean more tightly.

$$Z = \frac{97 - 100}{2.5} = \frac{-3}{2.5} = -1.20$$

The critical value for a left-tailed test is $-z_{0.05} = -1.645$. Since $-1.20 > -1.645$, you fail to reject $H_0$. The sample mean is only 1.20 standard errors below the claim — not far enough into the left tail to reject.

---

**Example 3: Reporting the p-value**

For Example 1 with $Z = 1.15$, the p-value is the probability of observing a test statistic at least this extreme if $H_0$ is true. For a two-sided test, both tails count:

$$p = 2 \cdot P(Z > 1.15) = 2 \cdot (1 - \Phi(1.15)) = 2 \cdot (1 - 0.8749) = 2 \cdot 0.1251 = 0.250$$

Since $p = 0.250 > 0.05$, you fail to reject $H_0$. The p-value gives more information than a binary reject/fail-to-reject decision — here, $p = 0.25$ indicates the data are quite consistent with $H_0$ and provide little evidence against it.

## Common Mistakes

- **Using z when $\sigma$ is unknown.** If you don't know the true population standard deviation, you must use the t-test instead. Plugging in the sample standard deviation $s$ and treating it as known underestimates uncertainty, especially for small samples.
- **Confusing one-sided and two-sided critical values.** For a two-sided test at $\alpha = 0.05$, the critical value is $1.96$, not $1.645$. Using $1.645$ for a two-sided test silently inflates your Type I error rate to $10\%$.
- **Interpreting "fail to reject" as proof that $H_0$ is true.** A non-significant result only means you lack sufficient evidence to reject — it does not confirm that $\mu = \mu_0$.

## Quick Check

Try these before using hints:

1. $\mu_0 = 200$, $\sigma = 20$, $n = 100$, $\bar{x} = 203$. Compute $Z$.
2. Using $Z = 1.5$ and a two-sided test at $\alpha = 0.05$, what is your decision?
3. For $Z = -2.10$ and a left-tailed test at $\alpha = 0.05$, do you reject $H_0$?

*(Answers: 1. $Z = 1.5$; 2. Fail to reject, since $1.5 < 1.96$; 3. Yes, reject, since $-2.10 < -1.645$)*
