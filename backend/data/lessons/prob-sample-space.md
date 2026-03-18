# Sample Spaces

## Overview

A **sample space** $\Omega$ is the set of all possible outcomes of a random experiment. An **event** is any subset of $\Omega$. Probability theory is built on this foundation.

## Key Idea

Every probability problem starts with defining $\Omega$. Outcomes must be **mutually exclusive** and **exhaustive** — no outcome is repeated and together they cover all possibilities.

## Worked Examples

**Example 1: Flip a coin once**

$\Omega = \{H, T\}$. Event "heads" = $\{H\}$.

---

**Example 2: Roll a die**

$\Omega = \{1, 2, 3, 4, 5, 6\}$. Event "even" = $\{2, 4, 6\}$.

---

**Example 3: Flip two coins**

$\Omega = \{HH, HT, TH, TT\}$. Event "at least one head" = $\{HH, HT, TH\}$.

## Common Mistakes

- **Missing outcomes.** For two dice, $\Omega$ has 36 elements, not 11.
- **Treating ordered and unordered outcomes interchangeably.** $(H,T)$ and $(T,H)$ are different outcomes.

## Quick Check

1. $|\Omega|$ for rolling two dice?
2. Sample space for drawing one card from {A, K, Q}?
3. Event "sum > 10" when rolling two dice: how many outcomes?

*(Answers: 36; {A,K,Q}; 6: (5,6),(6,5),(6,6),(4,… wait — (5,6),(6,5),(4,… let me recalculate: (5,6),(6,5),(6,6) if sum>11, or (3,…) — sums >10: 11,12 → (5,6),(6,5),(6,6) plus (4,… no. Sum=11: (5,6),(6,5). Sum=12: (6,6). Sum=10: excluded. So 3 outcomes)*
