# Confidence Intervals Using the t-Distribution

## Overview

When $\sigma$ is unknown and must be estimated from data, replacing $\sigma$ with the sample standard deviation $s$ introduces additional uncertainty. To account for this, the pivot $(\bar{X} - \mu)/(s/\sqrt{n})$ follows a **t-distribution** with $n-1$ degrees of freedom — not a standard normal. The t-distribution has heavier tails than the normal, which reflects the extra variability from estimating $\sigma$. As $n \to \infty$, the t-distribution converges to the standard normal.

## Key Idea

The confidence interval for $\mu$ when $\sigma$ is unknown is:

$$\bar{X} \pm t_{\alpha/2,\,n-1} \frac{s}{\sqrt{n}}$$

The degrees of freedom $n-1$ determine the shape of the t-distribution. You look up $t_{\alpha/2, n-1}$ in a t-table or software. Because $t_{\alpha/2, n-1} > z_{\alpha/2}$ for any finite $n$, the t-interval is always wider than the z-interval for the same data.

## Worked Examples

**Example 1: 95% CI with $n=10$, $\bar{x}=25$, $s=4$**

Degrees of freedom: $n - 1 = 9$. The critical value is $t_{0.025, 9} = 2.262$. The standard error is $s/\sqrt{n} = 4/\sqrt{10} \approx 1.265$.

$$25 \pm 2.262 \times 1.265 \approx 25 \pm 2.861 \implies (22.139,\ 27.861)$$

The critical value 2.262 is notably larger than $z_{0.025} = 1.96$, making the interval wider. This wider interval honestly reflects that you estimated $\sigma$ from only 10 observations — you have less information, so your uncertainty is greater.

---

**Example 2: 90% CI with $n=25$, $\bar{x}=100$, $s=15$**

Degrees of freedom: $n - 1 = 24$. The critical value is $t_{0.05, 24} = 1.711$. The standard error is $15/\sqrt{25} = 3$.

$$100 \pm 1.711 \times 3 = 100 \pm 5.133 \implies (94.867,\ 105.133)$$

With 25 observations, the t-distribution is closer to the normal ($t_{0.05, 24} = 1.711$ versus $z_{0.05} = 1.645$), so the extra width from using $t$ instead of $z$ is relatively small. The difference shrinks as $n$ increases.

---

**Example 3: Why the t-interval is always wider than the z-interval**

Suppose you have data with $n=10$, $\bar{x}=25$, $s=4$, and you mistakenly treated $s$ as if it were $\sigma$ and used $z_{0.025} = 1.96$ instead of $t_{0.025,9} = 2.262$. The "z-interval" would be $25 \pm 1.96 \times 1.265 = 25 \pm 2.479$. The correct t-interval is $25 \pm 2.861$ — about 15% wider. The reason is that $s$ is a random variable: in some samples it underestimates $\sigma$, leading the z-interval to undercover. The t-distribution corrects for this by widening the interval to maintain the nominal coverage probability.

## Common Mistakes

- **Using $z$ critical values when $\sigma$ is unknown.** If you substitute $s$ for $\sigma$ but keep the $z$ critical value, your interval has actual coverage below the stated level, especially for small $n$.

- **Using the wrong degrees of freedom.** The degrees of freedom for a one-sample t-interval are $n-1$, not $n$. Using $n$ gives a slightly different (incorrect) critical value.

- **Assuming the t-interval requires normality for large $n$.** For large samples, the Central Limit Theorem makes $\bar{X}$ approximately normal regardless of the population. The t-interval is still valid, and it nearly coincides with the z-interval.

## Quick Check

Try these before using hints:

1. Construct a 95% CI when $n=16$, $\bar{x}=42$, $s=8$. Use $t_{0.025,15} = 2.131$.
2. Why is the t-interval wider when $n=5$ than when $n=50$?
3. At what rough sample size do the $t$ and $z$ critical values become nearly indistinguishable at the 95% level?

*(Answers: 1. $(37.738,\ 46.262)$; 2. fewer degrees of freedom means heavier tails and a larger critical value; 3. around $n=30$, $t_{0.025,29} \approx 2.045$, close to 1.96)*
