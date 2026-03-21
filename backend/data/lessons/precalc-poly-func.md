# Polynomial Functions

## Overview

A **polynomial function** has the form $p(x) = a_n x^n + a_{n-1}x^{n-1} + \cdots + a_1 x + a_0$, where $n$ is a non-negative integer and the coefficients $a_i$ are real numbers. The degree $n$ controls both the end behavior of the graph and the maximum number of real zeros and turning points.

## Key Idea

The leading term $a_n x^n$ determines end behavior:

$$\text{As } x \to \pm\infty, \quad p(x) \approx a_n x^n$$

A degree-$n$ polynomial has at most $n$ real zeros and at most $n-1$ turning points. The multiplicity of a zero tells you whether the graph crosses through the $x$-axis (odd multiplicity) or just touches and turns back (even multiplicity).

## Worked Examples

**Example 1: Describe end behavior of $f(x) = -2x^3 + x$**

The leading term is $-2x^3$. Since the degree is odd and the leading coefficient is negative:
- As $x \to +\infty$: $-2x^3 \to -\infty$, so $f(x) \to -\infty$
- As $x \to -\infty$: $-2x^3 \to +\infty$, so $f(x) \to +\infty$

The graph falls to the right and rises to the left — the reverse of a standard cubic with positive leading coefficient.

---

**Example 2: Analyze zeros of $p(x) = x(x - 2)^2(x + 3)$**

Set $p(x) = 0$. The factors give zeros at $x = 0$, $x = 2$, and $x = -3$.

- $x = 0$: multiplicity 1 (odd) — graph crosses the $x$-axis here.
- $x = 2$: multiplicity 2 (even) — graph touches the $x$-axis and turns back; it does not cross.
- $x = -3$: multiplicity 1 (odd) — graph crosses.

The degree is $1 + 2 + 1 = 4$, so there are at most 3 turning points.

---

**Example 3: Find all real zeros of $f(x) = x^3 - 4x$**

Factor out the GCF first: $x(x^2 - 4)$. Then factor the difference of squares: $x(x-2)(x+2)$.

Setting each factor equal to zero: $x = 0$, $x = 2$, $x = -2$.

All three zeros have multiplicity 1, so the graph crosses the $x$-axis at each. The function has degree 3 with positive leading coefficient, so it rises to the right and falls to the left.

## Common Mistakes

- **Assuming degree equals the number of real zeros.** A degree-$n$ polynomial has at most $n$ real zeros, but it may have fewer. For example, $f(x) = x^4 + 1$ has degree 4 but no real zeros — all four zeros are complex.
- **Misidentifying end behavior for even vs. odd degree.** Even-degree polynomials with positive leading coefficient go up on both ends ($U$-shape). Odd-degree with positive leading coefficient goes down left and up right. The leading coefficient's sign controls which way each end points.
- **Ignoring multiplicity when sketching.** At a zero of multiplicity 2, the graph is tangent to the $x$-axis (touches but does not cross). Treating it as a crossing gives an incorrect graph.

## Quick Check

Try these before using hints:

1. Describe the end behavior of $f(x) = 3x^4 - x$.
2. At most how many turning points can $p(x) = x^5 + 1$ have?
3. Find all real zeros of $q(x) = x^2(x+1)(x-1)$.

*(Answers: both ends rise to $+\infty$ (even degree, positive leading coefficient); 4; $x = 0$ (mult. 2), $x = -1$, $x = 1$)*
