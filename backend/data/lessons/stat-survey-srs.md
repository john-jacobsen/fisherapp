# Simple Random Sampling

## Overview

**Simple random sampling (SRS)** is the most basic probability sampling method: every sample of size $n$ from a population of size $N$ has an equal chance of being selected. It is the benchmark for all other sampling designs.

## Key Idea

Under SRS without replacement: $E[\bar{x}] = \mu$, and the variance includes a **finite population correction (FPC)**:

$$\text{Var}(\bar{x}) = \frac{\sigma^2}{n} \cdot \frac{N-n}{N-1}$$

When $n/N < 5\%$, the FPC $\approx 1$ and you can ignore it.

## Worked Examples

**Example 1: Population of 1000, $\sigma=10$. SRS of $n=50$. SE?**

FPC $= \sqrt{(1000-50)/999} \approx 0.975$. $\text{SE} = (10/\sqrt{50}) \times 0.975 \approx 1.38$.

---

**Example 2: When is FPC negligible?**

$n/N = 50/1000 = 5\%$ — borderline. If $n/N < 5\%$, skip FPC.

---

**Example 3: Sampling frame vs. sample**

The **sampling frame** is the list from which you draw. Bias occurs when the frame misses parts of the population.

## Common Mistakes

- **Using SRS when systematic bias exists** (e.g., convenience sampling is not SRS).
- **Ignoring FPC for large sampling fractions.**

## Quick Check

1. Every sample of size $n$ has equal probability in SRS — true?
2. FPC for $n=100$, $N=200$?
3. What is the sampling frame?

*(Answers: yes; $\sqrt{100/199}\approx0.708$; list of units from which sample is drawn)*
