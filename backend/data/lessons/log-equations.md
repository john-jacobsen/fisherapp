# Solving Logarithmic Equations

## Overview

A **logarithmic equation** contains the variable inside a logarithm. The main strategy is to isolate the log and convert to exponential form, or use log properties to combine logs before converting.

## Key Idea

Isolate the logarithm, then apply the definition $\log_b x = y \iff b^y = x$. Always **check for extraneous solutions**: the argument of any log must be positive.

## Worked Examples

**Example 1: $\log_3(x + 1) = 4$**

Convert: $x + 1 = 3^4 = 81$. Solution: $x = 80$. Check: $80 + 1 = 81 > 0$ ✓

---

**Example 2: $\log x + \log(x - 3) = 1$**

Combine: $\log[x(x-3)] = 1$, so $x(x-3) = 10$. Quadratic: $x^2 - 3x - 10 = 0 \Rightarrow (x-5)(x+2)=0$.

$x = 5$ (valid) or $x = -2$ (invalid, since $\log(-2)$ is undefined).

---

**Example 3: $2\ln x - \ln(x - 1) = \ln 4$**

$$\ln\frac{x^2}{x-1} = \ln 4 \Rightarrow x^2 = 4(x-1) \Rightarrow x^2 - 4x + 4 = 0 \Rightarrow x = 2$$

## Common Mistakes

- **Forgetting to check for extraneous solutions.** Squaring or multiplying can introduce invalid answers.
- **Applying $\log_b(M + N) = \log_b M + \log_b N$ (false rule).**

## Quick Check

1. $\log_2(x - 1) = 3$
2. $\log(x) + \log(x+9) = 1$
3. $\ln(2x) = \ln(x + 3)$

*(Answers: 9; $x=1$ (reject $x=-10$); $x=3$)*
