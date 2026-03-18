# Power and Sample Size

## Overview

**Sample size determination** calculates the minimum $n$ needed to achieve a target power (e.g., 80%) at a specified effect size, given $\alpha$. It is done at the design stage before collecting data.

## Key Idea

For a one-sample $Z$-test:

$$n = \left(\frac{(z_{\alpha/2} + z_\beta)\sigma}{\delta}\right)^2$$

where $\delta = |\mu_1 - \mu_0|$ is the minimum effect size to detect and $z_\beta$ comes from the desired power $1-\beta$.

## Worked Examples

**Example 1: $\alpha=0.05$, power$=0.8$, $\sigma=10$, $\delta=5$**

$z_{0.025} = 1.96$, $z_{0.2} = 0.842$.

$n = ((1.96+0.842)\cdot10/5)^2 = (5.604)^2 \approx 31.4$. Use $n=32$.

---

**Example 2: Effect of halving $\delta$**

Halving the effect size quadruples the required $n$ (since $n \propto 1/\delta^2$).

---

**Example 3: Power given $n$**

Rearrange to find power: $\text{power} = P(Z > z_{\alpha/2} - \delta\sqrt{n}/\sigma)$.

## Common Mistakes

- **Using $z_{\alpha}$ instead of $z_{\alpha/2}$ for two-sided tests.**
- **Forgetting to round $n$ up** to the nearest integer.

## Quick Check

1. $n$ doubles — what happens to power?
2. $n$ formula for one-sided test vs. two-sided?
3. Effect size $\delta$ = 0 means what about sample size?

*(Answers: increases; replace $z_{\alpha/2}$ with $z_{\alpha}$; no finite $n$ achieves power > $\alpha$)*
