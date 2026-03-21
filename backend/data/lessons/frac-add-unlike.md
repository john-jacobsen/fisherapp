# Adding Fractions (Unlike Denominators)

## Overview

Adding fractions with **different denominators** requires converting both fractions to use the same-size pieces before you can count them together. You cannot directly add $\frac{1}{3}$ and $\frac{1}{4}$ because thirds and fourths are different sizes — like trying to add inches to centimeters without converting first.

## Key Idea

Find the LCD of the two denominators, rewrite both fractions with that denominator, then add the numerators:

$$\frac{a}{b} + \frac{c}{d} = \frac{a \cdot ({\rm LCD}/b)}{\rm LCD} + \frac{c \cdot ({\rm LCD}/d)}{\rm LCD} = \frac{a \cdot ({\rm LCD}/b) + c \cdot ({\rm LCD}/d)}{\rm LCD}$$

Using the LCD (rather than the product $b \cdot d$) keeps the numbers smaller and reduces simplification at the end.

## Worked Examples

**Example 1: $\frac{1}{3} + \frac{1}{4}$**

Step 1 — Find the LCD. LCM(3, 4) = 12, because 3 and 4 share no factors, so the smallest shared multiple is $3 \times 4 = 12$.

Step 2 — Convert each fraction. To reach denominator 12: multiply $\frac{1}{3}$ by $\frac{4}{4}$ (since $12 \div 3 = 4$), and $\frac{1}{4}$ by $\frac{3}{3}$ (since $12 \div 4 = 3$). Multiplying top and bottom by the same number preserves the fraction's value.

Step 3 — Add the numerators, keep the denominator:

$$\frac{1}{3} + \frac{1}{4} = \frac{4}{12} + \frac{3}{12} = \frac{7}{12}$$

GCF(7, 12) = 1, so $\frac{7}{12}$ is fully simplified.

---

**Example 2: $\frac{2}{5} + \frac{3}{4}$**

Step 1 — LCM(5, 4) = 20, since 5 and 4 share no common factors.

Step 2 — Convert: $\frac{2}{5} \times \frac{4}{4} = \frac{8}{20}$ and $\frac{3}{4} \times \frac{5}{5} = \frac{15}{20}$. Each conversion multiplies both parts by the same factor, so the value is unchanged.

Step 3 — Add:

$$\frac{2}{5} + \frac{3}{4} = \frac{8}{20} + \frac{15}{20} = \frac{23}{20}$$

This is an improper fraction ($23 > 20$), which equals the mixed number $1\frac{3}{20}$.

---

**Example 3: $\frac{5}{6} + \frac{7}{9}$**

Step 1 — LCM(6, 9). Since $6 = 2 \cdot 3$ and $9 = 3^2$, LCM = $2 \cdot 3^2 = 18$.

Step 2 — Convert: $\frac{5}{6} \times \frac{3}{3} = \frac{15}{18}$ and $\frac{7}{9} \times \frac{2}{2} = \frac{14}{18}$.

Step 3 — Add:

$$\frac{5}{6} + \frac{7}{9} = \frac{15}{18} + \frac{14}{18} = \frac{29}{18}$$

GCF(29, 18) = 1, so the answer is already simplified.

## Common Mistakes

- **Adding numerators and denominators separately.** This is incorrect: $\frac{1}{2} + \frac{1}{3} \ne \frac{2}{5}$. You must convert to a common denominator first.
- **Forgetting to adjust the numerator when changing the denominator.** If you multiply the denominator by 4, you must also multiply the numerator by 4, or the fraction's value changes.
- **Skipping simplification.** After adding, check whether GCF of the result is greater than 1.

## Quick Check

Try these before using hints:

1. $\frac{1}{2} + \frac{1}{3}$
2. $\frac{3}{4} + \frac{1}{6}$
3. $\frac{2}{3} + \frac{3}{5}$

*(Answers: $\frac{5}{6}$, $\frac{11}{12}$, $\frac{19}{15}$)*
