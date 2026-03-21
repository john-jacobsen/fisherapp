# P-Values

## Overview

The **p-value** is the probability of observing a test statistic at least as extreme as the one actually observed, assuming $H_0$ is true. A small p-value means the observed data would be very unusual if $H_0$ were true, which is evidence against $H_0$. You reject $H_0$ when the p-value falls below the pre-chosen significance level $\alpha$. The p-value is not the probability that $H_0$ is true — it is a statement about the data under the assumption that $H_0$ is true.

## Key Idea

For a two-sided test with observed test statistic $z_{obs}$, the p-value is the total probability in both tails beyond $|z_{obs}|$:

$$p = P(|Z| \geq |z_{obs}| \mid H_0) \quad \text{(two-sided)}$$

For a one-sided test ($H_1: \mu > \mu_0$), only the upper tail contributes: $p = P(Z \geq z_{obs} \mid H_0)$.

## Worked Examples

**Example 1: Two-sided p-value for $z_{obs} = 2.1$**

You are testing $H_0: \mu = \mu_0$ vs $H_1: \mu \neq \mu_0$. The observed z-statistic is 2.1. Because the test is two-sided, you double the tail probability:

$$p = 2 \times P(Z \geq 2.1) = 2 \times (1 - \Phi(2.1)) = 2 \times 0.0179 = 0.0357$$

At $\alpha = 0.05$, you reject $H_0$ because $0.0357 < 0.05$. The observed test statistic is far enough from zero that data this extreme would occur only 3.57% of the time under $H_0$.

---

**Example 2: One-sided p-value for $z_{obs} = -1.8$**

You are testing $H_0: \mu \geq \mu_0$ vs $H_1: \mu < \mu_0$. Only the left tail matters:

$$p = P(Z \leq -1.8) = \Phi(-1.8) = 1 - \Phi(1.8) = 1 - 0.9641 = 0.0359$$

At $\alpha = 0.05$, you reject $H_0$ because $0.0359 < 0.05$. Note: if you incorrectly computed a two-sided p-value here, you would get $p = 0.0718$ and fail to reject — using the wrong tail is a consequential error.

---

**Example 3: Interpreting $p = 0.03$ at $\alpha = 0.05$**

You observe $p = 0.03$ and $\alpha = 0.05$, so you reject $H_0$. Here is what this does and does NOT mean:

- **It means:** If $H_0$ were true, data at least this extreme would occur only 3% of the time. The data are unlikely under $H_0$.
- **It does NOT mean:** The probability that $H_0$ is true is 3%. The p-value says nothing about how probable $H_0$ is — $H_0$ is either true or false, and a frequentist p-value does not assign it a probability.
- **It does NOT mean:** The result is practically important. A tiny effect with a huge sample can yield $p < 0.05$. Always consider the magnitude of the effect alongside the p-value.

## Common Mistakes

- **"The p-value is the probability $H_0$ is true."** This is the most common misinterpretation. The p-value is computed under the assumption $H_0$ is true — it cannot simultaneously measure the probability of that assumption.

- **Using a two-sided p-value formula for a one-sided test.** Doubling the tail probability when you have a one-sided alternative doubles the p-value and can cause you to fail to reject a hypothesis that should be rejected.

- **Choosing $\alpha$ after computing the p-value.** Setting $\alpha = 0.04$ because you observe $p = 0.03$ is not valid. You must commit to $\alpha$ before seeing the data.

## Quick Check

Try these before using hints:

1. Compute the two-sided p-value for $z_{obs} = 1.5$. Use $\Phi(1.5) = 0.9332$.
2. For a one-sided test ($H_1: \mu > \mu_0$) with $z_{obs} = 1.8$, is $p < 0.05$?
3. Can a p-value tell you the probability that the alternative $H_1$ is true?

*(Answers: 1. $p = 2(1 - 0.9332) = 0.1336$; 2. $p = 1 - \Phi(1.8) = 0.0359 < 0.05$, yes; 3. No — p-values cannot assign probabilities to hypotheses)*
