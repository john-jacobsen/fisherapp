# Neyman-Pearson Lemma

## Overview

The **Neyman-Pearson Lemma** identifies the most powerful test for a simple null vs. simple alternative hypothesis. The optimal test uses the likelihood ratio as the test statistic.

## Key Idea

For $H_0: \theta = \theta_0$ vs. $H_1: \theta = \theta_1$, the most powerful level-$\alpha$ test rejects when:

$$\frac{L(\theta_1)}{L(\theta_0)} > k$$

where $k$ is chosen so that $P(\text{reject} | H_0) = \alpha$.

## Worked Examples

**Example 1: $X \sim N(\theta, 1)$. $H_0: \theta=0$ vs. $H_1: \theta=1$. MP test.**

LR $= e^{x - 1/2} > k$, i.e., $X > c$. Reject when $X > z_{\alpha}$. This is the UMP test.

---

**Example 2: $X \sim \text{Pois}(\lambda)$. $H_0: \lambda=1$ vs. $H_1: \lambda=3$.**

LR $= 3^x e^{-2}$. Reject when $X > c$. Larger $\lambda$ → large observed count is evidence against $H_0$.

---

**Example 3: NP is for simple vs. simple**

The lemma applies only when both $H_0$ and $H_1$ specify a single parameter value.

## Common Mistakes

- **Applying NP to composite hypotheses.** Use UMP tests or GLRT for composite hypotheses.
- **Forgetting that the critical value $k$ is determined by $\alpha$.**

## Quick Check

1. What does the NP Lemma guarantee?
2. What is the test statistic in the NP framework?
3. NP applies to simple vs. simple — what does "simple" mean?

*(Answers: most powerful level-$\alpha$ test; likelihood ratio; $H$ specifies a single parameter value)*
