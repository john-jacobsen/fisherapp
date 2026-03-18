# Chi-Squared Test of Homogeneity

## Overview

The **chi-squared test of homogeneity** tests whether multiple populations have the same distribution across categories. It uses the same formula as the independence test but arises from a different sampling design.

## Key Idea

Same test statistic as independence:

$$\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}} \sim \chi^2_{(r-1)(c-1)}$$

**Key difference from independence test:** In homogeneity, row totals are fixed by design (you sample a predetermined number from each group).

## Worked Examples

**Example 1: 100 Democrats, 100 Republicans asked if they support a policy.**

| | Support | Oppose |
|---|---|---|
| Dem | 60 | 40 |
| Rep | 45 | 55 |

$E_{11} = 100 \times 105/200 = 52.5$. $\chi^2 \approx 4.52$. df $= 1$. Reject at $\alpha = 0.05$.

---

**Example 2: Homogeneity vs. independence**

Homogeneity: fixed row totals, testing if column distributions are the same across rows.

Independence: one random sample, testing if row and column variables are associated.

---

**Example 3: Interpretation**

Reject → the distributions differ across groups. The proportions in each category are not homogeneous.

## Common Mistakes

- **Applying the independence test formula to homogeneity data** (they're the same formula, but interpretation differs).
- **Using counts less than 5** — merge cells.

## Quick Check

1. Null hypothesis for homogeneity test?
2. Same formula as which other test?
3. df for comparing 4 groups on 3 categories?

*(Answers: all groups have the same distribution; independence test; $(4-1)(3-1)=6$)*
