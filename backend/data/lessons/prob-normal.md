# Normal Distribution

## Overview

The **Normal (Gaussian) distribution** is the bell-shaped, symmetric distribution that appears throughout statistics due to the Central Limit Theorem. It is parameterized by mean $\mu$ and variance $\sigma^2$.

## Key Idea

$X \sim N(\mu, \sigma^2)$ has PDF:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

**Standardize:** $Z = (X - \mu)/\sigma \sim N(0,1)$. Use $Z$-tables or software to find probabilities.

## Worked Examples

**Example 1: $X \sim N(100, 225)$. $P(X < 112)$?**

$Z = (112-100)/15 = 0.8$. $P(Z < 0.8) \approx 0.788$.

---

**Example 2: 68-95-99.7 rule**

$P(\mu - \sigma < X < \mu + \sigma) \approx 0.68$. $P(|Z| < 2) \approx 0.954$. $P(|Z| < 3) \approx 0.997$.

---

**Example 3: $P(a < X < b)$**

$P(80 < X < 110) = P(-4/3 < Z < 2/3) \approx P(Z < 0.67) - P(Z < -1.33) \approx 0.749 - 0.092 = 0.657$.

## Common Mistakes

- **Forgetting to standardize before using the $Z$-table.**
- **Confusing $N(\mu, \sigma^2)$ with $N(\mu, \sigma)$.** Always check whether the second parameter is variance or SD.

## Quick Check

1. $Z$ for $x=75$ if $X \sim N(80, 100)$?
2. $P(-1 < Z < 1) \approx ?$
3. $P(X > \mu)$ for any normal distribution?

*(Answers: $-0.5$; 0.68; 0.5)*
