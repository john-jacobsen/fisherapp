# Continuity

## Overview

A function is **continuous at $a$** if its graph has no holes, jumps, or vertical asymptotes at that point — informally, you can draw it through $a$ without lifting your pencil. Continuity is the formal way to say "the limit equals the function value." It matters because continuous functions behave predictably: you can swap limits and function evaluations, and you can use powerful results like the Intermediate Value Theorem.

## Key Idea

$f$ is continuous at $a$ if all three conditions hold simultaneously:

$$\text{(1) } f(a) \text{ is defined} \qquad \text{(2) } \lim_{x\to a} f(x) \text{ exists} \qquad \text{(3) } \lim_{x\to a} f(x) = f(a)$$

Each condition can fail independently. Missing just one means the function has a discontinuity at $a$, even if the other two hold.

**Types of discontinuity:** removable (hole — limit exists but doesn't match $f(a)$), jump (left and right limits differ), infinite (vertical asymptote).

## Worked Examples

**Example 1: Is $f(x) = x^2 + 1$ continuous at $x = 2$?**

Check all three conditions. The function is a polynomial, so it's defined everywhere, its limit is found by substitution, and those two values always match for polynomials.

$f(2) = 5$. $\lim_{x \to 2}(x^2 + 1) = 5$. Both equal 5.

All three conditions hold — $f$ is continuous at $x = 2$. Polynomials are always continuous on $\mathbb{R}$.

---

**Example 2: Is $g(x) = \dfrac{x^2 - 4}{x - 2}$ continuous at $x = 2$?**

Check condition (1) first: $g(2) = 0/0$, which is undefined. Condition (1) fails immediately, so $g$ is not continuous at $x = 2$.

The limit still exists: $\lim_{x \to 2} g(x) = 4$ (by factoring). This means the discontinuity is removable — you could fill the hole by defining $g(2) = 4$ and get a continuous function. But as written, $g$ is not continuous at $x = 2$.

---

**Example 3: Using the Intermediate Value Theorem**

If $f$ is continuous on $[a, b]$ and $k$ is any value between $f(a)$ and $f(b)$, then there exists at least one $c \in (a, b)$ with $f(c) = k$.

Show $f(x) = x^3 - 2$ has a root in $(1, 2)$. Check: $f(1) = -1 < 0$ and $f(2) = 6 > 0$. Since $f$ is continuous (it's a polynomial) and 0 is between $-1$ and $6$, the IVT guarantees a $c \in (1, 2)$ with $f(c) = 0$. You don't need to find $c$ — just confirm the sign change and invoke continuity.

## Common Mistakes

- **Assuming a limit existing means the function is continuous.** You also need $f(a)$ to be defined and equal to that limit. A function with a hole has a limit at the hole but is not continuous there.
- **Confusing discontinuity types.** A removable discontinuity (hole) is different from a jump discontinuity (two different one-sided limits). The IVT applies only to functions that are genuinely continuous — a jump discontinuity disqualifies it.
- **Forgetting to verify $f(a)$ is defined.** Students often compute the limit successfully, then forget to check whether the function is even defined at that point.

## Quick Check

1. Is $f(x) = |x|$ continuous at $x = 0$?
2. Where is $g(x) = \dfrac{1}{x - 3}$ discontinuous?
3. $h(x) = 5$ for $x < 1$ and $h(x) = x + 4$ for $x \ge 1$. Continuous at $x = 1$?

*(Answers: yes; $x = 3$; yes, since $\lim_{x\to1^-}h = 5$ and $h(1) = 5$)*
