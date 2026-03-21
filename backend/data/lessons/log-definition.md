# Definition of Logarithm

## Overview

A **logarithm** is the answer to the question "what exponent do I need?" Specifically, $\log_b(x)$ asks: to what power must the base $b$ be raised to produce $x$? Because exponentiation and logarithms undo each other, logs are the inverse operation of exponentials — just as subtraction undoes addition, $\log_b$ undoes $b^{\,\cdot\,}$.

## Key Idea

The definition of a logarithm establishes a two-way equivalence:

$$\log_b(x) = y \iff b^y = x \qquad (b > 0,\ b \ne 1,\ x > 0)$$

Every logarithmic statement can be rewritten as an exponential statement, and vice versa. The base, exponent, and result are the same three numbers in both forms — they just get rearranged.

Two special shorthand conventions: $\log$ without a base means $\log_{10}$ (common log), and $\ln$ means $\log_e$ (natural log, where $e \approx 2.718$).

## Worked Examples

**Example 1: Evaluate $\log_2(8)$**

The question is: what power of 2 equals 8? Think through the powers of 2: $2^1 = 2$, $2^2 = 4$, $2^3 = 8$. The answer is 3, because that is the exponent that makes the statement true.

You can confirm by writing it in exponential form:

$$\log_2(8) = 3 \iff 2^3 = 8 \checkmark$$

---

**Example 2: Evaluate $\log_3\!\left(\dfrac{1}{9}\right)$**

The question is: what power of 3 equals $\frac{1}{9}$? Negative exponents produce fractions, so think about $3^{-2} = \frac{1}{3^2} = \frac{1}{9}$. The exponent is $-2$.

$$\log_3\!\left(\frac{1}{9}\right) = -2 \iff 3^{-2} = \frac{1}{9} \checkmark$$

This shows that logarithms can be negative — a negative log means the argument is between 0 and 1.

---

**Example 3: Evaluate $\ln(e^5)$**

Recall that $\ln$ is $\log_e$, so the question is: what power of $e$ equals $e^5$? The answer is plainly 5, because $e^5$ is already written as a power of $e$.

$$\ln(e^5) = 5 \iff e^5 = e^5 \checkmark$$

This is a general pattern: $\ln(e^k) = k$ and $\log_b(b^k) = k$ for any base, because the log simply reads off the exponent.

## Common Mistakes

- **Believing $\log_b(0)$ is defined.** There is no exponent that turns a positive base into 0, so $\log_b(0)$ is undefined. Similarly, $\log_b(x)$ is undefined for $x < 0$ in the real numbers.
- **Swapping the base and the argument.** $\log_3(9) = 2$ because $3^2 = 9$ — the base is 3, not 9. Writing $\log_9(3) = 2$ is a different (and incorrect) statement for this situation.
- **Thinking a larger argument always means a larger log.** This is only true when comparing within the same base; the base matters.

## Quick Check

1. Evaluate $\log_2(16)$
2. Evaluate $\log_5(125)$
3. Evaluate $\log_{10}(0.01)$

*(Answers: 4, 3, −2)*
