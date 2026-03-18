# Continuity

## Overview

A function is **continuous at $a$** if its graph has no holes, jumps, or vertical asymptotes at $a$. Informally, you can draw it without lifting your pencil. Most functions you encounter in calculus are continuous on their domains.

## Key Idea

$f$ is continuous at $a$ if all three conditions hold:
1. $f(a)$ is defined.
2. $\lim_{x\to a} f(x)$ exists.
3. $\lim_{x\to a} f(x) = f(a)$.

## Worked Examples

**Example 1: Is $f(x) = x^2 + 1$ continuous at $x = 2$?**

$f(2) = 5$; $\lim_{x\to2}(x^2+1) = 5$. Both equal ✓ — continuous.

---

**Example 2: Is $g(x) = \frac{x^2-4}{x-2}$ continuous at $x = 2$?**

$g(2)$ is undefined (division by zero). Not continuous at 2. (Removable discontinuity.)

---

**Example 3: Intermediate Value Theorem**

$f(x) = x^3 - 2$ is continuous. $f(1) = -1 < 0$ and $f(2) = 6 > 0$, so by IVT there exists $c \in (1,2)$ with $f(c) = 0$.

## Common Mistakes

- **Assuming a limit existing means continuity.** You also need $f(a)$ defined and equal to the limit.
- **Confusing removable discontinuities (holes) with jump discontinuities.**

## Quick Check

1. Is $f(x) = |x|$ continuous at 0?
2. Where is $g(x) = \frac{1}{x-3}$ discontinuous?
3. $h(x) = 5$ for $x<1$ and $h(x) = x+4$ for $x\ge1$. Continuous at $x=1$?

*(Answers: yes; $x=3$; yes)*
