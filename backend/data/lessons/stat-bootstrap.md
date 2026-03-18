# Bootstrap

## Overview

The **bootstrap** estimates the sampling distribution of a statistic by repeatedly resampling from the observed data **with replacement**. It requires no distributional assumptions and works for almost any estimator.

## Key Idea

1. Draw $B$ bootstrap samples of size $n$ from the data (with replacement).
2. Compute the statistic $\hat{\theta}^*$ for each.
3. Use the distribution of $\hat{\theta}^*$ values to estimate the SE, bias, or confidence interval of $\hat{\theta}$.

**Bootstrap SE:** $\widehat{\text{SE}} = \text{SD of }\{\hat{\theta}^*_1, \ldots, \hat{\theta}^*_B\}$.

## Worked Examples

**Example 1: Bootstrap SE of the median**

No closed-form formula for SE of median. Bootstrap: resample 1000 times, compute median each time, take SD.

---

**Example 2: Percentile confidence interval**

Sort $\hat{\theta}^*$ values. 95% CI: $(\hat{\theta}^*_{0.025}, \hat{\theta}^*_{0.975})$.

---

**Example 3: When is $B = 1000$ enough?**

For SE estimation, $B = 200$–$500$ often suffices. For CI, $B \ge 1000$ is safer.

## Common Mistakes

- **Resampling without replacement.** Bootstrap requires replacement.
- **Thinking bootstrap overcomes small $n$.** It cannot fix a fundamentally unrepresentative sample.

## Quick Check

1. What is the bootstrap principle?
2. Bootstrap SE is estimated by what?
3. Does bootstrap require parametric assumptions?

*(Answers: resample from data with replacement; SD of bootstrap statistics; no)*
