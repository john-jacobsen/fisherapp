# Factoring: Greatest Common Factor

## Overview

**Factoring out the GCF** is the first step in any factoring problem. You identify the greatest common factor of all terms in a polynomial and rewrite it as a product, placing the GCF out front and the remaining expression inside parentheses. This is the reverse of distributing — and always the first thing to try.

## Key Idea

The distributive property run in reverse:

$$ab + ac = a(b + c)$$

The GCF is the largest factor — both numerical and variable — that divides evenly into every term. For the variable part, use the lowest power of each variable that appears in all terms.

## Worked Examples

**Example 1: Factor $12x^3 + 8x^2$**

Find the numerical GCF of 12 and 8: both are divisible by 4, and 4 is the largest such number. For the variable part: both terms have $x^2$ or higher, so the variable GCF is $x^2$ (the lower power).

GCF $= 4x^2$. Divide each term:

$$12x^3 + 8x^2 = 4x^2(3x + 2)$$

Check by distributing: $4x^2 \cdot 3x + 4x^2 \cdot 2 = 12x^3 + 8x^2$ ✓

---

**Example 2: Factor $6a^2b - 9ab^2 + 3ab$**

Numerical GCF of 6, 9, 3: all divisible by 3. Variable GCF: $a$ appears in all terms with power at least 1; $b$ appears in all terms with power at least 1. So GCF $= 3ab$.

Divide each term: $\frac{6a^2b}{3ab} = 2a$, $\frac{9ab^2}{3ab} = 3b$, $\frac{3ab}{3ab} = 1$.

$$6a^2b - 9ab^2 + 3ab = 3ab(2a - 3b + 1)$$

The 1 at the end is essential — do not drop it.

---

**Example 3: Factor $5(x+2) + 3x(x+2)$**

The GCF here is the binomial $(x + 2)$, which appears in both terms. Factor it out:

$$5(x+2) + 3x(x+2) = (x+2)(5 + 3x)$$

This works the same way as factoring out a number — you just divide both terms by the common factor $(x+2)$.

## Common Mistakes

- **Not finding the full GCF.** Factoring out only part of the common factor (e.g., pulling out 2 when the GCF is 6) leaves a result that could still be factored. Always confirm that GCF of the remaining terms inside the parentheses is 1.
- **Dropping the remaining 1.** When an entire term equals the GCF — as in factoring $3x + 3 = 3(x + 1)$ — a 1 must remain inside the parentheses. Omitting it changes the polynomial.
- **Incorrect variable GCF.** The variable GCF uses the lowest exponent appearing in any term, not the highest. For $x^3 + x^5$, the GCF is $x^3$, not $x^5$.

## Quick Check

Try these before using hints:

1. Factor $10x^2 + 15x$
2. Factor $4a^3 - 2a^2 + 6a$
3. Factor $7y(y-3) - 2(y-3)$

*(Answers: $5x(2x+3)$; $2a(2a^2-a+3)$; $(y-3)(7y-2)$)*
