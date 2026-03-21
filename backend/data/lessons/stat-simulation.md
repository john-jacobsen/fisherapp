# Monte Carlo Simulation

## Overview

**Monte Carlo simulation** estimates quantities that are difficult or impossible to compute analytically by averaging over many random draws. The core idea is simple: if you can simulate from a distribution, you can approximate any expectation, probability, or quantile to arbitrary precision just by drawing enough samples. The method applies to integrals, sampling distributions of complex statistics, power calculations, and much more.

## Key Idea

To estimate $E[g(X)]$, draw $X_1, \ldots, X_B$ independently from the distribution of $X$ and average the transformed values. By the Law of Large Numbers:

$$\hat{\mu} = \frac{1}{B}\sum_{b=1}^B g(X_b) \xrightarrow{a.s.} E[g(X)]$$

The error of the Monte Carlo estimate is $O(1/\sqrt{B})$ regardless of the dimension of $X$ — this dimension-independence is the crucial advantage over numerical integration methods, which become exponentially expensive in high dimensions.

## Worked Examples

**Example 1: Estimate $P(Z > 1.5)$ for $Z \sim N(0,1)$**

The exact value is $P(Z > 1.5) \approx 0.0668$. To estimate it by simulation: draw $B = 10{,}000$ standard normal values, compute the fraction that exceed 1.5:

$$\hat{p} = \frac{1}{B}\sum_{b=1}^B \mathbf{1}(Z_b > 1.5)$$

Here $g(z) = \mathbf{1}(z > 1.5)$, so you are computing $E[g(Z)] = P(Z > 1.5)$. With $B = 10{,}000$, the standard error of $\hat{p}$ is approximately $\sqrt{p(1-p)/B} \approx \sqrt{0.067 \cdot 0.933 / 10000} \approx 0.0025$ — the estimate is accurate to about two decimal places.

---

**Example 2: Estimate $E[X^2]$ for $X \sim U(0,1)$**

The exact value is $E[X^2] = \int_0^1 x^2\,dx = 1/3 \approx 0.333$. To estimate it: draw $B$ uniform values on $(0,1)$ and average their squares:

$$\hat{\mu} = \frac{1}{B}\sum_{b=1}^B X_b^2$$

This works because $E[\hat{\mu}] = E[X^2] = 1/3$ by the definition of expectation, and the LLN guarantees $\hat{\mu} \to 1/3$ as $B \to \infty$. For $B = 1{,}000$ you typically get an estimate within $\pm 0.01$ of the truth. For $B = 4{,}000$ the error halves — error scales as $1/\sqrt{B}$, so quadrupling $B$ halves the error.

---

**Example 3: Estimate $\pi$ using the unit circle**

Sample $(X, Y)$ uniformly from the unit square $[0,1]^2$. A point falls inside the quarter-unit-disk if $X^2 + Y^2 \le 1$. The area of this quarter-disk is $\pi/4$, and the area of the square is 1, so:

$$\frac{\pi}{4} = P(X^2 + Y^2 \le 1) \implies \pi = 4 \cdot E[\mathbf{1}(X^2 + Y^2 \le 1)]$$

Estimate $\pi$ by $4 \times (\text{fraction of points inside the disk})$. With $B = 10{,}000$ draws you typically recover $\pi \approx 3.14$ to two decimal places. This example shows that Monte Carlo can estimate mathematical constants and definite integrals by reframing them as expectations.

## Common Mistakes

- **Too few replicates.** Because error $\propto 1/\sqrt{B}$, you need $B = 40{,}000$ to halve the error of a $B = 10{,}000$ simulation. If your estimate is noisy, the remedy is more draws, not a different method.

- **Reusing the same random seed without realizing it.** If your simulation always starts from the same seed, you are not actually averaging over randomness — you get the same answer every time, which can mask bugs. Use a fixed seed intentionally (for reproducibility) but ensure you understand what it does.

## Quick Check

Try these before using hints:

1. You run a Monte Carlo simulation with $B = 100$ and get a standard error of 0.05. How many draws would you need to reduce the standard error to 0.01?
2. Describe how you would estimate $P(X_1 + X_2 > 3)$ for $X_1, X_2 \overset{iid}{\sim} U(0,2)$ by simulation.
3. What theorem guarantees that the Monte Carlo estimate converges to the true expectation?

*(Answers: 1. $B = 2500$ — error scales as $1/\sqrt{B}$, so to reduce by factor 5 you need 25 times as many draws; 2. Draw $B$ pairs $(X_1, X_2)$ uniform on $(0,2)$, compute fraction with $X_1 + X_2 > 3$; 3. The Law of Large Numbers)*
