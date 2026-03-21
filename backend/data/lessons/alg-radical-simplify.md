# Simplifying Radicals

## Overview

**Simplifying a radical** means rewriting it so that no perfect-power factors remain under the radical sign. A square root is simplified when the radicand has no perfect square factor other than 1. A cube root is simplified when the radicand has no perfect cube factor. The underlying rule is that radicals distribute over multiplication but not over addition.

## Key Idea

Radicals distribute over products:

$$\sqrt[n]{a \cdot b} = \sqrt[n]{a} \cdot \sqrt[n]{b}$$

Strategy: factor the radicand into a perfect power times a remaining factor, then pull the perfect power out front.

## Worked Examples

**Example 1: Simplify $\sqrt{72}$**

Find the largest perfect square factor of 72. Write out factor pairs: $72 = 4 \times 18 = 9 \times 8 = 36 \times 2$. The largest perfect square is 36.

$$\sqrt{72} = \sqrt{36 \times 2} = \sqrt{36} \cdot \sqrt{2} = 6\sqrt{2}$$

If you had only noticed $4 \times 18$, you would get $2\sqrt{18}$, which is not fully simplified because $18 = 9 \times 2$. Always use the largest perfect square factor to finish in one step.

---

**Example 2: Simplify $\sqrt{50x^3}$**

Separate the numeric and variable parts. For the number: $50 = 25 \times 2$, so $\sqrt{50} = 5\sqrt{2}$. For the variable: $x^3 = x^2 \cdot x$, so $\sqrt{x^3} = x\sqrt{x}$ (assuming $x \ge 0$, so we can take the square root of $x^2$).

$$\sqrt{50x^3} = \sqrt{25x^2 \cdot 2x} = \sqrt{25x^2} \cdot \sqrt{2x} = 5x\sqrt{2x}$$

The condition $x \ge 0$ is required because $\sqrt{x^2} = |x|$, which equals $x$ only when $x \ge 0$.

---

**Example 3: Simplify $\sqrt[3]{54}$**

Find the largest perfect cube factor of 54. Cube factors to check: $8, 27$. Does $27 \mid 54$? Yes: $54 = 27 \times 2$.

$$\sqrt[3]{54} = \sqrt[3]{27 \times 2} = \sqrt[3]{27} \cdot \sqrt[3]{2} = 3\sqrt[3]{2}$$

Since $27 = 3^3$, its cube root is simply 3.

## Common Mistakes

- **Not using the largest perfect square factor.** $\sqrt{72} = \sqrt{4 \times 18} = 2\sqrt{18}$ still has $\sqrt{9}$ hiding inside $\sqrt{18}$. The result is not fully simplified. Find the largest perfect square factor upfront.
- **Applying the product rule to sums.** $\sqrt{a + b} \ne \sqrt{a} + \sqrt{b}$. This is a very common error. For example, $\sqrt{9 + 16} = \sqrt{25} = 5$, but $\sqrt{9} + \sqrt{16} = 3 + 4 = 7 \ne 5$.
- **Ignoring variable assumptions.** $\sqrt{x^2} = |x|$, not simply $x$. Write $x$ (without absolute value) only when you are told $x \ge 0$.

## Quick Check

Try these before using hints:

1. Simplify $\sqrt{48}$
2. Simplify $\sqrt{18x^4}$
3. Simplify $\sqrt[3]{16}$

*(Answers: $4\sqrt{3}$; $3x^2\sqrt{2}$; $2\sqrt[3]{2}$)*
