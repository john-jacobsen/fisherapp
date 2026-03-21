# Chi-Squared Goodness-of-Fit Test

## Overview

The **chi-squared goodness-of-fit test** tests whether observed category frequencies match what you would expect under a specified probability model. For example, you might test whether a die is fair, whether births are uniformly distributed across months, or whether a dataset follows a Poisson distribution. The test measures how far the observed counts stray from the expected counts under $H_0$.

## Key Idea

Suppose you have $K$ categories. Under $H_0$, each category $k$ has expected count $E_k = n \cdot p_k$, where $p_k$ is the hypothesized probability and $n$ is the total sample size. The test statistic is:

$$\chi^2 = \sum_{k=1}^K \frac{(O_k - E_k)^2}{E_k}$$

Each term $(O_k - E_k)^2/E_k$ measures the squared discrepancy in category $k$, scaled by the expected count (so categories with larger $E_k$ are not artificially penalized for larger raw gaps). Under $H_0$, this statistic follows a $\chi^2$ distribution with $K - 1 - p$ degrees of freedom, where $p$ is the number of parameters estimated from the data.

## Worked Examples

**Example 1: Testing a fair die**

You roll a die $n = 60$ times and observe: $O = \{8, 12, 9, 11, 10, 10\}$ for faces 1–6. Under $H_0$ (fair die), each face has probability $1/6$, so $E_k = 60/6 = 10$ for all $k$.

Compute each contribution:

$$\frac{(8-10)^2}{10} + \frac{(12-10)^2}{10} + \frac{(9-10)^2}{10} + \frac{(11-10)^2}{10} + \frac{(10-10)^2}{10} + \frac{(10-10)^2}{10}$$

$$= \frac{4}{10} + \frac{4}{10} + \frac{1}{10} + \frac{1}{10} + 0 + 0 = 1.0$$

Degrees of freedom: $K - 1 = 6 - 1 = 5$ (no parameters were estimated from the data). The critical value is $\chi^2_{0.05, 5} = 11.07$. Since $1.0 \ll 11.07$, you fail to reject $H_0$. The die shows no evidence of unfairness.

---

**Example 2: Testing uniformity of births across months**

You observe $n = 120$ births and want to test whether they are uniformly distributed across 12 months. Under $H_0$, each month has probability $1/12$, giving $E_k = 120/12 = 10$ births each.

Suppose observed counts are $\{15, 7, 9, 11, 8, 12, 10, 9, 13, 10, 8, 8\}$. Compute:

$$\chi^2 = \frac{(15-10)^2}{10} + \frac{(7-10)^2}{10} + \ldots = \frac{25+9+1+1+4+4+0+1+9+0+4+4}{10} = \frac{62}{10} = 6.2$$

With $df = 12 - 1 = 11$ and $\chi^2_{0.05,11} = 19.68$, you fail to reject $H_0$. These birth counts are consistent with uniformity.

---

**Example 3: The validity condition — why $E_k \geq 5$ matters**

The $\chi^2$ approximation relies on the test statistic's distribution being well-approximated by a chi-squared distribution. This approximation breaks down when expected counts are very small. With $E_k < 5$ in any cell, there are so few observations that the discrete category counts don't resemble a continuous chi-squared variable, and the p-value becomes unreliable.

When some $E_k < 5$, combine adjacent categories to create cells with larger expected counts. For example, if you're testing whether data follow a Poisson distribution and the expected count for "5 or more events" is only 2, merge it with "4 events" into "4 or more events." This reduces $K$, changes the degrees of freedom, but restores the validity of the approximation.

## Common Mistakes

- **Using $O_k - E_k$ instead of $(O_k - E_k)^2$.** The signed differences cancel out ($\sum O_k = \sum E_k = n$), so you must square them. The chi-squared statistic measures total squared deviation, not net deviation.
- **Using the wrong degrees of freedom when parameters are estimated.** If you estimate $p$ parameters from the data to compute $E_k$, then $df = K - 1 - p$, not $K - 1$. Forgetting to subtract $p$ understates the degrees of freedom and produces p-values that are too small.
- **Confusing expected counts with expected proportions.** $E_k$ must be a count ($n \cdot p_k$), not just $p_k$. Using $p_k$ directly inflates the chi-squared statistic by a factor of $n$.

## Quick Check

Try these before using hints:

1. $K = 4$ categories, $n = 40$, all categories equally likely. What is $E_k$?
2. Observed = $\{12, 8, 10, 10\}$, $E_k = 10$ for all. Compute $\chi^2$.
3. What is $df$ for a goodness-of-fit test with $K = 4$ categories and no estimated parameters?

*(Answers: 1. $E_k = 10$; 2. $\chi^2 = 4/10 + 4/10 + 0 + 0 = 0.8$; 3. $df = 3$)*
