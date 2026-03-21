# Bayesian Inference: Posterior Distributions

## Overview

In **Bayesian inference**, you treat the unknown parameter $\theta$ as a random variable with a **prior distribution** $\pi(\theta)$ that encodes your beliefs before seeing data. After observing data $\mathbf{x}$, you update via Bayes' theorem to get the **posterior distribution** $\pi(\theta \mid \mathbf{x})$, which encodes your updated beliefs. All inference — point estimates, interval estimates, predictions — flows from this posterior.

## Key Idea

Bayes' theorem gives the posterior up to a normalizing constant:

$$\pi(\theta \mid \mathbf{x}) \propto L(\theta \mid \mathbf{x})\,\pi(\theta)$$

Read this as: posterior is proportional to likelihood times prior. A **conjugate prior** is one where the posterior belongs to the same distributional family as the prior, which makes computation exact and tractable.

## Worked Examples

**Example 1: Beta-Binomial conjugacy**

Suppose $X \mid \theta \sim \text{Binomial}(n, \theta)$ and you place a prior $\theta \sim \text{Beta}(\alpha, \beta)$. The likelihood is $L(\theta \mid x) \propto \theta^x (1-\theta)^{n-x}$ and the prior is $\pi(\theta) \propto \theta^{\alpha-1}(1-\theta)^{\beta-1}$. Multiplying:

$$\pi(\theta \mid x) \propto \theta^{x+\alpha-1}(1-\theta)^{n-x+\beta-1}$$

This is the kernel of a $\text{Beta}(\alpha + x,\, \beta + n - x)$ distribution. The data "update" the Beta parameters by adding the observed successes to $\alpha$ and the observed failures to $\beta$. If you started with $\text{Beta}(1, 1)$ (uniform prior — no prior information) and observed $x = 7$ successes in $n = 10$ trials, the posterior is $\text{Beta}(8, 4)$ with mean $8/12 \approx 0.67$.

---

**Example 2: Normal-Normal conjugacy — posterior mean as a weighted average**

Suppose $X_1, \ldots, X_n \overset{iid}{\sim} N(\mu, \sigma^2)$ with known $\sigma^2$, and you place a prior $\mu \sim N(\mu_0, \tau^2)$. The posterior is also normal:

$$\mu \mid \mathbf{x} \sim N\!\left(\frac{\frac{\mu_0}{\tau^2} + \frac{n\bar{x}}{\sigma^2}}{\frac{1}{\tau^2} + \frac{n}{\sigma^2}},\ \left(\frac{1}{\tau^2} + \frac{n}{\sigma^2}\right)^{-1}\right)$$

The posterior mean is a precision-weighted average of the prior mean $\mu_0$ and the data mean $\bar{x}$. When the prior is vague ($\tau^2 \to \infty$), the data dominate and the posterior mean approaches $\bar{x}$. When $n$ is small, the prior pulls the posterior mean toward $\mu_0$ — this is called **shrinkage**.

---

**Example 3: Posterior mean vs. MLE — the role of the prior**

In the Beta-Binomial example, the MLE of $\theta$ is $\hat{\theta}_{\text{MLE}} = x/n$. The posterior mean is $(\alpha + x)/(\alpha + \beta + n)$. For small $n$, these differ substantially. With $n = 3$, $x = 3$ (all successes) and a $\text{Beta}(2, 2)$ prior: $\hat{\theta}_{\text{MLE}} = 1.0$ (implausibly certain), while the posterior mean is $5/9 \approx 0.56$ — pulled toward the prior belief that $\theta \approx 0.5$. The prior prevents the MLE from overreacting to a small extreme sample. As $n \to \infty$, the data overwhelm any fixed prior and the posterior mean converges to the MLE.

## Common Mistakes

- **Confusing a Bayesian credible interval with a frequentist confidence interval.** A 95% credible interval $[a, b]$ satisfies $P(a \le \theta \le b \mid \mathbf{x}) = 0.95$ — a direct probability statement about $\theta$ given the observed data. A frequentist 95% CI is a statement about the procedure: 95% of such intervals will contain the true $\theta$ in repeated sampling. These are different claims.

- **Treating the normalizing constant as negligible.** Writing $\pi(\theta \mid \mathbf{x}) \propto L(\theta \mid \mathbf{x})\pi(\theta)$ is fine for deriving the form of the posterior, but you need the correct normalizing constant when computing probabilities or expectations from the posterior.

## Quick Check

Try these before using hints:

1. Prior is $\text{Beta}(3, 3)$; you observe $x = 5$ successes in $n = 8$ trials. What is the posterior?
2. In the Normal-Normal model, what happens to the posterior mean as $n \to \infty$?
3. State one advantage of using a conjugate prior.

*(Answers: 1. $\text{Beta}(8, 6)$; 2. It converges to $\bar{x}$ — the data overwhelm the prior; 3. The posterior is available in closed form, making computation exact)*
