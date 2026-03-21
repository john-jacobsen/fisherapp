# Permutation Tests

## Overview

A **permutation test** computes the null distribution of a test statistic by considering all possible reassignments of the observed data under $H_0$. Rather than assuming the data come from a specific distribution (like normal), it constructs the reference distribution directly from the data. This makes permutation tests assumption-free and exact — the p-value is valid for any data, in any sample size.

## Key Idea

Under $H_0$, the group labels are exchangeable — any assignment of observations to groups is equally likely. You compute the test statistic $T_{obs}$ for the actual labeling, then compute $T^*$ for every possible relabeling. The p-value is the fraction of relabelings that produce a statistic at least as extreme:

$$p = \frac{\#\{\text{permutations with } T^* \geq T_{obs}\}}{\text{total permutations}}$$

For two groups of sizes $n_1$ and $n_2$, the total number of permutations is $\binom{n_1 + n_2}{n_1}$.

## Worked Examples

**Example 1: Enumerate all permutations**

Group A: $\{4, 6\}$, Group B: $\{1, 3\}$. Test whether Group A has a larger mean. $T_{obs} = \bar{X}_A - \bar{X}_B = 5 - 2 = 3$.

The pool is $\{1, 3, 4, 6\}$. Assign any 2 to Group A and the rest to Group B. There are $\binom{4}{2} = 6$ ways:

| Group A    | Group B    | $T^* = \bar{A} - \bar{B}$ |
|------------|------------|--------------------------|
| $\{1, 3\}$ | $\{4, 6\}$ | $2 - 5 = -3$             |
| $\{1, 4\}$ | $\{3, 6\}$ | $2.5 - 4.5 = -2$         |
| $\{1, 6\}$ | $\{3, 4\}$ | $3.5 - 3.5 = 0$          |
| $\{3, 4\}$ | $\{1, 6\}$ | $3.5 - 3.5 = 0$          |
| $\{3, 6\}$ | $\{1, 4\}$ | $4.5 - 2.5 = 2$          |
| $\{4, 6\}$ | $\{1, 3\}$ | $5 - 2 = 3$              |

Only 1 out of 6 permutations has $T^* \geq 3$ (the original labeling). So $p = 1/6 \approx 0.167$. At $\alpha = 0.05$, you fail to reject $H_0$.

---

**Example 2: Why permutation tests are exact**

The p-value $1/6$ from Example 1 required no distributional assumptions. If $H_0$ is true (group labels are irrelevant), each of the 6 labelings is equally probable. By definition, the probability of getting $T^*$ at least as large as the observed value is exactly $1/6$. No approximation is involved. This exactness holds even for tiny samples where asymptotic tests (z, t, chi-squared) may be inaccurate.

The trade-off is computational cost. With $n_1 = n_2 = 15$, the number of permutations is $\binom{30}{15} \approx 155$ million. Enumerating all of them is feasible for computers but slow. For $n_1 = n_2 = 30$, it becomes impractical to enumerate all $\binom{60}{30} \approx 1.18 \times 10^{17}$ permutations.

---

**Example 3: Random permutation sampling**

When exact enumeration is infeasible, you approximate the permutation distribution by drawing a large random sample of relabelings (typically 10,000–100,000). For each random relabeling, compute $T^*$. The approximate p-value is the fraction of these sampled $T^*$ values that equal or exceed $T_{obs}$:

$$\hat{p} \approx \frac{\#\{T^* \geq T_{obs}\}}{B}$$

where $B$ is the number of random permutations used. With $B = 10{,}000$, the standard error of $\hat{p}$ is at most $\sqrt{0.25/10{,}000} = 0.005$, which is usually sufficient precision for hypothesis testing. This randomized permutation test loses only a tiny amount of exactness in exchange for massive computational savings.

## Common Mistakes

- **Resampling with replacement (bootstrapping) instead of without.** A permutation test relabels the observed data without replacement — each data point appears exactly once in each permutation. Resampling with replacement is the bootstrap, a different method for different purposes.
- **Counting only $T^* > T_{obs}$ instead of $T^* \geq T_{obs}$.** The observed labeling is itself one of the valid permutations. It must be included in the count, or the p-value will be systematically too small.
- **Using a one-sided test when the original hypothesis was two-sided.** For a two-sided test, count permutations where $|T^*| \geq |T_{obs}|$, not just $T^* \geq T_{obs}$.

## Quick Check

Try these before using hints:

1. Two groups of size 2 each: how many total permutations are there?
2. If 3 out of 10 random permutations give $T^* \geq T_{obs}$, what is the estimated p-value?
3. Why does the permutation test not require a normality assumption?

*(Answers: 1. $\binom{4}{2} = 6$; 2. $\hat{p} = 3/10 = 0.30$; 3. The null distribution is built from the observed data directly, not from a parametric model)*
