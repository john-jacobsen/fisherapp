# Order Statistics

## Overview

If $X_1, X_2, \ldots, X_n$ are i.i.d. random variables, the **order statistics** $X_{(1)} \leq X_{(2)} \leq \cdots \leq X_{(n)}$ are their values sorted from smallest to largest. $X_{(1)}$ is the minimum, $X_{(n)}$ is the maximum, and $X_{(k)}$ is the $k$-th smallest. Order statistics arise naturally in reliability (when does the first component fail?), quality control (what is the sample range?), and nonparametric statistics.

## Key Idea

Let $F(x)$ and $f(x)$ be the CDF and PDF of each $X_i$. The CDF and PDF of the $k$-th order statistic are:

$$F_{(k)}(x) = \sum_{j=k}^{n} \binom{n}{j}[F(x)]^j[1-F(x)]^{n-j}$$

$$f_{(k)}(x) = \frac{n!}{(k-1)!(n-k)!}[F(x)]^{k-1}[1-F(x)]^{n-k}f(x)$$

The PDF formula has a clean interpretation: $\frac{n!}{(k-1)!(n-k)!}$ counts the arrangements of $n$ items into the roles of "below $x$," "equal to $x$," and "above $x$"; the powers of $F(x)$ and $1-F(x)$ give the probabilities for each role; and $f(x)$ is the density at the point $x$ itself.

## Worked Examples

**Example 1: PDF of the maximum $X_{(n)}$ for $n$ i.i.d. Uniform$(0,1)$**

For Uniform$(0,1)$: $F(x) = x$ and $f(x) = 1$ on $(0,1)$. The maximum corresponds to $k = n$, so $[F(x)]^{k-1} = x^{n-1}$, $[1-F(x)]^{n-k} = (1-x)^0 = 1$, and the coefficient is $\frac{n!}{(n-1)! \cdot 0!} = n$.

$$f_{(n)}(x) = n \cdot x^{n-1} \cdot 1 \cdot 1 = nx^{n-1}, \quad 0 < x < 1$$

This makes intuitive sense: the maximum of $n$ uniform samples is skewed toward 1, and the density concentrates near 1 as $n$ grows. The formula $nx^{n-1}$ is the derivative of $F_{(n)}(x) = [F(x)]^n = x^n$, which follows because all $n$ observations must fall below $x$ for the maximum to be below $x$.

---

**Example 2: PDF of the minimum $X_{(1)}$**

For the minimum, $k = 1$: $[F(x)]^{k-1} = x^0 = 1$, $[1-F(x)]^{n-1} = (1-x)^{n-1}$, and the coefficient is $\frac{n!}{0!(n-1)!} = n$.

$$f_{(1)}(x) = n(1-x)^{n-1}, \quad 0 < x < 1$$

The minimum is skewed toward 0 — at least one of $n$ observations must fall below $x$ for the minimum to be below $x$, and with more observations it becomes increasingly likely that some observation is close to 0. The CDF of the minimum is $F_{(1)}(x) = 1 - (1-x)^n$ (the complement of all observations exceeding $x$), and $f_{(1)}(x)$ is its derivative.

---

**Example 3: Find $E[X_{(n)}]$ for Uniform$(0,1)$**

Using the PDF from Example 1, $f_{(n)}(x) = nx^{n-1}$ on $(0,1)$, integrate $x$ against this density. The integral weights each possible maximum value by its density:

$$E[X_{(n)}] = \int_0^1 x \cdot nx^{n-1} \, dx = n\int_0^1 x^n \, dx = n \cdot \frac{x^{n+1}}{n+1}\Bigg|_0^1 = \frac{n}{n+1}$$

As $n \to \infty$, $E[X_{(n)}] \to 1$, which confirms that the maximum of a large sample from Uniform$(0,1)$ concentrates near the upper bound. For $n = 1$, $E[X_{(1)}] = 1/2$, the mean of a single observation, as expected.

## Common Mistakes

- **Applying the maximum CDF formula $[F(x)]^n$ to the minimum.** The CDF of the maximum is $[F(x)]^n$ (all below $x$), but the CDF of the minimum is $1 - [1-F(x)]^n$ (not all above $x$). These are easy to mix up.
- **Forgetting the $n!/(k-1)!(n-k)!$ coefficient in the PDF.** This combinatorial factor accounts for which observation plays the role of $X_{(k)}$. Omitting it makes the PDF fail to integrate to 1.
- **Assuming order statistics are independent.** They are not — the value of $X_{(1)}$ constrains all larger order statistics. Only the original i.i.d. observations are independent.

## Quick Check

1. For $n = 3$ i.i.d. Uniform$(0,1)$, write the PDF of the minimum $X_{(1)}$
2. What is $E[X_{(1)}]$ for $n$ i.i.d. Uniform$(0,1)$? (Hint: use the PDF $n(1-x)^{n-1}$)
3. What is the CDF of $X_{(n)}$ for i.i.d. random variables with CDF $F(x)$?

*(Answers: $f_{(1)}(x) = 3(1-x)^2$; $E[X_{(1)}] = \int_0^1 x \cdot n(1-x)^{n-1}dx = 1/(n+1)$; $[F(x)]^n$)*
