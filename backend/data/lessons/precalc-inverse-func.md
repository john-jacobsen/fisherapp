# Inverse Functions

## Overview

The **inverse function** $f^{-1}$ reverses what $f$ does: if $f$ maps $a$ to $b$, then $f^{-1}$ maps $b$ back to $a$. Not every function has an inverse that is also a function — only one-to-one functions do. A function is one-to-one if every output value comes from exactly one input value, which you can verify graphically using the horizontal line test.

## Key Idea

To find $f^{-1}$: write $y = f(x)$, swap $x$ and $y$, solve for $y$. The defining property of inverses is:

$$f(f^{-1}(x)) = x \quad \text{and} \quad f^{-1}(f(x)) = x \text{ for all } x \text{ in the domain}$$

The notation $f^{-1}$ does not mean $\frac{1}{f(x)}$ — the $-1$ denotes the inverse function, not a reciprocal.

## Worked Examples

**Example 1: Find the inverse of $f(x) = 2x + 3$**

Write $y = 2x + 3$, then swap $x$ and $y$: $x = 2y + 3$.

Solve for $y$: subtract 3, then divide by 2:

$$y = \frac{x - 3}{2}$$

So $f^{-1}(x) = \dfrac{x-3}{2}$.

Check: $f(f^{-1}(x)) = 2 \cdot \dfrac{x-3}{2} + 3 = (x - 3) + 3 = x$ ✓

---

**Example 2: Find the inverse of $f(x) = x^3 - 1$**

Write $y = x^3 - 1$, swap: $x = y^3 - 1$.

Solve: $y^3 = x + 1$, so $y = \sqrt[3]{x + 1}$.

$$f^{-1}(x) = \sqrt[3]{x + 1}$$

This function has an inverse for all real numbers because $x^3$ is strictly increasing — it passes the horizontal line test on all of $\mathbb{R}$.

---

**Example 3: Verify the inverse for $f(x) = 2x + 3$ from Example 1**

Check both compositions. Forward: $f(f^{-1}(x)) = 2 \cdot \dfrac{x-3}{2} + 3 = x - 3 + 3 = x$ ✓

Backward: $f^{-1}(f(x)) = \dfrac{(2x+3)-3}{2} = \dfrac{2x}{2} = x$ ✓

Both compositions returning $x$ confirms that $f$ and $f^{-1}$ are true inverses.

## Common Mistakes

- **Confusing $f^{-1}(x)$ with $\frac{1}{f(x)}$.** The reciprocal of $f(x) = 2x + 3$ is $\frac{1}{2x+3}$, which is completely different from the inverse function $\frac{x-3}{2}$. The exponent $-1$ on $f$ denotes the inverse, not a power.
- **Finding an inverse for a non-one-to-one function without restricting the domain.** $f(x) = x^2$ fails the horizontal line test: both $f(2) = 4$ and $f(-2) = 4$. To define an inverse, you must restrict to $x \ge 0$ (or $x \le 0$), giving $f^{-1}(x) = \sqrt{x}$.
- **Forgetting to verify.** After finding $f^{-1}$, always check at least one composition. Algebra errors during the swap-and-solve step are common.

## Quick Check

Try these before using hints:

1. Find the inverse of $f(x) = x - 7$.
2. Find the inverse of $g(x) = 5x$.
3. What is $f^{-1}(3)$ if $f(x) = 2x - 1$?

*(Answers: $f^{-1}(x) = x + 7$; $g^{-1}(x) = \frac{x}{5}$; 2)*
