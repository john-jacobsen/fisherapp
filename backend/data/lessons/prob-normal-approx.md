# Normal Approximation

## Overview

The **Normal approximation** uses the Central Limit Theorem to approximate the distribution of a sum or mean by a Normal distribution. It is especially useful for the Binomial when $n$ is large.

## Key Idea

$X \sim \text{Bin}(n,p) \approx N(np, np(1-p))$ when $np \ge 5$ and $n(1-p) \ge 5$.

**Continuity correction:** To improve accuracy, use $P(X \le k) \approx P\!\left(Z \le \frac{k + 0.5 - np}{\sqrt{np(1-p)}}\right)$.

## Worked Examples

**Example 1: $X \sim \text{Bin}(100, 0.4)$. Approximate $P(X \le 35)$.**

$\mu = 40$, $\sigma = \sqrt{24} \approx 4.9$. $Z = (35.5-40)/4.9 \approx -0.92$. $P(Z \le -0.92) \approx 0.179$.

---

**Example 2: Without continuity correction**

$Z = (35-40)/4.9 \approx -1.02$. $P \approx 0.154$ (less accurate).

---

**Example 3: Rule of thumb check**

$np = 40 \ge 5$ and $n(1-p) = 60 \ge 5$ ✓ — approximation is valid.

## Common Mistakes

- **Forgetting the continuity correction for discrete → continuous approximation.**
- **Using the approximation when $n$ is small or $p$ is near 0 or 1.**

## Quick Check

1. Is Normal approx appropriate for Bin(10, 0.5)?
2. $P(X \le 50)$ with continuity correction for Bin$(100, 0.5)$?
3. $\mu$ and $\sigma$ for Bin$(200, 0.3)$?

*(Answers: borderline ($np=5$); $P(Z \le 0.1)\approx0.54$; $\mu=60$, $\sigma=\sqrt{42}\approx6.48$)*
