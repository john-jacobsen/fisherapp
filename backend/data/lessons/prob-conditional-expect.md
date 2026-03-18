# Conditional Expectation

## Overview

**Conditional expectation** $E[Y|X]$ is a random variable (a function of $X$) that gives the expected value of $Y$ given the value of $X$. It is central to prediction and the tower property.

## Key Idea

$$E[Y|X=x] = \int y\, f_{Y|X}(y|x)\,dy \quad \text{(or sum for discrete)}$$

**Tower property (Law of Total Expectation):** $E[Y] = E[E[Y|X]]$.

**Law of Total Variance:** $\text{Var}(Y) = E[\text{Var}(Y|X)] + \text{Var}(E[Y|X])$.

## Worked Examples

**Example 1: $Y|X=x \sim N(x, 1)$, $X \sim N(0,1)$. Find $E[Y]$.**

$E[Y] = E[E[Y|X]] = E[X] = 0$.

---

**Example 2: $N$ is random, $X_1, \ldots, X_N$ iid with mean $\mu$. $E[S_N]$ where $S_N = \sum_{i=1}^N X_i$.**

$E[S_N|N=n] = n\mu$. By tower: $E[S_N] = E[N\mu] = \mu E[N]$.

---

**Example 3: Eve's law (Law of Total Variance)**

$\text{Var}(Y) = E[\text{Var}(Y|X)] + \text{Var}(E[Y|X])$.

## Common Mistakes

- **Treating $E[Y|X]$ as a number.** It is a random variable (function of $X$).
- **Using $E[Y|X=x]$ when you need $E[Y|X]$.** The former is a number; the latter is a RV.

## Quick Check

1. $E[E[Y|X]] = ?$
2. $E[Y|X=x] = 2x + 3$. If $E[X] = 1$, find $E[Y]$.
3. Var$(Y) \ge$ Var$(E[Y|X])$?

*(Answers: $E[Y]$; 5; yes)*
