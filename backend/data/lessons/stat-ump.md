# Uniformly Most Powerful Tests

## Overview

A **uniformly most powerful (UMP)** test is a level-$\alpha$ test that achieves the highest possible power simultaneously for every value of $\theta$ under $H_1$. UMP tests are the gold standard for one-sided hypothesis testing in one-parameter exponential families. The key insight is that applying the Neyman-Pearson lemma separately to each simple alternative $H_1: \theta = \theta_1$ (for all $\theta_1 > \theta_0$) yields the same rejection region every time — making the test uniformly most powerful.

## Key Idea

For $H_0: \theta \leq \theta_0$ vs $H_1: \theta > \theta_0$ in a one-parameter exponential family, the UMP test rejects when the natural sufficient statistic $T(\mathbf{X})$ exceeds a critical value $c$:

$$\text{Reject } H_0 \text{ when } T(\mathbf{X}) > c, \quad \text{where } P(T > c \mid \theta = \theta_0) = \alpha$$

The threshold $c$ is set using the boundary value $\theta_0$, and power increases as $\theta$ moves further above $\theta_0$.

## Worked Examples

**Example 1: One-sided z-test is UMP for $\mu > \mu_0$ in Normal with known $\sigma^2$**

Fix any $\mu_1 > \mu_0$. By the Neyman-Pearson lemma, the most powerful test for $H_0: \mu = \mu_0$ vs $H_1: \mu = \mu_1$ rejects when $\bar{X} > k$ (as derived in the NP lesson). Crucially, the direction of the rejection region (right tail) does not depend on the specific value of $\mu_1$ — any $\mu_1 > \mu_0$ leads to the same form. Therefore, the test "reject when $Z = (\bar{X}-\mu_0)/(\sigma/\sqrt{n}) > z_\alpha$" is most powerful against every single point $\mu_1 > \mu_0$, making it UMP for the composite alternative $H_1: \mu > \mu_0$.

---

**Example 2: No UMP test exists for two-sided alternatives**

For $H_0: \mu = \mu_0$ vs $H_1: \mu \neq \mu_0$, the Neyman-Pearson lemma gives different rejection regions depending on the sign of the alternative. For $\mu_1 > \mu_0$ the most powerful test rejects in the right tail; for $\mu_1 < \mu_0$ it rejects in the left tail. No single test can simultaneously maximize power in both tails — any test that is most powerful against $\mu_1 > \mu_0$ has reduced power against $\mu_1 < \mu_0$. This is why two-sided UMP tests do not exist in general, and one must settle for unbiased or other compromise tests.

---

**Example 3: UMP test for Poisson with $H_0: \lambda \leq 2$ vs $H_1: \lambda > 2$**

The Poisson family is an exponential family with natural sufficient statistic $T = \sum_{i=1}^n X_i$. By the UMP theory for exponential families, the most powerful test against any fixed $\lambda_1 > 2$ rejects when $T$ is large. The same rejection region "reject when $\sum X_i > c$" works for every $\lambda_1 > 2$, so it is the UMP test. The threshold $c$ satisfies $P(\sum X_i > c \mid \lambda = 2) = \alpha$, where $\sum X_i \sim \text{Poisson}(2n)$ under $H_0$.

## Common Mistakes

- **Claiming UMP tests always exist.** UMP tests exist for one-sided alternatives in exponential families. They generally do not exist for two-sided alternatives or families lacking monotone likelihood ratios.

- **Setting the critical value using an interior point of $H_0$.** For $H_0: \theta \leq \theta_0$, you always set $c$ using the boundary value $\theta_0$. Using any other value under $H_0$ gives the wrong size.

- **Confusing UMP with uniformly most accurate (UMA) for confidence intervals.** UMP tests and UMA confidence intervals are dual concepts, but they apply in different contexts. A UMP test for one-sided $H_0$ corresponds to a one-sided UMA confidence bound.

## Quick Check

Try these before using hints:

1. For $X_1,\ldots,X_n \overset{iid}{\sim} \text{Exp}(\lambda)$, is there a UMP test for $H_0: \lambda \leq \lambda_0$ vs $H_1: \lambda > \lambda_0$?
2. Why does no UMP test exist for $H_0: \mu = 0$ vs $H_1: \mu \neq 0$ in a Normal model?
3. In Example 3, if $n=5$ and $\alpha \approx 0.05$, would you reject when $\sum X_i \geq 13$ (using $\sum X_i \sim \text{Poisson}(10)$ under $H_0$)?

*(Answers: 1. Yes — exponential family, one-sided alternative; 2. different alternatives require different tail directions, no single rejection region is best for all; 3. Yes — $P(\text{Poisson}(10) \geq 13) \approx 0.0838$; for $\geq 14$ it is $\approx 0.048 \leq 0.05$, so reject when $\sum X_i \geq 14$)*
