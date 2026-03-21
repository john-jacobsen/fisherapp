# Conditional Expectation

## Overview

The **conditional expectation** $E[Y \mid X = x]$ is the expected value of $Y$ when $X$ is fixed at $x$ — it is computed exactly like an ordinary expectation, but using the conditional distribution of $Y$ given $X = x$ instead of the marginal distribution of $Y$. As $x$ varies, $E[Y \mid X = x]$ becomes a function of $x$, and the law of total expectation recovers the unconditional mean by averaging that function over $X$.

## Key Idea

For discrete random variables:

$$E[Y \mid X = x] = \sum_y y \cdot p_{Y|X}(y \mid x)$$

The **law of total expectation** (also called iterated expectation) connects conditional and unconditional expectations:

$$E[Y] = E\bigl[E[Y \mid X]\bigr] = \sum_x E[Y \mid X = x]\,p_X(x)$$

The inner expectation is over $Y$; the outer expectation is over $X$. This identity holds whenever all expectations exist.

## Worked Examples

**Example 1: Compute $E[Y \mid X = 2]$ from a joint PMF**

Suppose the joint PMF of $(X, Y)$ gives:

| | $Y=1$ | $Y=3$ | $Y=5$ |
|---|---|---|---|
| $X=1$ | 0.2 | 0.1 | 0.1 |
| $X=2$ | 0.1 | 0.3 | 0.2 |

The marginal $p_X(2) = 0.1 + 0.3 + 0.2 = 0.6$. Conditioning on $X = 2$ means you restrict attention to the $X = 2$ row and renormalize — the conditional PMF of $Y$ given $X = 2$ is:

$$p_{Y|X}(1 \mid 2) = \frac{1}{6}, \quad p_{Y|X}(3 \mid 2) = \frac{1}{2}, \quad p_{Y|X}(5 \mid 2) = \frac{1}{3}$$

Now compute the expected value using these weights. Each value of $Y$ is multiplied by its conditional probability, not its marginal probability:

$$E[Y \mid X = 2] = 1 \cdot \frac{1}{6} + 3 \cdot \frac{1}{2} + 5 \cdot \frac{1}{3} = \frac{1}{6} + \frac{3}{2} + \frac{5}{3} = \frac{1 + 9 + 10}{6} = \frac{20}{6} \approx 3.33$$

---

**Example 2: Apply the law of total expectation to find $E[Y]$**

Using the same table, compute $E[Y \mid X = 1]$ as well. The marginal $p_X(1) = 0.4$, giving conditional PMF $p_{Y|X}(1\mid 1) = 1/2$, $p_{Y|X}(3\mid 1) = 1/4$, $p_{Y|X}(5\mid 1) = 1/4$.

$$E[Y \mid X = 1] = 1 \cdot \frac{1}{2} + 3 \cdot \frac{1}{4} + 5 \cdot \frac{1}{4} = \frac{1}{2} + \frac{3}{4} + \frac{5}{4} = 2.5$$

The law of total expectation says to average the conditional means, weighted by the marginal probabilities of $X$. This works because each conditional mean represents the average of $Y$ in a subpopulation, and weighting by $p_X(x)$ recombines those subpopulations into the overall average:

$$E[Y] = E[Y \mid X=1]\,p_X(1) + E[Y \mid X=2]\,p_X(2) = 2.5(0.4) + 3.33(0.6) = 1.0 + 2.0 = 3.0$$

---

**Example 3: Iterated expectation in a two-stage experiment**

A factory produces batches. Each batch has a random size $N \sim \text{Poisson}(5)$. Each item in a batch is defective independently with probability 0.1. Let $D$ be the number of defectives in a batch.

Conditioning on $N$ first: given $N = n$, each item is independently defective with probability 0.1, so $D \mid N = n \sim \text{Binomial}(n, 0.1)$, giving $E[D \mid N = n] = 0.1n$.

By the law of total expectation, averaging over $N$:

$$E[D] = E[E[D \mid N]] = E[0.1N] = 0.1\,E[N] = 0.1 \times 5 = 0.5$$

Conditioning on the intermediate quantity $N$ first simplified the problem dramatically — instead of computing the marginal distribution of $D$ directly, you used a two-step average.

## Common Mistakes

- **Confusing $E[Y \mid X = x]$ with $E[Y]$.** The conditional expectation depends on $x$ and changes as $x$ changes. Setting $x$ to a fixed value gives a number; treating $X$ as random gives the random variable $E[Y \mid X]$.
- **Applying total expectation without weighting by $p_X(x)$.** Simply averaging the conditional means $E[Y \mid X = x]$ equally across values of $x$ is wrong unless $X$ is uniform. You must weight by $p_X(x)$ (or $f_X(x)$ in the continuous case).
- **Forgetting that $E[E[Y \mid X]] = E[Y]$, not $E[Y^2]$ or any other moment.** The law of total expectation recovers the mean of $Y$, not its variance or any higher moment.

## Quick Check

1. If $E[Y \mid X = 0] = 4$ and $E[Y \mid X = 1] = 10$, and $P(X = 0) = 0.6$, what is $E[Y]$?
2. Why is $E[Y \mid X = x]$ called a function of $x$?
3. If $Y = 3X + 2$, what is $E[Y \mid X = x]$?

*(Answers: $4(0.6) + 10(0.4) = 6.4$; because it assigns a number to each value $x$ that $X$ can take; $3x + 2$)*
