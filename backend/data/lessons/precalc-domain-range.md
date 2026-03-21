# Domain and Range

## Overview

The **domain** of a function is the complete set of valid input values ($x$-values). The **range** is the complete set of output values ($y$-values). Three common sources of domain restrictions are: even-index radicals (the expression inside must be $\ge 0$), denominators (cannot equal zero), and logarithms (the argument must be $> 0$). Finding the range often requires analyzing the shape of the function.

## Key Idea

To find the domain, identify every $x$-value that would cause a problem and exclude it:

$$\text{Domain} = \{x \in \mathbb{R} : \text{no denominator is 0, no even radical is negative}\}$$

Write the domain in interval notation. Use $\cup$ (union) to join intervals when values are excluded in the middle.

## Worked Examples

**Example 1: Domain of $f(x) = \frac{1}{x - 3}$**

The denominator is $x - 3$. Set it equal to zero: $x - 3 = 0 \implies x = 3$. This value must be excluded — you cannot divide by zero.

Domain: all real numbers except 3, written as $(-\infty, 3) \cup (3, \infty)$.

Check: any $x \ne 3$ produces a defined output. For example, $f(4) = \frac{1}{1} = 1$ ✓ and $f(0) = \frac{1}{-3} = -\frac{1}{3}$ ✓.

---

**Example 2: Domain of $g(x) = \sqrt{2x - 6}$**

The expression under a square root must be non-negative (zero is allowed — $\sqrt{0} = 0$). Set up the inequality:

$$2x - 6 \ge 0 \implies 2x \ge 6 \implies x \ge 3$$

Domain: $[3, \infty)$. The bracket at 3 indicates 3 is included.

Check: $g(3) = \sqrt{0} = 0$ ✓ and $g(4) = \sqrt{2}$ ✓. What about $g(2) = \sqrt{-2}$? Undefined. ✓

---

**Example 3: Range of $f(x) = x^2 + 2$**

The domain is all real numbers (no restrictions). To find the range, analyze the output. Since $x^2 \ge 0$ for all real $x$, the smallest possible output is $0 + 2 = 2$, occurring at $x = 0$. As $|x|$ grows, $x^2$ grows without bound, so the output grows without bound.

Range: $[2, \infty)$. Every value $\ge 2$ is achievable, and nothing below 2 is.

## Common Mistakes

- **Confusing domain and range.** Domain is the set of valid inputs; range is the set of achievable outputs. A common mnemonic: $d$ comes before $r$, and input comes before output.
- **Using strict inequality for square roots.** $\sqrt{x}$ requires $x \ge 0$, not $x > 0$. Zero is a valid input: $\sqrt{0} = 0$. The domain of $\sqrt{x}$ is $[0, \infty)$, not $(0, \infty)$.
- **Forgetting to use union notation.** If $x = 2$ and $x = -2$ are both excluded from the domain, write $(-\infty, -2) \cup (-2, 2) \cup (2, \infty)$, not just "$x \ne \pm 2$" (though the latter is acceptable shorthand).

## Quick Check

Try these before using hints:

1. Find the domain of $h(x) = \sqrt{x + 4}$
2. Find the domain of $\frac{x}{x^2 - 1}$
3. Find the range of $g(x) = -x^2 + 3$

*(Answers: $[-4, \infty)$; $x \ne \pm 1$, i.e., $(-\infty,-1)\cup(-1,1)\cup(1,\infty)$; $(-\infty, 3]$)*
