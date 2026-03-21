# Solving Logarithmic Equations

## Overview

A **logarithmic equation** is an equation where the variable appears inside a logarithm. There are two main strategies: (1) isolate the log and convert directly to exponential form, or (2) use log rules to combine multiple logs into one before converting. After solving, you must always check that every log argument is positive.

## Key Idea

Logarithm and exponential are inverse operations. The definition $\log_b x = y \iff b^y = x$ lets you swap between forms freely:

$$\log_b x = y \quad\Longleftrightarrow\quad x = b^y$$

When two logs are set equal — $\log_b A = \log_b B$ — you can drop the log on both sides and conclude $A = B$. Always check for **extraneous solutions**: any value that makes a log argument zero or negative must be rejected.

## Worked Examples

**Example 1: Solve $\log_2(x) = 5$**

The log is already isolated. Convert directly: the equation says "2 raised to what power gives $x$? The answer is 5." Applying the definition:

$$x = 2^5 = 32$$

Check: $\log_2(32) = 5$ and $32 > 0$, so $x = 32$ is valid.

---

**Example 2: Solve $\log(x) + \log(x - 3) = 1$**

Two logs are added on the left. The product rule says $\log A + \log B = \log(AB)$, so you can compress them into one log:

$$\log\bigl[x(x-3)\bigr] = 1$$

Now convert using base 10 (since $\log$ without a base means $\log_{10}$):

$$x(x - 3) = 10^1 = 10$$

Expand and rearrange: $x^2 - 3x - 10 = 0$. Factor: $(x - 5)(x + 2) = 0$, giving $x = 5$ or $x = -2$.

Check both: if $x = -2$, then $\log(-2)$ is undefined — reject it. If $x = 5$: $\log(5) + \log(2) = \log(10) = 1$ ✓

The only solution is $x = 5$.

---

**Example 3: Solve $2\ln x - \ln(x - 1) = \ln 12$**

Rewrite the left side using log rules. The power rule converts $2\ln x = \ln x^2$, and the quotient rule converts subtraction to division:

$$\ln\frac{x^2}{x - 1} = \ln 12$$

Because the logs have the same base and are equal, the arguments must be equal:

$$\frac{x^2}{x - 1} = 12$$

Multiply both sides by $(x - 1)$: $x^2 = 12x - 12$, so $x^2 - 12x + 12 = 0$. Using the quadratic formula:

$$x = \frac{12 \pm \sqrt{144 - 48}}{2} = \frac{12 \pm \sqrt{96}}{2} = 6 \pm 2\sqrt{6}$$

Check: $6 - 2\sqrt{6} \approx 1.1 > 1$, so $x - 1 > 0$ ✓. Both solutions are positive, so both are valid.

## Common Mistakes

- **Forgetting to check for extraneous solutions.** Combining logs or squaring can introduce values that make an argument negative — always verify every candidate.
- **Applying a false product rule.** $\log(M + N) \neq \log M + \log N$. The product rule only works for multiplication inside the argument.
- **Dropping a log too early.** You can only cancel logs on both sides if both sides are a single log with the same base. Combine everything first.

## Quick Check

1. Solve $\log_3(x - 1) = 4$
2. Solve $\log(x) + \log(x + 9) = 1$
3. Solve $\ln(2x) = \ln(x + 5)$

*(Answers: $x = 82$; $x = 1$ (reject $x = -10$); $x = 5$)*
