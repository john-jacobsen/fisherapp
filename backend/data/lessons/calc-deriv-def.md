# Definition of the Derivative

## Overview

The **derivative** $f'(a)$ measures the instantaneous rate of change of $f$ at $x = a$. It equals the slope of the tangent line to the curve at that point. It is defined as a limit.

## Key Idea

$$f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h}$$

If this limit exists, $f$ is **differentiable** at $a$. The function $f'(x)$ is the derivative at every point.

## Worked Examples

**Example 1: Find $f'(x)$ for $f(x) = x^2$ using the definition**

$$f'(x) = \lim_{h\to0}\frac{(x+h)^2 - x^2}{h} = \lim_{h\to0}\frac{2xh + h^2}{h} = \lim_{h\to0}(2x + h) = 2x$$

---

**Example 2: Find the slope of $f(x) = 3x + 1$ at any point**

$$f'(x) = \lim_{h\to0}\frac{3(x+h)+1-(3x+1)}{h} = \lim_{h\to0} 3 = 3$$

---

**Example 3: Find $f'(2)$ for $f(x) = x^3$**

Using the definition: $f'(x) = 3x^2$, so $f'(2) = 12$.

## Common Mistakes

- **Forgetting to take the limit.** The difference quotient by itself is not the derivative.
- **Algebraic errors expanding $(x+h)^n$.** Use binomial expansion carefully.

## Quick Check

1. Find $f'(x)$ from the definition for $f(x) = 5x - 2$.
2. What is $f'(0)$ if $f(x) = x^2$?
3. Is $f(x) = |x|$ differentiable at $x = 0$?

*(Answers: 5; 0; no — left and right limits differ)*
