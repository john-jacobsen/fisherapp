# Confounding

## Overview

**Confounding** occurs when a third variable (the confounder) is associated with both the exposure and the outcome, creating a spurious or distorted association. Ignoring confounders leads to biased estimates of causal effects.

## Key Idea

A variable $C$ is a **confounder** if:
1. $C$ is associated with the exposure $X$
2. $C$ is associated with the outcome $Y$
3. $C$ is not on the causal pathway from $X$ to $Y$

Confounders cannot be removed by larger samples — only by study design (randomization) or statistical adjustment (regression, stratification).

## Worked Examples

**Example 1: Ice cream and drowning**

Both are associated, but both are caused by warm weather (the confounder). No causal relationship between ice cream and drowning.

---

**Example 2: Coffee and lung cancer**

Early studies found a link, but smokers drink more coffee. Smoking is the confounder.

---

**Example 3: Controlling for confounders**

Include the confounder in a regression model. $\hat{\beta}_X$ after adjustment estimates the effect of $X$ holding $C$ fixed.

## Common Mistakes

- **Adjusting for mediators.** A variable on the causal pathway should not be adjusted for.
- **Thinking observational studies can always be fixed with regression.** Unmeasured confounders remain a problem.

## Quick Check

1. Three criteria for confounding?
2. Best way to eliminate confounding at the design stage?
3. Can confounding be fixed by collecting more data?

*(Answers: associated with X, associated with Y, not a mediator; randomization; no — only by adjusting or better design)*
