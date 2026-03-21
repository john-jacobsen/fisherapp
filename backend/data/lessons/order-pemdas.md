# Order of Operations (PEMDAS)

## Overview

**PEMDAS** is the universal convention that makes mathematical expressions unambiguous. Without an agreed order, $2 + 3 \times 4$ could equal 14 or 20 depending on who reads it. PEMDAS eliminates that ambiguity so every reader reaches the same result.

## Key Idea

Evaluate in this priority order:

$$\textbf{P} \to \textbf{E} \to \textbf{M/D} \to \textbf{A/S}$$

1. **P**arentheses — resolve any grouped expression first
2. **E**xponents — evaluate all powers
3. **M**ultiplication and **D**ivision — left to right, equal priority
4. **A**ddition and **S**ubtraction — left to right, equal priority

The left-to-right rule at steps 3 and 4 is critical: M and D do not have a ranking between themselves, nor do A and S.

## Worked Examples

**Example 1: $2 + 3 \times 4$**

There are no parentheses or exponents, so you start at multiplication. The rule says multiply before you add — not because multiplication is "more important" in some abstract sense, but because that is the agreed convention.

$$2 + 3 \times 4 = 2 + 12 = 14$$

If you had added first you would get $5 \times 4 = 20$, which is wrong. The convention exists precisely to prevent this split.

---

**Example 2: $(5 + 3)^2 \div 4 - 1$**

Work through each layer in order. Parentheses create a self-contained value that must be resolved before anything outside them can proceed.

- **P:** $5 + 3 = 8$, so the expression becomes $8^2 \div 4 - 1$
- **E:** $8^2 = 64$, giving $64 \div 4 - 1$
- **M/D (left to right):** $64 \div 4 = 16$, giving $16 - 1$
- **A/S:** $16 - 1 = 15$

$$\boxed{15}$$

---

**Example 3: $3 \times 2^3 - 12 \div (4 - 2)$**

Two groupings compete here: a parenthesized expression and an exponent. P comes before E, so handle the parentheses first, even though the exponent appears earlier in the expression from left to right.

- **P:** $4 - 2 = 2$, giving $3 \times 2^3 - 12 \div 2$
- **E:** $2^3 = 8$, giving $3 \times 8 - 12 \div 2$
- **M/D (left to right):** $3 \times 8 = 24$ and $12 \div 2 = 6$, giving $24 - 6$
- **A/S:** $24 - 6 = 18$

$$\boxed{18}$$

## Common Mistakes

- **Treating M/D as strictly "multiplication before division."** They are equal priority — go left to right. $8 \div 2 \times 4 = (8 \div 2) \times 4 = 16$, not $8 \div (2 \times 4) = 1$.
- **Ignoring implicit grouping from fraction bars.** In $\dfrac{6 + 2}{4}$, the entire numerator $6 + 2$ is grouped; you must add before dividing. Writing it inline as $(6 + 2) \div 4$ makes this explicit.
- **Applying exponents before parentheses.** In $(3 + 1)^2$, you must add inside the parentheses first: $(3+1)^2 = 4^2 = 16$, not $3 + 1^2 = 4$.

## Quick Check

Try these before using hints:

1. $10 - 2 \times 3$
2. $(10 - 2) \times 3$
3. $2^3 + 4 \div 2$

*(Answers: $4$, $24$, $10$)*
