# MLE: Multiparameter

## Overview

When a distribution has multiple parameters (e.g., $\mu$ and $\sigma^2$ in the normal), MLE requires simultaneous maximization over all parameters using a system of score equations.

## Key Idea

Take partial derivatives of the log-likelihood with respect to each parameter and set all equal to zero:

$$\frac{\partial \ell}{\partial \theta_j} = 0 \quad \text{for all } j$$

## Worked Examples

**Example 1: MLE for $N(\mu, \sigma^2)$ (both unknown)**

Score equations: $\partial\ell/\partial\mu = 0 \Rightarrow \hat{\mu} = \bar{X}$; $\partial\ell/\partial\sigma^2 = 0 \Rightarrow \hat{\sigma}^2 = \frac{1}{n}\sum(X_i-\bar{X})^2$.

Note: $\hat{\sigma}^2_{MLE}$ uses $n$, making it biased.

---

**Example 2: MLE for Gamma$(r, \lambda)$**

Coupled equations — no closed form for $r$; numerical optimization is needed.

---

**Example 3: Fisher information matrix**

The inverse of the Fisher information matrix gives the asymptotic covariance of the MLE vector.

## Common Mistakes

- **Solving score equations one at a time ignoring interactions.** They must be solved simultaneously.
- **Ignoring boundary solutions.** Always check if the maximum is interior or on the boundary of the parameter space.

## Quick Check

1. MLE of $\mu$ for Normal$(\mu,\sigma^2)$?
2. MLE of $\sigma^2$ for Normal$(\mu,\sigma^2)$ — is it biased?
3. How many score equations for a 3-parameter model?

*(Answers: $\bar{X}$; yes (divides by $n$, not $n-1$); 3)*
