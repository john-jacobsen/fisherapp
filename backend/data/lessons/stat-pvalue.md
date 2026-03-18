# p-Values

## Overview

The **p-value** is the probability, under $H_0$, of observing a test statistic at least as extreme as the one computed. It measures the evidence against $H_0$: smaller p-value = stronger evidence against $H_0$.

## Key Idea

$$p = P(T \ge t_{\text{obs}} | H_0) \quad \text{(one-sided)}$$

Reject $H_0$ at level $\alpha$ if $p < \alpha$. The p-value is NOT the probability that $H_0$ is true.

## Worked Examples

**Example 1: $Z = 2.1$, two-sided test**

$p = 2 \times P(Z > 2.1) = 2 \times 0.018 = 0.036$. Reject at $\alpha = 0.05$.

---

**Example 2: $t = 1.8$, $n = 20$, one-sided**

$p = P(t_{19} > 1.8) \approx 0.044$. Reject at $\alpha = 0.05$.

---

**Example 3: p-value = 0.20**

Fail to reject $H_0$ at any standard level. The data is consistent with $H_0$.

## Common Mistakes

- **"p = 0.04 means 4% chance $H_0$ is true."** The p-value is a probability under $H_0$, not about $H_0$.
- **Comparing p-value to $\beta$, not $\alpha$.**

## Quick Check

1. $p = 0.03$, $\alpha = 0.05$. Decision?
2. $p = 0.10$, $\alpha = 0.05$. Decision?
3. Is $p < 0.05$ always practically significant?

*(Answers: reject $H_0$; fail to reject; no — statistical vs. practical significance differ)*
