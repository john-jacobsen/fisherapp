# Order Statistics

## Overview

Given an iid sample $X_1, \ldots, X_n$, the **order statistics** $X_{(1)} \le X_{(2)} \le \cdots \le X_{(n)}$ are the sample values sorted from smallest to largest. $X_{(1)}$ is the sample minimum and $X_{(n)}$ is the sample maximum. Order statistics arise naturally in reliability theory (time to first failure), extreme-value analysis, and distribution-free inference. Their distributions can be derived exactly from the population CDF $F$ and pdf $f$.

## Key Idea

The pdf of the $k$-th order statistic is:

$$f_{X_{(k)}}(x) = \frac{n!}{(k-1)!(n-k)!} \,[F(x)]^{k-1}\,[1-F(x)]^{n-k}\,f(x)$$

This formula counts the ways exactly $k-1$ of the $n$ observations fall below $x$, one falls at $x$, and $n-k$ fall above $x$ — weighted by the probability of each configuration. Special cases: the minimum uses $k=1$ and the maximum uses $k=n$.

## Worked Examples

**Example 1: pdf of the maximum for $U(0,1)$**

For $X_i \overset{iid}{\sim} U(0,1)$: $f(x) = 1$ and $F(x) = x$ on $[0,1]$. Set $k = n$ in the general formula. The term $(1-F(x))^{n-k} = (1-x)^0 = 1$:

$$f_{X_{(n)}}(x) = \frac{n!}{(n-1)!\, 0!}\, x^{n-1} \cdot 1 \cdot 1 = n\, x^{n-1}, \quad 0 < x < 1$$

This makes intuitive sense: the maximum of $n$ uniform samples is skewed toward 1, and the skew increases with $n$. For $n = 1$ you get the flat $U(0,1)$ density; for large $n$ the distribution concentrates near 1.

---

**Example 2: Expected value of the maximum for $U(0,1)$**

Using the pdf $f_{X_{(n)}}(x) = nx^{n-1}$:

$$E[X_{(n)}] = \int_0^1 x \cdot nx^{n-1}\,dx = n\int_0^1 x^n\,dx = n \cdot \frac{1}{n+1} = \frac{n}{n+1}$$

This result is intuitive: with more observations, the maximum tends to be closer to the upper bound of 1. For $n = 1$, $E[X_{(1)}] = 1/2$ (the mean of $U(0,1)$). For $n = 9$, $E[X_{(9)}] = 9/10 = 0.9$. As $n \to \infty$, the expected maximum approaches 1.

---

**Example 3: Distribution of the minimum of Exponential random variables**

Let $X_i \overset{iid}{\sim} \text{Exp}(\lambda)$, so $F(x) = 1 - e^{-\lambda x}$ and $f(x) = \lambda e^{-\lambda x}$. Set $k = 1$:

$$f_{X_{(1)}}(x) = \frac{n!}{0!\,(n-1)!}\,(1 - e^{-\lambda x})^0\,(e^{-\lambda x})^{n-1}\,\lambda e^{-\lambda x} = n\lambda e^{-n\lambda x}$$

This is the pdf of $\text{Exp}(n\lambda)$. The result has a clean interpretation: the minimum of $n$ independent exponential clocks with rate $\lambda$ is itself exponential with rate $n\lambda$ (it fires $n$ times faster). This is the memoryless property at work.

## Common Mistakes

- **Assuming order statistics are independent.** They are not — for example, knowing $X_{(1)} = 0.9$ tells you all other order statistics are at least 0.9. Only in special cases (like the spacings of uniform order statistics) do independence-like properties emerge.

- **Confusing $k$ and $n - k + 1$ in the formula.** The formula uses $(k-1)!$ in the denominator (below the $k$-th value) and $(n-k)!$ (above it). Swapping these gives the pdf of $X_{(n-k+1)}$ instead.

## Quick Check

Try these before using hints:

1. Write the pdf of $X_{(1)}$ (the minimum) for a general iid sample with CDF $F$ and pdf $f$.
2. Find $E[X_{(1)}]$ for $X_i \overset{iid}{\sim} U(0,1)$.
3. For $n = 4$ iid $\text{Exp}(2)$ random variables, what is the distribution of the minimum?

*(Answers: 1. $f_{X_{(1)}}(x) = n[1-F(x)]^{n-1}f(x)$; 2. $E[X_{(1)}] = 1/(n+1) = 1/2$ for $n=1$, generally $1/(n+1)$; 3. $\text{Exp}(8)$)*
