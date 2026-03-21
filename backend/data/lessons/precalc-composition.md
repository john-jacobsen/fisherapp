# Composition of Functions

## Overview

The **composition** of two functions $f$ and $g$, written $f \circ g$ or $f(g(x))$, means: apply $g$ first, then feed the result into $f$. The output of the inner function becomes the input of the outer function. Composition is not commutative — $f(g(x))$ and $g(f(x))$ are generally different functions.

## Key Idea

$$(f \circ g)(x) = f(g(x))$$

The right-to-left reading: start with $x$, apply $g$ to get $g(x)$, then apply $f$ to that result. The domain of $f \circ g$ consists of all $x$ in the domain of $g$ for which $g(x)$ is in the domain of $f$.

## Worked Examples

**Example 1: $f(x) = x^2$, $g(x) = 2x + 1$. Find $(f \circ g)(3)$.**

Work from inside out. First apply $g$:

$$g(3) = 2(3) + 1 = 7$$

Then apply $f$ to that result:

$$f(7) = 7^2 = 49$$

So $(f \circ g)(3) = 49$. If you had applied $f$ first: $f(3) = 9$, then $g(9) = 19$ — a different answer entirely. Order matters.

---

**Example 2: Same functions. Find the formula for $(f \circ g)(x)$.**

Substitute the entire expression $g(x) = 2x + 1$ in place of $x$ in $f$:

$$f(g(x)) = f(2x + 1) = (2x + 1)^2 = 4x^2 + 4x + 1$$

The key step is replacing $x$ in $f(x) = x^2$ with the full expression $2x + 1$, written in parentheses. Then expand.

---

**Example 3: $f(x) = \sqrt{x}$, $g(x) = x - 5$. Find the domain of $f \circ g$.**

The composition is $f(g(x)) = \sqrt{x - 5}$. For the square root to be defined, its argument must be non-negative:

$$x - 5 \ge 0 \implies x \ge 5$$

Domain of $f \circ g$: $[5, \infty)$.

Notice why: $g$ can accept any real $x$, but its output $g(x) = x - 5$ must be $\ge 0$ for $f$ to accept it. That constraint traces back to $x \ge 5$.

## Common Mistakes

- **Reversing the order.** $f(g(x))$ means $g$ is applied first. The notation can be misleading: $f$ appears on the outside but acts second. Think of it as nesting: $f(\underline{\hspace{1cm}})$ with $g(x)$ filling the blank.
- **Treating $f \circ g$ as multiplication.** $(f \circ g)(x)$ is function composition, not $f(x) \times g(x)$. The circle symbol $\circ$ specifically denotes composition.
- **Forgetting to substitute the full expression.** In Example 2, $f(2x+1) = (2x+1)^2$, not $2x + 1^2$. Wrap the substituted expression in parentheses before applying the outer function.

## Quick Check

Try these before using hints:

1. $f(x) = 3x$, $g(x) = x - 2$. Find $(f \circ g)(x)$.
2. Same functions. Find $(g \circ f)(x)$.
3. $f(x) = x^2$, $g(x) = x + 1$. Evaluate $(f \circ g)(4)$.

*(Answers: $3x - 6$; $3x - 2$; 25)*
