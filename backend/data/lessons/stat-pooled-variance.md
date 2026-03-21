# Pooled Variance in Two-Sample Tests

## Overview

When two independent populations share the same variance ($\sigma_1^2 = \sigma_2^2 = \sigma^2$), you can **pool** the two sample variances into a single, more accurate estimate of the common $\sigma^2$. Pooling uses all $n_1 + n_2 - 2$ degrees of freedom rather than estimating $\sigma^2$ separately from each group, which gives a more precise estimate and a t-test with higher power.

## Key Idea

The **pooled sample variance** is a weighted average of $s_1^2$ and $s_2^2$, with weights proportional to the degrees of freedom each group contributes:

$$s_p^2 = \frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}$$

The weights $(n_i - 1)$ reflect how much information each sample provides — larger samples get more weight. The pooled t-statistic is then:

$$T = \frac{\bar{X}_1 - \bar{X}_2}{s_p\sqrt{1/n_1 + 1/n_2}} \sim t_{n_1+n_2-2}$$

The term $s_p\sqrt{1/n_1 + 1/n_2}$ is the standard error of the difference, using the shared variance estimate.

## Worked Examples

**Example 1: Compute $s_p^2$**

Group 1: $n_1 = 10$, $s_1^2 = 16$. Group 2: $n_2 = 12$, $s_2^2 = 20$.

The numerator is the total sum of squares from both groups: $(n_1 - 1)s_1^2 = 9 \times 16 = 144$ and $(n_2 - 1)s_2^2 = 11 \times 20 = 220$. Adding gives $144 + 220 = 364$.

$$s_p^2 = \frac{364}{10 + 12 - 2} = \frac{364}{20} = 18.2$$

Notice that $s_p^2 = 18.2$ lies between $s_1^2 = 16$ and $s_2^2 = 20$, and closer to $s_2^2$ because Group 2 has more observations and thus more influence on the pooled estimate.

---

**Example 2: Full pooled t-test**

Two fertilizer treatments are applied to separate plots. Treatment 1: $n_1 = 15$, $\bar{x}_1 = 30$, $s_1 = 5$. Treatment 2: $n_2 = 15$, $\bar{x}_2 = 27$, $s_2 = 5$. Test $H_0: \mu_1 = \mu_2$ at $\alpha = 0.05$.

Because $s_1 = s_2 = 5$, equal variances are plausible, so pooling is appropriate. Since $n_1 = n_2$ and $s_1 = s_2$, the pooled variance is simply $s_p^2 = 25$, so $s_p = 5$.

$$SE = s_p\sqrt{\frac{1}{15} + \frac{1}{15}} = 5\sqrt{\frac{2}{15}} = 5 \times 0.3651 \approx 1.826$$

$$T = \frac{30 - 27}{1.826} \approx 1.64$$

With $df = 15 + 15 - 2 = 28$, the two-sided critical value is $t_{0.025, 28} \approx 2.048$. Since $1.64 < 2.048$, you fail to reject $H_0$.

---

**Example 3: When pooling is appropriate vs risky**

Pooling is appropriate when you have strong reason to believe $\sigma_1^2 \approx \sigma_2^2$ — for example, when both groups are drawn from the same population under slightly different conditions, or when theory supports equal spread. In that case, pooling reduces the standard error estimate's variability and gives a more powerful test.

Pooling is risky when the variances are actually unequal. Suppose $\sigma_1^2 = 4$ and $\sigma_2^2 = 100$. The pooled estimate would blur these together into something that doesn't represent either group. The resulting t-test would use the wrong standard error and the wrong degrees of freedom formula, producing inflated or deflated p-values. Welch's test is safer as a default — when variances are truly equal, it loses little power compared to the pooled test.

## Common Mistakes

- **Pooling when variances look very different.** If $s_1^2$ and $s_2^2$ differ by a factor of 3 or more, pooling is questionable. Use Welch's test unless you have strong prior reason to assume equal population variances.
- **Using the wrong degrees of freedom.** The pooled t-test uses $df = n_1 + n_2 - 2$, not the Welch-Satterthwaite approximation. Using the wrong $df$ gives the wrong critical value.
- **Forgetting to take the square root of $s_p^2$ before computing SE.** The formula uses $s_p$ (the pooled standard deviation), not $s_p^2$. Leaving it squared gives a wildly incorrect standard error.

## Quick Check

Try these before using hints:

1. $n_1 = 5$, $s_1^2 = 10$, $n_2 = 5$, $s_2^2 = 14$. Compute $s_p^2$.
2. Using $s_p^2 = 12$, $n_1 = n_2 = 6$, and $\bar{x}_1 - \bar{x}_2 = 3$, compute $T$.
3. What is the $df$ for the pooled t-test in question 2?

*(Answers: 1. $s_p^2 = 12$; 2. $SE = \sqrt{12 \cdot (1/6 + 1/6)} = \sqrt{4} = 2$, so $T = 3/2 = 1.5$; 3. $df = 6 + 6 - 2 = 10$)*
