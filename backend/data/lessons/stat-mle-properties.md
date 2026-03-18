# MLE: Properties and Invariance

## Overview

MLEs have strong theoretical properties: they are **consistent**, **asymptotically normal**, and **asymptotically efficient**. The **invariance principle** says the MLE of $g(\theta)$ is $g(\hat{\theta}_{MLE})$.

## Key Idea

- **Invariance:** $\widehat{g(\theta)} = g(\hat{\theta})$
- **Asymptotic normality:** $\sqrt{n}(\hat{\theta} - \theta) \xrightarrow{d} N(0, I(\theta)^{-1})$
- **Asymptotic efficiency:** Achieves the Cramér-Rao lower bound asymptotically

## Worked Examples

**Example 1: MLE of $\sigma$ given MLE of $\sigma^2$**

$\hat{\sigma}^2 = \frac{1}{n}\sum(X_i-\bar{X})^2$. By invariance, $\hat{\sigma} = \sqrt{\hat{\sigma}^2}$.

---

**Example 2: MLE of $e^\mu$ for Normal$(\mu,1)$**

$\hat{\mu} = \bar{X}$. By invariance, $\widehat{e^\mu} = e^{\bar{X}}$.

---

**Example 3: Asymptotic variance**

The asymptotic variance of the MLE $\hat{\theta}$ is $1/(nI(\theta))$, where $I(\theta)$ is the Fisher information.

## Common Mistakes

- **Thinking invariance applies to bias.** Invariance is about the estimator's functional form, not its bias properties.
- **Assuming MLEs are always unbiased.** The MLE of $\sigma^2$ is biased.

## Quick Check

1. MLE of $\lambda^2$ if $\hat{\lambda} = \bar{X}$?
2. Are MLEs always unbiased?
3. What is asymptotic efficiency?

*(Answers: $\bar{X}^2$; no; achieving the CRLB as $n \to \infty$)*
