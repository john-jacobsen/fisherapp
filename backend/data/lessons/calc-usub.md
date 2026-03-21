# U-Substitution

## Overview

**U-substitution** is the integration analogue of the chain rule. When an integrand contains a composite function and its inner derivative appears as a factor, substituting $u$ for the inner function simplifies the integral into a form you can evaluate directly. It is the most widely used integration technique after the basic antiderivative rules.

## Key Idea

Let $u = g(x)$, so $du = g'(x)\,dx$. The integral transforms as:

$$\int f(g(x))\,g'(x)\,dx = \int f(u)\,du$$

Integrate in terms of $u$, then substitute back $u = g(x)$ to express the answer in terms of $x$. For definite integrals, you can either substitute back or change the limits of integration to $u$-values (often cleaner).

**Choosing $u$:** look for an expression whose derivative also appears in the integrand (up to a constant factor).

## Worked Examples

**Example 1: $\int 2x(x^2 + 1)^4\,dx$**

Notice that the derivative of $x^2 + 1$ is $2x$, which appears as the factor in front. This signals that $u = x^2 + 1$ is the right substitution.

Let $u = x^2 + 1$, so $du = 2x\,dx$. The entire factor $2x\,dx$ equals $du$ — it disappears perfectly.

$$\int (x^2+1)^4 \cdot 2x\,dx = \int u^4\,du = \frac{u^5}{5} + C$$

Substitute back: $\dfrac{(x^2 + 1)^5}{5} + C$.

---

**Example 2: $\int\sin(3x)\,dx$**

The inner function is $3x$, and its derivative is 3. The integrand is $\sin(3x) \cdot 1$, so the factor $1$ is off by a constant from the needed $du$.

Let $u = 3x$, so $du = 3\,dx$, which means $dx = \frac{du}{3}$.

$$\int\sin(3x)\,dx = \int\sin(u)\,\frac{du}{3} = \frac{1}{3}\int\sin u\,du = -\frac{\cos u}{3} + C = -\frac{\cos(3x)}{3} + C$$

Dividing by 3 handles the mismatch — the inner derivative was 3, not 1.

---

**Example 3: $\int_0^1 2x\,e^{x^2}\,dx$ (definite integral)**

The inner function is $x^2$, its derivative $2x$ appears as the leading factor. Let $u = x^2$, $du = 2x\,dx$.

Change the limits: when $x = 0$, $u = 0$; when $x = 1$, $u = 1$.

$$\int_{x=0}^{x=1} e^{x^2} \cdot 2x\,dx = \int_0^1 e^u\,du = \left[e^u\right]_0^1 = e^1 - e^0 = e - 1$$

Changing limits at the start means you never need to substitute back — the integral is evaluated entirely in $u$.

## Common Mistakes

- **Forgetting to transform $dx$ (or the limits).** After substituting $u = g(x)$, you must also replace $dx$ using $du = g'(x)\,dx$. Neglecting this leaves a mix of $u$ and $x$ in the integral.
- **Choosing a $u$ that leaves leftover $x$-terms you can't replace.** If after substituting there are still $x$'s that can't be written in terms of $u$, try a different choice.
- **Substituting the limits but then substituting back.** For definite integrals, once you change the limits to $u$-values, the integral is entirely in $u$ — don't convert back to $x$ before evaluating.

## Quick Check

1. $\int 3(3x - 1)^2\,dx$
2. $\int\dfrac{2x}{x^2 + 4}\,dx$
3. $\int_0^{\pi/2}\cos x \cdot e^{\sin x}\,dx$

*(Answers: $(3x-1)^3 + C$; $\ln(x^2+4) + C$; $e - 1$)*
