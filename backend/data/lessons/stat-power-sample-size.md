# Power Analysis and Sample Size

## Overview

**Power analysis** determines the sample size $n$ needed to reliably detect an effect of a given magnitude. Before collecting data, you specify four quantities: the significance level $\alpha$, the desired power $1-\beta$, the effect size $\delta = \mu_1 - \mu_0$, and the standard deviation $\sigma$. These four quantities are linked by a formula — knowing any three lets you solve for the fourth. Power analysis prevents underpowered studies (which miss real effects) and overpowered ones (which waste resources).

## Key Idea

For a one-sample two-sided z-test of $H_0: \mu = \mu_0$ vs $H_1: \mu \neq \mu_0$, the required sample size is:

$$n = \left(\frac{(z_{\alpha/2} + z_\beta)\sigma}{\delta}\right)^2$$

Here $z_{\alpha/2}$ is the critical value for the significance level and $z_\beta$ is the critical value for the desired power (e.g., $z_{0.20} = 0.84$ for 80% power, $z_{0.10} = 1.28$ for 90% power). Always round $n$ up to the next integer.

## Worked Examples

**Example 1: Find $n$ for 80% power, $\alpha=0.05$, $\delta=5$, $\sigma=15$**

With $z_{\alpha/2} = z_{0.025} = 1.96$ and $z_\beta = z_{0.20} = 0.84$:

$$n = \left(\frac{(1.96 + 0.84) \times 15}{5}\right)^2 = \left(\frac{2.80 \times 15}{5}\right)^2 = \left(\frac{42}{5}\right)^2 = (8.4)^2 = 70.56$$

Round up to $n = 71$. With 71 observations, you have an 80% chance of detecting a true difference of 5 units when $\sigma = 15$.

---

**Example 2: Find $n$ for 90% power, same parameters**

Now $z_\beta = z_{0.10} = 1.28$:

$$n = \left(\frac{(1.96 + 1.28) \times 15}{5}\right)^2 = \left(\frac{3.24 \times 15}{5}\right)^2 = \left(\frac{48.6}{5}\right)^2 = (9.72)^2 = 94.48$$

Round up to $n = 95$. Increasing power from 80% to 90% requires 95 instead of 71 observations — about 34% more. This illustrates why higher power demands a substantially larger investment in sample size. The numerator grows because $z_\beta$ increases, and since $n$ scales as the square, costs grow quickly.

---

**Example 3: How power depends on $n$, $\delta$, and $\alpha$**

The formula reveals three levers for increasing power:

1. **Increase $n$:** Larger $n$ reduces the standard error $\sigma/\sqrt{n}$, making the sampling distribution under $H_1$ further from the rejection boundary under $H_0$. Power increases monotonically with $n$.

2. **Increase $\delta$ (effect size):** A larger true difference between $\mu_1$ and $\mu_0$ moves the distribution further from $H_0$, making it easier to detect. If $\delta$ doubles, the required $n$ drops by a factor of 4 (since $n \propto 1/\delta^2$).

3. **Increase $\alpha$:** A larger $\alpha$ expands the rejection region, so the test rejects more often — including more often when $H_0$ is false. This increases power but also increases the Type I error rate. This trade-off is why you should not inflate $\alpha$ just to gain power.

## Common Mistakes

- **Using $z_\beta$ for the wrong tail.** For 80% power, $\beta = 0.20$, so $z_\beta = z_{0.20} = 0.84$ (the 80th percentile of the standard normal). Students sometimes use $z_{0.80} = 0.842$ correctly but accidentally substitute $z_{0.20} = -0.842$; since you add $z_\beta$ to $z_{\alpha/2}$, always use the positive value.

- **Forgetting to round up.** The formula gives a non-integer; always take the ceiling. Rounding down gives slightly less power than desired.

- **Planning for a one-sided test but using the two-sided formula.** For a one-sided test, replace $z_{\alpha/2}$ with $z_\alpha$ (e.g., $z_{0.05} = 1.645$ instead of $z_{0.025} = 1.96$). One-sided tests require fewer observations for the same power.

## Quick Check

Try these before using hints:

1. Find the required $n$ for 80% power ($z_\beta = 0.84$), $\alpha=0.05$ two-sided ($z_{\alpha/2}=1.96$), $\delta=10$, $\sigma=15$.
2. How does the required $n$ change if you double the effect size $\delta$ from 5 to 10?
3. If you run a study with $n = 50$ when you need $n = 95$ for 90% power, is your power above or below 90%?

*(Answers: 1. $n = \lceil((2.80 \times 15)/10)^2\rceil = \lceil 17.64 \rceil = 18$; 2. $n$ decreases by a factor of 4; 3. below 90% — insufficient $n$ means the study is underpowered)*
