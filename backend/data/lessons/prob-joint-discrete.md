# Joint Distributions (Discrete)

## Overview

The **joint PMF** $p(x, y) = P(X = x, Y = y)$ fully describes the probabilistic behavior of two discrete random variables together. It tells you the probability of every possible combination of outcomes. From it you can recover each variable's individual distribution (the marginals), compute joint probabilities, and test for independence — all by summing appropriately.

## Key Idea

The joint PMF must satisfy:

$$\sum_x \sum_y p(x, y) = 1, \qquad p(x, y) \geq 0$$

Marginals are recovered by summing out the other variable:

$$p_X(x) = \sum_y p(x, y), \qquad p_Y(y) = \sum_x p(x, y)$$

Independence: $X$ and $Y$ are independent if and only if $p(x, y) = p_X(x)\, p_Y(y)$ for every pair $(x, y)$.

## Worked Examples

**Example 1: Write the joint PMF table for two fair dice and read off a joint probability.**

Let $X$ be the result of die 1 and $Y$ the result of die 2. Since the dice are fair and independent, every pair $(i, j)$ with $i, j \in \{1, 2, 3, 4, 5, 6\}$ has equal probability. There are 36 equally likely outcomes, so:

$$p(i, j) = P(X = i, Y = j) = \frac{1}{36} \quad \text{for all } i, j \in \{1,\ldots,6\}$$

Reading off a specific joint probability: $P(X = 3, Y = 5) = 1/36$. The joint table is a $6 \times 6$ grid of $1/36$ entries, and summing all 36 entries gives 1.

---

**Example 2: Recover a marginal PMF by summing rows or columns.**

Consider the joint PMF table:

| $p(x,y)$ | $Y = 0$ | $Y = 1$ | $Y = 2$ |
|---|---|---|---|
| $X = 0$ | 0.10 | 0.15 | 0.05 |
| $X = 1$ | 0.20 | 0.30 | 0.20 |

The marginal of $X$ is found by summing each row — you are adding up all the ways $X$ can take a given value, regardless of what $Y$ does. This is the law of total probability applied to a partition over $Y$.

$$p_X(0) = 0.10 + 0.15 + 0.05 = 0.30$$
$$p_X(1) = 0.20 + 0.30 + 0.20 = 0.70$$

The marginal of $Y$ is found by summing each column: $p_Y(0) = 0.30$, $p_Y(1) = 0.45$, $p_Y(2) = 0.25$. Check: all marginals sum to 1.

---

**Example 3: Check whether $X$ and $Y$ are independent.**

Using the table from Example 2, test the independence condition $p(x, y) = p_X(x)\,p_Y(y)$ at one cell. Independence requires this to hold for every $(x, y)$ pair — a single failure is enough to conclude dependence.

$$p_X(0) \cdot p_Y(0) = 0.30 \times 0.30 = 0.09 \neq 0.10 = p(0, 0)$$

The condition fails, so $X$ and $Y$ are not independent. Intuitively, knowing $X = 0$ shifts the distribution of $Y$ — the conditional probabilities of $Y$ given $X = 0$ are $1/6$, $1/2$, $1/6$, which differ from the marginal probabilities of $Y$. Dependence means one variable carries information about the other.

## Common Mistakes

- **Confusing the joint PMF with the conditional PMF.** The joint gives $P(X = x, Y = y)$; the conditional gives $P(X = x \mid Y = y) = p(x,y)/p_Y(y)$. These are different quantities — the conditional rescales by the marginal of the given variable.
- **Declaring independence from a single matching cell.** You must verify $p(x,y) = p_X(x)\,p_Y(y)$ for every $(x, y)$ pair. Finding one cell that matches does not establish independence.

## Quick Check

1. A joint PMF table has entries: $p(0,0) = 0.2$, $p(0,1) = 0.3$, $p(1,0) = 0.1$, $p(1,1) = 0.4$. Find $p_Y(1)$.
2. For the same table, are $X$ and $Y$ independent?
3. What must the sum of all entries in a joint PMF table equal?

*(Answers: $p_Y(1) = 0.3 + 0.4 = 0.7$; check $p_X(0)\,p_Y(0) = 0.5 \times 0.3 = 0.15 \neq 0.2$, so no; 1)*
