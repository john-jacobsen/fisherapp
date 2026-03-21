# Common Denominators

## Overview

A **common denominator** is a shared multiple of two or more denominators. You need one before you can add or subtract fractions with different denominators, because you can only combine pieces that are the same size. The **least common denominator** (LCD) is the smallest such shared multiple, which keeps the numbers as manageable as possible.

## Key Idea

To find the LCD of $\frac{a}{b}$ and $\frac{c}{d}$, compute LCM$(b, d)$. Then rewrite each fraction with that denominator by multiplying numerator and denominator by the same factor:

$$\frac{a}{b} = \frac{a \cdot (\text{LCD} \div b)}{\text{LCD}}$$

Multiplying top and bottom by the same number is the same as multiplying by 1, so the value of the fraction does not change — only its appearance does.

## Worked Examples

**Example 1: Find the LCD of $\frac{1}{4}$ and $\frac{1}{6}$, then rewrite both fractions**

List multiples of each denominator until you find the first overlap. Multiples of 4: 4, 8, **12**, 16, ... Multiples of 6: 6, **12**, 18, ... The first number on both lists is 12, so LCD = 12.

To convert $\frac{1}{4}$: you need to multiply the denominator by 3 to reach 12, so multiply the numerator by 3 as well. To convert $\frac{1}{6}$: multiply both parts by 2.

$$\frac{1}{4} = \frac{1 \cdot 3}{4 \cdot 3} = \frac{3}{12}, \quad \frac{1}{6} = \frac{1 \cdot 2}{6 \cdot 2} = \frac{2}{12}$$

---

**Example 2: Rewrite $\frac{2}{3}$ and $\frac{3}{4}$ with a common denominator**

LCM(3, 4) = 12, because 3 and 4 share no common factors, so their LCM is simply $3 \times 4 = 12$.

Multiply $\frac{2}{3}$ by $\frac{4}{4}$ (since $12 \div 3 = 4$), and $\frac{3}{4}$ by $\frac{3}{3}$ (since $12 \div 4 = 3$):

$$\frac{2}{3} = \frac{8}{12}, \quad \frac{3}{4} = \frac{9}{12}$$

Both fractions now use twelfths and can be compared or combined directly.

---

**Example 3: Find the LCD of $\frac{5}{6}$ and $\frac{7}{9}$**

6 and 9 share a common factor of 3, so their LCM is smaller than their product. LCM(6, 9) = 18 (since $6 = 2 \cdot 3$ and $9 = 3^2$, the LCM is $2 \cdot 3^2 = 18$).

Multiply $\frac{5}{6}$ by $\frac{3}{3}$, and $\frac{7}{9}$ by $\frac{2}{2}$:

$$\frac{5}{6} = \frac{15}{18}, \quad \frac{7}{9} = \frac{14}{18}$$

## Common Mistakes

- **Using the product $b \cdot d$ instead of the LCM.** This always produces a valid common denominator, but not always the smallest one. Larger denominators mean more simplification work at the end.
- **Multiplying only the denominator, not the numerator.** You must multiply both parts by the same factor. Changing just the denominator changes the fraction's value.
- **Confusing LCM with GCF.** The GCF is used to simplify fractions; the LCM is used to find common denominators. They serve opposite purposes.

## Quick Check

Try these before using hints:

1. What is the LCD of $\frac{1}{3}$ and $\frac{1}{4}$?
2. Rewrite $\frac{2}{5}$ with denominator 20.
3. What is the LCD of $\frac{3}{8}$ and $\frac{5}{12}$?

*(Answers: 12, $\frac{8}{20}$, 24)*
