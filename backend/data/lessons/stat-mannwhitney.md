# Mann-Whitney U Test

## Overview

The **Mann-Whitney U test** (Wilcoxon rank-sum test) is a nonparametric alternative to the two-sample $t$-test. It tests whether one group tends to have larger values than the other, without assuming normality.

## Key Idea

Rank all $n_1 + n_2$ observations from both groups together. The test statistic $U$ is based on the sum of ranks in one group. Under $H_0$ (no difference in distribution), $U$ has a known distribution.

$$U_1 = n_1 n_2 + \frac{n_1(n_1+1)}{2} - W_1$$

where $W_1$ is the sum of ranks in group 1.

## Worked Examples

**Example 1: Group A: 3,5,8; Group B: 1,4,6. $H_0$: same distribution.**

Ranks: 1→1, 3→2, 4→3, 5→4, 6→5, 8→6. $W_A = 2+4+6 = 12$. $U_A = 9 + 6 - 12 = 3$. $U_B = 9 - 3 = 6$.

---

**Example 2: Interpretation**

$U = 0$ means all of group A ranks above all of group B. $U = n_1 n_2 / 2$ is the expected value under $H_0$.

---

**Example 3: When to use**

Use when normality is doubtful, data is ordinal, or there are outliers.

## Common Mistakes

- **Using Mann-Whitney when data is paired.** Use Wilcoxon signed-rank test instead.
- **Thinking U tests the median.** It tests whether one distribution tends to be stochastically larger.

## Quick Check

1. What is the Mann-Whitney test's null hypothesis?
2. What does $U = 0$ indicate?
3. Normal equivalent of Mann-Whitney?

*(Answers: the two populations have the same distribution (stochastic equality); group 1 dominates entirely; two-sample t-test)*
