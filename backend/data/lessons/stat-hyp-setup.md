# Setting Up Hypothesis Tests

## Overview

A **hypothesis test** is a formal procedure for using data to decide between two competing claims about a population parameter. The **null hypothesis** $H_0$ is the default claim — a specific value or range you assume true until evidence shows otherwise. The **alternative hypothesis** $H_1$ is what you aim to detect — the claim you would conclude if the data are sufficiently inconsistent with $H_0$. You reject $H_0$ when the test statistic falls in the rejection region, which is calibrated so that the probability of a false rejection equals $\alpha$.

## Key Idea

The **significance level** $\alpha$ is the probability of rejecting $H_0$ when it is actually true — a false positive. You choose $\alpha$ before collecting data; common choices are 0.05 and 0.01.

$$\alpha = P(\text{reject } H_0 \mid H_0 \text{ true})$$

The rejection region is the set of test statistic values that lead you to reject $H_0$. Its boundaries (critical values) are determined by $\alpha$ and the distribution of the test statistic under $H_0$.

## Worked Examples

**Example 1: Is a coin fair? — Two-sided test**

You want to test whether a coin has $p = 0.5$ (the probability of heads). Because you would reject fairness for either too many or too few heads, you use a two-sided alternative.

$$H_0: p = 0.5 \quad \text{vs} \quad H_1: p \neq 0.5$$

The two-sided alternative means the rejection region sits in both tails of the distribution. You reject $H_0$ if the test statistic is either much larger or much smaller than expected under $H_0$. Using $\alpha = 0.05$, you reject when $|Z| > 1.96$.

---

**Example 2: Does a new drug reduce recovery time? — One-sided test**

A standard treatment has mean recovery time $\mu_0 = 14$ days. You believe the new drug is better (shorter recovery time). A one-sided alternative captures this:

$$H_0: \mu \geq \mu_0 \quad \text{vs} \quad H_1: \mu < \mu_0$$

You only reject $H_0$ if the sample mean is substantially below $\mu_0$. The rejection region is in the left tail only. For $\alpha = 0.05$, you reject when $Z < -1.645$.

---

**Example 3: One-sided vs two-sided — when to use each**

Choose a **two-sided** alternative ($H_1: \theta \neq \theta_0$) when you want to detect a difference in either direction and have no prior reason to expect a specific direction. Choose a **one-sided** alternative ($H_1: \theta > \theta_0$ or $H_1: \theta < \theta_0$) only when theory or prior evidence strongly supports a specific direction before you see the data.

One-sided tests have more power in the favored direction — at $\alpha = 0.05$, the critical value is $z = 1.645$ instead of $z = 1.96$. However, you cannot switch to a one-sided test after seeing the data just because the result went in one direction; this inflates the actual Type I error rate.

## Common Mistakes

- **Choosing $H_1$ after looking at the data.** The hypotheses must be specified before data collection. Choosing a one-sided alternative because the observed mean happened to go in one direction is data dredging and invalidates the stated $\alpha$.

- **Confusing $H_0$ and $H_1$.** The null hypothesis always carries the equality ($=$, $\leq$, or $\geq$). The alternative is what you are trying to find evidence for — the "interesting" claim.

- **Failing to specify $\alpha$ before the test.** If you choose $\alpha$ after seeing the test statistic, you can always make the result "significant," which defeats the purpose of the procedure.

## Quick Check

Try these before using hints:

1. Set up hypotheses to test whether a population mean exceeds 100.
2. For a two-sided test at $\alpha = 0.05$, what are the critical values for a z-test?
3. You observe $Z = 2.10$. Do you reject $H_0: \mu = 50$ vs $H_1: \mu \neq 50$ at $\alpha = 0.05$?

*(Answers: 1. $H_0: \mu \leq 100$ vs $H_1: \mu > 100$; 2. $\pm 1.96$; 3. Yes, because $|2.10| > 1.96$)*
