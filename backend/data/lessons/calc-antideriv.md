# Antiderivatives

## Overview

An **antiderivative** of $f(x)$ is any function $F(x)$ whose derivative equals $f(x)$: that is, $F'(x) = f(x)$. Integration runs differentiation in reverse — you ask "what function, when differentiated, gives me this?" The general antiderivative always includes an arbitrary constant $C$ because differentiating a constant yields zero, meaning any shift of $F$ by a constant is also a valid antiderivative.

## Key Idea

$$\int f(x)\,dx = F(x) + C \quad \text{where} \quad F'(x) = f(x)$$

**Power rule for antiderivatives** (the reverse of the power rule for derivatives):

$$\int x^n\,dx = \frac{x^{n+1}}{n+1} + C \qquad (n \ne -1)$$

Special cases you must memorize:

$$\int x^{-1}\,dx = \ln|x| + C \qquad \int e^x\,dx = e^x + C \qquad \int \cos x\,dx = \sin x + C$$

## Worked Examples

**Example 1: Find $\int x^3\,dx$**

Apply the antiderivative power rule: increase the exponent by 1 (from 3 to 4), then divide by the new exponent. This is the reverse of "bring the exponent down and subtract 1."

$$\int x^3\,dx = \frac{x^4}{4} + C$$

Check by differentiating: $\frac{d}{dx}\!\left[\frac{x^4}{4}\right] = \frac{4x^3}{4} = x^3$. ✓

---

**Example 2: Find $\int(3x^2 - 2x + 5)\,dx$**

Apply the antiderivative rule term by term. Constants integrate to a constant times $x$ (since the derivative of $cx$ is $c$). A single constant $C$ is sufficient for the whole expression.

$$\int(3x^2 - 2x + 5)\,dx = 3 \cdot \frac{x^3}{3} - 2 \cdot \frac{x^2}{2} + 5x + C = x^3 - x^2 + 5x + C$$

---

**Example 3: Find $\int\sqrt{x}\,dx$**

First rewrite the root as a power: $\sqrt{x} = x^{1/2}$. This is essential — the power rule formula requires the function to be in the form $x^n$.

Apply the antiderivative power rule with $n = 1/2$: increase exponent to $3/2$, divide by $3/2$:

$$\int x^{1/2}\,dx = \frac{x^{3/2}}{3/2} + C$$

Dividing by $3/2$ is the same as multiplying by $2/3$:

$$= \frac{2}{3}x^{3/2} + C$$

Check: $\frac{d}{dx}\!\left[\frac{2}{3}x^{3/2}\right] = \frac{2}{3} \cdot \frac{3}{2} x^{1/2} = x^{1/2} = \sqrt{x}$. ✓

## Common Mistakes

- **Omitting $+ C$.** The $+C$ is not optional — it represents the entire family of antiderivatives. Without it, you have specified one particular antiderivative, not the general one. On exams, forgetting $C$ typically costs points.
- **Using the power rule for $n = -1$.** The formula $\frac{x^{n+1}}{n+1}$ fails at $n = -1$ because you'd divide by zero. Instead, $\int x^{-1}\,dx = \ln|x| + C$. This is a completely separate rule.
- **Forgetting to convert roots and reciprocals before integrating.** $\int\sqrt{x}\,dx$ requires rewriting as $\int x^{1/2}\,dx$ first. Similarly, $\int\frac{1}{x^2}\,dx = \int x^{-2}\,dx$, which gives $-x^{-1} + C$.

## Quick Check

1. $\int 4x^3\,dx$
2. $\int(2x + 3)\,dx$
3. $\int x^{-2}\,dx$

*(Answers: $x^4 + C$; $x^2 + 3x + C$; $-x^{-1} + C$)*
