# Discrete Random Variables

## Overview

A **discrete random variable** $X$ takes countable values, each with a certain probability. Its **probability mass function (PMF)** specifies $P(X = x)$ for each value $x$.

## Key Idea

The PMF $p(x) = P(X = x)$ must satisfy:
1. $p(x) \ge 0$ for all $x$
2. $\sum_x p(x) = 1$

The **CDF** is $F(x) = P(X \le x) = \sum_{t \le x} p(t)$.

## Worked Examples

**Example 1: Roll a fair die. PMF?**

$p(k) = 1/6$ for $k = 1, 2, 3, 4, 5, 6$; $p(k) = 0$ otherwise.

---

**Example 2: $X$ has PMF $p(1)=0.2$, $p(2)=0.5$, $p(3)=0.3$. Find $P(X \le 2)$.**

$F(2) = p(1) + p(2) = 0.7$.

---

**Example 3: Valid PMF?**

$p(0)=0.4$, $p(1)=0.3$, $p(2)=0.4$. Sum $= 1.1 \ne 1$. Not valid.

## Common Mistakes

- **PMF summing to more or less than 1.** Always verify.
- **Confusing PMF and CDF.** PMF gives probability at a point; CDF gives cumulative probability.

## Quick Check

1. Valid PMF: $p(1)=p(2)=p(3)=1/3$?
2. For the die, $P(X \le 3)$?
3. $F(2)$ vs. $p(2)$: what's the difference?

*(Answers: yes; 1/2; $F(2)$ is cumulative; $p(2)$ is just $P(X=2)$)*
