# Kruskal-Wallis Test

## Overview

The **Kruskal-Wallis test** is the nonparametric alternative to one-way ANOVA. It tests whether samples from $k$ groups come from the same distribution, using ranks instead of raw values.

## Key Idea

Rank all $N$ observations across groups. Let $R_i$ be the sum of ranks in group $i$.

$$H = \frac{12}{N(N+1)} \sum_{i=1}^k \frac{R_i^2}{n_i} - 3(N+1) \sim \chi^2_{k-1}$$

## Worked Examples

**Example 1: 3 groups, $n_i = 4$ each, $N = 12$. Rank sums $R_1 = 30, R_2 = 25, R_3 = 23$.**

$H = \frac{12}{12 \times 13}\left(\frac{900+625+529}{4}\right) - 3(13) = \frac{12}{156} \times 513.5 - 39 \approx 0.48$.

---

**Example 2: When to use**

When ANOVA normality assumption is violated or data is ordinal.

---

**Example 3: Post-hoc for Kruskal-Wallis**

Use Dunn's test or pairwise Mann-Whitney with Bonferroni correction.

## Common Mistakes

- **Applying Kruskal-Wallis for continuous, normally distributed data.** ANOVA is more powerful in that case.
- **Concluding equal means from fail-to-reject.** KW tests the distribution, not just the mean.

## Quick Check

1. What does the Kruskal-Wallis test use instead of raw values?
2. $H \sim ?$ asymptotically?
3. Parametric equivalent of Kruskal-Wallis?

*(Answers: ranks; $\chi^2_{k-1}$; one-way ANOVA)*
