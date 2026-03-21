# Discrete Random Variables

## Overview

A **discrete random variable** $X$ is a function that assigns a numerical value to each outcome in a sample space. Rather than working with the outcomes themselves (like $HH$ or $TT$), you work with numbers ($0$, $1$, $2$, …) that summarize what happened. The **probability mass function (PMF)** $p(x) = P(X = x)$ specifies the probability that $X$ takes each possible value. The PMF is the complete description of how probability is distributed across the values of $X$.

## Key Idea

A function $p$ is a valid PMF if and only if it satisfies two conditions:

$$p(x) \geq 0 \quad \text{for all } x, \qquad \text{and} \qquad \sum_{x} p(x) = 1$$

The sum runs over all values $x$ that $X$ can take. From the PMF you can compute probabilities of any event involving $X$ — for example, $P(X > a) = \sum_{x > a} p(x)$.

## Worked Examples

**Example 1: Define $X$ = number of heads in 2 flips and write the PMF table**

Flip a fair coin twice. The sample space is $\{HH, HT, TH, TT\}$, each with probability $1/4$. Define $X$ = the number of heads. $X$ can take the values 0, 1, or 2.

Count outcomes for each value:
- $X = 0$: only $TT$ — one outcome, so $p(0) = 1/4$
- $X = 1$: outcomes $HT$ and $TH$ — two outcomes, so $p(1) = 2/4 = 1/2$
- $X = 2$: only $HH$ — one outcome, so $p(2) = 1/4$

| $x$ | 0 | 1 | 2 |
|---|---|---|---|
| $p(x)$ | $1/4$ | $1/2$ | $1/4$ |

Verify: $1/4 + 1/2 + 1/4 = 1$ ✓. The PMF table is the complete description of $X$'s distribution. Every probability question about $X$ can be answered from this table.

---

**Example 2: Verify a proposed PMF is valid**

A proposed PMF for a random variable $Y$ taking values $\{1, 2, 3, 4\}$ is:

$$p(1) = 0.1, \quad p(2) = 0.3, \quad p(3) = 0.4, \quad p(4) = 0.25$$

Check the two conditions. First, all values are non-negative ✓. Second, sum: $0.1 + 0.3 + 0.4 + 0.25 = 1.05 \neq 1$. The PMF is **not valid** — the probabilities sum to more than 1, which violates the second condition.

A corrected version could rescale all values by dividing by 1.05, but the proposed assignment as stated does not define a legitimate probability distribution. This check — summing the PMF values — is always the first thing to verify.

---

**Example 3: Compute $P(X > 1)$ from a PMF**

Use the PMF from Example 1: $p(0) = 1/4$, $p(1) = 1/2$, $p(2) = 1/4$. Find $P(X > 1)$.

"$X > 1$" means $X \geq 2$. The only value of $X$ that satisfies this is $X = 2$:

$$P(X > 1) = p(2) = \frac{1}{4}$$

Alternatively, use the complement: $P(X > 1) = 1 - P(X \leq 1) = 1 - [p(0) + p(1)] = 1 - [1/4 + 1/2] = 1 - 3/4 = 1/4$.

Both routes agree. The complement approach is especially useful when the event "$X > a$" covers many values — summing the complement $P(X \leq a)$ involves fewer terms.

## Common Mistakes

- **PMF values that do not sum to 1.** This is the most common validity error. A PMF that sums to 0.95 or 1.05 is invalid — it does not describe a complete probability distribution.
- **Confusing the PMF with the cumulative distribution function (CDF).** The PMF gives $P(X = x)$, the probability of a single value. The CDF gives $F(x) = P(X \leq x)$, the cumulative probability up to $x$. These are different functions: $p(2) = 1/4$ but $F(2) = P(X \leq 2) = 1$ for the two-flip example.
- **Trying to apply a discrete PMF to a continuous random variable.** Discrete PMFs work when $X$ takes a countable set of values. For continuous variables (like $X$ uniform on $[0,1]$), you need a probability density function instead.

## Quick Check

1. $X$ takes values $\{0, 1, 2\}$ with $p(0) = 0.2$, $p(1) = 0.5$, $p(2) = 0.3$. Is this a valid PMF?
2. For the same PMF, find $P(X \geq 1)$.
3. A fair four-sided die (faces 1–4) defines $X$ = result. Write the PMF and find $P(X \leq 2)$.

*(Answers: yes, all values $\geq 0$ and sum $= 1.0$; $P(X \geq 1) = p(1)+p(2) = 0.8$; $p(k) = 1/4$ for $k=1,2,3,4$; $P(X \leq 2) = 1/4+1/4 = 1/2$)*
