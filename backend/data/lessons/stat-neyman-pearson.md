# The Neyman-Pearson Lemma

## Overview

When testing a simple null $H_0: \theta = \theta_0$ against a simple alternative $H_1: \theta = \theta_1$ (both are point hypotheses), the **Neyman-Pearson lemma** guarantees that the most powerful test at level $\alpha$ is the **likelihood ratio test**: reject $H_0$ when the ratio of the data's probability under $H_1$ to its probability under $H_0$ exceeds a threshold $c$. This is the foundational result of classical hypothesis testing — any other level-$\alpha$ test for these hypotheses has equal or lower power.

## Key Idea

The likelihood ratio $\Lambda$ compares how much more plausible the data are under $H_1$ than under $H_0$:

$$\Lambda = \frac{L(\theta_1;\mathbf{x})}{L(\theta_0;\mathbf{x})} > c$$

The threshold $c$ is chosen so that $P(\Lambda > c \mid H_0) = \alpha$. In practice, the inequality $\Lambda > c$ often simplifies to a familiar one-sided test on a sufficient statistic.

## Worked Examples

**Example 1: Most powerful test for $\mu_0 = 0$ vs $\mu_1 = 1$, Normal with known $\sigma^2$**

For $X_1, \ldots, X_n \overset{iid}{\sim} N(\mu, \sigma^2)$ with $\sigma^2$ known, the likelihoods are products of normal densities. Taking the ratio and simplifying:

$$\Lambda = \frac{L(\mu_1)}{L(\mu_0)} = \exp\!\left(\frac{n(\mu_1 - \mu_0)}{\sigma^2}\bar{X} - \frac{n(\mu_1^2 - \mu_0^2)}{2\sigma^2}\right)$$

Because $\mu_1 > \mu_0$ and the exponential is monotone, $\Lambda > c$ if and only if $\bar{X} > k$ for some threshold $k$. The NP lemma says this one-sided test on $\bar{X}$ is the most powerful test — no other level-$\alpha$ test can achieve higher power at $\mu_1 = 1$.

---

**Example 2: Bernoulli LR test — $p_0 = 0.3$ vs $p_1 = 0.6$**

For $X_1, \ldots, X_n \overset{iid}{\sim} \text{Bernoulli}(p)$, the likelihood ratio is:

$$\Lambda = \frac{(0.6)^{\sum x_i}(0.4)^{n - \sum x_i}}{(0.3)^{\sum x_i}(0.7)^{n - \sum x_i}} = \left(\frac{0.6 \times 0.7}{0.3 \times 0.4}\right)^{\sum x_i} \times \left(\frac{0.4}{0.7}\right)^n$$

Since $(0.6 \times 0.7)/(0.3 \times 0.4) = 3.5 > 1$, the ratio increases with $\sum x_i$. Therefore $\Lambda > c$ if and only if $\sum X_i > k$ for some integer $k$. The NP lemma confirms that rejecting when the total number of successes is large is the most powerful strategy.

---

**Example 3: Why the NP lemma requires simple hypotheses**

The NP lemma applies only when both $H_0$ and $H_1$ specify a single parameter value. If $H_1: \mu > 0$ (composite), then $L(\theta_1)$ is not a single number — it depends on which $\mu > 0$ is the true value. The likelihood ratio $\Lambda$ then varies with the unknown $\mu_1$, and a single threshold $c$ cannot simultaneously maximize power for all $\mu_1 > 0$. This limitation motivates the theory of uniformly most powerful tests for composite alternatives.

## Common Mistakes

- **Forgetting to simplify $\Lambda > c$ into a test on a sufficient statistic.** The raw likelihood ratio is rarely convenient. Always simplify algebraically — the NP lemma guarantees an equivalent form in terms of $\bar{X}$ or $\sum X_i$.

- **Applying the NP lemma to composite hypotheses.** The lemma applies only to simple vs simple testing. For composite hypotheses, you need the theory of UMP tests or generalized likelihood ratio tests.

- **Confusing "most powerful" with "most accurate."** The NP lemma maximizes power at a specific alternative $\theta_1$. It says nothing about performance at other parameter values.

## Quick Check

Try these before using hints:

1. In the Normal example (Example 1), what direction does the rejection region go when $\mu_1 < \mu_0$?
2. In the Bernoulli example, what is the most powerful rejection region if $p_0 = 0.6$ and $p_1 = 0.3$?
3. Name one reason why the NP lemma cannot directly be applied when $H_1: \mu \neq \mu_0$.

*(Answers: 1. Reject when $\bar{X} < k$ (left tail); 2. Reject when $\sum X_i < k$ (low count favors smaller $p$); 3. $H_1: \mu \neq \mu_0$ is composite — no single $\mu_1$ to put in the numerator of $\Lambda$)*
