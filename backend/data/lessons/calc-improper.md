# Improper Integrals

## Overview

An **improper integral** has either an infinite limit of integration (Type I) or an integrand with a vertical asymptote on the interval (Type II). You evaluate them using limits.

## Key Idea

**Type I** (infinite limits):

$$\int_a^\infty f(x)\,dx = \lim_{b\to\infty}\int_a^b f(x)\,dx$$

**Type II** (infinite integrand at $x = c$):

$$\int_a^b f(x)\,dx = \lim_{t\to c^-}\int_a^t f(x)\,dx \quad\text{(if } f \to \infty \text{ at } c)$$

## Worked Examples

**Example 1: Type I — $\int_1^\infty \frac{1}{x^2}\,dx$**

$$\lim_{b\to\infty}\left[-\frac{1}{x}\right]_1^b = \lim_{b\to\infty}\left(-\frac{1}{b} + 1\right) = 1$$

Converges to 1.

---

**Example 2: Type I — $\int_1^\infty \frac{1}{x}\,dx$**

$$\lim_{b\to\infty}[\ln x]_1^b = \lim_{b\to\infty}\ln b = \infty$$

Diverges.

---

**Example 3: Type II — $\int_0^1 \frac{1}{\sqrt{x}}\,dx$**

Integrand blows up at $x=0$: $\lim_{t\to0^+}\int_t^1 x^{-1/2}\,dx = \lim_{t\to0^+}[2\sqrt{x}]_t^1 = 2 - 0 = 2$.

## Common Mistakes

- **Evaluating without taking a limit.** Writing $\int_0^\infty e^{-x}\,dx = [-e^{-x}]_0^\infty = 1$ requires the limit argument.
- **Missing a discontinuity inside the interval** (Type II). Check the integrand carefully.

## Quick Check

1. Does $\int_1^\infty x^{-3}\,dx$ converge? If so, find its value.
2. Does $\int_0^\infty e^{-x}\,dx$ converge?
3. Evaluate $\int_0^1 \frac{1}{\sqrt{1-x}}\,dx$.

*(Answers: yes, 1/2; yes, 1; 2)*
