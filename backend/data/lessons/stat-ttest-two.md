# Two-Sample t-Test

## Overview

The **two-sample $t$-test** compares the means of two independent groups. It tests $H_0: \mu_1 = \mu_2$ (no difference between groups).

## Key Idea

Assuming equal variances (pooled $t$-test):

$$T = \frac{\bar{X}_1 - \bar{X}_2}{S_p\sqrt{1/n_1 + 1/n_2}} \sim t_{n_1+n_2-2}$$

where $S_p^2 = \frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{n_1+n_2-2}$ is the pooled variance.

Welch's $t$-test (unequal variances) uses a different denominator and approximate df.

## Worked Examples

**Example 1: $\bar{x}_1 = 10$, $\bar{x}_2 = 8$, $s_1 = s_2 = 3$, $n_1 = n_2 = 16$. Pooled $t$-test, $\alpha = 0.05$.**

$S_p = 3$, SE $= 3\sqrt{2/16} = 1.06$. $T = 2/1.06 = 1.89$. $t_{30,0.025} = 2.042$. Fail to reject.

---

**Example 2: Checking equal variances**

Use Levene's test or compare $s_1/s_2$; if ratio is extreme, use Welch.

---

**Example 3: 95% CI for $\mu_1 - \mu_2$**

$(2 \pm 2.042 \times 1.06) = (-0.16, 4.16)$. Contains 0 → consistent with no difference.

## Common Mistakes

- **Using pooled test when variances are very unequal.** Use Welch's test instead.
- **Wrong df.** Pooled: $n_1+n_2-2$; Welch: approximate (Satterthwaite).

## Quick Check

1. $H_0$ in a two-sample $t$-test?
2. Pooled df for $n_1=10$, $n_2=15$?
3. What does Welch's test assume about variances?

*(Answers: $\mu_1=\mu_2$; 23; they need not be equal)*
