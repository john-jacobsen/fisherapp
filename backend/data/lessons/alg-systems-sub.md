# Systems of Equations: Substitution

## Overview

A **system of equations** is two or more equations sharing the same variables. The **substitution method** solves the system by isolating one variable in one equation and replacing it in the other. This reduces two equations in two unknowns to one equation in one unknown — which you already know how to solve.

## Key Idea

The substitution strategy in three steps:

$$\text{1. Isolate} \to \text{2. Substitute} \to \text{3. Back-substitute}$$

Pick the equation where isolating a variable is simplest (no fractions, small coefficients). Substituting into the *other* equation is essential — substituting back into the same equation gives a tautology.

## Worked Examples

**Example 1: Solve $y = 2x - 1$ and $3x + y = 9$**

The first equation already isolates $y$, so substitute $2x - 1$ for $y$ in the second equation:

$$3x + (2x - 1) = 9 \implies 5x - 1 = 9 \implies 5x = 10 \implies x = 2$$

Now back-substitute into $y = 2x - 1$: $y = 2(2) - 1 = 3$.

Check: $3(2) + 3 = 9$ ✓. Solution: $(2, 3)$.

---

**Example 2: Solve $x + 2y = 8$ and $3x - y = 3$**

Neither variable is isolated. The easiest isolation: $x = 8 - 2y$ from the first equation. Substitute into the second:

$$3(8 - 2y) - y = 3 \implies 24 - 6y - y = 3 \implies -7y = -21 \implies y = 3$$

Back-substitute: $x = 8 - 2(3) = 2$.

Check: $2 + 2(3) = 8$ ✓ and $3(2) - 3 = 3$ ✓. Solution: $(2, 3)$.

---

**Example 3: Solve $2x + 3y = 12$ and $x - y = 1$**

Isolate $x$ from the second equation: $x = y + 1$. Substitute into the first:

$$2(y + 1) + 3y = 12 \implies 2y + 2 + 3y = 12 \implies 5y = 10 \implies y = 2$$

Back-substitute: $x = 2 + 1 = 3$. Solution: $(3, 2)$.

## Common Mistakes

- **Substituting into the same equation you isolated from.** If you solve equation 1 for $x$, substitute into equation 2, not equation 1 again. Substituting back into the same equation produces $0 = 0$ — true but useless.
- **Distributing incorrectly after substitution.** In Example 2, $3(8 - 2y) = 24 - 6y$, not $24 - 2y$. Write out the distribution step explicitly.
- **Forgetting to back-substitute.** You need both variables. After finding one, always substitute back to find the other.

## Quick Check

Try these before using hints:

1. Solve: $y = x + 1$, $2x + y = 7$
2. Solve: $x = 3y$, $x + y = 8$
3. Solve: $y = -x + 5$, $y = 2x - 1$

*(Answers: $(2, 3)$; $(6, 2)$; $(2, 3)$)*
