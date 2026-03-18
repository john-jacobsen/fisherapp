# Multiple Linear Regression

## Overview

**Multiple linear regression (MLR)** extends SLR to multiple predictors: $Y = \beta_0 + \beta_1 X_1 + \cdots + \beta_p X_p + \varepsilon$. The OLS estimator and matrix formulas remain the same.

## Key Idea

$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{Y}$.

$\hat{\beta}_j$ is the estimated change in $Y$ per unit increase in $X_j$, holding all other predictors fixed.

**Adjusted $R^2$** penalizes for the number of predictors: $R^2_{adj} = 1 - (1-R^2)(n-1)/(n-p-1)$.

## Worked Examples

**Example 1: Interpret $\hat{\beta}_1 = 2.5$ in a model with $X_1$ = hours studied and $X_2$ = prior GPA.**

Each extra hour of study is associated with a 2.5-point score increase, holding prior GPA constant.

---

**Example 2: Adding a useless predictor**

$R^2$ always increases when adding variables. Adjusted $R^2$ may decrease — signaling the variable is not useful.

---

**Example 3: Multicollinearity**

If predictors are highly correlated, $\mathbf{X}^T\mathbf{X}$ is near-singular, inflating standard errors. Check VIF (variance inflation factor).

## Common Mistakes

- **Interpreting coefficients marginally.** MLR coefficients are partial (holding others fixed).
- **Using $R^2$ to compare models with different numbers of predictors.** Use adjusted $R^2$ or AIC.

## Quick Check

1. $\hat{\beta}_j$ in MLR represents what?
2. Why prefer adjusted $R^2$ over $R^2$?
3. What is multicollinearity?

*(Answers: partial effect of $X_j$ controlling for others; it penalizes for more predictors; high correlation among predictors)*
