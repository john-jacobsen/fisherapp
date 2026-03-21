# Chain Rule

## Overview

The **chain rule** differentiates composite functions — functions of the form $f(g(x))$, where one function is nested inside another. The rule says: differentiate the outer function at the inner function (leave the inner intact), then multiply by the derivative of the inner function. Every time you see a function "applied to something other than plain $x$", the chain rule applies.

## Key Idea

$$\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)$$

The outer derivative is evaluated at the inner function — do not simplify the inner function before differentiating the outer. Then multiply by the inner derivative. This multiplicative correction accounts for the fact that the inner function is itself changing with $x$.

In Leibniz notation with $u = g(x)$: $\dfrac{dy}{dx} = \dfrac{dy}{du} \cdot \dfrac{du}{dx}$.

## Worked Examples

**Example 1: Differentiate $h(x) = (3x + 1)^5$**

Identify the structure: outer function is $u^5$, inner function is $u = 3x + 1$.

Outer derivative: $5u^4$ — but evaluated at the inner function, not at $u$ alone.
Inner derivative: $\frac{d}{dx}(3x+1) = 3$.

Apply the chain rule — outer at inner, times inner derivative:

$$h'(x) = 5(3x + 1)^4 \cdot 3 = 15(3x + 1)^4$$

The $(3x+1)$ stays inside the parentheses after differentiating. You do not expand it.

---

**Example 2: Differentiate $f(x) = \sin(x^2)$**

Outer function: $\sin(\cdot)$; inner function: $x^2$.

Derivative of $\sin$ is $\cos$ — evaluated at the inner function, so the result starts with $\cos(x^2)$.
Inner derivative: $\frac{d}{dx}(x^2) = 2x$.

$$f'(x) = \cos(x^2) \cdot 2x = 2x\cos(x^2)$$

Compare with $\frac{d}{dx}[\sin x] = \cos x$: the only difference is the chain rule correction factor $2x$.

---

**Example 3: Differentiate $g(x) = e^{-x^2}$**

Outer function: $e^{(\cdot)}$; inner function: $-x^2$.

The derivative of $e^u$ is $e^u$ — but evaluated at the inner function, giving $e^{-x^2}$.
Inner derivative: $\frac{d}{dx}(-x^2) = -2x$.

$$g'(x) = e^{-x^2} \cdot (-2x) = -2x\,e^{-x^2}$$

The exponential factor does not change form — $e^{-x^2}$ appears in both the original and the derivative.

## Common Mistakes

- **Forgetting the chain rule when it's needed.** $\frac{d}{dx}[\sin(x^2)] \ne \cos(x^2)$. Any time the argument of a function is more than plain $x$, multiply by the derivative of that argument.
- **Applying the chain rule when it's not needed.** $f(x) = x^3$ is just the power rule — there is no inner function to differentiate. Over-applying produces phantom factors.
- **Evaluating the outer derivative at $x$ instead of at the inner function.** The outer derivative must be evaluated at $g(x)$, not at $x$ alone. $\frac{d}{dx}[(3x+1)^5] = 5(3x+1)^4 \cdot 3$, not $5x^4 \cdot 3$.

## Quick Check

1. $\dfrac{d}{dx}\!\left(\sqrt{2x + 3}\right)$
2. $\dfrac{d}{dx}\!\left(\cos(5x)\right)$
3. $\dfrac{d}{dx}\!\left((x^2 + 1)^4\right)$

*(Answers: $\dfrac{1}{\sqrt{2x+3}}$; $-5\sin(5x)$; $8x(x^2+1)^3$)*
