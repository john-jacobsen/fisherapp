# Model Comparison (AIC/BIC)

## Overview

**AIC** (Akaike Information Criterion) and **BIC** (Bayesian Information Criterion) balance model fit against complexity. They are used to select the best model when comparing nested or non-nested models.

## Key Idea

$$\text{AIC} = -2\ell(\hat{\theta}) + 2k, \quad \text{BIC} = -2\ell(\hat{\theta}) + k\ln n$$

where $\ell(\hat{\theta})$ is the maximized log-likelihood and $k$ is the number of parameters. **Smaller is better.** BIC penalizes complexity more heavily for large $n$.

## Worked Examples

**Example 1: Two models, $\ell_1 = -100$, $k_1 = 3$; $\ell_2 = -98$, $k_2 = 5$, $n = 50$.**

$\text{AIC}_1 = 206$, $\text{AIC}_2 = 206$. $\text{BIC}_1 = 200+3\ln50 \approx 211.7$, $\text{BIC}_2 = 196+5\ln50 \approx 215.5$. BIC prefers model 1.

---

**Example 2: AIC vs. BIC**

AIC asymptotically selects the model with best predictive accuracy. BIC selects the true model (if in the candidate set) for large $n$.

---

**Example 3: Delta AIC**

$\Delta\text{AIC} < 2$: little evidence to prefer one model. $\Delta\text{AIC} > 10$: strong preference.

## Common Mistakes

- **Minimizing AIC/BIC from different datasets.** They are comparable only on the same data.
- **Using AIC to compare models with different response transformations** (e.g., $Y$ vs. $\ln Y$).

## Quick Check

1. AIC formula?
2. Which penalizes extra parameters more for large $n$?
3. If $\text{AIC}_1 < \text{AIC}_2$, prefer which?

*(Answers: $-2\ell+2k$; BIC; model 1)*
