# Paired t-Test

## Overview

A **paired t-test** compares two measurements that are linked — typically the same subjects measured twice (before/after), or two treatments applied to matched pairs. Because each pair shares background characteristics, you subtract the two measurements to eliminate that shared variability. This leaves differences $D_i = X_{i1} - X_{i2}$ that contain only the treatment effect plus within-subject noise.

## Key Idea

Once you compute the differences, the paired t-test reduces to a one-sample t-test on $D_1, D_2, \ldots, D_n$:

$$T = \frac{\bar{D}}{s_D/\sqrt{n}} \sim t_{n-1}$$

Here $\bar{D}$ is the mean difference and $s_D$ is the standard deviation of the differences. The key insight is that pairing removes between-subject variability. If subjects vary widely from each other, pairing can dramatically reduce the denominator (the standard error) and increase the power of the test.

## Worked Examples

**Example 1: Before/after study**

Eight subjects take a memory test before and after a training program. The differences (after minus before) are computed, giving $\bar{d} = 3.5$ and $s_d = 2.1$. Test $H_0: \mu_D = 0$ vs $H_1: \mu_D > 0$ at $\alpha = 0.05$.

Standard error of the mean difference: $s_D/\sqrt{n} = 2.1/\sqrt{8} = 2.1/2.828 \approx 0.743$.

$$T = \frac{3.5}{0.743} \approx 4.71$$

With $df = n - 1 = 7$, the one-sided critical value is $t_{0.05, 7} = 1.895$. Since $4.71 \gg 1.895$, you **reject $H_0$**. The training program is associated with a statistically significant increase in scores.

---

**Example 2: Paired product comparison**

Six tasters each try two snack products and rate them on a 10-point scale. The scores are:

| Taster | Product A | Product B | $d_i = A - B$ |
|--------|-----------|-----------|---------------|
| 1      | 7         | 5         | +2            |
| 2      | 6         | 7         | -1            |
| 3      | 8         | 6         | +2            |
| 4      | 5         | 4         | +1            |
| 5      | 9         | 7         | +2            |
| 6      | 6         | 5         | +1            |

$\bar{d} = (2 - 1 + 2 + 1 + 2 + 1)/6 = 7/6 \approx 1.17$. Computing $s_d$ from these six differences gives $s_d \approx 1.07$. Standard error: $1.07/\sqrt{6} \approx 0.437$. So $T \approx 1.17/0.437 \approx 2.68$. With $df = 5$ and two-sided critical value $t_{0.025,5} = 2.571$, you reject $H_0$ — Product A is rated significantly higher on average.

---

**Example 3: Why $n-1$ degrees of freedom, and when pairing helps**

The paired test has $n - 1$ degrees of freedom (not $2n - 2$) because you are analyzing $n$ differences, not $2n$ separate observations. Once you subtract, only $n$ values remain. Each difference costs one degree of freedom for estimating the mean, leaving $n - 1$.

Pairing helps most when between-subject variability is large relative to the treatment effect. If subjects are similar to each other, pairing provides little benefit — the within-subject error and the between-subject error are comparable. But when subjects differ dramatically in baseline performance, an unpaired test would mix that large between-subject noise into the denominator, masking the treatment effect. Pairing surgically removes that noise.

## Common Mistakes

- **Using an unpaired test on paired data.** If you ignore the pairing and run a two-sample t-test on paired data, the denominator will include between-subject variability, making the test less powerful — and the degrees of freedom will be wrong.
- **Forgetting to compute differences first.** The test operates on $D_i$, not on the raw $(X_{i1}, X_{i2})$ separately. Computing $\bar{X}_1 - \bar{X}_2$ directly without using the pairing structure discards information about correlation.
- **Pairing when subjects are not actually matched.** If the two groups are truly independent (different people, no matching), forcing a pairing is incorrect and can reduce power by using $n-1$ instead of $2n-2$ degrees of freedom.

## Quick Check

Try these before using hints:

1. Differences are $\{+4, +2, -1, +3\}$. Compute $\bar{d}$ and $df$.
2. $\bar{d} = 5$, $s_d = 4$, $n = 16$. Compute $T$.
3. A researcher has 20 matched pairs. What $df$ does the paired t-test use?

*(Answers: 1. $\bar{d} = 2$, $df = 3$; 2. $T = 5/(4/4) = 5.0$; 3. $df = 19$)*
