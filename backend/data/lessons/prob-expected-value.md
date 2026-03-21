# Expected Value

## Overview

The **expected value** $E[X]$ is the probability-weighted average of all values $X$ can take — the long-run mean outcome per trial. It does not tell you what will happen on any single trial; it tells you what you should expect on average over many repetitions. Think of it as the center of gravity of the distribution: each outcome contributes its value, weighted by how often it occurs.

## Key Idea

For a discrete random variable $X$ taking values $x$ with probabilities $p(x)$:

$$E[X] = \sum_x x \cdot p(x)$$

**Linearity of expectation** holds regardless of whether $X$ and $Y$ are independent:

$$E[aX + b] = aE[X] + b$$

$$E[X + Y] = E[X] + E[Y]$$

Linearity is one of the most powerful tools in probability — it lets you break a complicated random variable into simpler pieces.

## Worked Examples

**Example 1: Expected number of heads in 3 fair coin flips**

Let $X$ be the number of heads. The possible values are 0, 1, 2, 3. Each has a specific probability from the binomial distribution with $n = 3$, $p = 1/2$.

Build the weighted sum — each value multiplied by its probability:

$$E[X] = 0 \cdot \frac{1}{8} + 1 \cdot \frac{3}{8} + 2 \cdot \frac{3}{8} + 3 \cdot \frac{1}{8} = 0 + \frac{3}{8} + \frac{6}{8} + \frac{3}{8} = \frac{12}{8} = \frac{3}{2}$$

The expected number of heads is $1.5$. This makes sense: with a fair coin, you expect half the flips to land heads, and $3 \times \frac{1}{2} = 1.5$.

---

**Example 2: Expected winnings in a simple game**

You pay \$1 to play. You roll a fair die: if you roll a 6, you win \$5; otherwise you win nothing. Your net gain $X$ takes values $-1$ (probability $5/6$) and $+4$ (probability $1/6$, since you receive \$5 but paid \$1).

Applying the definition — multiply each net outcome by its probability and sum:

$$E[X] = (-1) \cdot \frac{5}{6} + 4 \cdot \frac{1}{6} = \frac{-5 + 4}{6} = \frac{-1}{6} \approx -0.17$$

The game has negative expected value, meaning you lose about 17 cents on average per play. This is why understanding $E[X]$ matters: a game can feel exciting even when it drains money in the long run.

---

**Example 3: Use linearity to compute $E[3X - 2]$ given $E[X] = 5$**

You are told $E[X] = 5$ and asked for $E[3X - 2]$. You do not need to know the full distribution of $X$ — linearity handles everything.

Pull the constant $a = 3$ out in front and subtract $b = 2$:

$$E[3X - 2] = 3E[X] - 2 = 3(5) - 2 = 15 - 2 = 13$$

The result is 13. Linearity works because expectation is a sum and that operation distributes over addition and pulls out constants. The shift $-2$ shifts the average by $-2$; the scale factor 3 stretches the average by 3.

## Common Mistakes

- **Confusing $E[f(X)]$ with $f(E[X])$.** In general $E[X^2] \neq (E[X])^2$. Linearity applies to linear functions only; for nonlinear functions you must use the full definition.
- **Forgetting to use net values.** In games or monetary problems, make sure $x$ represents your actual gain or loss, not just the prize. If you paid \$1 to play and win \$5, your net is \$4, not \$5.
- **Assuming $E[XY] = E[X]E[Y]$ always.** This identity holds only when $X$ and $Y$ are independent. Linearity of expectation ($E[X+Y] = E[X]+E[Y]$) requires no independence assumption, but the product rule does.

## Quick Check

1. A random variable takes value 2 with probability 0.3 and value 8 with probability 0.7. Find $E[X]$.
2. A game pays \$10 with probability 0.1 and \$0 otherwise; entry costs \$2. Find the expected net gain.
3. If $E[X] = 4$, find $E[5X + 3]$.

*(Answers: $0.3(2) + 0.7(8) = 6.2$; $10(0.1) - 2 = -1$; $5(4)+3 = 23$)*
