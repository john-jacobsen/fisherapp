# Product and Quotient Rules

## Overview

The derivative of a product of two functions is not simply the product of their derivatives — that intuition fails. The **product rule** and **quotient rule** give the correct formulas. Both follow from the limit definition of the derivative and the fact that you must track how both factors are changing simultaneously.

## Key Idea

**Product Rule:**

$$\frac{d}{dx}[f(x)\,g(x)] = f'(x)\,g(x) + f(x)\,g'(x)$$

**Quotient Rule:**

$$\frac{d}{dx}\left[\frac{f(x)}{g(x)}\right] = \frac{f'(x)\,g(x) - f(x)\,g'(x)}{[g(x)]^2}$$

A mnemonic for the product rule: "derivative of first times second, plus first times derivative of second." For the quotient rule: "lo d-hi minus hi d-lo, over lo squared" — where hi is the numerator and lo is the denominator.

## Worked Examples

**Example 1: Differentiate $h(x) = x^2 \sin x$**

Identify the two factors: $f(x) = x^2$ and $g(x) = \sin x$. Compute each derivative: $f'(x) = 2x$ and $g'(x) = \cos x$.

Apply the product rule — derivative of the first factor times the second, plus the first factor times the derivative of the second:

$$h'(x) = 2x \cdot \sin x + x^2 \cdot \cos x$$

Both terms are necessary. Neither factor differentiates to zero, so you cannot drop either term.

---

**Example 2: Differentiate $f(x) = (3x + 1)(x^2 - 2)$**

You could expand first, but the product rule works directly. Identify $f = 3x+1$ with $f' = 3$, and $g = x^2-2$ with $g' = 2x$.

$$\frac{d}{dx}[(3x+1)(x^2-2)] = 3(x^2-2) + (3x+1)(2x)$$

Expand: $3x^2 - 6 + 6x^2 + 2x = 9x^2 + 2x - 6$.

As a check: if you expanded the original first, $(3x+1)(x^2-2) = 3x^3 + x^2 - 6x - 2$, differentiating gives $9x^2 + 2x - 6$. Same result.

---

**Example 3: Differentiate $q(x) = \dfrac{x^2}{x + 1}$**

Apply the quotient rule with $f = x^2$, $g = x+1$, so $f' = 2x$ and $g' = 1$.

$$q'(x) = \frac{2x(x+1) - x^2 \cdot 1}{(x+1)^2} = \frac{2x^2 + 2x - x^2}{(x+1)^2} = \frac{x^2 + 2x}{(x+1)^2}$$

The numerator is hi d-lo minus lo d-hi, and the denominator is the square of the bottom. The subtraction order matters — reversing it changes the sign of the result.

## Common Mistakes

- **Using $(fg)' = f'g'$.** This is wrong. The product of derivatives is not the derivative of the product. The product rule has two terms, not one.
- **Reversing the subtraction in the quotient rule.** It is always (numerator's derivative × denominator) minus (numerator × denominator's derivative), not the other way around.
- **Forgetting to square the denominator in the quotient rule.** The $[g(x)]^2$ in the denominator is essential — omitting it gives a completely wrong answer.

## Quick Check

1. $\dfrac{d}{dx}[x \cdot e^x]$
2. $\dfrac{d}{dx}\!\left[\dfrac{x^2 - 1}{x + 2}\right]$
3. $\dfrac{d}{dx}[x \ln x]$

*(Answers: $e^x(1 + x)$; $\dfrac{x^2 + 4x + 1}{(x+2)^2}$; $\ln x + 1$)*
