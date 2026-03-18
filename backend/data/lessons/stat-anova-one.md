# One-Way ANOVA

## Overview

**One-way ANOVA** tests whether the means of three or more groups are equal. It partitions total variability into variability between groups (explained) and within groups (unexplained).

## Key Idea

$H_0: \mu_1 = \mu_2 = \cdots = \mu_k$.

$$F = \frac{\text{MS}_{\text{between}}}{\text{MS}_{\text{within}}} = \frac{SS_B/(k-1)}{SS_W/(n-k)} \sim F_{k-1,\, n-k}$$

Reject when $F > F_{k-1,n-k,\alpha}$.

## Worked Examples

**Example 1: Three groups with equal size $n=5$ each. $SS_B = 40$, $SS_W = 30$.**

$MS_B = 40/2 = 20$. $MS_W = 30/12 = 2.5$. $F = 8$. $F_{2,12,0.05} = 3.89$. Reject.

---

**Example 2: ANOVA table**

| Source | SS | df | MS | F |
|---|---|---|---|---|
| Between | 40 | 2 | 20 | 8 |
| Within | 30 | 12 | 2.5 | |
| Total | 70 | 14 | | |

---

**Example 3: Post-hoc tests**

ANOVA tells you if any means differ; post-hoc tests (Tukey, Bonferroni) identify which pairs.

## Common Mistakes

- **Running multiple $t$-tests instead of ANOVA.** Multiple tests inflate Type I error.
- **Assuming ANOVA identifies which groups differ.** Need post-hoc tests for pairwise comparisons.

## Quick Check

1. $H_0$ in one-way ANOVA?
2. df for $F$ ratio with $k=4$ groups, $n=20$ total?
3. Large $F$ means what?

*(Answers: all group means equal; $F_{3,16}$; between-group variance >> within-group)*
