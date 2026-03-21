# Regression Diagnostics

## Overview

OLS inference — t-tests, confidence intervals, F-tests — is valid only when four assumptions hold: (1) **linearity** of the mean function, (2) **independence** of errors, (3) **homoscedasticity** (constant error variance), and (4) **normality** of residuals. **Regression diagnostics** are graphical and numerical tools you use after fitting to check these assumptions. Catching violations early prevents you from reporting invalid inference.

## Key Idea

The primary diagnostic tool is the residual $e_i = Y_i - \hat{Y}_i$. Standardized residuals adjust for the fact that observations with high leverage $h_{ii}$ have smaller residual variance:

$$r_i = \frac{e_i}{\hat{\sigma}\sqrt{1 - h_{ii}}}$$

where $h_{ii}$ is the $i$-th diagonal of the hat matrix $\mathbf{H} = \mathbf{X}(\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top$. Under the model assumptions, standardized residuals should behave approximately like $N(0, 1)$ observations.

## Worked Examples

**Example 1: Residuals vs. fitted plot — detecting heteroscedasticity**

You plot residuals $e_i$ on the $y$-axis against fitted values $\hat{Y}_i$ on the $x$-axis. Under homoscedasticity, the points should scatter randomly in a horizontal band around zero with roughly constant width. If the band fans out — small residuals for small $\hat{Y}$, large residuals for large $\hat{Y}$ — you have heteroscedasticity. This means $\text{Var}(\varepsilon_i)$ grows with the mean, which is common in income or count data. A standard remedy is to log-transform the response $Y$ (or use weighted least squares), which often stabilizes variance.

---

**Example 2: Q-Q plot — detecting non-normality**

A normal Q-Q plot graphs the sorted residuals against the quantiles you would expect from a $N(0,1)$ distribution. If the residuals are normal, points fall on a straight diagonal line. Heavy tails produce an S-shape: both ends of the plot curve away from the line. Light tails produce the opposite curvature. Heavy tails mean extreme residuals occur more often than normality predicts — this inflates Type I error in t-tests. A remedy is robust regression (which uses loss functions less sensitive to outliers) or a transformation of $Y$.

---

**Example 3: High-leverage vs. high-influence points**

**Leverage** $h_{ii}$ measures how far observation $i$ is from the center of the $X$-space. A point with $h_{ii} > 2(p+1)/n$ is flagged as high-leverage. High leverage is not necessarily harmful — if the point happens to fall on the true regression line, it will not distort your estimates. **Influence** measures how much the estimates actually change when you remove that point. Cook's distance combines leverage and residual size:

$$D_i = \frac{r_i^2}{p+1} \cdot \frac{h_{ii}}{1 - h_{ii}}$$

A point with large residual and high leverage has large Cook's distance and is genuinely influential. Cook's $D_i > 1$ is a common warning threshold. You should investigate such points — they may be data errors, or they may be real observations that reveal that your model is misspecified in certain regions.

## Common Mistakes

- **Ignoring the residual vs. fitted plot and relying only on $R^2$.** A model can have a high $R^2$ and still violate assumptions badly. Diagnostic plots reveal structure that summary statistics hide.

- **Deleting outliers without investigation.** An extreme residual could reflect a data entry error (fix or remove) or a genuine unusual observation (keep and report). Silently dropping points inflates apparent model fit.

## Quick Check

Try these before using hints:

1. What pattern in a residuals vs. fitted plot indicates heteroscedasticity?
2. What does a Q-Q plot with both ends curving above the line indicate?
3. A point has $h_{ii} = 0.8$ but $e_i \approx 0$. Is it influential?

*(Answers: 1. A fan shape — residual spread increases with fitted value; 2. Heavy tails — more extreme residuals than normality predicts; 3. No — high leverage but tiny residual means Cook's distance is small; it falls near the fitted line)*
