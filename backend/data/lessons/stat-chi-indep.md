# Chi-Squared Test of Independence

## Overview

The **chi-squared test of independence** tests whether two categorical variables are independent. You collect data on both variables for a single sample of subjects, arrange the counts in a contingency table, and test whether knowing a subject's value on one variable tells you anything about the other. Under independence, knowing someone's row category gives you no information about their column category.

## Key Idea

For an $r \times c$ contingency table, the expected count in cell $(i, j)$ under independence is:

$$E_{ij} = \frac{R_i \cdot C_j}{n}$$

where $R_i$ is the total for row $i$, $C_j$ is the total for column $j$, and $n$ is the grand total. This formula comes directly from the definition of independence: $P(\text{row } i \cap \text{col } j) = P(\text{row } i) \cdot P(\text{col } j)$, estimated as $(R_i/n)(C_j/n)$, then multiplied by $n$.

The test statistic is:

$$\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}} \sim \chi^2_{(r-1)(c-1)}$$

## Worked Examples

**Example 1: $2 \times 2$ table**

A clinical trial records whether 100 patients received treatment (50) or placebo (50), and whether they improved (yes/no):

|           | Improved | Not Improved | Total |
|-----------|----------|--------------|-------|
| Treatment | 35       | 15           | 50    |
| Placebo   | 25       | 25           | 50    |
| **Total** | 60       | 40           | 100   |

Under independence, $E_{11} = (50 \times 60)/100 = 30$. This is the count you'd expect in the "Treatment, Improved" cell if treatment status had no relationship to improvement. All four expected counts:

$$E = \begin{pmatrix} 30 & 20 \ 30 & 20 \end{pmatrix}$$

$$\chi^2 = \frac{(35-30)^2}{30} + \frac{(15-20)^2}{20} + \frac{(25-30)^2}{30} + \frac{(25-20)^2}{20}$$

$$= \frac{25}{30} + \frac{25}{20} + \frac{25}{30} + \frac{25}{20} = 0.833 + 1.25 + 0.833 + 1.25 = 4.17$$

With $df = (2-1)(2-1) = 1$ and $\chi^2_{0.05,1} = 3.84$, you **reject $H_0$**. Treatment and outcome are not independent — treated patients improved more often.

---

**Example 2: $3 \times 2$ table**

A survey of 150 people records political affiliation (Liberal, Moderate, Conservative) and stance on a policy (Support, Oppose). Suppose the row totals are 50, 60, 40 and column totals are 80, 70.

$E_{11} = (50 \times 80)/150 = 26.7$, $E_{12} = (50 \times 70)/150 = 23.3$, and so on for all 6 cells. After computing all six contributions and summing, suppose $\chi^2 = 8.3$. With $df = (3-1)(2-1) = 2$ and $\chi^2_{0.05,2} = 5.99$, you reject $H_0$ — political affiliation and policy stance are not independent.

---

**Example 3: Independence test vs goodness-of-fit**

The goodness-of-fit test checks whether one categorical variable matches a specified distribution ($H_0$: data follow a particular model). The independence test checks whether two categorical variables are related ($H_0$: the two variables are independent).

The degrees of freedom formulas reflect this: goodness-of-fit uses $df = K - 1 - p$ (number of categories minus 1 minus estimated parameters), while the independence test uses $df = (r-1)(c-1)$ (rows minus 1 times columns minus 1). For a $2 \times 2$ table, $df = 1$; for a $4 \times 3$ table, $df = 6$.

## Common Mistakes

- **Using $E_{ij} = n/(r \times c)$, i.e., equal expected counts.** That formula is only valid when the marginal totals are all equal. The correct formula, $E_{ij} = R_i C_j / n$, always uses the actual row and column totals.
- **Using $df = rc - 1$ instead of $(r-1)(c-1)$.** The correct formula accounts for the fact that once you know all but one row total and all but one column total, the remaining expected counts are determined.
- **Applying the test when expected counts are below 5.** As with goodness-of-fit, the chi-squared approximation requires $E_{ij} \geq 5$ in each cell. Combine rare categories or use Fisher's exact test for small counts.

## Quick Check

Try these before using hints:

1. In a $2 \times 3$ table with grand total $n = 90$, $R_1 = 30$, $C_2 = 45$. Compute $E_{12}$.
2. What is $df$ for a $4 \times 2$ contingency table?
3. If all observed counts exactly equal their expected counts, what is $\chi^2$?

*(Answers: 1. $E_{12} = 30 \times 45 / 90 = 15$; 2. $df = (4-1)(2-1) = 3$; 3. $\chi^2 = 0$)*
