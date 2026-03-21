# Inference in Simple Linear Regression

## Overview

Fitting a regression line gives you estimates $\hat{\beta}_0$ and $\hat{\beta}_1$, but those are random — they depend on your sample. **Inference in simple linear regression** asks: is $\beta_1$ significantly different from zero? How precisely is it estimated? Under the normality assumption on $\varepsilon$, exact $t$-distributions govern these questions, and you can construct hypothesis tests and confidence intervals for any coefficient.

## Key Idea

Under $\varepsilon_i \overset{iid}{\sim} N(0, \sigma^2)$, the slope estimate is $\hat{\beta}_1 \sim N\!\left(\beta_1,\, \sigma^2 / S_{xx}\right)$ where $S_{xx} = \sum(X_i - \bar{X})^2$. Replacing the unknown $\sigma^2$ with the residual variance estimate $\hat{\sigma}^2 = \text{SSE}/(n-2)$ gives a $t$-statistic:

$$T = \frac{\hat{\beta}_1}{\hat{\sigma}/\sqrt{S_{xx}}} \sim t_{n-2}$$

The denominator $\hat{\sigma}/\sqrt{S_{xx}}$ is the standard error of $\hat{\beta}_1$. There are $n-2$ degrees of freedom because you estimate two parameters ($\beta_0$ and $\beta_1$) before computing residuals.

## Worked Examples

**Example 1: Estimate $\sigma^2$ from residuals**

You have $n = 5$ observations with residuals $e_i = -1, 2, 0, -1, 0$. The sum of squared errors is $\text{SSE} = 1 + 4 + 0 + 1 + 0 = 6$.

$$\hat{\sigma}^2 = \frac{\text{SSE}}{n - 2} = \frac{6}{3} = 2$$

You divide by $n - 2 = 3$, not $n$, because two degrees of freedom were used to estimate $\hat{\beta}_0$ and $\hat{\beta}_1$. Using $n$ in the denominator would systematically underestimate $\sigma^2$.

---

**Example 2: Test $H_0: \beta_1 = 0$**

Suppose $n = 20$, $\hat{\beta}_1 = 2.5$, and $\text{SE}(\hat{\beta}_1) = \hat{\sigma}/\sqrt{S_{xx}} = 0.8$. You want to test whether $X$ is a useful predictor.

$$T = \frac{2.5}{0.8} = 3.13$$

Under $H_0$, this follows $t_{18}$. The critical value at $\alpha = 0.05$ (two-sided) is $t_{18, 0.025} \approx 2.10$. Since $3.13 > 2.10$, you reject $H_0$ and conclude that $\beta_1$ is significantly different from zero. In other words, $X$ carries real predictive information about $Y$ in this sample.

---

**Example 3: Construct a 95% confidence interval for $\beta_1$**

Using the same values ($\hat{\beta}_1 = 2.5$, $\text{SE} = 0.8$, $n = 20$):

$$\hat{\beta}_1 \pm t_{18,\, 0.025} \cdot \text{SE} = 2.5 \pm 2.10 \cdot 0.8 = 2.5 \pm 1.68 = (0.82,\ 4.18)$$

Interpretation: if you repeated this study many times under the same conditions, about 95% of such intervals would contain the true $\beta_1$. Because the interval $(0.82, 4.18)$ does not include 0, this is consistent with rejecting $H_0: \beta_1 = 0$ at the 5% level — as expected.

## Common Mistakes

- **Using $n - 1$ degrees of freedom instead of $n - 2$.** In SLR you estimate two parameters, so residuals only have $n - 2$ free dimensions. Using $n - 1$ underestimates the standard error and produces $t$-statistics that are too large.

- **Confusing the confidence interval for the mean response with a prediction interval.** The CI for $E[Y \mid X = x_0]$ covers the average of $Y$ at $x_0$ and is narrower. A prediction interval for a new individual observation is wider because it must also account for the additional variance $\sigma^2$ from $\varepsilon$.

## Quick Check

Try these before using hints:

1. In SLR with $n = 25$, how many degrees of freedom does the $t$-test for $\beta_1$ use?
2. If $\hat{\beta}_1 = 1.2$ and $\text{SE}(\hat{\beta}_1) = 0.6$, compute the $t$-statistic.
3. Which is wider: the CI for $E[Y \mid X = 5]$ or the prediction interval for a new $Y$ at $X = 5$?

*(Answers: 1. $df = 23$; 2. $T = 2.0$; 3. The prediction interval is wider)*
