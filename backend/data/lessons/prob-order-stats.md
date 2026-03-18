# Order Statistics

## Overview

Given $n$ iid random variables, the **order statistics** $X_{(1)} \le X_{(2)} \le \cdots \le X_{(n)}$ are the values sorted in ascending order. $X_{(1)}$ is the minimum and $X_{(n)}$ is the maximum.

## Key Idea

PDF of the $k$-th order statistic $X_{(k)}$ (from iid $X_i$ with CDF $F$ and PDF $f$):

$$f_{(k)}(x) = \frac{n!}{(k-1)!(n-k)!} [F(x)]^{k-1}[1-F(x)]^{n-k} f(x)$$

For minimum: $F_{(1)}(x) = 1 - [1-F(x)]^n$.

For maximum: $F_{(n)}(x) = [F(x)]^n$.

## Worked Examples

**Example 1: CDF of maximum of $n$ iid $U(0,1)$**

$F_{(n)}(x) = x^n$ for $x \in [0,1]$. $f_{(n)}(x) = nx^{n-1}$.

---

**Example 2: CDF of minimum**

$F_{(1)}(x) = 1 - (1-x)^n$. $f_{(1)}(x) = n(1-x)^{n-1}$.

---

**Example 3: Expected maximum of $n = 2$ iid $U(0,1)$**

$E[X_{(2)}] = \int_0^1 x \cdot 2x\,dx = 2/3$.

## Common Mistakes

- **Using the marginal PDF of $X_i$ for $X_{(k)}$.** Order statistics have different PDFs.
- **Forgetting the multinomial coefficient** in the general $k$-th order statistic formula.

## Quick Check

1. $F_{X_{(n)}}(x)$ for $n$ iid variables with CDF $F$?
2. $E[\min(X_1,X_2)]$ for iid $U(0,1)$?
3. What is $X_{(1)}$ called?

*(Answers: $[F(x)]^n$; 1/3; the minimum (first order statistic))*
