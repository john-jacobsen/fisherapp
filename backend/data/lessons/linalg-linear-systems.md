# Linear Systems

## Overview

A **linear system** is a set of linear equations in the same unknowns. Solutions can be unique, infinitely many (underdetermined), or none (inconsistent). Row reduction is the systematic method for classifying and solving them.

## Key Idea

Write the system as an augmented matrix $[A | b]$, row-reduce to RREF, then read off solutions. A system is inconsistent if RREF has a row $[0 \cdots 0 | c]$ with $c \ne 0$.

## Worked Examples

**Example 1: Unique solution**

$x + y = 3$, $x - y = 1$. RREF gives $x = 2$, $y = 1$.

---

**Example 2: Infinite solutions**

$x + 2y = 4$, $2x + 4y = 8$. Second equation is twice the first — one free variable: $y = t$, $x = 4 - 2t$.

---

**Example 3: No solution (inconsistent)**

$x + y = 3$, $x + y = 5$. Contradiction — no solution.

## Common Mistakes

- **Stopping before full RREF.** Back-substitution is needed for non-RREF forms.
- **Missing free variables** when a column has no pivot.

## Quick Check

1. How many solutions can a linear system have?
2. What does a row $[0\ 0\ |\ 5]$ mean in an augmented matrix?
3. Identify: $x + y = 2$, $2x + 2y = 5$.

*(Answers: 0, 1, or infinitely many; no solution (inconsistent); inconsistent)*
