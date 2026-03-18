# One-Sample Z-Test

## Overview

The **one-sample Z-test** tests whether a population mean equals a specified value, using a known $\sigma$ (or large $n$ where $s \approx \sigma$). It is the prototype of all hypothesis tests.

## Key Idea

$$Z = \frac{\bar{X} - \mu_0}{\sigma/\sqrt{n}} \sim N(0,1) \text{ under } H_0$$

Reject $H_0$ at level $\alpha$ if $|Z| > z_{\alpha/2}$ (two-sided) or $Z > z_\alpha$ (one-sided).

## Worked Examples

**Example 1: $\mu_0 = 100$, $\sigma = 15$, $n = 25$, $\bar{x} = 106$. Two-sided, $\alpha = 0.05$.**

$Z = (106-100)/(15/5) = 2.0$. $|2.0| > 1.96$. Reject $H_0$.

---

**Example 2: Compute the p-value**

$p = 2P(Z > 2.0) = 2(0.023) = 0.046 < 0.05$. Reject.

---

**Example 3: One-sided test**

$H_1: \mu > 100$. Reject when $Z > 1.645$. Same data: $Z = 2.0 > 1.645$. Reject.

## Common Mistakes

- **Using $Z$-test when $\sigma$ is unknown and $n$ is small.** Use $t$-test.
- **Computing one-sided $p$-value but using two-sided critical value** (or vice versa).

## Quick Check

1. Test statistic formula for one-sample $Z$-test?
2. Critical value for $\alpha = 0.01$, two-sided?
3. $n=36$, $\sigma=12$, $\bar{x}=52$, $\mu_0=50$. $Z = ?$

*(Answers: $(\bar{X}-\mu_0)/(\sigma/\sqrt{n})$; 2.576; 1.0)*
