# Function Notation and Evaluation

## Overview

A **function** is a rule that assigns exactly one output to each input. Function notation $f(x)$ is read "f of x" — it means the output of function $f$ when the input is $x$. This notation is not multiplication: $f(x) \ne f \times x$. The letter in the parentheses is the input, and evaluating the function means substituting that input everywhere the variable appears.

## Key Idea

To evaluate $f$ at input $a$, replace every occurrence of the variable with $a$:

$$f(x) = \text{rule} \implies f(a) = \text{same rule with } x \text{ replaced by } a$$

This holds even when $a$ is an expression like $a + 1$ or $2t$. Substitute the entire expression, then simplify.

## Worked Examples

**Example 1: $f(x) = 3x^2 - 2x + 1$. Find $f(2)$.**

Replace every $x$ with 2:

$$f(2) = 3(2)^2 - 2(2) + 1 = 3(4) - 4 + 1 = 12 - 4 + 1 = 9$$

Order of operations: evaluate the exponent first ($2^2 = 4$), then multiply ($3 \cdot 4 = 12$, $2 \cdot 2 = 4$), then combine.

---

**Example 2: $g(x) = \frac{x+1}{x-2}$. Find $g(5)$.**

Replace $x$ with 5 in both numerator and denominator:

$$g(5) = \frac{5 + 1}{5 - 2} = \frac{6}{3} = 2$$

Note that $g(2)$ would be undefined — the denominator $2 - 2 = 0$ makes the expression invalid. Recognizing these exclusions is part of understanding the function.

---

**Example 3: $h(x) = x^2 + 1$. Find $h(a + 1)$.**

Replace $x$ with the entire expression $(a + 1)$:

$$h(a+1) = (a+1)^2 + 1$$

Expand $(a+1)^2 = a^2 + 2a + 1$:

$$h(a+1) = a^2 + 2a + 1 + 1 = a^2 + 2a + 2$$

The parentheses around $a + 1$ are essential. If you write $a + 1^2$ instead of $(a+1)^2$, the squaring only applies to the 1.

## Common Mistakes

- **Interpreting $f(x)$ as multiplication.** $f(3)$ means evaluate $f$ at input 3, not $f$ multiplied by 3. Writing $f(x) = 2x$ does not mean $f \cdot x = 2x$.
- **Partial substitution.** If $f(x) = x^2 + 3x$ and you compute $f(a+1)$, you must replace both $x$'s. $f(a+1) = (a+1)^2 + 3(a+1)$, not $a+1^2 + 3x$.
- **Skipping parentheses around the substituted expression.** Substituting $a + 1$ into $x^2$ requires writing $(a+1)^2$. Without parentheses, the exponent only applies to 1.

## Quick Check

Try these before using hints:

1. $f(x) = 2x - 5$. Find $f(3)$.
2. $g(x) = x^2 - 1$. Find $g(-2)$.
3. $h(x) = 4x + 1$. Find $h(t + 2)$.

*(Answers: 1; 3; $4t + 9$)*
