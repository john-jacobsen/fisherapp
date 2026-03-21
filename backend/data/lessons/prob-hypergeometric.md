# Hypergeometric Distribution

## Overview

The **hypergeometric distribution** counts the number of successes in a sample drawn without replacement from a finite population. Unlike the binomial, successive draws are not independent — removing an item changes what is left. Whenever you sample from a finite pool and do not return items, the hypergeometric is the right model.

## Key Idea

A population has $N$ items total, of which $K$ are "successes" and $N - K$ are "failures." You draw $n$ items without replacement. The number of successes $X$ in your sample follows the hypergeometric distribution:

$$P(X = k) = \frac{\displaystyle\binom{K}{k}\binom{N-K}{n-k}}{\displaystyle\binom{N}{n}}$$

The numerator counts favorable outcomes: choose $k$ successes from the $K$ available, and $n - k$ failures from the $N - K$ available. The denominator counts all ways to choose $n$ items from $N$.

The mean is:

$$E[X] = \frac{nK}{N}$$

This has the same form as $np$ for the binomial, with $p = K/N$ — the fraction of successes in the population.

## Worked Examples

**Example 1: Drawing 5 cards — probability of exactly 2 aces**

A standard deck has $N = 52$ cards, $K = 4$ aces, $N - K = 48$ non-aces. You draw $n = 5$ cards without replacement and want $k = 2$ aces.

The $\binom{4}{2}$ counts ways to choose 2 aces from the 4 available; $\binom{48}{3}$ counts ways to fill the remaining 3 spots from non-aces; $\binom{52}{5}$ counts all 5-card hands:

$$P(X = 2) = \frac{\binom{4}{2}\binom{48}{3}}{\binom{52}{5}} = \frac{6 \cdot 17296}{2598960} = \frac{103776}{2598960} \approx 0.0399$$

The probability is about 4.0%.

---

**Example 2: Quality control sampling**

A batch has $N = 20$ items, $K = 4$ defective. An inspector draws $n = 5$ at random without replacement. Find $P(X = 1)$, the probability of catching exactly 1 defective.

Choose 1 defective from the 4 available, and fill the remaining 4 slots with non-defective items from the $20 - 4 = 16$ non-defective ones:

$$P(X = 1) = \frac{\binom{4}{1}\binom{16}{4}}{\binom{20}{5}} = \frac{4 \cdot 1820}{15504} = \frac{7280}{15504} \approx 0.470$$

There is about a 47% chance the sample contains exactly 1 defective — a common calculation in acceptance sampling.

---

**Example 3: Computing the mean**

For the quality control setup above ($N = 20$, $K = 4$, $n = 5$), find the expected number of defective items in the sample.

You do not need to sum over all possible values of $k$. The mean formula gives it directly — the fraction of defectives in the population, $K/N$, times the sample size $n$:

$$E[X] = \frac{nK}{N} = \frac{5 \cdot 4}{20} = 1$$

On average, exactly 1 of the 5 sampled items is defective. This matches intuition: 4 out of 20 items (20%) are defective, and 20% of a sample of 5 is 1.

## Common Mistakes

- **Using the binomial when sampling without replacement from a small population.** If $n$ is a substantial fraction of $N$ (say, more than 5–10%), use the hypergeometric. The binomial is a good approximation only when $N$ is very large relative to $n$.
- **Mixing up $K$ and $N - K$ in the second binomial.** The second factor $\binom{N-K}{n-k}$ draws from the failures, not the successes. Keep track of what each group represents.
- **Forgetting the validity constraint.** $k$ must satisfy $\max(0, n - (N-K)) \leq k \leq \min(n, K)$. Outside this range, the probability is 0 — you cannot choose more aces than exist in the deck.

## Quick Check

1. A bag has 10 marbles: 3 red and 7 blue. You draw 4 without replacement. Find $P(X = 1)$ where $X$ counts red marbles.
2. For the same setup, find $E[X]$.
3. Why can't you use the binomial distribution to model this scenario exactly?

*(Answers: $\frac{\binom{3}{1}\binom{7}{3}}{\binom{10}{4}} = \frac{3 \cdot 35}{210} = \frac{105}{210} = 0.5$; $E[X] = \frac{4 \cdot 3}{10} = 1.2$; draws are not independent — removing a marble changes the composition of the bag)*
