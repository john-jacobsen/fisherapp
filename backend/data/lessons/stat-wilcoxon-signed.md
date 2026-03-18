# Wilcoxon Signed-Rank Test

## Overview

The **Wilcoxon signed-rank test** is a nonparametric alternative to the one-sample or paired $t$-test. It tests whether the median of differences equals zero, using the ranks of the absolute differences.

## Key Idea

1. Compute $D_i = X_i - \mu_0$ (or paired differences).
2. Rank $|D_i|$ from smallest to largest (drop zeros).
3. $W^+ = $ sum of ranks for positive $D_i$.

Under $H_0$ (symmetric around 0), $E[W^+] = n(n+1)/4$.

## Worked Examples

**Example 1: Data: 3, -1, 4, -2. $H_0$: median $= 0$.**

$|D|$: 3, 1, 4, 2. Ranks: 1→2, 2→1, 3→3, 4→4. $W^+ = 3 + 4 = 7$ (positive values: 3 and 4). Compare to table.

---

**Example 2: Advantage over sign test**

Signed-rank uses magnitude, not just sign — more powerful.

---

**Example 3: Assumption**

The distribution of differences must be symmetric around the median.

## Common Mistakes

- **Using Wilcoxon signed-rank when the distribution is asymmetric.** The symmetry assumption is required.
- **Confusing with Mann-Whitney.** Signed-rank is one-sample or paired; Mann-Whitney is two independent samples.

## Quick Check

1. What does the signed-rank test assume?
2. When do you drop differences?
3. Nonparametric equivalent of the paired $t$-test?

*(Answers: symmetric distribution around $\mu_0$; when $D_i = 0$; Wilcoxon signed-rank)*
