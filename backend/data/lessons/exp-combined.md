# Combined Exponent Rules

## Overview

Real exponent problems rarely ask you to apply just one rule in isolation. **Combining exponent rules** means reading an expression, deciding which rules apply and in what order, and simplifying step by step until the expression is fully reduced — no negative exponents, no unsimplified powers.

## Key Idea

The quotient rule is the one most central to combining rules:

$$\frac{a^m}{a^n} = a^{m-n}$$

Why does this work? You have $m$ copies of $a$ in the numerator and $n$ copies in the denominator. Those $n$ copies cancel with $n$ of the numerator's copies, leaving exactly $m - n$ copies. If $m - n$ is negative, the remaining factors belong in the denominator, which is exactly what the negative exponent rule captures.

The full toolkit:

$$a^m \cdot a^n = a^{m+n}, \quad \frac{a^m}{a^n} = a^{m-n}, \quad (a^m)^n = a^{mn}, \quad a^{-n} = \frac{1}{a^n}, \quad a^0 = 1$$

A reliable order: handle parentheses and power-of-a-power first, then products and quotients, then eliminate negative exponents.

## Worked Examples

**Example 1: Simplify $\dfrac{x^5 \cdot x^{-2}}{x^3}$**

Start in the numerator: two powers of $x$ are being multiplied, so add their exponents. $5 + (-2) = 3$, giving $x^3$ on top. Now apply the quotient rule: $x^3$ over $x^3$ means subtract the exponents, $3 - 3 = 0$. Any base to the zero power equals 1 — this is true because you subtract equal exponents, leaving nothing.

$$\frac{x^5 \cdot x^{-2}}{x^3} = \frac{x^3}{x^3} = x^0 = 1$$

---

**Example 2: Simplify $(3x^2 y^{-1})^2$**

The power-of-a-product rule says the exponent 2 distributes to every factor inside the parentheses. Apply it to each: $3^2 = 9$, $(x^2)^2 = x^{2 \cdot 2} = x^4$, $(y^{-1})^2 = y^{-1 \cdot 2} = y^{-2}$. Finally, rewrite $y^{-2}$ as a denominator to leave no negative exponents.

$$(3x^2 y^{-1})^2 = 9x^4 y^{-2} = \frac{9x^4}{y^2}$$

---

**Example 3: Simplify $\dfrac{(2a^3)^3}{4a^5}$**

First expand the numerator using the power rule: $2^3 = 8$ and $(a^3)^3 = a^9$, so the numerator is $8a^9$. Now apply the quotient rule: the coefficient $8 \div 4 = 2$, and for the variable $a^9 \div a^5 = a^{9-5} = a^4$. Both simplify cleanly.

$$\frac{(2a^3)^3}{4a^5} = \frac{8a^9}{4a^5} = 2a^4$$

## Common Mistakes

- **Skipping the power rule when there are parentheses.** In $(3x)^2$, the exponent applies to both the 3 and the $x$. The result is $9x^2$, not $3x^2$.
- **Subtracting exponents in the wrong direction.** The quotient rule is $a^m / a^n = a^{m-n}$ — numerator exponent minus denominator exponent. Reversing the subtraction gives the wrong sign.
- **Leaving negative exponents in the final answer.** Unless the problem says otherwise, a fully simplified expression has no negative exponents.

## Quick Check

1. Simplify $\dfrac{a^8}{a^3}$
2. Simplify $(x^3)^2 \cdot x^{-4}$
3. Simplify $\dfrac{(3y)^2}{9y}$

*(Answers: $a^5$, $x^2$, $y$)*
