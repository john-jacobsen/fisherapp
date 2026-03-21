# Wilcoxon Signed-Rank Test

## Overview

The **Wilcoxon signed-rank test** is a nonparametric alternative to the paired t-test. Like the paired t-test, it analyzes differences between paired observations. Unlike the paired t-test, it does not assume the differences are normally distributed — instead, it only requires that the distribution of differences is symmetric around 0 under $H_0$. It uses the magnitudes of the differences, not just their signs, which makes it more powerful than the simpler sign test.

## Key Idea

Compute the differences $D_i = X_{i1} - X_{i2}$, discard any $D_i = 0$, then rank the absolute values $|D_i|$ from smallest to largest. The test statistic is the sum of ranks corresponding to positive differences:

$$W^+ = \sum_{i:\,D_i > 0} R_i$$

Under $H_0$ (median difference = 0), the positive and negative differences should be roughly balanced in both number and magnitude, so $W^+$ should be near $n(n+1)/4$. Very large or very small values of $W^+$ provide evidence against $H_0$.

## Worked Examples

**Example 1: Compute $W^+$**

Six pairs have differences $\{+3, -1, +4, +2, -5, +1\}$. First rank the absolute values:

| $D_i$ | $|D_i|$ | Rank | Sign |
|--------|---------|------|------|
| $-1$   | 1       | 1.5  | $-$  |
| $+1$   | 1       | 1.5  | $+$  |
| $+2$   | 2       | 3    | $+$  |
| $+3$   | 3       | 4    | $+$  |
| $+4$   | 4       | 5    | $+$  |
| $-5$   | 5       | 6    | $-$  |

The two values of $|D_i| = 1$ tie for ranks 1 and 2, so each gets rank $(1+2)/2 = 1.5$. This is the midrank rule — it ensures tied observations are treated symmetrically.

$$W^+ = 1.5 + 3 + 4 + 5 = 13.5$$

---

**Example 2: Test $H_0$ for small $n$**

With $n = 6$ (no zeros), and $W^+ = 13.5$, use a table of critical values for the Wilcoxon signed-rank test. At $\alpha = 0.05$ two-sided with $n = 6$, the critical region is $W^+ \leq 2$ or $W^+ \geq 19$. Since $13.5$ falls in $[3, 18]$, you **fail to reject $H_0$**. The rank pattern is not extreme enough to conclude the median difference is nonzero.

For large $n$ (roughly $n > 20$), $W^+$ is approximately normal with mean $n(n+1)/4$ and variance $n(n+1)(2n+1)/24$, so you can convert to a $z$-score and use standard normal critical values.

---

**Example 3: Signed-rank vs sign test**

The sign test simply counts positive differences and ignores their size. It treats a difference of $+0.01$ identically to a difference of $+100$. The signed-rank test uses the ranks of the magnitudes, so a larger positive difference contributes more evidence for $H_1: \text{median} > 0$ than a tiny positive difference.

For Example 1, the sign test would count 4 positives and 2 negatives out of 6 total, and compare to a binomial distribution. The signed-rank test uses $W^+ = 13.5$, incorporating the fact that the two negative differences (ranks 1.5 and 6) are partially offset by four positive differences of varying size. By using magnitude information, the signed-rank test is more powerful than the sign test when the symmetry assumption holds.

## Common Mistakes

- **Forgetting to handle zeros.** If $D_i = 0$, that observation provides no information about the direction of the effect. Drop it from the analysis and reduce $n$ accordingly.
- **Forgetting midranks for ties.** When two absolute differences are equal, assign each the average of the ranks they would have occupied. Assigning arbitrary ranks disrupts the symmetry that the test relies on.
- **Using the signed-rank test on independent groups.** This test requires paired data. For independent groups, use the Mann-Whitney U test.

## Quick Check

Try these before using hints:

1. Differences are $\{+5, -2, +3\}$. Rank the absolute values and compute $W^+$.
2. Why does the Wilcoxon signed-rank test have more power than the sign test?
3. If $n = 25$, what is the mean of $W^+$ under $H_0$?

*(Answers: 1. Ranks: $|-2|=1$, $|+3|=2$, $|+5|=3$; $W^+ = 2 + 3 = 5$; 2. It uses magnitude information, not just the sign of each difference; 3. $25 \cdot 26/4 = 162.5$)*
