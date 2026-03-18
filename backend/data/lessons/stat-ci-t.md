# t Confidence Intervals

## Overview

When $\sigma$ is unknown, replace $z$ with the $t$-statistic. The **$t$ confidence interval** uses Student's $t$-distribution with $n-1$ degrees of freedom, which has heavier tails to account for estimating $\sigma$.

## Key Idea

$$\bar{X} \pm t_{n-1, \alpha/2} \frac{S}{\sqrt{n}}$$

where $S = \sqrt{\frac{1}{n-1}\sum(X_i-\bar{X})^2}$.

As $n \to \infty$, $t_{n-1} \to N(0,1)$.

## Worked Examples

**Example 1: $n=10$, $\bar{x}=25$, $s=4$. 95% CI.**

$t_{9,0.025} = 2.262$. $25 \pm 2.262(4/\sqrt{10}) = 25 \pm 2.86 = (22.14, 27.86)$.

---

**Example 2: Compare to $Z$ CI**

Same data: $Z$ CI would use $1.96$ instead of $2.262$ — narrower but less accurate with unknown $\sigma$.

---

**Example 3: Assumptions**

$X_i$ must be approximately normal (or $n$ large). Robust to mild non-normality.

## Common Mistakes

- **Using $z$ instead of $t$ when $\sigma$ is unknown and $n$ is small.**
- **Wrong degrees of freedom.** Use $n-1$, not $n$.

## Quick Check

1. df for $t$ CI with $n=25$?
2. $t_{9,0.025}$ vs. $z_{0.025}$: which is larger?
3. When does $t_{n-1}$ approximate $N(0,1)$?

*(Answers: 24; $t$ is larger; when $n$ is large)*
