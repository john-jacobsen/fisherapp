# Derivatives of Exponential and Log Functions

## Overview

The number $e \approx 2.718$ is defined precisely to make the exponential function **$e^x$ its own derivative**. This self-referential property makes $e^x$ indispensable in modeling growth, decay, and oscillation. The natural logarithm $\ln x$ is the inverse of $e^x$, and its derivative introduces a reciprocal. These two functions and their derivatives appear throughout science and engineering.

## Key Idea

$$\frac{d}{dx}\left[e^x\right] = e^x \qquad \frac{d}{dx}\left[\ln x\right] = \frac{1}{x}$$

For other bases:

$$\frac{d}{dx}\left[a^x\right] = a^x \ln a \qquad \frac{d}{dx}\left[\log_a x\right] = \frac{1}{x \ln a}$$

The $\ln a$ factor appears because other bases are related to $e$ via $a^x = e^{x \ln a}$. Note: all these rules, combined with the chain rule, handle any composite expression.

## Worked Examples

**Example 1: Differentiate $f(x) = 5e^x + \ln x$**

Apply the basic rules term by term. The constant 5 is just a coefficient — pull it through. The derivative of $\ln x$ is $1/x$, which holds for all $x > 0$.

$$f'(x) = 5e^x + \frac{1}{x}$$

No chain rule is needed here because both arguments are plain $x$.

---

**Example 2: Differentiate $g(x) = e^{3x}$**

The argument of the exponential is $3x$, not plain $x$, so the chain rule applies. Identify: outer is $e^{(\cdot)}$, inner is $3x$.

Derivative of the outer at the inner: $e^{3x}$ (the exponential is its own derivative, so it stays).
Derivative of the inner: $\frac{d}{dx}(3x) = 3$.

$$g'(x) = e^{3x} \cdot 3 = 3e^{3x}$$

---

**Example 3: Differentiate $h(x) = \ln(x^2 + 1)$**

The argument of $\ln$ is $x^2 + 1$, not plain $x$, so use the chain rule. Derivative of $\ln u$ is $1/u$, then multiply by the derivative of the inside.

$$h'(x) = \frac{1}{x^2 + 1} \cdot \frac{d}{dx}(x^2 + 1) = \frac{1}{x^2 + 1} \cdot 2x = \frac{2x}{x^2 + 1}$$

The denominator is always $x^2 + 1$, not $(x^2+1)^2$ — the chain rule adds a factor in the numerator, not another power in the denominator.

## Common Mistakes

- **Applying the power rule to $e^x$.** Writing $(e^x)' = xe^{x-1}$ is a category error. The power rule applies when $x$ is the base (like $x^3$). In $e^x$, the base is the constant $e$ and $x$ is the exponent — that's an exponential function, and it differentiates to itself.
- **Forgetting the chain rule when the exponent or argument is not plain $x$.** $\frac{d}{dx}[e^{3x}] = 3e^{3x}$, not $e^{3x}$. The inner derivative (here, 3) is the correction factor.
- **Writing $(\ln x)' = 1$ instead of $1/x$.** The derivative of $\ln x$ is $\frac{1}{x}$, which varies with $x$. It equals 1 only at $x = 1$.

## Quick Check

1. $\dfrac{d}{dx}(e^{-x})$
2. $\dfrac{d}{dx}(\ln(3x))$
3. $\dfrac{d}{dx}(2^x)$

*(Answers: $-e^{-x}$; $\dfrac{1}{x}$; $2^x \ln 2$)*
