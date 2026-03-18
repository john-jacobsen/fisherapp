# MLR Inference

## Overview

In MLR, inference involves testing individual coefficients, testing groups of coefficients simultaneously (F-test), and constructing confidence intervals.

## Key Idea

Individual test: $T_j = \hat{\beta}_j / \text{SE}(\hat{\beta}_j) \sim t_{n-p-1}$ under $H_0: \beta_j = 0$.

**Global F-test:** $H_0: \beta_1 = \cdots = \beta_p = 0$:

$$F = \frac{SS_R/p}{SS_E/(n-p-1)} \sim F_{p, n-p-1}$$

## Worked Examples

**Example 1: $t$-test for $\beta_1$**

$\hat{\beta}_1 = 3.2$, $\text{SE} = 1.1$, $n=50$, $p=3$. $T = 3.2/1.1 = 2.91$. $t_{46,0.025} \approx 2.01$. Reject.

---

**Example 2: Global F-test**

If the global $F$ is not significant, no individual predictors are likely significant.

---

**Example 3: Partial F-test**

Test whether adding 2 new predictors improves the model: $F = \frac{(SS_{E,\text{reduced}} - SS_{E,\text{full}})/2}{SS_{E,\text{full}}/(n-p-1)}$.

## Common Mistakes

- **Performing many individual $t$-tests without a global test.** Multiple comparisons inflate Type I error.
- **Wrong df.** $t_{n-p-1}$ has $n-p-1$ df ($p$ predictors, not counting intercept), or $n-p-1$ where $p$ includes intercept.

## Quick Check

1. df for individual $t$-test in MLR with $n=30$, 4 predictors (+ intercept)?
2. What does the global F-test test?
3. How do you test if two additional predictors improve model fit?

*(Answers: 25; whether ALL predictors together explain anything; partial F-test)*
