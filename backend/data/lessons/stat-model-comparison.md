# Model Comparison: AIC, BIC, and F-Tests

## Overview

Adding more predictors to a regression model always improves fit on the training data, but more complex models can overfit and predict new data poorly. **AIC** (Akaike Information Criterion) and **BIC** (Bayesian Information Criterion) are principled criteria that balance fit against complexity — lower values indicate a better model. For **nested models** (where one is a restricted version of the other), a partial **F-test** provides a formal hypothesis test of whether the extra predictors are worth including.

## Key Idea

Both AIC and BIC penalize the maximized log-likelihood $\ell(\hat{\theta})$ for the number of parameters $k$:

$$\text{AIC} = -2\ell(\hat{\theta}) + 2k, \quad \text{BIC} = -2\ell(\hat{\theta}) + k\ln n$$

Because $\ln n > 2$ whenever $n > e^2 \approx 7.4$, BIC always penalizes extra parameters more heavily than AIC for any sample size you will encounter in practice. Both criteria: **lower is better**.

## Worked Examples

**Example 1: Compare two models using AIC and BIC**

Model 1: log-likelihood $\ell_1 = -50$, number of parameters $k_1 = 3$. Model 2: $\ell_2 = -48$, $k_2 = 5$, $n = 100$.

$$\text{AIC}_1 = -2(-50) + 2(3) = 106, \qquad \text{AIC}_2 = -2(-48) + 2(5) = 106$$

The AIC values are tied — Model 2 fits slightly better ($\ell$ improved by 2) but uses 2 extra parameters that cost exactly 4 AIC units. Now BIC:

$$\text{BIC}_1 = 100 + 3\ln 100 = 100 + 13.8 = 113.8, \qquad \text{BIC}_2 = 96 + 5\ln 100 = 96 + 23.0 = 119.0$$

BIC prefers Model 1. The larger penalty for $n = 100$ means the modest improvement in fit does not justify the two extra parameters.

---

**Example 2: Partial F-test for nested models**

You want to test whether two additional predictors (going from $p = 1$ to $p = 3$) improve fit. With $n = 30$:

- Reduced model ($p = 1$): $\text{SSE}_{\text{red}} = 300$
- Full model ($p = 3$): $\text{SSE}_{\text{full}} = 240$

$$F = \frac{(\text{SSE}_{\text{red}} - \text{SSE}_{\text{full}})/2}{\text{SSE}_{\text{full}}/(n - p_{\text{full}} - 1)} = \frac{(300 - 240)/2}{240/(30 - 3 - 1)} = \frac{30}{240/26} = \frac{30}{9.23} \approx 3.25$$

Compare to $F_{2, 26}$ (critical value $\approx 3.37$ at $\alpha = 0.05$). Since $3.25 < 3.37$, you fail to reject $H_0$ — the two extra predictors do not significantly improve the model at this significance level.

---

**Example 3: Why BIC penalizes complexity more than AIC for large $n$**

The AIC penalty per parameter is always 2. The BIC penalty per parameter is $\ln n$, which grows with sample size: $\ln 10 \approx 2.3$, $\ln 100 \approx 4.6$, $\ln 1000 \approx 6.9$. So for large datasets, BIC strongly favors parsimonious models. This reflects a philosophical difference: AIC aims for the best predictive model; BIC aims to identify the true model (if it is in your candidate set) as $n \to \infty$.

## Common Mistakes

- **Comparing AIC or BIC values from models fit to different datasets.** These criteria are only meaningful when computed on the same data. Comparing AIC across different response variables or different subsets is invalid.

- **Using AIC or BIC to compare models with different response transformations.** If one model predicts $Y$ and another predicts $\ln Y$, their likelihoods are on different scales and cannot be directly compared.

- **Treating $\Delta\text{AIC} = 1$ as decisive.** A difference of less than 2 AIC units is generally considered weak evidence. Only $\Delta\text{AIC} > 10$ is considered strong.

## Quick Check

Try these before using hints:

1. Model A: $\ell = -80$, $k = 2$. Model B: $\ell = -78$, $k = 4$, $n = 50$. Which has lower AIC? Which has lower BIC?
2. What is the key difference between a partial F-test and the global F-test?
3. For $n = 100$, which criterion imposes a larger penalty per parameter: AIC or BIC?

*(Answers: 1. $\text{AIC}_A = 164$, $\text{AIC}_B = 164$ (tied); $\text{BIC}_A = 160 + 2\ln50 \approx 169.2$, $\text{BIC}_B = 156 + 4\ln50 \approx 174.4$ — BIC prefers A; 2. Partial F-test compares a reduced model to a full model; global F-test compares the full model to an intercept-only model; 3. BIC, since $\ln 100 \approx 4.6 > 2$)*
