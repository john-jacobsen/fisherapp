# Conditional Distributions

## Overview

The **conditional distribution** of $Y$ given $X = x$ is the joint divided by the marginal — it describes how $Y$ behaves when $X$ is fixed at $x$. You are essentially slicing the joint distribution at a particular value of $X$ and renormalizing so the result is a valid distribution. Every conditional distribution is a full probability distribution in its own right: it sums (or integrates) to 1.

## Key Idea

For discrete random variables, the conditional PMF is:

$$p_{Y|X}(y \mid x) = \frac{p(x,y)}{p_X(x)}$$

For continuous random variables, the conditional PDF is:

$$f_{Y|X}(y \mid x) = \frac{f(x,y)}{f_X(x)}$$

In both cases the marginal in the denominator — $p_X(x)$ or $f_X(x)$ — acts as the normalizing constant. It is what makes the conditional a valid distribution rather than just a slice of the joint.

## Worked Examples

**Example 1: Compute $p_{Y|X}(y \mid x = 1)$ from a joint PMF table**

Suppose the joint PMF of $(X, Y)$ is:

| | $Y=0$ | $Y=1$ | $Y=2$ |
|---|---|---|---|
| $X=0$ | 0.1 | 0.2 | 0.1 |
| $X=1$ | 0.1 | 0.3 | 0.2 |

You want the conditional distribution of $Y$ given $X = 1$. First find the marginal $p_X(1)$ by summing across the $X = 1$ row: $0.1 + 0.3 + 0.2 = 0.6$. This is the total weight assigned to the event $X = 1$.

Now divide each joint value in that row by 0.6:

$$p_{Y|X}(0 \mid 1) = \frac{0.1}{0.6} = \frac{1}{6}, \quad p_{Y|X}(1 \mid 1) = \frac{0.3}{0.6} = \frac{1}{2}, \quad p_{Y|X}(2 \mid 1) = \frac{0.2}{0.6} = \frac{1}{3}$$

Dividing by the marginal rescales the row so the probabilities add to 1, giving a valid PMF for $Y$ on $\{0, 1, 2\}$.

---

**Example 2: Find $f_{Y|X}(y \mid x)$ for a bivariate PDF**

Let $f(x, y) = 6x$ on $0 < y < x < 1$ and zero elsewhere. To find the conditional PDF of $Y$ given $X = x$, first compute the marginal of $X$:

$$f_X(x) = \int_0^x 6x \, dy = 6x^2, \quad 0 < x < 1$$

Now divide the joint by the marginal. The denominator $6x^2$ is a constant with respect to $y$, which is exactly why you divide — it normalizes the slice at $X = x$ into a valid PDF over $y$:

$$f_{Y|X}(y \mid x) = \frac{6x}{6x^2} = \frac{1}{x}, \quad 0 < y < x$$

This is a Uniform$(0, x)$ distribution. Once $X$ is fixed at $x$, $Y$ spreads uniformly from 0 to $x$.

---

**Example 3: Verify the conditional PDF integrates to 1**

Using the result from Example 2, $f_{Y|X}(y \mid x) = 1/x$ on $(0, x)$. A conditional PDF must integrate to 1 over all $y$ for each fixed $x$ — this confirms it is a valid distribution, not just a proportional slice of the joint.

$$\int_0^x \frac{1}{x} \, dy = \frac{1}{x} \cdot x = 1 \checkmark$$

The integral equals 1 because the marginal $f_X(x)$ was constructed precisely to make this happen. If you had divided by anything other than the true marginal, this check would fail.

## Common Mistakes

- **Forgetting to compute the marginal first.** You cannot use the joint values as-is. The conditional requires dividing by $p_X(x)$ or $f_X(x)$; skipping this step produces values that do not sum or integrate to 1.
- **Conditioning on a zero-probability event.** The formula $f_{Y|X}(y \mid x)$ is undefined when $f_X(x) = 0$. Conditioning on values outside the support of $X$ is not meaningful.
- **Treating conditional and marginal distributions as the same.** The conditional distribution of $Y$ given $X = x$ changes as $x$ changes. Only when $X$ and $Y$ are independent does $f_{Y|X}(y \mid x) = f_Y(y)$ for all $x$.

## Quick Check

1. From the table in Example 1, compute $p_{Y|X}(y \mid x = 0)$
2. If $f(x,y) = 2$ on $0 < x < y < 1$, find $f_{Y|X}(y \mid x)$
3. For the result in Question 2, verify it integrates to 1 over the appropriate range of $y$

*(Answers: $p_{Y|X}(0\mid 0)=\tfrac{1}{4}$, $p_{Y|X}(1\mid 0)=\tfrac{1}{2}$, $p_{Y|X}(2\mid 0)=\tfrac{1}{4}$; $f_{Y|X}(y\mid x)=\dfrac{1}{1-x}$ for $x < y < 1$; $\int_x^1 \frac{1}{1-x}dy = 1$ ✓)*
