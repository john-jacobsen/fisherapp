# Improper Integrals

## Overview

An **improper integral** extends definite integration to situations where the standard definition breaks down: either the interval of integration is unbounded (extends to $\pm\infty$), or the integrand has a vertical asymptote somewhere on the interval. In both cases, the strategy is the same — replace the problematic boundary with a limit parameter and evaluate. If the limit is finite, the integral **converges**; if it's infinite or fails to exist, it **diverges**.

## Key Idea

**Type I** (infinite limits of integration):

$$\int_a^\infty f(x)\,dx = \lim_{b \to \infty} \int_a^b f(x)\,dx$$

**Type II** (integrand blows up at $x = c$ on $[a, b]$):

$$\int_a^b f(x)\,dx = \lim_{t \to c^+} \int_t^b f(x)\,dx \quad \text{(if } c = a\text{)}$$

A key benchmark: $\displaystyle\int_1^\infty \frac{1}{x^p}\,dx$ converges if and only if $p > 1$.

## Worked Examples

**Example 1: Type I — $\int_1^\infty \dfrac{1}{x^2}\,dx$**

Replace $\infty$ with a finite upper limit $b$ and take the limit as $b \to \infty$. This makes the integral well-defined at every stage.

Find the antiderivative: $\int x^{-2}\,dx = -x^{-1} = -\frac{1}{x}$.

Evaluate from 1 to $b$, then take the limit:

$$\lim_{b \to \infty}\left[-\frac{1}{x}\right]_1^b = \lim_{b \to \infty}\left(-\frac{1}{b} + 1\right) = 0 + 1 = 1$$

The integral converges to 1. As $b \to \infty$, the $-1/b$ term vanishes.

---

**Example 2: Type I — $\int_1^\infty \dfrac{1}{x}\,dx$**

Same setup, but the antiderivative of $1/x$ is $\ln x$.

$$\lim_{b \to \infty}\left[\ln x\right]_1^b = \lim_{b \to \infty}(\ln b - \ln 1) = \lim_{b \to \infty}\ln b = \infty$$

The integral diverges. Even though the integrand $1/x$ approaches 0 as $x \to \infty$, it decreases too slowly for the integral to be finite. This is the key contrast with $1/x^2$.

---

**Example 3: Type II — $\int_0^1 \dfrac{1}{\sqrt{x}}\,dx$**

The integrand $1/\sqrt{x} = x^{-1/2}$ blows up at $x = 0$ (the left endpoint). Replace the lower limit with $t$ and take $t \to 0^+$.

Find the antiderivative: $\int x^{-1/2}\,dx = 2x^{1/2} = 2\sqrt{x}$.

Evaluate from $t$ to 1:

$$\lim_{t \to 0^+}\left[2\sqrt{x}\right]_t^1 = \lim_{t \to 0^+}(2\sqrt{1} - 2\sqrt{t}) = 2 - 0 = 2$$

The integral converges to 2. The singularity at 0 is integrable because the function blows up only like $x^{-1/2}$, which is not as severe as $1/x$.

## Common Mistakes

- **Evaluating without writing the limit.** Writing $\int_0^\infty e^{-x}\,dx = [-e^{-x}]_0^\infty = 1$ skips the formal limit step, which is required. You must set up $\lim_{b\to\infty}[-e^{-x}]_0^b$.
- **Missing a Type II discontinuity inside the interval.** If the integrand has a vertical asymptote at a point $c$ strictly between $a$ and $b$, you must split the integral at $c$ and apply limits to each piece separately. Integrating straight through gives a wrong answer.
- **Confusing convergence of $a_n \to 0$ with convergence of the integral.** The integrand shrinking to zero is necessary but not sufficient for convergence — $1/x \to 0$ but $\int_1^\infty 1/x\,dx$ diverges.

## Quick Check

1. Does $\int_1^\infty x^{-3}\,dx$ converge? If so, find its value.
2. Does $\int_0^\infty e^{-x}\,dx$ converge?
3. Evaluate $\int_0^1 \dfrac{1}{\sqrt{1-x}}\,dx$.

*(Answers: yes, $\frac{1}{2}$; yes, $1$; $2$)*
