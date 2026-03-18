# Regression Diagnostics

## Overview

**Regression diagnostics** check whether the assumptions of linear regression (linearity, normality of errors, homoscedasticity, independence) are satisfied. Violations can invalidate inferences.

## Key Idea

Four key assumptions (LINE):
1. **L**inearity: $E[Y|X]$ is linear in $X$
2. **I**ndependence: residuals are independent
3. **N**ormality: residuals $\sim N(0,\sigma^2)$
4. **E**qual variance (homoscedasticity): $\text{Var}(\varepsilon_i) = \sigma^2$

Check with residual plots, QQ-plots, and statistical tests.

## Worked Examples

**Example 1: Residual vs. fitted plot**

Random scatter around zero → OK. Fan-shaped → heteroscedasticity. Curved → non-linearity.

---

**Example 2: QQ-plot of residuals**

Points near the diagonal → normality. Heavy tails → violation.

---

**Example 3: Influential observations**

Cook's distance measures how much the estimates change if observation $i$ is removed. Cook's $D > 1$ is often flagged.

## Common Mistakes

- **Ignoring outliers without investigation.** An outlier may reveal a data error or an important phenomenon.
- **Concluding non-normality from small samples.** QQ-plots are unreliable for $n < 30$.

## Quick Check

1. What plot reveals heteroscedasticity?
2. What does a curved residual vs. fitted plot suggest?
3. What does Cook's distance measure?

*(Answers: residuals vs. fitted (fan shape); non-linearity; influence of each observation on $\hat{\boldsymbol{\beta}}$)*
