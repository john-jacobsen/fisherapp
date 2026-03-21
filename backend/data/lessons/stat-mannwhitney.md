# Mann-Whitney U Test

## Overview

The **Mann-Whitney U test** is a nonparametric test that compares two independent groups without assuming the data follow a normal distribution. Instead of comparing means, it tests whether one group tends to produce larger values than the other. The test works by pooling all observations, ranking them from smallest to largest, and then examining whether the ranks are distributed evenly between groups.

## Key Idea

Pool both groups together and rank all $n_1 + n_2$ observations from 1 to $n_1 + n_2$. Let $R_1$ be the sum of ranks in Group 1. Then compute:

$$U_1 = n_1 n_2 + \frac{n_1(n_1+1)}{2} - R_1$$

The term $n_1(n_1+1)/2$ is the smallest possible rank sum for Group 1 (if all Group 1 observations were smallest). So $U_1$ counts how many times a Group 2 observation exceeds a Group 1 observation. Also compute $U_2 = n_1 n_2 - U_1$, and use $U = \min(U_1, U_2)$ as the test statistic. Small $U$ means more separation between groups.

## Worked Examples

**Example 1: Small example**

Group A: $\{3, 5, 7\}$, Group B: $\{1, 4, 9\}$. Pool and rank all 6 values:

| Value | 1 | 3 | 4 | 5 | 7 | 9 |
|-------|---|---|---|---|---|---|
| Group | B | A | B | A | A | B |
| Rank  | 1 | 2 | 3 | 4 | 5 | 6 |

$R_1$ (sum of Group A ranks) $= 2 + 4 + 5 = 11$. With $n_1 = n_2 = 3$:

$$U_1 = 3 \cdot 3 + \frac{3 \cdot 4}{2} - 11 = 9 + 6 - 11 = 4$$

$U_2 = 9 - 4 = 5$, so $U = \min(4, 5) = 4$. For $n_1 = n_2 = 3$ and $\alpha = 0.05$, the critical value is 0 (two-sided). Since $U = 4 > 0$, you fail to reject $H_0$. The groups overlap too much to conclude a systematic difference.

---

**Example 2: Larger example**

Group 1: $\{12, 15, 18, 20, 25\}$, Group 2: $\{8, 10, 14, 16, 22\}$, so $n_1 = n_2 = 5$.

Rank all 10 observations: $8 \to 1$, $10 \to 2$, $12 \to 3$, $14 \to 4$, $15 \to 5$, $16 \to 6$, $18 \to 7$, $20 \to 8$, $22 \to 9$, $25 \to 10$.

$R_1 = 3 + 5 + 7 + 8 + 10 = 33$. Then $U_1 = 5 \cdot 5 + 15 - 33 = 7$, $U_2 = 25 - 7 = 18$, $U = 7$. For $n_1 = n_2 = 5$, the two-sided critical value at $\alpha = 0.05$ is 2. Since $7 > 2$, you fail to reject $H_0$. The rank sums are not extreme enough to conclude a difference.

---

**Example 3: When Mann-Whitney is preferred**

The Mann-Whitney test is preferable to the t-test when: (1) data are heavily skewed and the sample size is too small for the Central Limit Theorem to apply, (2) data are ordinal (e.g., survey ratings on a 1–5 scale) where means are not meaningful, or (3) outliers are present that would distort the mean. Because the test operates on ranks, extreme outliers have no more influence than any other observation in the extreme tail — rank 100 out of 100 is the same whether the value is 9.9 or 9,900.

## Common Mistakes

- **Treating U as if larger is always better.** You use $U = \min(U_1, U_2)$ and compare to the lower critical value. The test rejects for small $U$, not large $U$.
- **Confusing Mann-Whitney with the Wilcoxon signed-rank test.** Mann-Whitney is for independent groups; the Wilcoxon signed-rank test is for paired data. Both use ranking, but the procedure and hypotheses differ.
- **Ignoring ties.** When two observations have the same value, assign them the average of the ranks they would have occupied. Ignoring ties (giving arbitrary ranks) can distort $R_1$ and $U$.

## Quick Check

Try these before using hints:

1. Group A: $\{2, 6\}$, Group B: $\{4, 8\}$. Rank all four values and compute $R_1$ (Group A's rank sum).
2. Using $n_1 = n_2 = 2$ and $R_1 = 3$, compute $U_1$.
3. Name one situation where Mann-Whitney is clearly preferable to an independent-samples t-test.

*(Answers: 1. Ranks: 2→1, 4→2, 6→3, 8→4; $R_1 = 1 + 3 = 4$; 2. $U_1 = 4 + 3 - 4 = 3$; 3. When data are ordinal or severely skewed)*
