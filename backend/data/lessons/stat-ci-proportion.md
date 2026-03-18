# CI for Proportions

## Overview

A **confidence interval for a proportion** $p$ uses the fact that $\hat{p} = X/n$ is approximately normal for large $n$. Several constructions exist; the Wilson interval is more accurate than the Wald interval for small $n$.

## Key Idea

**Wald interval:**

$$\hat{p} \pm z_{\alpha/2}\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

Valid when $n\hat{p} \ge 5$ and $n(1-\hat{p}) \ge 5$.

## Worked Examples

**Example 1: 120 out of 200 surveyed prefer Brand A. 95% CI for $p$.**

$\hat{p} = 0.6$, $\text{SE} = \sqrt{0.6(0.4)/200} \approx 0.0346$.

$0.6 \pm 1.96(0.0346) = (0.532, 0.668)$.

---

**Example 2: Sample size for margin of error $\le 0.03$ at 95%**

$n \ge \left(\frac{1.96}{2 \times 0.03}\right)^2 = 1068$ (using $\hat{p}=0.5$ for worst case).

---

**Example 3: Wilson interval**

More accurate for small $n$, especially when $\hat{p}$ is near 0 or 1. Tilts toward 0.5.

## Common Mistakes

- **Using Wald when $n\hat{p} < 5$.** The normal approximation is poor.
- **Ignoring the continuity correction for discrete data.**

## Quick Check

1. $\hat{p}=0.4$, $n=100$. SE?
2. Margin of error for $n=400$, 95%?
3. Worst-case $\hat{p}$ for conservative sample size?

*(Answers: 0.049; $1.96 \cdot 0.5/\sqrt{400} = 0.049$; $\hat{p}=0.5$)*
