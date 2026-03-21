# Normal Distribution

## Overview

The **normal distribution** $N(\mu, \sigma^2)$ is the symmetric bell curve characterized by its mean $\mu$ and variance $\sigma^2$. It appears throughout probability and statistics because the Central Limit Theorem guarantees that sums of many independent random variables are approximately normal, regardless of the original distribution. To find probabilities, you standardize: convert $X$ to a standard normal $Z \sim N(0,1)$, then look up values in a $Z$-table.

## Key Idea

If $X \sim N(\mu, \sigma^2)$, the standardization formula converts any normal to the standard normal:

$$Z = \frac{X - \mu}{\sigma}$$

The PDF of the normal distribution is:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\, e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

You rarely compute probabilities directly from the PDF — instead you standardize to $Z$ and use the standard normal CDF $\Phi(z) = P(Z \leq z)$. Key values: $\Phi(1.645) \approx 0.95$, $\Phi(1.960) \approx 0.975$, $\Phi(2.326) \approx 0.99$.

## Worked Examples

**Example 1: Find $P(X < 70)$ for $X \sim N(60, 100)$**

Here $\mu = 60$ and $\sigma = \sqrt{100} = 10$. Standardizing converts the question about $X$ to an equivalent question about $Z$ — you subtract the mean and divide by the standard deviation, which shifts and scales the distribution to have mean 0 and variance 1:

$$P(X < 70) = P\!\left(Z < \frac{70 - 60}{10}\right) = P(Z < 1) = \Phi(1) \approx 0.8413$$

There is about an 84.1% chance that $X$ falls below 70. The $z$-score of 1 means that 70 is exactly one standard deviation above the mean.

---

**Example 2: Find $P(50 < X < 70)$**

With the same $X \sim N(60, 100)$, standardize both endpoints:

$$P(50 < X < 70) = P\!\left(\frac{50-60}{10} < Z < \frac{70-60}{10}\right) = P(-1 < Z < 1)$$

Use the symmetry of the standard normal — $P(Z < -1) = 1 - \Phi(1)$ because the distribution is symmetric around 0:

$$P(-1 < Z < 1) = \Phi(1) - \Phi(-1) = \Phi(1) - (1 - \Phi(1)) = 2\Phi(1) - 1 \approx 2(0.8413) - 1 = 0.6827$$

About 68.3% of the distribution lies within one standard deviation of the mean. This is the famous "68-95-99.7 rule" at work.

---

**Example 3: Find $x$ such that $P(X < x) = 0.975$**

This is an inverse normal problem: you are given a probability and need to find the corresponding value. Working backwards — the $Z$-table tells you $\Phi(1.96) \approx 0.975$, so the $z$-score you need is $z^* = 1.96$.

Reverse the standardization formula to recover $x$. If $z = (x - \mu)/\sigma$, then $x = \mu + z\sigma$:

$$x = \mu + z^*\sigma = 60 + 1.96 \cdot 10 = 60 + 19.6 = 79.6$$

The value $x = 79.6$ cuts off the upper 2.5% of the distribution. This is exactly how critical values for confidence intervals are constructed.

## Common Mistakes

- **Using $\sigma^2$ instead of $\sigma$ in the standardization formula.** The formula is $Z = (X - \mu)/\sigma$, dividing by the standard deviation, not the variance. Always take the square root of the variance first.
- **Forgetting to flip the inequality for $P(X > a)$.** Since $Z$-tables give $P(Z \leq z)$, you need $P(Z > z) = 1 - \Phi(z)$. Write out the complement explicitly before looking anything up.
- **Misreading $N(\mu, \sigma^2)$ vs. $N(\mu, \sigma)$.** Some textbooks parameterize the normal by standard deviation, others by variance. Always check which convention is in use before identifying $\sigma$.

## Quick Check

1. $X \sim N(100, 25)$. Find $P(X < 105)$.
2. For the same $X$, find $P(95 < X < 105)$.
3. Find $x$ such that $P(X > x) = 0.10$ for $X \sim N(100, 25)$.

*(Answers: $\sigma = 5$; $P(Z < 1) \approx 0.8413$; $P(-1 < Z < 1) \approx 0.6827$; $P(X > x) = 0.10 \Rightarrow z^* = 1.282$, $x = 100 + 1.282(5) \approx 106.4$)*
