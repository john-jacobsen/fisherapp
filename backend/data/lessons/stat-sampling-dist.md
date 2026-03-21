# Sampling Distributions

## Overview

A **sampling distribution** is the distribution of a statistic — such as the sample mean $\bar{X}$ — across all possible samples of size $n$ drawn from a population. You never observe this distribution directly; instead, you reason about it theoretically to make inferences. Understanding sampling distributions is what connects a single observed sample to claims about the population.

## Key Idea

If $X_1, X_2, \ldots, X_n \overset{iid}{\sim} (\mu, \sigma^2)$ (mean $\mu$, variance $\sigma^2$), then the sample mean satisfies:

$$\bar{X} \sim \left(\mu,\, \frac{\sigma^2}{n}\right)$$

The mean of $\bar{X}$ equals the population mean, and its variance shrinks by a factor of $n$. The Central Limit Theorem (CLT) adds that $\bar{X}$ is approximately normal for large $n$, regardless of the shape of the original population.

## Worked Examples

**Example 1: Find the mean and variance of $\bar{X}$**

Suppose $X_i \overset{iid}{\sim} (\mu, \sigma^2)$ with $\mu = 10$, $\sigma^2 = 100$, and $n = 25$.

Because each $X_i$ has mean $\mu$, linearity of expectation gives $E[\bar{X}] = \mu = 10$. The variance of a sum of independent variables adds, so $\text{Var}(X_1 + \cdots + X_{25}) = 25\sigma^2 = 2500$. Dividing by $n^2 = 625$ (since $\bar{X} = \frac{1}{n}\sum X_i$):

$$\text{Var}(\bar{X}) = \frac{\sigma^2}{n} = \frac{100}{25} = 4$$

So $\bar{X}$ is centered at 10 with standard error $\text{SE} = \sqrt{4} = 2$.

---

**Example 2: Compute $P(\bar{X} > 12)$ using the CLT**

Let $n = 36$, $\mu = 10$, $\sigma = 6$. By the CLT, $\bar{X}$ is approximately normal with mean 10 and variance $\sigma^2/n = 36/36 = 1$, so $\text{SE} = 1$.

Standardize by subtracting the mean and dividing by the SE. This works because a linear transformation of a normal random variable is also normal:

$$Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} = \frac{12 - 10}{1} = 2$$

$$P(\bar{X} > 12) = P(Z > 2) \approx 1 - 0.9772 = 0.0228$$

There is roughly a 2.3% chance of observing a sample mean above 12.

---

**Example 3: Compute $P(\bar{X} < 48)$**

Let $n = 16$, $\mu = 50$, $\sigma = 8$. The standard error is $\sigma/\sqrt{n} = 8/4 = 2$.

Standardize the cutoff:

$$Z = \frac{48 - 50}{2} = -1$$

$$P(\bar{X} < 48) = P(Z < -1) \approx 0.1587$$

There is about a 15.9% chance the sample mean falls below 48. The sample mean is less than 1 standard error below the population mean, so this event is not especially rare.

## Common Mistakes

- **Confusing $\sigma$ with $\sigma/\sqrt{n}$.** The population standard deviation $\sigma$ describes individual observations. The standard error $\sigma/\sqrt{n}$ describes the variability of the sample mean. Always divide by $\sqrt{n}$ when working with $\bar{X}$.
- **Applying the CLT to small samples.** The normal approximation for $\bar{X}$ requires a reasonably large $n$ (often $n \geq 30$ as a rule of thumb). For small samples from non-normal populations, the approximation can be poor.
- **Forgetting the i.i.d. assumption.** The formula $\text{Var}(\bar{X}) = \sigma^2/n$ requires the observations to be independent and identically distributed. Dependence among observations inflates the true variance of $\bar{X}$.

## Quick Check

Try these before using hints:

1. If $X_i \overset{iid}{\sim} (\mu, \sigma^2)$ with $\mu = 5$ and $\sigma^2 = 36$, what is $\text{Var}(\bar{X})$ when $n = 9$?
2. With $n = 64$, $\mu = 0$, $\sigma = 8$, what is $P(\bar{X} > 1)$?
3. For $n = 100$, $\mu = 20$, $\sigma = 10$, what is the standard error of $\bar{X}$?

*(Answers: 4, $P(Z > 1) \approx 0.1587$, 1)*
