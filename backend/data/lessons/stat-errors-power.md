# Type I Error, Type II Error, and Power

## Overview

Any hypothesis test can make two kinds of mistakes. A **Type I error** (false positive) occurs when you reject $H_0$ even though it is true. A **Type II error** (false negative) occurs when you fail to reject $H_0$ even though it is false. The **power** of a test is the probability of correctly rejecting a false $H_0$. Understanding these three quantities is essential for designing tests that are both reliable and sensitive.

## Key Idea

Let $\alpha$ be the significance level and $\beta$ be the Type II error probability. Power is $1 - \beta$ and depends on the true value of the parameter $\theta$:

$$\text{Power}(\theta) = P(\text{reject } H_0 \mid \theta)$$

Power is not a single number — it is a function of $\theta$. Power is higher when the true $\theta$ is far from $\theta_0$ (a large effect is easier to detect), when $n$ is large, and when $\alpha$ is large.

## Worked Examples

**Example 1: Rejection region for a two-sided z-test at $\alpha = 0.05$**

For $H_0: \mu = \mu_0$ vs $H_1: \mu \neq \mu_0$, the test statistic is $Z = (\bar{X} - \mu_0)/(\sigma/\sqrt{n})$. Under $H_0$, $Z \sim N(0,1)$. You reject when $|Z| > z_{0.025} = 1.96$.

The probability of falling in this rejection region when $H_0$ is true equals exactly $\alpha = 0.05$. This is the Type I error rate by construction — the rejection region is designed so that false positives occur 5% of the time.

---

**Example 2: Compute power when $\mu = 52$, $\mu_0 = 50$, $\sigma = 10$, $n = 25$**

The rejection region is $|Z| > 1.96$, i.e., $|\bar{X} - 50| > 1.96 \times 10/\sqrt{25} = 3.92$.

When $\mu = 52$, $\bar{X} \sim N(52, 4)$, so $Z^* = (\bar{X} - 50)/2 \sim N(1, 1)$ (mean shifted by 1). Power equals:

$$P(|Z^*| > 1.96) = P(Z^* > 1.96) + P(Z^* < -1.96)$$
$$= P(Z > 0.96) + P(Z < -2.96) \approx 0.1685 + 0.0015 = 0.170$$

Power is only 17% because the true effect ($\mu - \mu_0 = 2$) is small relative to the noise ($\sigma/\sqrt{n} = 2$). You would miss this effect 83% of the time.

---

**Example 3: The $\alpha$-$\beta$ trade-off**

Suppose you tighten the significance level from $\alpha = 0.05$ to $\alpha = 0.01$ to reduce false positives. The critical value grows from 1.96 to 2.576, shrinking the rejection region. Now the test requires stronger evidence to reject $H_0$. While Type I errors decrease, the test becomes harder to reject even when $H_0$ is false: $\beta$ increases and power decreases. You cannot simultaneously minimize both error types for a fixed $n$ — reducing one increases the other. The only way to decrease both is to increase $n$.

## Common Mistakes

- **Confusing $\alpha$ and $\beta$.** $\alpha$ is fixed by you before the test. $\beta$ depends on the unknown true $\theta$ — it is not something you directly control unless you choose $n$ deliberately via power analysis.

- **Thinking power is a fixed property of the test.** Power varies with the true parameter value. A test can have high power for large deviations from $H_0$ but low power for small deviations.

- **Interpreting "fail to reject $H_0$" as "accept $H_0$."** Failing to reject means the data did not provide sufficient evidence against $H_0$. It does not prove $H_0$ is true — the test may simply have low power.

## Quick Check

Try these before using hints:

1. For a one-sided z-test $H_1: \mu > \mu_0$ at $\alpha = 0.05$, what is the rejection region?
2. If power is 0.60, what is $\beta$?
3. You run a test at $\alpha = 0.05$ and fail to reject. Does this mean the null is true?

*(Answers: 1. $Z > 1.645$; 2. $\beta = 0.40$; 3. No — it means there was insufficient evidence to reject; the test may have low power)*
