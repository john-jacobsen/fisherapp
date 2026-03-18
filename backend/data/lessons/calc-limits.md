# Limits

## Overview

The **limit** of $f(x)$ as $x$ approaches $a$, written $\lim_{x \to a} f(x) = L$, means $f(x)$ can be made arbitrarily close to $L$ by taking $x$ sufficiently close to $a$ (but $x \ne a$). The function need not be defined at $a$.

## Key Idea

$$\lim_{x \to a} f(x) = L$$

The limit exists if and only if the left-hand limit $\lim_{x \to a^-} f(x)$ and right-hand limit $\lim_{x \to a^+} f(x)$ both equal $L$.

## Worked Examples

**Example 1: $\lim_{x \to 3} (2x + 1)$**

Substitute directly (no issues): $2(3) + 1 = 7$.

---

**Example 2: $\lim_{x \to 2} \frac{x^2 - 4}{x - 2}$**

Substituting gives $0/0$ — indeterminate. Factor: $\frac{(x-2)(x+2)}{x-2} = x + 2$. Limit $= 4$.

---

**Example 3: $\lim_{x \to 0} \frac{\sin x}{x}$**

This standard limit equals 1 (proof via squeeze theorem). It cannot be found by simple substitution.

## Common Mistakes

- **Equating $\lim_{x\to a} f(x)$ with $f(a)$.** They are equal when $f$ is continuous at $a$, but not in general.
- **Assuming $0/0$ means the limit is 0 or undefined.** It's indeterminate — more work is needed.

## Quick Check

1. $\lim_{x \to 4}(x^2 - 1)$
2. $\lim_{x \to 3} \frac{x^2-9}{x-3}$
3. $\lim_{x \to 0} \frac{\tan x}{x}$

*(Answers: 15; 6; 1)*
