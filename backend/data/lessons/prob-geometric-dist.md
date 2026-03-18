# Geometric Distribution

## Overview

The **Geometric distribution** counts the number of trials until the first success in a sequence of independent Bernoulli trials with success probability $p$.

## Key Idea

$X \sim \text{Geom}(p)$: number of trials until (and including) first success.

$$P(X = k) = (1-p)^{k-1} p, \quad k = 1, 2, 3, \ldots$$

$$E[X] = \frac{1}{p}, \quad \text{Var}(X) = \frac{1-p}{p^2}$$

## Worked Examples

**Example 1: Roll a die until a 6. $P(X = 3)$?**

$(5/6)^2(1/6) = 25/216 \approx 0.116$.

---

**Example 2: Expected rolls to get a 6?**

$E[X] = 1/(1/6) = 6$.

---

**Example 3: $P(X > 3)$ for $p = 1/4$?**

Fail first 3 times: $(3/4)^3 = 27/64 \approx 0.422$.

## Common Mistakes

- **Two versions of geometric exist.** $X$ = number of trials (starting from 1) vs. $X$ = number of failures before first success. Know which convention is used.
- **Thinking variance is $1/p^2$.** It's $(1-p)/p^2$.

## Quick Check

1. $P(X=1)$ for $\text{Geom}(0.3)$?
2. $E[X]$ for $p=0.5$?
3. $P(X \ge 2)$ for $p=0.4$?

*(Answers: 0.3; 2; 0.6)*
