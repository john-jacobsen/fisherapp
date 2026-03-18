# Generalized Likelihood Ratio Test

## Overview

The **Generalized Likelihood Ratio Test (GLRT)** extends the NP framework to composite hypotheses and multi-parameter settings. It compares the maximum likelihood under the full model to the maximum under the restricted null model.

## Key Idea

$$\Lambda = \frac{\sup_{\theta \in \Theta_0} L(\theta)}{\sup_{\theta \in \Theta} L(\theta)}$$

Reject $H_0$ when $\Lambda$ is small (or $-2\ln\Lambda$ is large). By Wilks' theorem, $-2\ln\Lambda \xrightarrow{d} \chi^2_k$ under $H_0$, where $k$ is the number of constraints.

## Worked Examples

**Example 1: Test $H_0: \mu = 0$ in $N(\mu,\sigma^2)$**

$-2\ln\Lambda = n\ln(1 + t^2/(n-1)) \approx t^2$ for large $n$, which is $\chi^2_1$. Equivalent to $t$-test.

---

**Example 2: Degrees of freedom in Wilks' theorem**

$k = \dim(\Theta) - \dim(\Theta_0)$. Testing 1 constraint: $\chi^2_1$. Testing 2 constraints simultaneously: $\chi^2_2$.

---

**Example 3: Practical use**

GLRT provides a general testing procedure when no UMP test exists.

## Common Mistakes

- **Wrong degrees of freedom.** Count the number of parameters restricted by $H_0$.
- **Wilks' theorem is asymptotic.** For small $n$, the $\chi^2$ approximation may be poor.

## Quick Check

1. What is the GLRT statistic $\Lambda$?
2. $-2\ln\Lambda$ has what asymptotic distribution?
3. Degrees of freedom for testing $H_0: \mu_1 = \mu_2 = 0$ in a 3-parameter model?

*(Answers: ratio of constrained to unconstrained max likelihood; $\chi^2_k$; 2)*
