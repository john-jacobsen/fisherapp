# Sufficient Statistics

## Overview

A statistic $T(\mathbf{X})$ is **sufficient** for $\theta$ if it captures all the information in the data about $\theta$. Once you know $T(\mathbf{X})$, the conditional distribution of the full data $\mathbf{X}$ given $T(\mathbf{X})$ does not depend on $\theta$. In other words, knowing the raw data gives no additional information about $\theta$ beyond what $T$ already provides.

## Key Idea

The practical tool for checking sufficiency is the **factorization theorem**: $T(\mathbf{X})$ is sufficient for $\theta$ if and only if the joint density (or PMF) factors as:

$$f(\mathbf{x};\theta) = g(T(\mathbf{x}),\theta)\,h(\mathbf{x})$$

Here $g$ depends on the data only through $T$ and depends on $\theta$, while $h$ depends on the data but not on $\theta$. Any factorization of this form certifies that $T$ is sufficient.

## Worked Examples

**Example 1: $T = \sum X_i$ is sufficient for $p$ in Bernoulli**

The joint PMF of $n$ i.i.d. Bernoulli$(p)$ observations is:

$$f(\mathbf{x}; p) = \prod_{i=1}^n p^{x_i}(1-p)^{1-x_i} = p^{\sum x_i}(1-p)^{n - \sum x_i}$$

Set $T(\mathbf{x}) = \sum x_i$. Then:

$$f(\mathbf{x};p) = \underbrace{p^T(1-p)^{n-T}}_{g(T, p)} \cdot \underbrace{1}_{h(\mathbf{x})}$$

The joint PMF depends on the data only through $T = \sum x_i$ and on $p$ through $g$. The function $h(\mathbf{x}) = 1$ does not involve $p$. By the factorization theorem, $T = \sum X_i$ (equivalently, $\bar{X}$) is sufficient for $p$.

---

**Example 2: $T = \sum X_i$ is sufficient for $\lambda$ in Poisson**

The joint PMF of $n$ i.i.d. Poisson$(\lambda)$ observations is:

$$f(\mathbf{x};\lambda) = \prod_{i=1}^n \frac{e^{-\lambda}\lambda^{x_i}}{x_i!} = e^{-n\lambda}\lambda^{\sum x_i} \cdot \frac{1}{\prod_{i=1}^n x_i!}$$

Again set $T = \sum x_i$:

$$f(\mathbf{x};\lambda) = \underbrace{e^{-n\lambda}\lambda^T}_{g(T,\lambda)} \cdot \underbrace{\left(\prod_{i=1}^n x_i!\right)^{-1}}_{h(\mathbf{x})}$$

The data enter $g$ only through $T$, and $h$ does not depend on $\lambda$. So $T = \sum X_i$ is sufficient for $\lambda$.

---

**Example 3: $T = (\sum X_i,\, \sum X_i^2)$ is sufficient for $(\mu, \sigma^2)$ in Normal**

The joint density of $n$ i.i.d. Normal$(\mu, \sigma^2)$ observations is:

$$f(\mathbf{x};\mu,\sigma^2) = \left(\frac{1}{\sqrt{2\pi\sigma^2}}\right)^n \exp\!\left(-\frac{1}{2\sigma^2}\sum_{i=1}^n(x_i-\mu)^2\right)$$

Expand $(x_i - \mu)^2 = x_i^2 - 2\mu x_i + \mu^2$ and collect terms:

$$= \underbrace{\left(\frac{1}{\sqrt{2\pi\sigma^2}}\right)^n \exp\!\left(-\frac{\sum x_i^2}{2\sigma^2} + \frac{\mu\sum x_i}{\sigma^2} - \frac{n\mu^2}{2\sigma^2}\right)}_{g(T_1, T_2,\,\mu,\sigma^2)} \cdot \underbrace{1}_{h(\mathbf{x})}$$

where $T_1 = \sum x_i$ and $T_2 = \sum x_i^2$. Since $g$ depends on the data only through $(T_1, T_2)$, the pair $(\sum X_i, \sum X_i^2)$ is jointly sufficient for $(\mu, \sigma^2)$.

## Common Mistakes

- **Confusing sufficiency with a small statistic.** A sufficient statistic need not be low-dimensional; $T = \mathbf{X}$ (the full data vector) is always trivially sufficient. The goal is to find a sufficient statistic that is also as simple as possible — a **minimal sufficient statistic**.
- **Applying the factorization theorem without identifying $g$ and $h$ explicitly.** The factorization must separate terms that involve $\theta$ (absorbed into $g$ via $T$) from terms that do not (absorbed into $h$). Be systematic: collect all $\theta$-dependent terms into $g$.
- **Assuming the MLE is always sufficient.** The MLE is often a function of the sufficient statistic, but that is a separate fact. Sufficiency is about the data information structure, not the estimation method.

## Quick Check

Try these before using hints:

1. For Exponential$(\lambda)$ with density $\lambda e^{-\lambda x}$, show that $T = \sum X_i$ is sufficient for $\lambda$.
2. Is $T = X_1$ (just the first observation) sufficient for $\lambda$ in Poisson? Why or why not?
3. What does it mean operationally that $T$ is sufficient — what can you discard once you know $T$?

*(Answers: factor the joint density as $\lambda^n e^{-\lambda T} \cdot 1$; no, $X_1$ alone loses information from the other observations; you can discard the raw data $\mathbf{X}$ and retain only $T$ without losing any information about $\theta$)*
