# Variance

## Overview

**Variance** measures the spread of a distribution around its mean. A large variance means values tend to be far from the mean; variance 0 means the variable is constant.

## Key Idea

$$\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

Standard deviation $\sigma = \sqrt{\text{Var}(X)}$.

For independent $X$ and $Y$: $\text{Var}(aX + bY) = a^2\text{Var}(X) + b^2\text{Var}(Y)$.

## Worked Examples

**Example 1: Variance of a fair die**

$E[X]=3.5$, $E[X^2] = \frac{1}{6}(1+4+9+16+25+36) = 91/6 \approx 15.17$.

$\text{Var}(X) = 91/6 - (3.5)^2 = 91/6 - 49/4 = 35/12 \approx 2.92$.

---

**Example 2: $\text{Var}(3X + 2)$ if $\text{Var}(X) = 5$**

$\text{Var}(3X+2) = 9\text{Var}(X) = 45$. (Constants don't add variance.)

---

**Example 3: Bernoulli$(p)$ variance**

$E[X] = p$, $E[X^2] = p$ (since $X^2 = X$ for 0/1). $\text{Var}(X) = p - p^2 = p(1-p)$.

## Common Mistakes

- **Adding variances for non-independent variables.** The formula $\text{Var}(X+Y)=\text{Var}(X)+\text{Var}(Y)$ requires independence.
- **Confusing standard deviation with variance.** $\text{SD} = \sqrt{\text{Var}}$.

## Quick Check

1. $E[X]=2$, $E[X^2]=8$. Find $\text{Var}(X)$.
2. $\text{Var}(5X)$ if $\text{Var}(X)=4$?
3. Minimum possible variance?

*(Answers: 4; 100; 0 (constant variable))*
