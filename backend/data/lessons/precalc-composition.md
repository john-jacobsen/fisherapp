# Composition of Functions

## Overview

The **composition** of functions $f$ and $g$, written $(f \circ g)(x)$ or $f(g(x))$, applies $g$ first, then feeds its output into $f$. The order matters.

## Key Idea

$$(f \circ g)(x) = f(g(x))$$

The domain of $f \circ g$ is restricted to inputs $x$ in the domain of $g$ for which $g(x)$ is in the domain of $f$.

## Worked Examples

**Example 1: $f(x) = x^2$, $g(x) = 2x + 1$. Find $(f \circ g)(3)$.**

$g(3) = 7$. Then $f(7) = 49$.

---

**Example 2: Same functions. Find $(f \circ g)(x)$.**

$$f(g(x)) = f(2x+1) = (2x+1)^2 = 4x^2 + 4x + 1$$

---

**Example 3: $f(x) = \sqrt{x}$, $g(x) = x - 5$. Find the domain of $f \circ g$.**

Need $g(x) \ge 0$: $x - 5 \ge 0 \Rightarrow x \ge 5$. Domain: $[5, \infty)$.

## Common Mistakes

- **Reversing order:** $f(g(x)) \ne g(f(x))$ in general.
- **Using $f \circ g$ notation to mean $f \cdot g$ (multiplication).**

## Quick Check

1. $f(x)=3x$, $g(x)=x-2$. Find $(f \circ g)(x)$.
2. Same functions. Find $(g \circ f)(x)$.
3. Evaluate $(f \circ g)(4)$ with $f(x)=x^2$, $g(x)=x+1$.

*(Answers: $3x-6$; $3x-2$; 25)*
