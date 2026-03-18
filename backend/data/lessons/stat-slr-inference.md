# SLR Inference

## Overview

After fitting a regression line, we want to make inferences: is $\beta_1$ significantly different from zero? What is the confidence interval for the mean response? **SLR inference** provides $t$-tests and intervals for each coefficient.

## Key Idea

Under normality: $\hat{\beta}_1 \sim N(\beta_1, \sigma^2/S_{XX})$.

$$T = \frac{\hat{\beta}_1 - \beta_{1,0}}{S/\sqrt{S_{XX}}} \sim t_{n-2} \quad \text{under } H_0: \beta_1 = \beta_{1,0}$$

where $S^2 = SS_E/(n-2)$ is the residual variance estimate.

## Worked Examples

**Example 1: Test $H_0: \beta_1 = 0$, $\hat{\beta}_1 = 2.5$, $S/\sqrt{S_{XX}} = 0.8$, $n=15$**

$T = 2.5/0.8 = 3.13$. $t_{13,0.025} = 2.16$. Reject — slope is significant.

---

**Example 2: 95% CI for $\beta_1$**

$\hat{\beta}_1 \pm t_{n-2,0.025} \cdot S/\sqrt{S_{XX}} = 2.5 \pm 2.16(0.8) = (0.77, 4.23)$.

---

**Example 3: CI for mean response vs. prediction interval**

CI for $E[Y|X=x_0]$: narrower. Prediction interval for a new $Y$: wider (adds $\sigma^2$ from $\varepsilon$).

## Common Mistakes

- **Using df $= n-1$ instead of $n-2$.** Regression uses $n-2$ df (estimating 2 parameters).
- **Confusing CI for mean response with PI for a new observation.**

## Quick Check

1. df for $t$-test of $\beta_1$ in SLR with $n=20$?
2. What does rejecting $H_0: \beta_1 = 0$ imply?
3. Which is wider: CI for mean or PI for new obs?

*(Answers: 18; $X$ is a significant predictor of $Y$; PI)*
