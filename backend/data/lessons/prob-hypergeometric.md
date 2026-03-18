# Hypergeometric Distribution

## Overview

The **Hypergeometric distribution** counts successes when sampling **without replacement** from a finite population. It differs from Binomial in that trials are not independent.

## Key Idea

Population: $N$ items, $K$ successes. Draw $n$ without replacement. Number of successes $X$:

$$P(X = k) = \frac{\binom{K}{k}\binom{N-K}{n-k}}{\binom{N}{n}}$$

$$E[X] = \frac{nK}{N}, \quad \text{Var}(X) = n\frac{K}{N}\frac{N-K}{N}\frac{N-n}{N-1}$$

## Worked Examples

**Example 1: Deck of 52 cards, 13 hearts. Draw 5. $P(\text{exactly 2 hearts})$?**

$$\frac{\binom{13}{2}\binom{39}{3}}{\binom{52}{5}} = \frac{78 \times 9139}{2598960} \approx 0.274$$

---

**Example 2: Lot of 20 items, 4 defective. Inspect 5. Expected defects?**

$E[X] = 5 \times 4/20 = 1$.

---

**Example 3: When does Hypergeometric ≈ Binomial?**

When $N$ is large relative to $n$ (say $n < 5\%$ of $N$), sampling with vs. without replacement makes little difference.

## Common Mistakes

- **Using Binomial when sampling without replacement** from a small population.
- **Mixing up $K$, $N-K$, $n$, $k$** in the formula.

## Quick Check

1. $N=10$, $K=4$, $n=3$. $E[X]$?
2. When is $\text{Bin}(n,K/N)$ a good approximation?
3. The variance-reducing factor $(N-n)/(N-1)$ is called what?

*(Answers: 1.2; when $N \gg n$; finite population correction factor)*
