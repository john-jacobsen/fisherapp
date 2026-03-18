# Simple Linear Regression

## Overview

**Simple linear regression (SLR)** models the relationship between a response $Y$ and a predictor $X$ as a line. The goal is to estimate the intercept and slope from data.

## Key Idea

Model: $Y_i = \beta_0 + \beta_1 X_i + \varepsilon_i$, where $\varepsilon_i \overset{iid}{\sim} N(0,\sigma^2)$.

OLS estimates:

$$\hat{\beta}_1 = \frac{\sum(X_i - \bar{X})(Y_i - \bar{Y})}{\sum(X_i - \bar{X})^2} = \frac{S_{XY}}{S_{XX}}, \quad \hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}$$

## Worked Examples

**Example 1: $(X,Y)$ pairs: $(1,2),(2,4),(3,5)$. Fit SLR.**

$\bar{X}=2$, $\bar{Y}=11/3$. $S_{XY} = 1.5+0+(-5/3) = ...$. Actually: $S_{XY}=(1-2)(2-11/3)+(2-2)(...)+(3-2)(5-11/3) = 5/3 + 0 + 4/3 = 3$. $S_{XX} = 2$. $\hat{\beta}_1 = 1.5$. $\hat{\beta}_0 = 11/3 - 3 = 2/3$.

---

**Example 2: Interpretation of $\hat{\beta}_1$**

For each 1-unit increase in $X$, $Y$ is expected to increase by $\hat{\beta}_1$.

---

**Example 3: $R^2$ coefficient of determination**

$R^2 = 1 - SS_E/SS_T$. Proportion of variance in $Y$ explained by $X$.

## Common Mistakes

- **Extrapolating outside the data range.** The linear model may not hold there.
- **Interpreting $\hat{\beta}_1$ causally.** Correlation $\ne$ causation.

## Quick Check

1. OLS minimizes what?
2. $\hat{\beta}_0$ interpretation when $X=0$?
3. $R^2=0.8$ means what?

*(Answers: $\sum(Y_i - \hat{Y}_i)^2$; estimated mean of $Y$ when $X=0$; 80% of variance in $Y$ explained by $X$)*
