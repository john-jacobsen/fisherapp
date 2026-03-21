# Multiple Linear Regression

## Overview

**Multiple linear regression** extends simple linear regression to $p$ predictors: $Y = \beta_0 + \beta_1 X_1 + \cdots + \beta_p X_p + \varepsilon$, where $\varepsilon \sim N(0, \sigma^2)$. The key distinction from SLR is that each coefficient $\beta_j$ represents the effect of $X_j$ while holding all other predictors fixed — these are called **partial effects**. In matrix form the model is $\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$, where $\mathbf{X}$ is now $n \times (p+1)$.

## Key Idea

The OLS estimator is the same formula as in SLR, just with a larger design matrix:

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{Y}$$

Adding more predictors always increases $R^2$ (the model can only fit better), so you use **adjusted $R^2$** to compare models of different sizes: $R^2_{\text{adj}} = 1 - \frac{(1-R^2)(n-1)}{n-p-1}$. The adjustment penalizes for the number of parameters $p$.

## Worked Examples

**Example 1: Interpret a coefficient in a two-predictor model**

You fit exam score $Y$ using hours studied $X_1$ and prior GPA $X_2$, obtaining $\hat{\beta}_2 = 3$.

Interpretation: holding $X_1$ (study hours) fixed, a one-unit increase in prior GPA is associated with a predicted 3-point increase in exam score. The phrase "holding other predictors fixed" is what makes this a partial effect — it is not the marginal effect of GPA ignoring study time. If you had run a simple regression of $Y$ on $X_2$ alone, you would get a different (marginal) coefficient because $X_1$ and $X_2$ may be correlated.

---

**Example 2: Why $R^2$ always increases — and why adjusted $R^2$ does not**

Suppose you add a predictor $X_3$ that is pure random noise. Because OLS minimizes $\text{SSE}$, adding any variable (even noise) can only decrease SSE or keep it the same, so $R^2 = 1 - \text{SSE}/\text{SST}$ can only increase. This makes $R^2$ useless for comparing models of different sizes.

Adjusted $R^2$ penalizes: $R^2_{\text{adj}} = 1 - \frac{\text{SSE}/(n-p-1)}{\text{SST}/(n-1)}$. If $X_3$ does not reduce SSE enough to offset the loss of one degree of freedom, $R^2_{\text{adj}}$ will decrease — correctly signaling that $X_3$ is not useful.

---

**Example 3: Multicollinearity inflates standard errors**

Suppose $X_1$ = income and $X_2$ = wealth, which are highly correlated. When $\mathbf{X}^\top\mathbf{X}$ is nearly singular, its inverse has large entries, and the variances of $\hat{\beta}_1$ and $\hat{\beta}_2$ blow up. Intuitively: the data cannot distinguish whether an outcome is due to income or wealth when they almost always move together. The fitted values $\hat{\mathbf{Y}}$ are still accurate, but the individual coefficient estimates are unreliable. The variance inflation factor (VIF) quantifies this: $\text{VIF}_j > 10$ is often flagged as problematic.

## Common Mistakes

- **Interpreting MLR coefficients as marginal effects.** Each $\hat{\beta}_j$ is a partial effect — it controls for the other predictors in the model. If you remove $X_2$ from the model, $\hat{\beta}_1$ will generally change, sometimes dramatically.

- **Using $R^2$ to compare models with different numbers of predictors.** Because $R^2$ never decreases when you add a variable, you must use adjusted $R^2$, AIC, or BIC to compare models of different complexity.

## Quick Check

Try these before using hints:

1. In a model with $p = 3$ predictors and $n = 50$, how many degrees of freedom does $\hat{\sigma}^2 = \text{SSE}/(n-p-1)$ use?
2. If $\hat{\beta}_1 = 2$ in a model that also includes $X_2$, what does this mean?
3. Why can multicollinearity exist even when the overall $F$-test is significant?

*(Answers: 1. $df = 46$; 2. Holding $X_2$ fixed, a 1-unit increase in $X_1$ is associated with a predicted 2-unit increase in $Y$; 3. The predictors together explain $Y$ well, but the individual effects cannot be disentangled)*
