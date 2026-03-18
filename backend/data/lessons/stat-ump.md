# Uniformly Most Powerful Tests

## Overview

A **Uniformly Most Powerful (UMP) test** is the most powerful test at level $\alpha$ for every possible value in $H_1$. UMP tests exist for one-sided hypotheses in one-parameter exponential families.

## Key Idea

A level-$\alpha$ test $\phi$ is UMP if $E_\theta[\phi(X)] \ge E_\theta[\psi(X)]$ for all $\theta \in H_1$ and all other level-$\alpha$ tests $\psi$.

For exponential families, the NP likelihood ratio test with a monotone likelihood ratio (MLR) provides the UMP.

## Worked Examples

**Example 1: UMP for $H_1: \mu > \mu_0$ in normal testing**

Reject when $\bar{X} > \bar{X}_{\alpha}$. This is UMP for all $\mu > \mu_0$ because the normal has MLR in $\bar{X}$.

---

**Example 2: No UMP for two-sided alternatives**

$H_1: \mu \ne \mu_0$ — no single rejection region maximizes power at both $\mu > \mu_0$ and $\mu < \mu_0$ simultaneously.

---

**Example 3: MLR property**

A family has monotone likelihood ratio in $T(X)$ if $L(\theta_1)/L(\theta_0)$ is monotone in $T$ for $\theta_1 > \theta_0$. This implies UMP tests exist for one-sided hypotheses.

## Common Mistakes

- **Assuming UMP tests always exist.** Two-sided and multi-parameter problems often have no UMP.
- **Confusing UMP with UMPU** (uniformly most powerful unbiased, for two-sided tests).

## Quick Check

1. Does a UMP test exist for $H_1: \mu \ne 0$?
2. What property guarantees a UMP test for a one-parameter exponential family?
3. Power function of UMP must satisfy what for all $\theta \in H_1$?

*(Answers: generally no; MLR property; it is $\ge$ power of any other level-$\alpha$ test)*
