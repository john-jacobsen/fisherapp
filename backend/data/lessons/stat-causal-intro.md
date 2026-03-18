# Causal Inference: Introduction

## Overview

**Causal inference** aims to estimate the effect of an intervention, not just an association. The key challenge is that we can never observe both the treated and untreated outcome for the same unit — the **fundamental problem of causal inference**.

## Key Idea

**Potential outcomes framework:** For each unit $i$, let $Y_i(1)$ be the outcome if treated and $Y_i(0)$ if untreated. The causal effect is $Y_i(1) - Y_i(0)$.

The **Average Treatment Effect (ATE)**: $E[Y(1) - Y(0)]$.

Randomization ensures $Y(1), Y(0) \perp T$ (treatment), so the ATE can be estimated by comparing group means.

## Worked Examples

**Example 1: Randomized experiment**

Randomly assign half to treatment. $E[\bar{Y}_1 - \bar{Y}_0] = \text{ATE}$ because randomization balances confounders.

---

**Example 2: Observational study**

Without randomization, treated and control groups may differ on covariates. Simple mean difference is biased.

---

**Example 3: Propensity score**

Propensity score $e(x) = P(T=1|X=x)$. Conditioning on propensity score removes confounding due to $X$.

## Common Mistakes

- **Equating statistical association with causation.** Regression coefficients are not causal without additional assumptions.
- **Ignoring positivity assumption.** Every unit must have a nonzero probability of receiving either treatment.

## Quick Check

1. What is the fundamental problem of causal inference?
2. Why does randomization enable causal inference?
3. What is the ATE?

*(Answers: can't observe both $Y(1)$ and $Y(0)$ for same unit; it balances confounders so treatment is independent of potential outcomes; $E[Y(1)-Y(0)]$)*
