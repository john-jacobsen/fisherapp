# Definition of the Derivative

## Overview

The **derivative** $f'(a)$ measures the instantaneous rate of change of $f$ at $x = a$ — exactly how fast the output is changing at that moment. Geometrically, it is the slope of the tangent line to the curve at $(a, f(a))$. The definition captures this precisely as a limit of the average rate of change over shorter and shorter intervals.

## Key Idea

$$f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h}$$

The numerator $f(a+h) - f(a)$ is the change in output; $h$ is the change in input. Their ratio is the average rate of change on $[a, a+h]$. Taking $h \to 0$ turns that average into an instantaneous rate. If the limit exists, $f$ is **differentiable** at $a$.

The function $f'(x)$ gives the derivative at every point simultaneously, using the same formula with $a$ replaced by $x$.

## Worked Examples

**Example 1: Find $f'(x)$ for $f(x) = x^2$ using the definition**

Start by forming the difference quotient — substitute $f(a+h)$ and $f(a)$ explicitly, then simplify.

$$\frac{f(x+h) - f(x)}{h} = \frac{(x+h)^2 - x^2}{h} = \frac{x^2 + 2xh + h^2 - x^2}{h} = \frac{2xh + h^2}{h}$$

Factor out $h$ from the numerator to cancel the denominator:

$$= \frac{h(2x + h)}{h} = 2x + h$$

Now take the limit: $\lim_{h \to 0}(2x + h) = 2x$. The $h$ disappears because we evaluated the limit.

$$f'(x) = 2x$$

---

**Example 2: Find the derivative of $f(x) = 3x + 1$**

For a linear function, the average rate of change between any two points is constant — the difference quotient will simplify to a number with no remaining $h$.

$$\frac{3(x+h) + 1 - (3x + 1)}{h} = \frac{3h}{h} = 3$$

The limit of a constant is that constant: $\lim_{h \to 0} 3 = 3$.

$$f'(x) = 3$$

This makes sense: a line with slope 3 has instantaneous rate of change 3 everywhere.

---

**Example 3: Is $f(x) = |x|$ differentiable at $x = 0$?**

Compute the left-hand and right-hand limits of the difference quotient separately.

Right-hand: $\lim_{h \to 0^+} \frac{|h| - 0}{h} = \lim_{h \to 0^+} \frac{h}{h} = 1$.

Left-hand: $\lim_{h \to 0^-} \frac{|h| - 0}{h} = \lim_{h \to 0^-} \frac{-h}{h} = -1$.

The two limits differ, so the overall limit does not exist. $f$ is not differentiable at $x = 0$. The graph has a sharp corner there — the slope coming from the left ($-1$) does not match the slope from the right ($+1$).

## Common Mistakes

- **Forgetting to take the limit.** The difference quotient $\frac{f(x+h)-f(x)}{h}$ is not the derivative — it's the average rate of change. The derivative is the limit of this expression as $h \to 0$.
- **Algebraic errors expanding $(x+h)^n$.** Use the binomial theorem carefully. For example, $(x+h)^3 = x^3 + 3x^2h + 3xh^2 + h^3$ — don't forget the middle terms.
- **Trying to cancel $h$ without simplifying first.** You must factor $h$ out of the numerator algebraically before canceling. Never divide by $h$ as if it were a nonzero number before the limit is taken.

## Quick Check

1. Find $f'(x)$ from the definition for $f(x) = 5x - 2$.
2. What is $f'(0)$ if $f(x) = x^2$?
3. Does the definition give a finite limit for $f(x) = x^{1/3}$ at $x = 0$?

*(Answers: 5; 0; no — the limit is $\infty$, so $f$ is not differentiable at 0)*
