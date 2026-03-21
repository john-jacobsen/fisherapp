# Exponential Form and Log Form

## Overview

Every logarithmic equation has an exactly equivalent **exponential form**, and every exponential equation has an exactly equivalent **log form**. These two forms express the same numerical relationship — they just organize the base, exponent, and result differently. Being able to switch between them instantly is one of the most useful skills in working with logarithms, because some problems are easier to see in one form than the other.

## Key Idea

The single equivalence that bridges both forms:

$$\log_b(x) = y \iff b^y = x$$

In log form, the base is written as a subscript and the exponent is the output. In exponential form, the base is the base of the power and the exponent is written explicitly. The three quantities — base ($b$), exponent ($y$), and result ($x$) — are the same in both; only the notation changes.

## Worked Examples

**Example 1: Convert $\log_4(64) = 3$ to exponential form**

Read off the three pieces: base $= 4$, exponent $= 3$, result $= 64$. In exponential form, the base is raised to the exponent and the result goes on the other side of the equals sign:

$$4^3 = 64$$

You can verify: $4^3 = 4 \times 4 \times 4 = 64$, so the statement is correct.

---

**Example 2: Convert $5^2 = 25$ to log form**

Now go the other direction. Read off: base $= 5$, exponent $= 2$, result $= 25$. In log form, the base becomes the subscript, the result becomes the argument of the log, and the exponent becomes the output:

$$\log_5(25) = 2$$

This says "the power of 5 that produces 25 is 2," which is exactly what $5^2 = 25$ says.

---

**Example 3: Solve $\log_x(27) = 3$**

This equation has an unknown base. Converting to exponential form makes the unknown appear in a position that is easier to solve:

$$x^3 = 27$$

Now take the cube root of both sides. Because $3^3 = 27$, you know the cube root of 27 is 3:

$$x = \sqrt[3]{27} = 3$$

Check by substituting back: $\log_3(27) = 3$ because $3^3 = 27$. Correct.

## Common Mistakes

- **Placing the base as the argument in log form.** Given $\log_4(64) = 3$, the exponential form is $4^3 = 64$, not $64^3 = 4$. The subscript is always the base of the power.
- **Mixing up the exponent and the result when converting.** There are three pieces. The exponent is what the log equals; the result is what is inside the log. Keep them straight by writing the equivalence $\log_b(x) = y \iff b^y = x$ and filling in each slot.
- **Forgetting that the base must be positive and not equal to 1.** $\log_1(x)$ and $\log_{-2}(x)$ are not valid logarithms.

## Quick Check

1. Write $\log_2(32) = 5$ in exponential form.
2. Write $3^4 = 81$ in log form.
3. Solve $\log_b(49) = 2$.

*(Answers: $2^5 = 32$; $\log_3(81) = 4$; $b = 7$)*
