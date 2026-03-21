# Simple Random Sampling

## Overview

A **simple random sample (SRS)** of size $n$ is drawn from a finite population of $N$ units by selecting every possible subset of size $n$ with equal probability. This equal-probability property is what makes SRS the foundation of survey sampling: it eliminates systematic bias in who gets selected, so the sample is representative in expectation.

## Key Idea

The natural estimator for the population mean is the sample mean $\hat{\mu} = \bar{x}$. When sampling from a finite population, the standard error includes a **finite population correction (FPC)**:

$$\text{SE}(\bar{x}) = \sqrt{\frac{s^2}{n}\left(1 - \frac{n}{N}\right)}$$

The factor $(1 - n/N)$ is the FPC. When $n \ll N$, it is close to 1 and can be ignored. When $n$ is a large fraction of $N$, the FPC reduces the standard error because sampling a large share of the population leaves less uncertainty.

## Worked Examples

**Example 1: Find the SE with $n = 100$, $N = 1000$, $s = 15$**

First compute the base standard error as if the population were infinite: $s/\sqrt{n} = 15/\sqrt{100} = 1.5$.

Next apply the FPC. The sampling fraction is $n/N = 100/1000 = 0.1$, so the FPC is $\sqrt{1 - 0.1} = \sqrt{0.9} \approx 0.949$.

$$\text{SE}(\bar{x}) = \frac{15}{\sqrt{100}} \cdot \sqrt{1 - \frac{100}{1000}} = 1.5 \times 0.949 \approx 1.42$$

Without the FPC you would overstate the uncertainty by about 5%. Here the correction is modest because you are sampling only 10% of the population.

---

**Example 2: SRS from a large population, $n = 50$, $s = 10$**

When the population is very large relative to $n$, the sampling fraction $n/N \approx 0$, so the FPC $\approx 1$. You can drop it:

$$\text{SE}(\bar{x}) \approx \frac{s}{\sqrt{n}} = \frac{10}{\sqrt{50}} = \frac{10}{7.07} \approx 1.41$$

A rough 95% confidence interval for the population mean uses $\bar{x} \pm 1.96 \cdot \text{SE}$. This works because the CLT guarantees $\bar{x}$ is approximately normal for $n = 50$:

$$\bar{x} \pm 1.96 \times 1.41 \approx \bar{x} \pm 2.77$$

You are 95% confident the population mean lies within about 2.77 units of your sample mean.

---

**Example 3: Why every unit has equal selection probability under SRS**

In an SRS of size $n$ from a population of $N$, the number of subsets containing any fixed unit $u$ is $\binom{N-1}{n-1}$ (choose the remaining $n-1$ units from the other $N-1$). The total number of subsets is $\binom{N}{n}$. The probability unit $u$ is selected is:

$$P(u \text{ selected}) = \frac{\binom{N-1}{n-1}}{\binom{N}{n}} = \frac{n}{N}$$

Every unit has exactly the same selection probability $n/N$, which is why $\bar{x}$ is unbiased for the population mean. Stratified sampling, by contrast, can give different selection probabilities to different groups — which is useful for oversampling rare subpopulations but requires post-stratification weights to avoid bias.

## Common Mistakes

- **Ignoring the FPC when it matters.** If you are sampling more than 5–10% of the population, the FPC meaningfully reduces the SE. Skipping it makes your confidence intervals unnecessarily wide.
- **Confusing SRS with convenience sampling.** SRS requires a sampling frame — a list of all $N$ units — and random selection. Grabbing the first $n$ available units does not give each unit an equal chance of selection and can introduce serious bias.
- **Using the wrong formula for SE.** The formula $s/\sqrt{n}$ applies to independent observations from an infinite population. With a finite population and no FPC, you overstate the variance of $\bar{x}$.

## Quick Check

Try these before using hints:

1. An SRS of $n = 400$ is drawn from $N = 400$. What is the FPC? What does this mean?
2. With $n = 25$, $N = 10{,}000$, $s = 20$, compute $\text{SE}(\bar{x})$.
3. Why is SRS unbiased for the population mean, while taking the first $n$ units from a list may not be?

*(Answers: FPC $= 0$, SE $= 0$ — you have a census; $\approx 4.0$; SRS gives each unit equal probability $n/N$ so there is no systematic over- or underrepresentation)*
