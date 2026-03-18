# Derivatives of Exponential and Log Functions

## Overview

The derivatives of $e^x$ and $\ln x$ have elegant formulas. Exponential functions with base $e$ are their own derivatives; logarithms introduce a reciprocal.

## Key Idea

$$\frac{d}{dx}[e^x] = e^x, \quad \frac{d}{dx}[\ln x] = \frac{1}{x}$$

For other bases: $\frac{d}{dx}[a^x] = a^x \ln a$ and $\frac{d}{dx}[\log_a x] = \frac{1}{x \ln a}$.

## Worked Examples

**Example 1: Differentiate $f(x) = 5e^x + \ln x$**

$$f'(x) = 5e^x + \frac{1}{x}$$

---

**Example 2: Differentiate $g(x) = e^{3x}$**

Chain rule: $g'(x) = 3e^{3x}$.

---

**Example 3: Differentiate $h(x) = \ln(x^2 + 1)$**

Chain rule: $h'(x) = \frac{2x}{x^2 + 1}$.

## Common Mistakes

- **Writing $(e^x)' = xe^{x-1}$.** That's the power rule — $e^x$ is exponential, not a power of $x$.
- **Forgetting the chain rule** when the exponent is not just $x$.

## Quick Check

1. $\frac{d}{dx}(e^{-x})$
2. $\frac{d}{dx}(\ln(3x))$
3. $\frac{d}{dx}(2^x)$

*(Answers: $-e^{-x}$; $1/x$; $2^x \ln 2$)*
