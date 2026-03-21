# Introduction to Causal Inference

## Overview

**Causal inference** asks a fundamentally different question from regression: not "what is the association between $X$ and $Y$?" but "what would happen to $Y$ if we intervened to set $X = x$?" The **potential outcomes framework** (also called the Rubin causal model) formalizes this distinction. For each unit $i$, define $Y_i(1)$ as the outcome that would occur under treatment and $Y_i(0)$ as the outcome under control. The individual causal effect is $Y_i(1) - Y_i(0)$, but you can never observe both — this is the **fundamental problem of causal inference**.

## Key Idea

The **average treatment effect (ATE)** averages individual effects across the population:

$$\text{ATE} = E[Y_i(1) - Y_i(0)]$$

Because you observe only one potential outcome per unit, estimating the ATE requires additional assumptions about how the unobserved potential outcomes relate to observed data. Randomization makes this feasible without strong assumptions.

## Worked Examples

**Example 1: Why randomization identifies the ATE**

In a randomized controlled trial (RCT), treatment $T_i$ is assigned independently of potential outcomes: $(Y_i(0), Y_i(1)) \perp T_i$. This independence means:

$$E[Y_i(1)] = E[Y_i(1) \mid T_i = 1] = E[Y_i \mid T_i = 1]$$

and similarly $E[Y_i(0)] = E[Y_i \mid T_i = 0]$. Therefore:

$$\text{ATE} = E[Y_i \mid T_i = 1] - E[Y_i \mid T_i = 0] = \bar{Y}_{\text{treated}} - \bar{Y}_{\text{control}}$$

The simple difference in observed group means is an unbiased estimator of the ATE. This works because randomization ensures the two groups are comparable in expectation — they have the same distribution of potential outcomes.

---

**Example 2: The ignorability assumption in observational studies**

Without randomization, treated and control units may differ systematically. You can still identify the ATE if you assume **strong ignorability**: $(Y(0), Y(1)) \perp T \mid \mathbf{X}$, meaning that within levels of observed covariates $\mathbf{X}$, treatment assignment is as good as random. Under this assumption:

$$E[Y(1) - Y(0)] = \int \bigl(E[Y \mid T=1, \mathbf{X}=x] - E[Y \mid T=0, \mathbf{X}=x]\bigr)\,dF_{\mathbf{X}}(x)$$

The catch: if any confounder is unmeasured, ignorability fails and your estimate is biased. This assumption cannot be verified from data — it requires subject-matter knowledge.

---

**Example 3: Naive estimate vs. true ATE when treatment is confounded**

Suppose a job training program is offered, and participants self-select. Workers with lower baseline earnings are more likely to enroll. True ATE $= \$2{,}000$ (the program genuinely helps). But because low-earners enroll, the treated group has lower average potential earnings under control than the untreated group. The naive comparison $\bar{Y}_{\text{treated}} - \bar{Y}_{\text{control}}$ might yield $\$500$ or even a negative number — severely understating the true effect. The bias is $E[Y(0) \mid T=1] - E[Y(0) \mid T=0]$, the difference in baseline potential outcomes between the two groups. Randomization sets this term to zero in expectation.

## Common Mistakes

- **Equating a regression coefficient with a causal effect.** The coefficient on $T$ in a regression of $Y$ on $T$ and covariates estimates the causal effect only if ignorability holds. Without that assumption, it estimates an association, not a causal quantity.

- **Ignoring the positivity assumption.** For causal inference to work, every unit must have a nonzero probability of receiving either treatment: $0 < P(T=1 \mid \mathbf{X}=x) < 1$ for all $x$ in the support of $\mathbf{X}$. If some subgroups can only receive one treatment, the ATE is not defined for those subgroups.

## Quick Check

Try these before using hints:

1. Define $Y_i(1)$ and $Y_i(0)$ in words.
2. What assumption does a randomized experiment satisfy that makes $\bar{Y}_{\text{treated}} - \bar{Y}_{\text{control}}$ an unbiased estimate of the ATE?
3. In an observational study, what is the name of the key assumption needed to identify causal effects from observational data?

*(Answers: 1. $Y_i(1)$ is the outcome unit $i$ would have under treatment; $Y_i(0)$ is the outcome under control — you observe exactly one of these; 2. $(Y(0), Y(1)) \perp T$ — treatment is independent of potential outcomes; 3. Strong ignorability: $(Y(0), Y(1)) \perp T \mid \mathbf{X}$)*
