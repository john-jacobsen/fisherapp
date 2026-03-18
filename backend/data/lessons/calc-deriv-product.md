# Product Rule

## Overview

The derivative of a product of two functions is not simply the product of their derivatives. The **product rule** gives the correct formula.

## Key Idea

$$\frac{d}{dx}[f(x)\,g(x)] = f'(x)\,g(x) + f(x)\,g'(x)$$

A helpful mnemonic: "derivative of first times second, plus first times derivative of second."

## Worked Examples

**Example 1: Differentiate $h(x) = x^2 \sin x$**

$$h'(x) = 2x \sin x + x^2 \cos x$$

---

**Example 2: Differentiate $f(x) = (3x + 1)(x^2 - 2)$**

$f' = 3(x^2-2) + (3x+1)(2x) = 3x^2 - 6 + 6x^2 + 2x = 9x^2 + 2x - 6$.

---

**Example 3: Differentiate $g(x) = e^x \ln x$**

$$g'(x) = e^x \ln x + e^x \cdot \frac{1}{x} = e^x\!\left(\ln x + \frac{1}{x}\right)$$

## Common Mistakes

- **Multiplying derivatives:** $(fg)' \ne f' g'$.
- **Forgetting the second term in the product rule.**

## Quick Check

1. $\frac{d}{dx}[x \cdot e^x]$
2. $\frac{d}{dx}[(x^2+1)(2x-3)]$
3. $\frac{d}{dx}[x \ln x]$

*(Answers: $e^x(1+x)$; $6x^2-6x+2$; $\ln x + 1$)*
