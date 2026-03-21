# Integration by Parts

## Overview

**Integration by parts** handles integrals of products where u-substitution doesn't apply — typically when two unrelated function types are multiplied together, such as a polynomial times an exponential or a logarithm times an algebraic term. The formula comes directly from integrating the product rule for derivatives.

## Key Idea

$$\int u\,dv = uv - \int v\,du$$

Choose $u$ and $dv$ so that the resulting $\int v\,du$ is simpler than the original. The **LIATE** priority guides which factor to assign as $u$: **L**ogarithm, **I**nverse trig, **A**lgebraic, **T**rigonometric, **E**xponential — choose the first type that appears as $u$. Whatever remains (together with $dx$) is $dv$.

## Worked Examples

**Example 1: $\int x e^x\,dx$**

Using LIATE: $x$ is Algebraic, $e^x$ is Exponential. Algebraic comes first, so $u = x$.

Assign: $u = x$, $dv = e^x\,dx$.

Compute: $du = dx$ (differentiate $u$), $v = e^x$ (integrate $dv$).

Apply the formula — $uv$ minus the new integral:

$$\int x e^x\,dx = x e^x - \int e^x\,dx = xe^x - e^x + C = e^x(x - 1) + C$$

The new integral $\int e^x\,dx$ was simpler than the original. That's the goal.

---

**Example 2: $\int x\ln x\,dx$**

Using LIATE: $\ln x$ is Logarithm, $x$ is Algebraic. Logarithm comes first, so $u = \ln x$.

Assign: $u = \ln x$, $dv = x\,dx$.

Compute: $du = \frac{1}{x}\,dx$ (differentiate $\ln x$), $v = \frac{x^2}{2}$ (integrate $x\,dx$).

Apply the formula:

$$\int x\ln x\,dx = \frac{x^2}{2}\ln x - \int\frac{x^2}{2} \cdot \frac{1}{x}\,dx = \frac{x^2}{2}\ln x - \int\frac{x}{2}\,dx$$

$$= \frac{x^2}{2}\ln x - \frac{x^2}{4} + C$$

The $1/x$ from differentiating $\ln x$ canceled one power of $x$ from $v$, making the remaining integral straightforward.

---

**Example 3: $\int e^x\sin x\,dx$**

Both factors are in the low-priority LIATE positions (Trig and Exponential), so either can be $u$. Choose $u = \sin x$, $dv = e^x\,dx$.

First application: $u = \sin x$, $du = \cos x\,dx$, $v = e^x$.

$$\int e^x\sin x\,dx = e^x\sin x - \int e^x\cos x\,dx$$

Apply by parts again to $\int e^x\cos x\,dx$ with $u = \cos x$, $du = -\sin x\,dx$, $v = e^x$:

$$= e^x\sin x - \left[e^x\cos x + \int e^x\sin x\,dx\right]$$

The original integral $I = \int e^x\sin x\,dx$ appears on both sides. Solve algebraically:

$$I = e^x\sin x - e^x\cos x - I \implies 2I = e^x(\sin x - \cos x) \implies I = \frac{e^x(\sin x - \cos x)}{2} + C$$

## Common Mistakes

- **Assigning $u$ and $dv$ in the wrong order.** If after applying the formula the new integral is harder than the original, switch the assignment.
- **Forgetting to subtract the entire $\int v\,du$, not just $v$.** The formula is $uv - \int v\,du$ — the subtraction applies to the whole integral, not just the integrand.
- **Changing the $u$-assignment mid-problem for Example 3 type integrals.** When applying by parts twice to get the original integral back, you must make consistent choices both times (same type as $u$). Switching breaks the algebra.

## Quick Check

1. $\int x\cos x\,dx$
2. $\int\ln x\,dx$
3. $\int x^2 e^x\,dx$

*(Answers: $x\sin x + \cos x + C$; $x\ln x - x + C$; $e^x(x^2 - 2x + 2) + C$)*
