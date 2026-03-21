# Generalized Likelihood Ratio Tests

## Overview

The **generalized likelihood ratio test (GLRT)** extends the Neyman-Pearson idea to composite hypotheses, where $H_0$ or $H_1$ specifies a range of parameter values rather than a single point. The test compares the maximum likelihood achievable under $H_0$ alone to the maximum likelihood achievable over all parameter values. If restricting to $H_0$ substantially reduces the likelihood, the data are inconsistent with $H_0$ and you reject. The GLRT is a general-purpose tool that recovers many classical tests as special cases.

## Key Idea

Define the likelihood ratio $\Lambda$ as the ratio of the maximized constrained likelihood to the maximized unconstrained likelihood. Wilks' theorem gives the asymptotic null distribution:

$$-2\log\Lambda \xrightarrow{d} \chi^2_r$$

where $r$ is the number of constraints imposed by $H_0$ (the difference in dimension between the full parameter space and the restricted space). You reject $H_0$ when $-2\log\Lambda > \chi^2_{r,\alpha}$.

## Worked Examples

**Example 1: GLRT for $H_0: \mu = \mu_0$ in Normal with unknown $\sigma^2$**

The full model has parameters $(\mu, \sigma^2)$, both free. Under $H_0$, $\mu$ is fixed at $\mu_0$ and only $\sigma^2$ is free. Computing both maximized likelihoods:

- Under $H_0$: $\hat{\sigma}^2_0 = \frac{1}{n}\sum(X_i - \mu_0)^2$
- Under full model: $\hat{\mu} = \bar{X}$, $\hat{\sigma}^2 = \frac{1}{n}\sum(X_i - \bar{X})^2$

After simplification, $-2\log\Lambda$ is a monotone function of $(\bar{X}-\mu_0)^2/s^2$, and the rejection region becomes $|\bar{X}-\mu_0|/(s/\sqrt{n}) > t_{\alpha/2, n-1}$. The GLRT reduces exactly to the t-test — confirming that the t-test is the natural GLRT for this problem. Here $r = 1$ because one parameter ($\mu$) is constrained.

---

**Example 2: GLRT for $H_0: p = p_0$ in Binomial**

Observe $X \sim \text{Binomial}(n, p)$. Under $H_0$, $L(\theta_0) = p_0^x(1-p_0)^{n-x}$. Under the full model, $\hat{p} = X/n$ and $L(\hat{p}) = \hat{p}^x(1-\hat{p})^{n-x}$.

$$-2\log\Lambda = -2\left[x\log\frac{p_0}{\hat{p}} + (n-x)\log\frac{1-p_0}{1-\hat{p}}\right]$$

By Wilks' theorem with $r=1$, you reject when $-2\log\Lambda > \chi^2_{1, \alpha} = 3.841$ at $\alpha = 0.05$. For large $n$, this gives nearly the same result as the Wald z-test for proportions.

---

**Example 3: Degrees of freedom — $r=1$ vs $r=2$**

The degrees of freedom $r$ equals the number of free parameters you fix under $H_0$. If $H_0: \mu = \mu_0$ in a bivariate normal model where both $\mu_1$ and $\mu_2$ are free, constraining both gives $r=2$ and $-2\log\Lambda \sim \chi^2_2$ under $H_0$. The critical value at $\alpha=0.05$ rises from $\chi^2_{1,0.05} = 3.841$ to $\chi^2_{2,0.05} = 5.991$, requiring stronger evidence to reject. More constraints always increase degrees of freedom and raise the bar for rejection.

## Common Mistakes

- **Using $\chi^2_r$ for small samples.** Wilks' theorem is asymptotic. For small $n$, the $\chi^2$ approximation may be poor, especially for discrete distributions. Use exact tests or simulation-based calibration when $n$ is small.

- **Miscounting degrees of freedom.** Count $r$ as the dimension of the full parameter space minus the dimension of the parameter space under $H_0$. For $H_0: \mu = \mu_0$ with one mean parameter constrained, $r=1$; for $H_0: \mu = \mu_0, \sigma = \sigma_0$, $r=2$.

- **Confusing $\Lambda$ with $-2\log\Lambda$.** Some sources define $\Lambda$ as the ratio (between 0 and 1); others define the test statistic as $-2\log\Lambda$ (which is non-negative and $\chi^2$-distributed). Make sure you know which form you are using.

## Quick Check

Try these before using hints:

1. For a Normal model with both $\mu$ and $\sigma^2$ unknown, what are the degrees of freedom for $H_0: \mu = 0, \sigma^2 = 1$?
2. In Example 2, if $n=100$, $x=60$, and $p_0=0.5$, will you reject at $\alpha=0.05$?
3. What classical test does the GLRT recover when testing $H_0: \mu = \mu_0$ in Normal with known $\sigma^2$?

*(Answers: 1. $r = 2$; 2. $\hat{p}=0.6$, $-2\log\Lambda \approx 4.02 > 3.841$, so yes; 3. the z-test)*
