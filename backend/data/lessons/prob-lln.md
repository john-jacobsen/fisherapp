# Law of Large Numbers

## Overview

The **Law of Large Numbers (LLN)** guarantees that the sample mean $\bar{X}_n$ converges to the population mean $\mu$ as $n \to \infty$. It justifies using averages to estimate expected values.

## Key Idea

Let $X_1, X_2, \ldots$ be iid with $E[X_i] = \mu$. Then $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i \to \mu$.

- **Weak LLN:** $\bar{X}_n \xrightarrow{P} \mu$ (convergence in probability)
- **Strong LLN:** $\bar{X}_n \to \mu$ almost surely

## Worked Examples

**Example 1: Coin flip. $\bar{X}_n$ for $X_i \in \{0,1\}$ with $p=0.5$.**

$E[X] = 0.5$. By LLN, the proportion of heads approaches 0.5 as $n \to \infty$.

---

**Example 2: Gambling fallacy**

After 10 tails, it is tempting to think "heads is due." LLN says the long-run frequency goes to 0.5, but individual future flips are still fair.

---

**Example 3: Monte Carlo integration**

$E[g(X)] \approx \frac{1}{n}\sum_{i=1}^n g(X_i)$. By LLN, this converges to the true integral.

## Common Mistakes

- **Gambler's fallacy.** LLN says the average converges, not that individual outcomes "correct" themselves.
- **Applying LLN when variables are not iid.** Some conditions on dependence are needed.

## Quick Check

1. What does $\bar{X}_n \xrightarrow{P} \mu$ mean?
2. Does LLN say $\bar{X}_{100}$ will be exactly $\mu$?
3. What distribution assumption does the Weak LLN require?

*(Answers: $P(|\bar{X}_n - \mu| > \epsilon) \to 0$; no, approximately; finite mean)*
