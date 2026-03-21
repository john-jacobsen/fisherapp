# Factoring Quadratics

## Overview

**Factoring a quadratic** $ax^2 + bx + c$ means writing it as a product of two binomials. When $a = 1$, the method is straightforward: find two numbers whose product is $c$ and whose sum is $b$. When $a \ne 1$, the AC method handles the extra coefficient systematically.

## Key Idea

For $x^2 + bx + c$, find integers $p$ and $q$ such that $p \cdot q = c$ and $p + q = b$:

$$x^2 + bx + c = (x + p)(x + q)$$

You can verify this by expanding the right side: $x^2 + px + qx + pq = x^2 + (p+q)x + pq$, which matches when $p + q = b$ and $pq = c$.

## Worked Examples

**Example 1: Factor $x^2 + 5x + 6$**

You need two numbers with product 6 and sum 5. List factor pairs of 6: $(1,6)$ and $(2,3)$. Their sums are 7 and 5 respectively. The pair $(2, 3)$ works.

$$x^2 + 5x + 6 = (x + 2)(x + 3)$$

Check: $(x+2)(x+3) = x^2 + 3x + 2x + 6 = x^2 + 5x + 6$ ✓

---

**Example 2: Factor $x^2 - 7x + 12$**

Product is $+12$, sum is $-7$. Since the product is positive and the sum is negative, both numbers must be negative. Factor pairs of 12 (both negative): $(-1,-12), (-2,-6), (-3,-4)$. Their sums: $-13, -8, -7$. The pair $(-3, -4)$ works.

$$x^2 - 7x + 12 = (x - 3)(x - 4)$$

Check: $(x-3)(x-4) = x^2 - 4x - 3x + 12 = x^2 - 7x + 12$ ✓

---

**Example 3: Factor $2x^2 + 7x + 3$ (the AC method)**

Since $a = 2 \ne 1$, use the AC method. Compute $A \cdot C = 2 \cdot 3 = 6$. Find two numbers with product 6 and sum 7: $(1, 6)$. Split the middle term using these numbers:

$$2x^2 + x + 6x + 3$$

Group and factor each pair:

$$x(2x + 1) + 3(2x + 1) = (2x + 1)(x + 3)$$

Check: $(2x+1)(x+3) = 2x^2 + 6x + x + 3 = 2x^2 + 7x + 3$ ✓

## Common Mistakes

- **Sign errors.** For $x^2 - 7x + 12$, both numbers must be negative (positive product, negative sum). For $x^2 + x - 6$, the numbers have opposite signs (negative product). Always check the sign of the product first to determine whether the signs match or differ.
- **Not verifying by expanding.** After factoring, always multiply out the result to confirm you get the original quadratic. This catches both sign errors and arithmetic mistakes.
- **Trying to factor expressions that are prime.** Not every quadratic factors over integers. If no integer pair works, the quadratic is prime (irreducible) or requires the quadratic formula.

## Quick Check

Try these before using hints:

1. Factor $x^2 + 7x + 10$
2. Factor $x^2 - x - 6$
3. Factor $3x^2 + 10x - 8$

*(Answers: $(x+2)(x+5)$; $(x-3)(x+2)$; $(3x-2)(x+4)$)*
