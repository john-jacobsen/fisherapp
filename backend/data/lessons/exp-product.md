# Product Rule for Exponents

## Overview

The **product rule** tells you how to multiply two exponential expressions that share the same base: add the exponents. This is not an arbitrary shortcut — it comes directly from unpacking what exponents mean.

## Key Idea

$$a^m \cdot a^n = a^{m+n}$$

Why? By definition, $a^m$ is $a$ multiplied by itself $m$ times, and $a^n$ is $a$ multiplied by itself $n$ more times. When you write them side by side, you have $m + n$ copies of $a$ all being multiplied together — which is exactly $a^{m+n}$.

The base must be the same for this rule to apply. You cannot combine $a^2 \cdot b^3$ this way because the factors are different quantities.

## Worked Examples

**Example 1: $x^3 \cdot x^4$**

Write out what each power means to see why the rule works:

$$x^3 \cdot x^4 = \underbrace{x \cdot x \cdot x}_{3} \cdot \underbrace{x \cdot x \cdot x \cdot x}_{4} = \underbrace{x \cdot x \cdot x \cdot x \cdot x \cdot x \cdot x}_{7} = x^7$$

Adding exponents gives the same result: $x^{3+4} = x^7$. Once you trust the pattern, you never need to expand — just add.

---

**Example 2: $2^5 \cdot 2^3$**

The base is 2 in both terms, so the rule applies directly.

$$2^5 \cdot 2^3 = 2^{5+3} = 2^8$$

You can verify: $2^5 = 32$ and $2^3 = 8$, and $32 \times 8 = 256 = 2^8$. The rule gives the same result as multiplying the numbers directly, but much faster for large exponents.

---

**Example 3: $3x^2 \cdot 5x^4$**

When coefficients are present, handle them separately from the variable part. Coefficients multiply normally; the exponent rule applies only to the $x$ terms.

$$3x^2 \cdot 5x^4 = (3 \cdot 5) \cdot (x^2 \cdot x^4) = 15 \cdot x^{2+4} = 15x^6$$

The reason you can rearrange the factors is the commutative and associative properties of multiplication. Once you group like parts, each group follows its own rule.

## Common Mistakes

- **Multiplying the exponents instead of adding them.** $x^3 \cdot x^4 = x^7$, not $x^{12}$. Multiplying exponents is what happens in the power rule — a different situation entirely.
- **Applying the rule when the bases are different.** $x^3 \cdot y^4$ stays as $x^3 y^4$. You can only add exponents when the base is identical.
- **Forgetting to multiply the coefficients.** In $3x^2 \cdot 5x^4$, the coefficients 3 and 5 multiply to give 15. Only the variable exponents are added — the coefficients are separate.

## Quick Check

Try these before using hints:

1. $x^2 \cdot x^5$
2. $3^2 \cdot 3^4$
3. $4y^3 \cdot 2y$

*(Answers: $x^7$, $3^6 = 729$, $8y^4$)*
