# Type I/II Errors and Power

## Overview

**Type I error** (false positive): rejecting $H_0$ when it's true. **Type II error** (false negative): failing to reject $H_0$ when $H_1$ is true. **Power** is the probability of correctly rejecting a false $H_0$.

## Key Idea

- $\alpha = P(\text{Type I}) = P(\text{reject } H_0 | H_0 \text{ true})$ (significance level)
- $\beta = P(\text{Type II}) = P(\text{fail to reject } H_0 | H_1 \text{ true})$
- $\text{Power} = 1 - \beta = P(\text{reject } H_0 | H_1 \text{ true})$

Reducing $\alpha$ increases $\beta$; increasing $n$ reduces both simultaneously.

## Worked Examples

**Example 1: $\alpha = 0.05$ means what?**

A 5% chance of rejecting $H_0$ when it is actually true.

---

**Example 2: Power calculation for $Z$-test, $\mu_1 = 1$, $\sigma = 2$, $n = 25$, $\alpha = 0.05$**

$\text{SE} = 0.4$. Reject when $Z > 1.645$. Under $H_1$: $Z' = (Z - 1/0.4) = Z - 2.5$. Power $= P(Z > 1.645 - 2.5) = P(Z > -0.855) \approx 0.804$.

---

**Example 3: Effect of $n$ on power**

Quadrupling $n$ cuts SE by half, moving the power curve right and increasing power.

## Common Mistakes

- **Confusing $\alpha$ and $\beta$.** $\alpha$ is set by the researcher; $\beta$ depends on the true effect.
- **Thinking high power is always desirable at all costs.** It comes at the expense of sample size.

## Quick Check

1. What is power in terms of $\beta$?
2. Increasing $n$ affects $\alpha$?
3. Trade-off: decreasing $\alpha$ does what to $\beta$?

*(Answers: $1-\beta$; no (fixed by researcher); increases $\beta$ (unless $n$ increases too))*
