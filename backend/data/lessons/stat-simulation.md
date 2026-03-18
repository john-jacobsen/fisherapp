# Monte Carlo Simulation

## Overview

**Monte Carlo simulation** uses random sampling to estimate quantities that are difficult to compute analytically — integrals, probabilities, expected values, and sampling distributions of complex estimators.

## Key Idea

To estimate $E[g(X)]$: generate $X_1, \ldots, X_B$ from $F$, then:

$$\hat{E} = \frac{1}{B}\sum_{b=1}^B g(X_b) \xrightarrow{P} E[g(X)]$$

by the LLN. The error is $O(1/\sqrt{B})$ regardless of dimension.

## Worked Examples

**Example 1: Estimate $\pi$ via Monte Carlo**

Sample $(X,Y) \sim U(-1,1)^2$. $\pi/4 \approx $ fraction with $X^2+Y^2 < 1$.

---

**Example 2: Estimate $\int_0^1 e^{-x^2}\,dx$**

Sample $X \sim U(0,1)$, estimate $E[e^{-X^2}] \approx \frac{1}{B}\sum e^{-X_b^2}$.

---

**Example 3: Simulate power of a test**

Generate data under $H_1$ many times. Fraction of times $H_0$ is rejected $\approx$ power.

## Common Mistakes

- **Insufficient replicates.** Error $\propto 1/\sqrt{B}$; to halve error, quadruple $B$.
- **Using a poor random number generator.** Always use a well-tested PRNG.

## Quick Check

1. Monte Carlo error scales as?
2. How would you simulate a 95% CI coverage probability?
3. What fundamental theorem justifies Monte Carlo?

*(Answers: $O(1/\sqrt{B})$; generate many datasets, compute CI each time, count fraction containing $\theta$; Law of Large Numbers)*
