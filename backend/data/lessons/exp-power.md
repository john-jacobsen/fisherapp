# Power of a Power Rule

## Overview

The **power of a power rule** tells you what to do when an exponent is raised to another exponent: multiply the two exponents together. Like the product rule, this follows directly from what exponents mean — no memorization required once you see the reasoning.

## Key Idea

$$\left(a^m\right)^n = a^{m \cdot n}$$

The rule extends to products and quotients inside parentheses:

$$(ab)^n = a^n b^n \qquad \left(\frac{a}{b}\right)^n = \frac{a^n}{b^n}$$

## Worked Examples

**Example 1: $(x^3)^4$**

Raising $x^3$ to the 4th power means writing $x^3$ out four times and multiplying:

$$(x^3)^4 = x^3 \cdot x^3 \cdot x^3 \cdot x^3$$

Now apply the product rule — you have four groups of 3 factors of $x$, so $3 + 3 + 3 + 3 = 12$ total:

$$(x^3)^4 = x^{3 \cdot 4} = x^{12}$$

The multiplication of exponents is not arbitrary — it counts how many times $x$ appears as a factor when you fully expand the expression.

---

**Example 2: $(2x^2)^3$**

The outer exponent applies to every factor inside the parentheses. Both the coefficient 2 and the variable $x^2$ get raised to the 3rd power.

$$\left(2x^2\right)^3 = 2^3 \cdot \left(x^2\right)^3 = 8 \cdot x^{2 \cdot 3} = 8x^6$$

Why does the exponent distribute over multiplication? Because $(2x^2)^3 = (2x^2)(2x^2)(2x^2)$. Regrouping the 2s and the $x^2$s gives $2^3$ and $(x^2)^3$ separately — the distribution is just reorganizing a product.

---

**Example 3: $\left(\dfrac{3y^2}{z}\right)^2$**

The exponent distributes to the numerator and denominator independently, because raising a fraction to a power means multiplying the fraction by itself — which multiplies tops with tops and bottoms with bottoms.

$$\left(\frac{3y^2}{z}\right)^2 = \frac{(3y^2)^2}{z^2} = \frac{3^2 \cdot (y^2)^2}{z^2} = \frac{9y^4}{z^2}$$

Work through the numerator carefully: the coefficient 3 is squared to give 9, and $y^2$ is raised to the 2nd power using the power rule to give $y^{2 \cdot 2} = y^4$.

## Common Mistakes

- **Adding instead of multiplying the exponents.** $(x^3)^4 = x^{12}$, not $x^7$. Adding exponents is for the product rule ($x^3 \cdot x^4$) — a completely different operation.
- **Forgetting to raise the coefficient to the power.** $(2x)^3 = 2^3 \cdot x^3 = 8x^3$, not $2x^3$. The exponent applies to every factor inside the parentheses, including any number out front.
- **Confusing $-a^n$ with $(-a)^n$.** The expression $-x^2$ means $-(x^2)$, while $(-x)^2 = x^2$. Parentheses determine whether the negative sign is included in the base.

## Quick Check

Try these before using hints:

1. $(y^4)^3$
2. $(3x)^2$
3. $\left(\dfrac{x^2}{y}\right)^3$

*(Answers: $y^{12}$, $9x^2$, $\dfrac{x^6}{y^3}$)*
