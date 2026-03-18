# Permutation Tests

## Overview

A **permutation test** is a nonparametric test that generates the null distribution by reassigning the group labels many times. It requires minimal assumptions and is exact for exchangeable data.

## Key Idea

1. Compute the observed test statistic $T_{\text{obs}}$.
2. Randomly permute the group labels $B$ times; compute $T^*_b$ for each.
3. $p$-value $= $ fraction of $T^*_b \ge T_{\text{obs}}$.

## Worked Examples

**Example 1: Two groups, 3 observations each. Observed mean difference = 5.**

There are $\binom{6}{3} = 20$ possible permutations. Count how many yield a difference $\ge 5$. If 1 out of 20: $p = 0.05$.

---

**Example 2: Continuous test statistic**

Use $B = 10{,}000$ random permutations. p-value = fraction with statistic more extreme than observed.

---

**Example 3: What null hypothesis does it test?**

$H_0$: the labels are exchangeable — the two groups come from the same distribution.

## Common Mistakes

- **Insufficient permutations $B$.** Use at least 1000, preferably 10000+.
- **Permuting when observations are not exchangeable under $H_0$** (e.g., dependent data).

## Quick Check

1. What is the null distribution in a permutation test?
2. Exact p-value for $B = 20$ permutations with 2 more extreme?
3. Advantage over $t$-test?

*(Answers: distribution of $T^*$ over all permutations; 2/20 = 0.1; no normality assumption needed)*
