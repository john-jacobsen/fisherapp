# Power Rule

## Overview

The **power rule** is the most-used differentiation shortcut. It gives the derivative of any power of $x$ in one step, bypassing the limit definition entirely. You bring the exponent down as a coefficient, then reduce the exponent by one. It works for all real exponents — positive integers, fractions, and negative powers — making it the go-to rule for polynomials and root functions.

## Key Idea

$$\frac{d}{dx}\left[x^n\right] = n x^{n-1}$$

Two companion rules work with it:

$$\frac{d}{dx}[c \cdot f(x)] = c \cdot f'(x) \qquad \text{(Constant Multiple Rule)}$$

$$\frac{d}{dx}[f(x) + g(x)] = f'(x) + g'(x) \qquad \text{(Sum Rule)}$$

These three together let you differentiate any polynomial in one pass.

## Worked Examples

**Example 1: Differentiate $f(x) = x^5$**

Apply the power rule: bring the exponent (5) down as a coefficient, reduce the exponent by 1 (from 5 to 4).

$$f'(x) = 5x^4$$

Nothing else needed. The exponent was already an integer, so no rewriting is required.

---

**Example 2: Differentiate $g(x) = 3x^4 - 2x^2 + 7$**

Apply the sum rule to differentiate term by term, the constant multiple rule to pull constants through, and the power rule to each power of $x$. Constants differentiate to 0 because they have no $x$ dependence.

$$g'(x) = 3 \cdot 4x^3 - 2 \cdot 2x + 0 = 12x^3 - 4x$$

The derivative of 7 is 0 — any constant disappears under differentiation, since a flat graph has zero slope everywhere.

---

**Example 3: Differentiate $h(x) = \sqrt{x}$**

Rewrite the root as a power first: $\sqrt{x} = x^{1/2}$. This is the key step — the power rule requires the function to be in the form $x^n$ before you can apply it.

Apply the power rule with $n = 1/2$:

$$h'(x) = \frac{1}{2} x^{1/2 - 1} = \frac{1}{2} x^{-1/2}$$

Rewrite to avoid negative exponents:

$$h'(x) = \frac{1}{2\sqrt{x}}$$

This result tells you the slope of $\sqrt{x}$ is large near $x = 0$ (denominator small) and shrinks as $x$ grows — matching the visual shape of the graph.

## Common Mistakes

- **Not converting roots and fractions to power form first.** You cannot apply the power rule to $\sqrt{x}$ directly — rewrite it as $x^{1/2}$, and similarly $1/x^3 = x^{-3}$, before differentiating.
- **Forgetting to bring the exponent down AND reduce it.** The power rule does both: $\frac{d}{dx}x^3 = 3x^2$, not just $x^2$ or $3x^3$.
- **Differentiating the constant as if it's $x^0 = 1$.** The derivative of a constant is 0, not 1. Although $7 = 7x^0$, applying the power rule gives $7 \cdot 0 \cdot x^{-1} = 0$.

## Quick Check

1. $\dfrac{d}{dx}(x^7)$
2. $\dfrac{d}{dx}(4x^3 - x)$
3. $\dfrac{d}{dx}(x^{-2})$

*(Answers: $7x^6$; $12x^2 - 1$; $-2x^{-3}$)*
