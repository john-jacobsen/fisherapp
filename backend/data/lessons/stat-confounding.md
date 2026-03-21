# Confounding in Observational Studies

## Overview

A **confounder** is a variable that is associated with both the exposure of interest and the outcome, creating a spurious or distorted association between them. In observational data — where you cannot randomly assign exposures — confounding is the central threat to drawing valid conclusions. More data does not fix confounding; only careful study design or statistical adjustment can address it.

## Key Idea

A variable $C$ confounds the relationship between exposure $X$ and outcome $Y$ when three conditions hold simultaneously: (1) $C$ is associated with $X$, (2) $C$ is associated with $Y$, and (3) $C$ is not on the causal pathway from $X$ to $Y$. When a confounder is present, the observed association between $X$ and $Y$ does not accurately represent the causal effect of $X$ on $Y$. Crucially, an apparent trend in the overall data can reverse direction once you control for the confounder — this reversal is called **Simpson's paradox**.

## Worked Examples

**Example 1: Ice cream sales and drowning rates**

You notice that on days when ice cream sales are high, drowning rates are also high. A naive analysis might conclude that ice cream causes drowning. The confounder is **temperature**: hot weather drives both increased ice cream consumption and more swimming, which increases drowning risk. Once you control for temperature (e.g., by stratifying data by season), the association between ice cream sales and drowning disappears. Neither variable causes the other — both are effects of a common cause.

---

**Example 2: Simpson's paradox — a drug that appears harmful overall**

Suppose a new drug is tested in a hospital. Overall, treated patients have a higher death rate than untreated patients. But when you break results down by disease severity, the drug reduces death rates in both mild and severe cases. How? Sicker patients were far more likely to receive the drug, and sicker patients are far more likely to die regardless. Disease severity confounds the treatment-outcome relationship. Aggregating without adjusting mixes together two very different groups, reversing the apparent direction of the drug's effect. The correct analysis conditions on severity.

---

**Example 3: Three approaches to control confounding**

Once you identify potential confounders, you have three main tools:

**Stratification**: analyze the $X$-$Y$ relationship separately within levels of $C$ (e.g., within each severity group), then combine the stratum-specific estimates (e.g., via a Mantel-Haenszel weighted average). This works well when $C$ has a small number of categories.

**Regression adjustment**: include $C$ as a covariate in a regression model. The coefficient on $X$ then estimates the association between $X$ and $Y$ holding $C$ fixed. This extends naturally to multiple confounders but requires correctly specifying the model.

**Randomization**: the gold standard. By randomly assigning exposure, you ensure that $C$ is, on average, balanced across groups — so it cannot confound the comparison. Randomization handles both measured and unmeasured confounders, which is why randomized experiments are the strongest design for causal questions.

## Common Mistakes

- **Adjusting for a mediator.** A mediator is a variable on the causal pathway from $X$ to $Y$ — for example, if $X$ causes $C$ which causes $Y$, then $C$ is a mediator. Controlling for a mediator blocks the very pathway through which $X$ affects $Y$, biasing your estimate of the $X \to Y$ effect downward.

- **Assuming all confounders have been measured.** Regression and stratification can only control for confounders you have measured. Unmeasured confounders remain a threat in any observational study. Sensitivity analyses can assess how large an unmeasured confounder would have to be to explain away the observed association.

## Quick Check

Try these before using hints:

1. List the three conditions that make $C$ a confounder of the $X$-$Y$ relationship.
2. What is Simpson's paradox, in one sentence?
3. Why does randomization eliminate confounding from unmeasured variables, while regression adjustment does not?

*(Answers: 1. $C$ is associated with $X$; $C$ is associated with $Y$; $C$ is not on the causal pathway from $X$ to $Y$; 2. An overall trend reverses direction within each subgroup because a third variable is unevenly distributed across groups; 3. Randomization makes treatment assignment independent of all baseline variables — measured or not — on average; regression can only adjust for variables that were recorded)*
