# Chi-Squared Goodness-of-Fit

## Overview

The **chi-squared goodness-of-fit test** tests whether observed frequencies match expected frequencies from a specified distribution.

## Key Idea

$$\chi^2 = \sum_{i=1}^k \frac{(O_i - E_i)^2}{E_i} \overset{\text{approx}}{\sim} \chi^2_{k-1-p}$$

where $O_i$ are observed counts, $E_i = n p_i$ are expected, $k$ is the number of categories, and $p$ is the number of estimated parameters.

## Worked Examples

**Example 1: Fair die. Roll 60 times. Expected = 10 per face. Observed: 8,11,9,12,10,10.**

$\chi^2 = (4+1+1+4+0+0)/10 = 1.0$. df $= 5$. $p > 0.9$. Fail to reject.

---

**Example 2: $E_i < 5$**

Cells with expected count $< 5$ should be merged. The $\chi^2$ approximation requires all $E_i \ge 5$.

---

**Example 3: Estimating parameters**

If you estimate $m$ parameters from the data to get $E_i$, df $= k - 1 - m$.

## Common Mistakes

- **Using $\chi^2$ GOF with small expected counts.** Merge cells.
- **Wrong df.** Subtract 1 for the constraint $\sum O_i = n$, and one more for each estimated parameter.

## Quick Check

1. df for $k=6$ categories, no estimated parameters?
2. Minimum $E_i$ for the $\chi^2$ approximation?
3. $\chi^2 = 0$ means what?

*(Answers: 5; 5; observed = expected exactly)*
