# Limits

## Overview

The **limit** of $f(x)$ as $x$ approaches $a$, written $\lim_{x \to a} f(x) = L$, captures what value a function is heading toward — not necessarily the value it actually takes at $a$. The function does not even need to be defined at $a$ for a limit to exist. This idea is the foundation of all of calculus: derivatives and integrals are both defined using limits.

## Key Idea

$$\lim_{x \to a} f(x) = L$$

The limit exists if and only if both one-sided limits agree:

$$\lim_{x \to a^-} f(x) = L \quad \text{and} \quad \lim_{x \to a^+} f(x) = L$$

For polynomials and most elementary functions, you can evaluate a limit simply by substituting $x = a$. The interesting cases are when substitution gives an indeterminate form like $0/0$ — that means more work is needed, not that the limit fails to exist.

## Worked Examples

**Example 1: $\lim_{x \to 3}(2x + 1)$**

This is a polynomial, so there are no issues at $x = 3$. Substituting directly gives a well-defined answer — no holes, no asymptotes, no cancellation needed.

Substitute $x = 3$:

$$2(3) + 1 = 7$$

The limit is 7. When the function is continuous at the point (as polynomials always are), the limit equals the function value.

---

**Example 2: $\lim_{x \to 2} \dfrac{x^2 - 4}{x - 2}$**

Substituting $x = 2$ gives $0/0$, which is indeterminate — the function is not defined at $x = 2$. But the limit can still exist. The $0/0$ form signals that a common factor is canceling.

Factor the numerator: $x^2 - 4 = (x-2)(x+2)$.

$$\frac{(x-2)(x+2)}{x-2} = x + 2 \quad (x \ne 2)$$

Now substitute: $2 + 2 = 4$. The limit is 4. The hole at $x = 2$ doesn't affect what the function approaches — only what it equals there.

---

**Example 3: $\lim_{x \to 0} \dfrac{\sin x}{x}$**

Substitution gives $0/0$ again, and factoring won't help here. This limit cannot be evaluated by elementary algebra — it requires the squeeze theorem or a geometric argument.

The standard result, which you should memorize, is:

$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$

This limit appears repeatedly in derivatives of trig functions. The key insight is that near $x = 0$, $\sin x \approx x$, so the ratio approaches 1.

## Common Mistakes

- **Equating $\lim_{x \to a} f(x)$ with $f(a)$.** These are equal only when $f$ is continuous at $a$. If there's a hole or the function isn't defined at $a$, the limit may still exist even though $f(a)$ does not.
- **Concluding the limit doesn't exist when you get $0/0$.** That form is indeterminate — it means try harder (factor, rationalize, or use a known result), not that the limit is undefined.
- **Confusing one-sided limits.** If $\lim_{x \to a^-} f(x) \ne \lim_{x \to a^+} f(x)$, the two-sided limit does not exist. Always check both sides when the function behaves differently to the left and right.

## Quick Check

1. $\lim_{x \to 4}(x^2 - 1)$
2. $\lim_{x \to 3} \dfrac{x^2 - 9}{x - 3}$
3. $\lim_{x \to 0} \dfrac{\tan x}{x}$

*(Answers: 15; 6; 1)*
