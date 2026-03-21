# Continuous Random Variables and PDFs

## Overview

A **continuous random variable** has a probability density function (PDF) $f(x)$ such that probability equals the area under the curve over an interval. Unlike discrete random variables, a continuous RV can take any value in an interval, and the probability of landing at any single exact point is zero — only intervals have positive probability. This is a conceptual shift: you never ask "what is $P(X = 3)$?" for a continuous RV; you always ask about ranges.

## Key Idea

For a continuous random variable $X$ with PDF $f(x)$:

$$P(a \leq X \leq b) = \int_a^b f(x)\,dx$$

A function $f(x)$ qualifies as a valid PDF if and only if it satisfies two conditions:

$$f(x) \geq 0 \text{ for all } x \qquad \text{and} \qquad \int_{-\infty}^{\infty} f(x)\,dx = 1$$

The first condition says density is never negative; the second says total probability is 1. The expected value generalizes the discrete formula:

$$E[X] = \int_{-\infty}^{\infty} x\, f(x)\,dx$$

## Worked Examples

**Example 1: Verify that $f(x) = 2x$ on $[0, 1]$ (and 0 elsewhere) is a valid PDF**

You need to check both conditions. First, on $[0,1]$: $x \geq 0$ so $f(x) = 2x \geq 0$. Non-negativity is satisfied.

Second, integrate over the entire real line — since $f$ is zero outside $[0,1]$, only the integral over $[0,1]$ matters:

$$\int_0^1 2x\,dx = \left[x^2\right]_0^1 = 1 - 0 = 1$$

Both conditions hold, so $f(x) = 2x$ is a valid PDF. The density increases linearly, meaning values closer to 1 are more probable than values closer to 0.

---

**Example 2: Compute $P(1 < X < 3)$ from a PDF**

Let $f(x) = \frac{1}{8}x$ on $[0, 4]$ and 0 elsewhere. Find $P(1 < X < 3)$.

Probability equals the area under the curve between the limits — set up the definite integral over the interval of interest:

$$P(1 < X < 3) = \int_1^3 \frac{x}{8}\,dx = \frac{1}{8}\left[\frac{x^2}{2}\right]_1^3 = \frac{1}{8} \cdot \frac{9 - 1}{2} = \frac{1}{8} \cdot 4 = \frac{1}{2}$$

The probability is exactly $1/2$. Notice that because $P(X = 1) = 0$ and $P(X = 3) = 0$ for a continuous RV, the probabilities $P(1 < X < 3)$ and $P(1 \leq X \leq 3)$ are identical — endpoint inclusion never matters for continuous distributions.

---

**Example 3: Find the constant $c$ that makes $f(x) = cx^2$ on $[0, 1]$ a valid PDF**

You need to choose $c$ so that the total area under $f$ equals 1. Set up the normalization condition and solve for $c$ — this is why the condition $\int f = 1$ is so useful:

$$\int_0^1 cx^2\,dx = c \cdot \frac{x^3}{3}\Bigg|_0^1 = \frac{c}{3} = 1$$

Solving: $c = 3$. The valid PDF is $f(x) = 3x^2$ on $[0, 1]$. You can verify: $\int_0^1 3x^2\,dx = [x^3]_0^1 = 1$. The constant $c$ must always be positive to ensure $f(x) \geq 0$.

## Common Mistakes

- **Treating $f(x)$ as a probability.** The PDF value $f(x)$ at a single point is a density, not a probability. It can exceed 1. Only the integral of $f$ over an interval gives a probability.
- **Forgetting that $P(X = a) = 0$ for any single point.** This means $P(X \leq a) = P(X < a)$ for continuous RVs — you can always include or exclude endpoints freely.
- **Integrating over the wrong limits.** Always check that your interval of integration lies within the support of $f$. If $f$ is zero outside $[0, 4]$ and you want $P(-1 < X < 2)$, you integrate from 0 to 2, not from $-1$ to 2.

## Quick Check

1. Is $f(x) = x - 1$ on $[1, 2]$ a valid PDF? Check both conditions.
2. For $f(x) = 3x^2$ on $[0, 1]$, compute $P(X > 0.5)$.
3. Find $c$ so that $f(x) = c$ on $[2, 7]$ is a valid PDF (uniform distribution).

*(Answers: Yes — $f \geq 0$ on $[1,2]$ and $\int_1^2(x-1)\,dx = [x^2/2 - x]_1^2 = 1/2$; $\int_{0.5}^1 3x^2\,dx = 1 - (0.5)^3 = 0.875$; $5c = 1 \Rightarrow c = 1/5$)*
