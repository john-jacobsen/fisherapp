# Systems of Equations: Elimination

## Overview

The **elimination method** (also called the addition method) solves a system by strategically adding equations together so that one variable cancels out. It works best when variables have coefficients that can be made equal and opposite with a single multiplication step.

## Key Idea

Multiply one or both equations by constants so that the coefficients of one variable are opposites, then add the equations:

$$\text{If } ca + db = e \text{ and } -ca + fb = g, \text{ then adding gives } (d+f)b = e+g$$

The key is making coefficients sum to zero for the variable you want to eliminate.

## Worked Examples

**Example 1: Solve $2x + 3y = 13$ and $2x - y = 5$**

Both equations have $+2x$. Subtract the second from the first to eliminate $x$ (subtracting $2x$ from $2x$ gives zero):

$$( 2x + 3y) - (2x - y) = 13 - 5 \implies 4y = 8 \implies y = 2$$

Back-substitute into $2x - y = 5$: $2x - 2 = 5 \implies x = 3.5$.

Check: $2(3.5) + 3(2) = 7 + 6 = 13$ ✓. Solution: $(3.5, 2)$.

---

**Example 2: Solve $3x + 4y = 10$ and $x + 2y = 4$**

The $y$ coefficients are 4 and 2. Multiply the second equation by 2 so both have $+4y$, then subtract:

$$\text{Eq 2} \times 2: \quad 2x + 4y = 8$$

$$( 3x + 4y) - (2x + 4y) = 10 - 8 \implies x = 2$$

Back-substitute: $2 + 2y = 4 \implies y = 1$. Solution: $(2, 1)$.

---

**Example 3: Solve $5x + 2y = 16$ and $3x - 4y = -4$**

The $y$ coefficients are 2 and $-4$. Multiply the first equation by 2 to get $+4y$, then add (since $+4y + (-4y) = 0$):

$$\text{Eq 1} \times 2: \quad 10x + 4y = 32$$

$$( 10x + 4y) + (3x - 4y) = 32 + (-4) \implies 13x = 28 \implies x = \frac{28}{13}$$

Back-substitute: $5\!\left(\tfrac{28}{13}\right) + 2y = 16 \implies 2y = 16 - \tfrac{140}{13} = \tfrac{68}{13} \implies y = \tfrac{34}{13}$.

## Common Mistakes

- **Adding when you should subtract (or vice versa).** If both equations have $+3y$, subtracting eliminates $y$. If they have $+3y$ and $-3y$, adding eliminates $y$. Check the signs before deciding.
- **Forgetting to multiply every term in the equation.** When you multiply equation 2 by 2, every term — including the right-hand side — must be multiplied. $x + 2y = 4$ becomes $2x + 4y = 8$, not $2x + 4y = 4$.
- **Arithmetic errors after adding.** Write the combined equation explicitly before simplifying.

## Quick Check

Try these before using hints:

1. Solve: $x + y = 5$, $x - y = 1$
2. Solve: $2x + y = 7$, $x + y = 5$
3. Solve: $3x + 2y = 11$, $x - 2y = 1$

*(Answers: $(3, 2)$; $(2, 3)$; $(3, 1)$)*
