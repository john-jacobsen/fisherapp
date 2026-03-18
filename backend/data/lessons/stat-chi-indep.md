# Chi-Squared Test of Independence

## Overview

The **chi-squared test of independence** tests whether two categorical variables are associated in a contingency table. $H_0$: the two variables are independent.

## Key Idea

For an $r \times c$ contingency table with observed counts $O_{ij}$, the expected counts under independence are:

$$E_{ij} = \frac{(\text{row } i \text{ total})(\text{col } j \text{ total})}{n}$$

$$\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}} \sim \chi^2_{(r-1)(c-1)}$$

## Worked Examples

**Example 1: $2 \times 2$ table**

| | Smoker | Non-smoker |
|---|---|---|
| Disease | 30 | 20 |
| No disease | 10 | 40 |

$n=100$. $E_{11} = 50 \times 40/100 = 20$. $\chi^2 = (30-20)^2/20 + \ldots \approx 16.7$. df $= 1$. Reject at $\alpha = 0.05$.

---

**Example 2: df for $3 \times 4$ table**

df $= (3-1)(4-1) = 6$.

---

**Example 3: $\chi^2$ large means?**

Large $\chi^2$ → large discrepancy between observed and expected → evidence against independence.

## Common Mistakes

- **Confusing independence test with homogeneity test.** Same formula, different sampling design.
- **Using $\chi^2$ with small $E_{ij}$.** Apply Fisher's exact test for 2×2 tables with small counts.

## Quick Check

1. df for $2\times3$ table?
2. $E_{ij}$ formula?
3. Reject $H_0$ when $\chi^2 > ?$ ($\alpha = 0.05$, df$=1$)?

*(Answers: 2; (row total)(col total)/n; 3.84)*
