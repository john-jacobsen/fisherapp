# One-Way ANOVA

## Overview

**One-way ANOVA** (Analysis of Variance) tests whether $k \geq 2$ group means are all equal: $H_0: \mu_1 = \mu_2 = \cdots = \mu_k$. Rather than comparing each pair of means with separate t-tests, ANOVA compares the variation between groups to the variation within groups. If the groups truly have the same mean, between-group variation should be about as large as within-group variation — just due to chance.

## Key Idea

ANOVA partitions the total variability in the data into two components. The F-statistic is their ratio:

$$F = \frac{\text{MSB}}{\text{MSW}} = \frac{\text{SSB}/(k-1)}{\text{SSW}/(n-k)} \sim F_{k-1,\,n-k}$$

**SSB** (Sum of Squares Between) measures how much group means deviate from the grand mean. **SSW** (Sum of Squares Within) measures the typical variability of individual observations around their own group mean. If $H_0$ is true, both MSB and MSW estimate the same population variance $\sigma^2$, so $F \approx 1$. A large $F$ means the group means are more spread out than within-group noise would predict.

## Worked Examples

**Example 1: Compute the F-statistic**

Three teaching methods are each applied to $n_1 = n_2 = n_3 = 5$ students. Group means are $\bar{x}_1 = 10$, $\bar{x}_2 = 12$, $\bar{x}_3 = 14$. The grand mean is $\bar{x} = (10 + 12 + 14)/3 = 12$. The within-group mean square is $\text{MSW} = 4$.

Compute SSB — the between-group sum of squares:

$$\text{SSB} = \sum_{i=1}^{3} n_i(\bar{x}_i - \bar{x})^2 = 5(10-12)^2 + 5(12-12)^2 + 5(14-12)^2 = 5(4) + 0 + 5(4) = 40$$

Each term measures how far one group's mean strays from the grand mean, weighted by that group's size.

$$\text{MSB} = \frac{\text{SSB}}{k-1} = \frac{40}{2} = 20, \qquad F = \frac{20}{4} = 5.0$$

With $df_1 = k - 1 = 2$ and $df_2 = n - k = 15 - 3 = 12$, the critical value is $F_{0.05, 2, 12} = 3.89$. Since $5.0 > 3.89$, you **reject $H_0$**. The teaching methods do not all produce the same average score.

---

**Example 2: Full ANOVA table**

Using Example 1 values (SSB = 40, MSW = 4, so SSW = $4 \times 12 = 48$, SST = SSB + SSW = 88):

| Source  | SS | df | MS | F   |
|---------|----|----|----|-----|
| Between | 40 | 2  | 20 | 5.0 |
| Within  | 48 | 12 | 4  |     |
| Total   | 88 | 14 |    |     |

The ANOVA table organizes the partition of variability: SST = SSB + SSW and $df_{total} = df_{between} + df_{within}$. MSW is the pooled estimate of within-group variance, assuming all groups have the same population variance $\sigma^2$.

---

**Example 3: Why ANOVA instead of multiple t-tests**

Suppose you have 5 groups and perform all $\binom{5}{2} = 10$ pairwise t-tests, each at $\alpha = 0.05$. The probability of at least one false positive (incorrectly rejecting at least one true $H_0$) is approximately $1 - (0.95)^{10} \approx 0.40$. Running 10 tests inflates the family-wise error rate from 5% to roughly 40%.

ANOVA tests all group means simultaneously in a single test, maintaining the Type I error rate at exactly $\alpha$. If ANOVA rejects $H_0$, you can follow up with post-hoc tests (e.g., Tukey's HSD) that adjust for multiple comparisons. ANOVA is the correct first step — it controls the error rate that multiple t-tests would inflate.

## Common Mistakes

- **Concluding which means differ after rejecting $H_0$.** ANOVA only tells you that not all means are equal. To identify which pairs differ, you need a post-hoc procedure such as Tukey's or Bonferroni correction.
- **Ignoring the equal-variance assumption.** ANOVA assumes all groups have the same population variance $\sigma^2$. If variances differ substantially across groups, MSW is a poor estimate of any one group's variance. Use Welch's ANOVA or a variance-stabilizing transformation instead.
- **Confusing $df$ for between and within.** Between uses $k - 1$ (number of groups minus one); within uses $n - k$ (total observations minus number of groups). Mixing them up gives wrong F-critical values.

## Quick Check

Try these before using hints:

1. $k = 4$ groups, $n = 20$ total. What are $df_{between}$ and $df_{within}$?
2. SSB = 30, $df_{between} = 3$, SSW = 60, $df_{within} = 12$. Compute $F$.
3. Why does a large $F$-statistic provide evidence against $H_0$?

*(Answers: 1. $df_{between} = 3$, $df_{within} = 16$; 2. $F = (30/3)/(60/12) = 10/5 = 2.0$; 3. Large $F$ means between-group variation is much larger than within-group variation, which is unlikely if all group means are equal)*
