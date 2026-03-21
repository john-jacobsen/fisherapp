# Chi-Squared Test of Homogeneity

## Overview

The **chi-squared test of homogeneity** tests whether the distribution of a categorical variable is the same across two or more separate populations. You draw independent samples from each population, record one categorical outcome variable per subject, and test whether the outcome proportions are the same in every population. The test is mechanically identical to the independence test, but it arises from a different study design and answers a different question.

## Key Idea

Arrange the data in an $r \times c$ table where rows are populations (groups) and columns are outcome categories. Under $H_0$ (homogeneity), the outcome distribution is the same in every row. The expected counts and test statistic use the same formulas as the independence test:

$$\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}} \sim \chi^2_{(r-1)(c-1)}$$

with $E_{ij} = R_i C_j / n$ as before. The degrees of freedom are $(r-1)(c-1)$, where $r$ is the number of groups (rows) and $c$ is the number of outcome categories (columns).

## Worked Examples

**Example 1: Pass/fail rates at three schools**

Three schools are sampled independently. Each student is classified as Pass or Fail:

|          | Pass | Fail | Total |
|----------|------|------|-------|
| School A | 40   | 10   | 50    |
| School B | 55   | 20   | 75    |
| School C | 30   | 20   | 50    |
| **Total**| 125  | 50   | 175   |

$H_0$: the pass rate is the same at all three schools. Under $H_0$, expected counts are $E_{ij} = R_i C_j / 175$. For School A: $E_{A,\text{pass}} = (50 \times 125)/175 \approx 35.7$, $E_{A,\text{fail}} = (50 \times 50)/175 \approx 14.3$.

---

**Example 2: Compute $\chi^2$ and decide**

Continuing Example 1, compute all six expected counts:

| Expected  | Pass  | Fail  |
|-----------|-------|-------|
| School A  | 35.71 | 14.29 |
| School B  | 53.57 | 21.43 |
| School C  | 35.71 | 14.29 |

Now compute the chi-squared contributions:

$$\chi^2 = \frac{(40 - 35.71)^2}{35.71} + \frac{(10 - 14.29)^2}{14.29} + \frac{(55 - 53.57)^2}{53.57} + \frac{(20 - 21.43)^2}{21.43} + \frac{(30 - 35.71)^2}{35.71} + \frac{(20 - 14.29)^2}{14.29}$$

$$\approx 0.516 + 1.289 + 0.038 + 0.096 + 0.911 + 2.277 = 5.13$$

With $df = (3-1)(2-1) = 2$ and $\chi^2_{0.05, 2} = 5.99$, you fail to reject $H_0$. The pass rate differences across schools are not statistically significant at the 5% level. School C's lower pass rate (60% vs 80% for School A) is within the range of sampling variability.

---

**Example 3: Independence vs homogeneity — same math, different logic**

Both tests use the same $\chi^2$ formula and the same $df = (r-1)(c-1)$. The difference is in how the data were collected and what the null hypothesis says.

**Independence test**: you draw one sample and measure two variables on each subject. $H_0$: the two variables are independent (knowing one tells you nothing about the other). Example: sample 200 adults and record both their education level and their income category.

**Homogeneity test**: you draw separate samples from $r$ predefined populations and measure one variable per subject. $H_0$: the distribution of that variable is the same in every population. Example: sample 50 adults from each of three cities and record their income category.

In the independence test, both marginal totals are random — you don't know in advance how many people will fall in each row or column. In the homogeneity test, the row totals are fixed by your sampling design. Despite this difference, the calculation is identical.

## Common Mistakes

- **Confusing homogeneity with goodness-of-fit.** Goodness-of-fit tests whether one group's data fit a specified theoretical distribution. Homogeneity tests whether multiple groups share the same distribution. The number of populations and the nature of $H_0$ are different.
- **Swapping rows and columns carelessly.** The formula $E_{ij} = R_i C_j / n$ requires consistent orientation. Make sure rows represent groups (populations) and columns represent outcomes, and don't mix them up mid-calculation.
- **Forgetting that each $E_{ij} \geq 5$ is required.** This condition applies here just as in the independence and goodness-of-fit tests. If a school has very few students, combine it with another or use exact methods.

## Quick Check

Try these before using hints:

1. In a $3 \times 2$ homogeneity test, what is $df$?
2. $R_2 = 40$, $C_1 = 60$, $n = 120$. Compute $E_{21}$.
3. What is the key design difference between the independence test and the homogeneity test?

*(Answers: 1. $df = (3-1)(2-1) = 2$; 2. $E_{21} = 40 \times 60 / 120 = 20$; 3. Independence: one sample, two variables measured; Homogeneity: separate samples drawn from each population, one variable measured)*
