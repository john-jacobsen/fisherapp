# Fundamental Theorem of Calculus

## Overview

The **Fundamental Theorem of Calculus (FTC)** is the central result of the subject. It reveals that differentiation and integration are inverse operations — two seemingly different processes that undo each other. Part 1 says that integrating $f$ and then differentiating gives you $f$ back. Part 2 gives a practical formula: to evaluate a definite integral, find any antiderivative and subtract its values at the endpoints. This turns area calculations into algebra.

## Key Idea

**FTC Part 1** (differentiation of an integral with variable upper limit):

$$\frac{d}{dx}\int_a^x f(t)\,dt = f(x)$$

**FTC Part 2** (evaluation of definite integrals):

$$\int_a^b f(x)\,dx = F(b) - F(a)$$

where $F$ is any antiderivative of $f$, i.e., $F'(x) = f(x)$. The notation $\Big[F(x)\Big]_a^b$ means $F(b) - F(a)$.

## Worked Examples

**Example 1: Evaluate $\int_1^3(2x + 1)\,dx$**

Find an antiderivative of $2x + 1$. The antiderivative of $2x$ is $x^2$ (power rule in reverse), and the antiderivative of $1$ is $x$. So $F(x) = x^2 + x$.

Apply FTC Part 2 — evaluate $F$ at the upper limit, subtract $F$ at the lower limit:

$$F(3) - F(1) = (9 + 3) - (1 + 1) = 12 - 2 = 10$$

The definite integral equals 10. Note that the constant $C$ from the antiderivative cancels: $(F(b)+C)-(F(a)+C) = F(b)-F(a)$. This is why you don't need $+C$ for definite integrals.

---

**Example 2: Evaluate $\int_0^{\pi}\sin x\,dx$**

An antiderivative of $\sin x$ is $F(x) = -\cos x$ (since $\frac{d}{dx}[-\cos x] = \sin x$).

$$F(\pi) - F(0) = -\cos\pi - (-\cos 0) = -(-1) - (-1) = 1 + 1 = 2$$

Geometrically, this is the area of one arch of the sine curve, which lies entirely above the $x$-axis on $[0, \pi]$.

---

**Example 3: $\dfrac{d}{dx}\displaystyle\int_0^{x^2}\sin t\,dt$**

The upper limit is $x^2$, not $x$, so you need FTC Part 1 combined with the chain rule. By FTC Part 1, differentiating $\int_0^x \sin t\,dt$ gives $\sin x$. But the upper limit is $x^2$, so apply the chain rule: evaluate the integrand at $x^2$, then multiply by the derivative of $x^2$.

$$\frac{d}{dx}\int_0^{x^2}\sin t\,dt = \sin(x^2) \cdot \frac{d}{dx}[x^2] = \sin(x^2) \cdot 2x = 2x\sin(x^2)$$

## Common Mistakes

- **Forgetting to subtract $F(a)$.** The result is $F(b) - F(a)$, not just $F(b)$. The lower limit contributes a subtracted term — omitting it gives a completely wrong answer.
- **Not applying the chain rule in FTC Part 1 when the upper limit is a function of $x$.** If the limit is $g(x)$ rather than $x$, the derivative is $f(g(x)) \cdot g'(x)$.
- **Using the wrong antiderivative.** Any antiderivative works for Part 2 (the $+C$ cancels), but you must find a correct one. Verify by differentiating your $F$ before substituting.

## Quick Check

1. $\int_0^2 3x^2\,dx$
2. $\int_1^4 \sqrt{x}\,dx$
3. $\dfrac{d}{dx}\displaystyle\int_0^x e^t\,dt$

*(Answers: 8; $\dfrac{14}{3}$; $e^x$)*
