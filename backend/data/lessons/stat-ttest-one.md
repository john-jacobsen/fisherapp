# One-Sample t-Test

## Overview

The **one-sample $t$-test** tests whether the population mean equals $\mu_0$ when $\sigma$ is unknown. It uses the sample standard deviation $S$ and the $t$-distribution.

## Key Idea

$$T = \frac{\bar{X} - \mu_0}{S/\sqrt{n}} \sim t_{n-1} \text{ under } H_0 \text{ (for normal data)}$$

The $t$-distribution has heavier tails than $N(0,1)$, accounting for the uncertainty in estimating $\sigma$.

## Worked Examples

**Example 1: $\mu_0 = 5$, $n = 10$, $\bar{x} = 6$, $s = 2$. $\alpha = 0.05$, two-sided.**

$T = (6-5)/(2/\sqrt{10}) = 1.58$. $t_{9,0.025} = 2.262$. $1.58 < 2.262$. Fail to reject.

---

**Example 2: 95% CI using $t$**

$(6 - 2.262 \cdot 0.632, 6 + 2.262 \cdot 0.632) = (4.57, 7.43)$.

---

**Example 3: Assumption**

Data should be approximately normal. Robust to mild departures when $n \ge 15$.

## Common Mistakes

- **Using $n$ instead of $n-1$ degrees of freedom.**
- **Applying $t$-test to heavily skewed data with small $n$.** Use nonparametric alternatives.

## Quick Check

1. df for one-sample $t$-test with $n=20$?
2. For large $n$, $t_{n-1} \approx ?$
3. $T = 3.0$, $n = 15$. Reject at $\alpha = 0.05$ (two-sided)?

*(Answers: 19; $N(0,1)$; yes, $t_{14,0.025} = 2.145 < 3.0$)*
