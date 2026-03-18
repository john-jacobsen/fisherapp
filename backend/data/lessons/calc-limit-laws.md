# Limit Laws

## Overview

**Limit laws** let you break complicated limits into simpler pieces. Rather than analyzing each limit from scratch, you can combine limits using rules for sums, products, and quotients.

## Key Idea

If $\lim_{x\to a} f(x) = L$ and $\lim_{x\to a} g(x) = M$, then:

$$\lim_{x\to a}[f(x) + g(x)] = L + M, \quad \lim_{x\to a}[f(x)\cdot g(x)] = LM$$

$$\lim_{x\to a}\frac{f(x)}{g(x)} = \frac{L}{M} \quad (M \ne 0), \quad \lim_{x\to a}[f(x)]^n = L^n$$

## Worked Examples

**Example 1: $\lim_{x\to 2}(3x^2 - 5x + 1)$**

Apply sum/power laws: $3(4) - 5(2) + 1 = 12 - 10 + 1 = 3$.

---

**Example 2: $\lim_{x\to 3}\sqrt{x^2 + 7}$**

$$\sqrt{\lim_{x\to 3}(x^2 + 7)} = \sqrt{9 + 7} = 4$$

---

**Example 3: $\lim_{x\to 1}\frac{x^2 - 1}{x - 1}$**

Factor first: $x + 1 \to 2$. (Can't use quotient law directly since denominator $\to 0$.)

## Common Mistakes

- **Applying the quotient law when the denominator limit is 0.** Factor and simplify first.
- **Forgetting that limit laws require both limits to exist.**

## Quick Check

1. $\lim_{x\to 0}(x^3 + 5)$
2. $\lim_{x\to 4}\sqrt{x+12}$
3. $\lim_{x\to 2}(x^2+1)(x-3)$

*(Answers: 5; 4; −5)*
