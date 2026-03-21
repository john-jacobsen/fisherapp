# Inference in Multiple Linear Regression

## Overview

In multiple linear regression, inference involves two levels: testing **individual coefficients** (is predictor $j$ useful after accounting for the others?) and testing **all predictors jointly** (does the model explain anything at all?). The first uses a $t$-test; the second uses the **F-test**. Understanding when each is appropriate — and why they can give different answers — is essential for interpreting regression output correctly.

## Key Idea

Each coefficient has its own $t$-test: $T_j = \hat{\beta}_j / \text{SE}(\hat{\beta}_j)$, which follows a $t_{n-p-1}$ distribution under $H_0: \beta_j = 0$. The global F-test asks whether all slope coefficients are simultaneously zero:

$$F = \frac{\text{SSR}/p}{\text{SSE}/(n-p-1)} \sim F_{p,\,n-p-1}$$

Here SSR $= \sum(\hat{Y}_i - \bar{Y})^2$ is the regression sum of squares (variance explained by the model) and SSE $= \sum(Y_i - \hat{Y}_i)^2$ is the residual sum of squares.

## Worked Examples

**Example 1: $t$-test for an individual coefficient**

You fit a model with $p = 2$ predictors ($n = 30$), obtaining $\hat{\beta}_1 = 1.5$ and $\text{SE}(\hat{\beta}_1) = 0.5$.

$$T_1 = \frac{1.5}{0.5} = 3.0$$

The degrees of freedom are $n - p - 1 = 30 - 2 - 1 = 27$. The critical value at $\alpha = 0.05$ (two-sided) is $t_{27, 0.025} \approx 2.05$. Since $3.0 > 2.05$, you reject $H_0: \beta_1 = 0$. This means that $X_1$ is a statistically significant predictor of $Y$ after controlling for $X_2$.

---

**Example 2: Overall F-test**

With $p = 2$ predictors and $n = 23$, suppose $\text{SSR} = 200$ and $\text{SSE} = 100$.

$$F = \frac{200/2}{100/(23-2-1)} = \frac{100}{100/20} = \frac{100}{5} = 20$$

Compare to $F_{2, 20}$. The critical value at $\alpha = 0.05$ is approximately 3.49. Since $20 \gg 3.49$, you reject $H_0: \beta_1 = \beta_2 = 0$. The model as a whole explains a significant amount of variance in $Y$. The F-statistic is large because the model explains 200 units of variance while each residual degree of freedom explains only 5 units on average.

---

**Example 3: When the F-test and individual t-tests disagree**

Imagine you fit a model with $p = 5$ predictors. The overall $F$-test is highly significant ($p < 0.001$), but only one of the five $t$-tests is significant. This is entirely possible: one strong predictor can drive a large $F$-statistic even while the other four contribute very little. Conversely, the $F$-test can be non-significant while individual $t$-tests appear significant — this happens when predictors are highly correlated and individually appear useful but their combined effect is modest. Always look at both levels of inference.

## Common Mistakes

- **Performing only individual $t$-tests without the global $F$-test.** With many predictors, some $t$-tests will be significant by chance. The $F$-test provides a single overall guard against this inflation.

- **Wrong degrees of freedom.** The $t$-test uses $n - p - 1$ df (subtracting the intercept and all $p$ slopes). The $F$-test uses $(p,\, n-p-1)$ df. Using $n - p$ or $n - 1$ is a common error.

- **Concluding that a non-significant predictor has zero effect.** Failing to reject $H_0: \beta_j = 0$ does not mean $\beta_j = 0$. It may simply mean your sample is too small to detect the effect.

## Quick Check

Try these before using hints:

1. In MLR with $p = 3$ and $n = 40$, what are the df for the $t$-test of $\beta_2$?
2. Compute $F$ given $\text{SSR} = 150$, $\text{SSE} = 100$, $p = 3$, $n = 24$.
3. A model has a significant $F$-test but no significant individual $t$-test. What might explain this?

*(Answers: 1. $df = 36$; 2. $F = (150/3)/(100/20) = 50/5 = 10$; 3. Multicollinearity — predictors are correlated, inflating individual SEs while the joint effect is real)*
