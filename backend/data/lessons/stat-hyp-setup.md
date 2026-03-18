# Hypothesis Test Setup

## Overview

A **hypothesis test** starts with a null hypothesis $H_0$ (the default claim) and an alternative $H_1$. Data is used to decide whether to reject $H_0$ in favor of $H_1$, controlling the probability of error.

## Key Idea

- **$H_0$:** default (e.g., $\mu = 0$, no effect)
- **$H_1$:** the research claim (e.g., $\mu \ne 0$, $\mu > 0$, or $\mu < 0$)
- **Test statistic:** a function of the data computed under $H_0$
- **Rejection region:** values of the test statistic leading to rejection

## Worked Examples

**Example 1: Coin fairness. Set up the test.**

$H_0: p = 0.5$ vs. $H_1: p \ne 0.5$ (two-sided). Test statistic: $Z = (\hat{p} - 0.5)/\sqrt{0.25/n}$.

---

**Example 2: One-sided test**

Drug lowers blood pressure. $H_0: \mu = 0$ vs. $H_1: \mu < 0$ (reduction).

---

**Example 3: Simple vs. composite**

$H_0: \mu = 5$ is simple (single value). $H_1: \mu > 5$ is composite (many values).

## Common Mistakes

- **Setting up $H_1$ based on the data** — hypotheses must be stated before seeing data.
- **Reversing null and alternative.** The burden of proof is on $H_1$; $H_0$ is rejected only with strong evidence.

## Quick Check

1. Which is the "innocent until proven guilty" hypothesis?
2. One-sided vs. two-sided: when do you use each?
3. Can $H_0$ be "accepted"?

*(Answers: $H_0$; one-sided when direction is known in advance; no — only "fail to reject")*
