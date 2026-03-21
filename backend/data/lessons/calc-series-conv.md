# Series Convergence

## Overview

An **infinite series** $\displaystyle\sum_{n=1}^\infty a_n$ converges if its partial sums $S_N = \sum_{n=1}^N a_n$ approach a finite limit as $N \to \infty$. Figuring out whether a series converges — and sometimes finding its sum — requires a collection of tests. Each test is suited to a particular type of series. Knowing which test to apply, and when each test is inconclusive, is the main skill.

## Key Idea

Key convergence tests:

$$\text{Divergence test: if } \lim_{n\to\infty} a_n \ne 0 \text{, the series diverges}$$

$$p\text{-series: } \sum_{n=1}^\infty \frac{1}{n^p} \text{ converges} \iff p > 1$$

$$\text{Ratio test: } L = \lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|; \text{ converges if } L < 1\text{, diverges if } L > 1\text{, inconclusive if } L = 1$$

$$\text{Comparison test: if } 0 \le a_n \le b_n \text{ and } \sum b_n \text{ converges, then } \sum a_n \text{ converges}$$

## Worked Examples

**Example 1: Does $\displaystyle\sum_{n=1}^\infty \dfrac{1}{n^2}$ converge?**

This is a $p$-series with $p = 2$. The $p$-series test says: converges if $p > 1$, diverges if $p \le 1$. Since $2 > 1$, the series converges.

Its sum is $\pi^2/6$ (a famous result, but you don't need to derive it to confirm convergence). The $p$-series test alone answers the question.

---

**Example 2: Does $\displaystyle\sum_{n=1}^\infty \dfrac{n}{n+1}$ converge?**

Apply the divergence test first — it's the cheapest test to run. Compute the limit of the general term:

$$\lim_{n\to\infty}\frac{n}{n+1} = \lim_{n\to\infty}\frac{1}{1 + 1/n} = 1 \ne 0$$

Because the terms do not approach 0, the series diverges immediately by the divergence test. No further work is needed.

---

**Example 3: Does $\displaystyle\sum_{n=0}^\infty \dfrac{2^n}{n!}$ converge?**

The ratio test is well-suited when factorials or exponentials appear. Compute the ratio of consecutive terms:

$$\left|\frac{a_{n+1}}{a_n}\right| = \frac{2^{n+1}/(n+1)!}{2^n/n!} = \frac{2^{n+1}}{2^n} \cdot \frac{n!}{(n+1)!} = 2 \cdot \frac{1}{n+1} = \frac{2}{n+1}$$

Take the limit: $L = \lim_{n\to\infty}\dfrac{2}{n+1} = 0$.

Since $L = 0 < 1$, the ratio test confirms the series converges. (Its sum is $e^2$, but convergence alone follows from the ratio test.)

## Common Mistakes

- **Concluding convergence from $a_n \to 0$ alone.** The divergence test runs one direction only: if $a_n \not\to 0$, the series diverges. But $a_n \to 0$ does not guarantee convergence. The harmonic series $\sum 1/n$ diverges even though $1/n \to 0$.
- **Applying the ratio test when $L = 1$.** When the ratio test gives $L = 1$, it is completely inconclusive — the series could converge or diverge. Use a different test (comparison, $p$-series, alternating series).
- **Confusing the divergence test with other tests.** The divergence test can only prove divergence, never convergence. Using it as proof that a series converges is a fundamental error.

## Quick Check

1. Does $\sum 1/n^3$ converge?
2. Does $\sum (-1)^n$ converge?
3. Does $\sum n!/2^n$ converge?

*(Answers: yes, $p$-series with $p = 3 > 1$; no, terms don't approach 0; no, ratio test gives $L = \infty > 1$)*
