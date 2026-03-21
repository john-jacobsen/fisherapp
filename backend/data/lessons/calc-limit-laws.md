# Limit Laws

## Overview

**Limit laws** let you evaluate complicated limits by breaking them into simpler pieces. Rather than analyzing each limit from scratch using the definition, you can combine limits using algebraic rules for sums, products, and quotients — as long as each individual limit exists. They formalize the intuition that limits behave the way you'd expect arithmetic to behave.

## Key Idea

If $\lim_{x \to a} f(x) = L$ and $\lim_{x \to a} g(x) = M$, then:

$$\lim_{x\to a}[f(x) + g(x)] = L + M \qquad \text{(Sum Law)}$$

$$\lim_{x\to a}[f(x) \cdot g(x)] = L \cdot M \qquad \text{(Product Law)}$$

$$\lim_{x\to a}\frac{f(x)}{g(x)} = \frac{L}{M} \quad (M \ne 0) \qquad \text{(Quotient Law)}$$

$$\lim_{x\to a}[f(x)]^n = L^n \qquad \text{(Power Law)}$$

The quotient law has a critical restriction: it only applies when the denominator's limit is nonzero. When the denominator approaches 0, factor and simplify first.

## Worked Examples

**Example 1: $\lim_{x \to 2}(3x^2 - 5x + 1)$**

This is a polynomial, so you can apply the limit laws term by term. Each power of $x$ has its own limit, and constants pull out as multipliers. This is why direct substitution works for polynomials.

Apply the sum and power laws:

$$3(2)^2 - 5(2) + 1 = 12 - 10 + 1 = 3$$

---

**Example 2: $\lim_{x \to 3}\sqrt{x^2 + 7}$**

The root function is continuous, so you can move the limit inside — this follows from the composition law. First compute the limit of the inside expression, then apply the root.

Compute the inner limit: $\lim_{x \to 3}(x^2 + 7) = 9 + 7 = 16$.

Apply the root:

$$\sqrt{16} = 4$$

The limit is 4. Moving the limit inside works here because $\sqrt{\,\cdot\,}$ is continuous and the inner limit is positive.

---

**Example 3: $\lim_{x \to 1} \dfrac{x^2 - 1}{x - 1}$**

The denominator approaches 0 at $x = 1$, so the quotient law cannot be applied directly — you would get $0/0$. The fix is to simplify the expression before taking the limit.

Factor the numerator: $x^2 - 1 = (x-1)(x+1)$.

$$\frac{(x-1)(x+1)}{x-1} = x + 1 \quad (x \ne 1)$$

Now the quotient law is not needed at all. Substitute: $1 + 1 = 2$.

The limit is 2. Factoring and canceling first avoids the $0/0$ trap.

## Common Mistakes

- **Applying the quotient law when the denominator's limit is 0.** The law requires $M \ne 0$. If the denominator approaches 0, factor and cancel before using any limit laws.
- **Forgetting that limit laws require both limits to exist.** You cannot combine limits using these rules if either $\lim f$ or $\lim g$ is undefined or infinite.
- **Treating $\infty/\infty$ as 1.** That form is indeterminate just like $0/0$ — it requires additional analysis (divide by the dominant term, or use L'Hôpital's rule).

## Quick Check

1. $\lim_{x \to 0}(x^3 + 5)$
2. $\lim_{x \to 4}\sqrt{x + 12}$
3. $\lim_{x \to 2}(x^2 + 1)(x - 3)$

*(Answers: 5; 4; $-5$)*
