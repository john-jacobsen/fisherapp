# Simple Linear Regression

## Overview

**Simple linear regression** models the relationship between a single predictor $X$ and a response $Y$ as a straight line. The model is $Y_i = \beta_0 + \beta_1 X_i + \varepsilon_i$, where $\beta_0$ is the intercept, $\beta_1$ is the slope, and $\varepsilon_i \overset{iid}{\sim} N(0, \sigma^2)$ is random noise. Your goal is to estimate $\beta_0$ and $\beta_1$ from observed data.

## Key Idea

Ordinary least squares (OLS) finds the estimates that minimize the total squared vertical distance between observed values and the fitted line. The closed-form solutions are:

$$\hat{\beta}_1 = \frac{\sum_{i=1}^n (X_i - \bar{X})(Y_i - \bar{Y})}{\sum_{i=1}^n (X_i - \bar{X})^2}, \quad \hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}$$

The numerator measures how $X$ and $Y$ move together; the denominator scales by the spread of $X$. Once you have $\hat{\beta}_1$, the intercept formula forces the fitted line to pass exactly through the point $(\bar{X}, \bar{Y})$.

## Worked Examples

**Example 1: Compute OLS estimates from summary statistics**

You are given: $\sum(X_i - \bar{X})(Y_i - \bar{Y}) = 120$, $\sum(X_i - \bar{X})^2 = 30$, $\bar{X} = 5$, $\bar{Y} = 20$.

Apply the slope formula. The numerator (120) captures total co-movement between $X$ and $Y$; dividing by the denominator (30) normalizes this per unit of $X$-spread:

$$\hat{\beta}_1 = \frac{120}{30} = 4$$

Now compute the intercept by forcing the line through $(\bar{X}, \bar{Y}) = (5, 20)$:

$$\hat{\beta}_0 = 20 - 4 \cdot 5 = 0$$

The fitted line is $\hat{Y} = 4X$.

---

**Example 2: Predict a new value**

Using $\hat{Y} = 4X$ from Example 1, predict $\hat{Y}$ when $X = 6$.

$$\hat{Y} = 4(6) = 24$$

This works because the regression line estimates $E[Y \mid X]$ — the average value of $Y$ at a given $X$. An individual new observation at $X = 6$ will not equal exactly 24 (the error term $\varepsilon$ introduces scatter), but 24 is your best point prediction. Predicting at $X = 100$ would be unreliable because you are far outside the range of observed data, where the linear relationship may not hold.

---

**Example 3: Interpret the slope**

Suppose you fit a model predicting exam score $Y$ from study hours $X$ and obtain $\hat{\beta}_1 = 5.2$.

Interpretation: for each additional hour of study, the predicted exam score increases by 5.2 points **on average**. The phrase "on average" is critical — it acknowledges that individual students scatter around the fitted line due to $\varepsilon$. The slope describes the average trend across many students, not a guaranteed result for any one person. If $\hat{\beta}_1$ were negative, each additional hour would be associated with a lower predicted score on average, which would prompt you to question the model or look for confounders.

## Common Mistakes

- **Interpreting the slope as causal.** OLS estimates a linear association, not a causal effect. A third variable could drive both $X$ and $Y$, producing a positive $\hat{\beta}_1$ even when $X$ has no causal influence on $Y$.

- **Computing $\hat{\beta}_0$ incorrectly.** The intercept is always $\hat{\beta}_0 = \bar{Y} - \hat{\beta}_1 \bar{X}$. A common error is to solve for the intercept by substituting one arbitrary data point into the equation instead of using the sample means.

- **Extrapolating far beyond the observed data range.** The linear model is calibrated to your data. Predicting at $X$ values far outside $[\min X_i, \max X_i]$ can produce nonsensical results if the true relationship curves or breaks down outside that range.

## Quick Check

Try these before using hints:

1. Given $\sum(X_i - \bar{X})(Y_i - \bar{Y}) = 50$ and $\sum(X_i - \bar{X})^2 = 25$, what is $\hat{\beta}_1$?
2. If $\hat{\beta}_1 = 2$, $\bar{X} = 4$, and $\bar{Y} = 10$, what is $\hat{\beta}_0$?
3. With the line from (2), predict $\hat{Y}$ when $X = 7$.

*(Answers: 1. $\hat{\beta}_1 = 2$; 2. $\hat{\beta}_0 = 2$; 3. $\hat{Y} = 16$)*
