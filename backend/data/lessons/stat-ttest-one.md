# One-Sample t-Test

## Overview

The **one-sample t-test** tests a hypothesis about a population mean when the population standard deviation $\sigma$ is unknown — the typical situation in practice. You estimate $\sigma$ with the sample standard deviation $s$, but this introduces extra uncertainty. To account for it, the test statistic follows a $t$-distribution with $n-1$ degrees of freedom rather than the standard normal.

## Key Idea

Under $H_0: \mu = \mu_0$, the test statistic is:

$$T = \frac{\bar{X} - \mu_0}{s/\sqrt{n}} \sim t_{n-1}$$

The $t$-distribution has heavier tails than the standard normal, reflecting the added uncertainty from estimating $\sigma$. As $n$ grows, $s$ converges to $\sigma$ and the $t$-distribution converges to $N(0,1)$. For small samples (say $n < 30$), the difference matters substantially — the t-critical values are noticeably larger than $\pm 1.96$.

## Worked Examples

**Example 1: Two-sided test**

A process is supposed to produce parts with mean diameter $\mu_0 = 10$ mm. You measure $n = 16$ parts and find $\bar{x} = 11.2$ mm and $s = 2.4$ mm. Test $H_0: \mu = 10$ vs $H_1: \mu \neq 10$ at $\alpha = 0.05$.

The standard error is $s/\sqrt{n} = 2.4/\sqrt{16} = 2.4/4 = 0.6$. This is your best estimate of how much $\bar{X}$ varies from sample to sample.

$$T = \frac{11.2 - 10}{0.6} = \frac{1.2}{0.6} = 2.00$$

With $n - 1 = 15$ degrees of freedom, the critical value is $t_{0.025, 15} = 2.131$. Since $|2.00| = 2.00 < 2.131$, you **fail to reject $H_0$** — but just barely. The result is close to the boundary.

---

**Example 2: One-sided test**

You want to test whether a new training program raises average scores above $\mu_0 = 5$. A pilot with $n = 9$ participants gives $\bar{x} = 6.1$ and $s = 3$. Test $H_0: \mu = 5$ vs $H_1: \mu > 5$ at $\alpha = 0.05$.

Standard error: $3/\sqrt{9} = 3/3 = 1$.

$$T = \frac{6.1 - 5}{1} = 1.10$$

With $df = 8$, the one-sided critical value is $t_{0.05, 8} = 1.860$. Since $1.10 < 1.860$, you fail to reject $H_0$. Despite the sample mean being above 5, the variability ($s = 3$) is large enough relative to the sample size that the difference is not significant.

---

**Example 3: Why t is wider than z**

Take the same numbers as Example 1: $\bar{x} = 11.2$, $s = 2.4$, $n = 16$, $T = 2.00$.

If you mistakenly used a z-test, the critical value would be $z_{0.025} = 1.96$, and you would reject $H_0$ (since $2.00 > 1.96$). But with the correct t-test using $df = 15$, the critical value is $2.131$, and you fail to reject. The t-test is more conservative because $s$ is a random estimate of $\sigma$ — treating it as certain would overstate your confidence. This difference shrinks as $n$ increases, but for $n = 16$ it can change your conclusion entirely.

## Common Mistakes

- **Using $z$ critical values with sample standard deviation.** When $\sigma$ is unknown, using $1.96$ as your cutoff ignores the extra variability in $s$, inflating the Type I error rate — especially for small $n$.
- **Forgetting to check the normality assumption.** The t-test assumes the data (or their mean) follow a normal distribution. For very small samples, you should examine whether this is reasonable. For large samples, the Central Limit Theorem protects you.
- **Using $n$ instead of $n-1$ for degrees of freedom.** The denominator of $s^2$ is $n-1$ (not $n$), and degrees of freedom for the t-distribution is $n-1$. Using $n$ gives a slightly wrong critical value and p-value.

## Quick Check

Try these before using hints:

1. $\mu_0 = 50$, $\bar{x} = 53$, $s = 6$, $n = 9$. Compute $T$.
2. With $df = 9$ and $\alpha = 0.05$ two-sided, the critical value is $t = 2.262$. Is $T = 1.5$ significant?
3. Why does the t-distribution have heavier tails than the standard normal?

*(Answers: 1. $T = 1.5$; 2. No, $1.5 < 2.262$; 3. Because $s$ estimates $\sigma$ with uncertainty — more variability in the denominator spreads the distribution)*
