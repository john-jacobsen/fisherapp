# Kruskal-Wallis Test

## Overview

The **Kruskal-Wallis test** is a nonparametric alternative to one-way ANOVA. It tests whether $k \geq 2$ independent groups tend to produce different values, without requiring the data to be normally distributed or the groups to have equal variances. Like the Mann-Whitney test for two groups, it works by replacing raw data with ranks. If $H_0$ is true (all groups have the same distribution), the ranks should be spread roughly evenly across groups.

## Key Idea

Rank all $n = n_1 + n_2 + \cdots + n_k$ observations together from 1 to $n$. Let $R_i$ denote the sum of ranks in group $i$. The Kruskal-Wallis statistic is:

$$H = \frac{12}{n(n+1)}\sum_{i=1}^k \frac{R_i^2}{n_i} - 3(n+1) \sim \chi^2_{k-1}$$

Under $H_0$, the average rank in each group should be close to $(n+1)/2$. The formula measures weighted deviations of each group's rank sum from what you'd expect under equal distributions. For $n$ large enough (roughly $n_i \geq 5$ per group), $H$ follows a $\chi^2$ distribution with $k-1$ degrees of freedom.

## Worked Examples

**Example 1: Compute $H$ for three groups of size 3**

Group 1: $\{2, 5, 8\}$, Group 2: $\{1, 4, 7\}$, Group 3: $\{3, 6, 9\}$. Total $n = 9$.

Rank all 9 observations: $1 \to 1$, $2 \to 2$, $3 \to 3$, $4 \to 4$, $5 \to 5$, $6 \to 6$, $7 \to 7$, $8 \to 8$, $9 \to 9$.

Rank sums: $R_1 = 2 + 5 + 8 = 15$, $R_2 = 1 + 4 + 7 = 12$, $R_3 = 3 + 6 + 9 = 18$.

$$H = \frac{12}{9 \cdot 10}\left(\frac{15^2}{3} + \frac{12^2}{3} + \frac{18^2}{3}\right) - 3(10)$$

$$= \frac{12}{90}\left(75 + 48 + 108\right) - 30 = \frac{12}{90}(231) - 30 = 30.8 - 30 = 0.8$$

With $df = k - 1 = 2$ and $\chi^2_{0.05, 2} = 5.99$, you fail to reject $H_0$. The rank sums are not sufficiently unequal.

---

**Example 2: Compare to one-way ANOVA on the same data**

Using the same data as Example 1, compute the group means: $\bar{x}_1 = 5$, $\bar{x}_2 = 4$, $\bar{x}_3 = 6$, grand mean $= 5$. MSB = $3[(5-5)^2 + (4-5)^2 + (6-5)^2]/2 = 3 \cdot 2 / 2 = 3$. MSW requires computing within-group variance; for this perfectly spread dataset, $s_i^2 = 9$ for each group, so MSW $= 9$. $F = 3/9 = 0.33$, also not significant.

Both tests agree here: no significant difference. When data are normally distributed, one-way ANOVA is slightly more powerful than Kruskal-Wallis because ANOVA uses the actual values while Kruskal-Wallis uses only ranks (and ranks discard some information). For non-normal data, Kruskal-Wallis can be more powerful than ANOVA.

---

**Example 3: When Kruskal-Wallis is preferred and its limitation**

Kruskal-Wallis is preferred when: (1) the data are clearly non-normal (e.g., highly skewed or heavy-tailed) and samples are too small for the Central Limit Theorem to rescue ANOVA, (2) data are ordinal (e.g., pain ratings from 1–10), or (3) there are extreme outliers that would distort ANOVA's sum-of-squares calculations.

An important limitation: Kruskal-Wallis tests whether the rank distributions differ across groups, not specifically whether the means differ. Two groups can have the same mean but different variances or shapes, causing Kruskal-Wallis to reject $H_0$ even when means are equal. When you specifically care about means, ANOVA is more targeted. After rejecting with Kruskal-Wallis, use Dunn's test for pairwise post-hoc comparisons.

## Common Mistakes

- **Forgetting to assign midranks for tied observations.** When two or more observations have the same value, assign each the average of the ranks they would occupy. Failing to do so distorts $R_i$ and $H$.
- **Using Kruskal-Wallis for paired or dependent groups.** Kruskal-Wallis requires independent groups. For repeated measures or matched data, use the Friedman test.
- **Interpreting a non-significant result as evidence that all distributions are identical.** Failing to reject $H_0$ only means you lack enough evidence to detect a difference — the test may simply be underpowered for small $n$.

## Quick Check

Try these before using hints:

1. Three groups of sizes $n_1 = n_2 = n_3 = 4$. What is $n$ and what is $df$ for $H$?
2. If $H = 7.5$ and $df = 2$, is the test significant at $\alpha = 0.05$ (critical value $5.99$)?
3. Under $H_0$ with $n = 12$, what should $R_1/n_1$ be approximately equal to for each group?

*(Answers: 1. $n = 12$, $df = 2$; 2. Yes, reject ($7.5 > 5.99$); 3. The average rank $(n+1)/2 = 6.5$ — each group should average about rank 6.5)*
