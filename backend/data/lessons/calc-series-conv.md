# Series Convergence

## Overview

An **infinite series** $\sum_{n=1}^\infty a_n$ converges if its partial sums approach a finite limit. Several tests determine whether a series converges without finding the actual sum.

## Key Idea

Key tests:
- **Divergence test:** If $a_n \not\to 0$, the series diverges.
- **$p$-series:** $\sum 1/n^p$ converges iff $p > 1$.
- **Ratio test:** $L = \lim |a_{n+1}/a_n|$; converges if $L < 1$, diverges if $L > 1$.
- **Comparison test:** Compare to a known series.

## Worked Examples

**Example 1: Does $\sum_{n=1}^\infty \frac{1}{n^2}$ converge?**

$p = 2 > 1$, so yes (p-series). Sum $= \pi^2/6$.

---

**Example 2: Does $\sum_{n=1}^\infty \frac{n}{n+1}$ converge?**

$a_n = n/(n+1) \to 1 \ne 0$. Diverges by the divergence test.

---

**Example 3: Does $\sum_{n=0}^\infty \frac{2^n}{n!}$ converge?**

Ratio test: $L = \lim \frac{2^{n+1}/(n+1)!}{2^n/n!} = \lim \frac{2}{n+1} = 0 < 1$. Converges.

## Common Mistakes

- **Concluding convergence from $a_n \to 0$ alone.** The harmonic series $\sum 1/n$ diverges even though $1/n \to 0$.
- **Applying the ratio test when $L = 1$** — the test is inconclusive there.

## Quick Check

1. Does $\sum 1/n^3$ converge?
2. Does $\sum (-1)^n$ converge?
3. Does $\sum n!/2^n$ converge?

*(Answers: yes (p-series, p=3); no (terms don't → 0); no (ratio test, L = ∞))*
