# Logarithm Rules

## Overview

The **logarithm rules** — product, quotient, and power — let you expand a single log into a sum or difference of simpler logs, or condense a sum or difference back into a single log. They work because logarithms are exponents, and these rules mirror the exponent rules exactly: when you multiply powers you add exponents, so when you take the log of a product you add logs.

## Key Idea

The three fundamental rules (all with the same base $b$):

$$\log_b(MN) = \log_b M + \log_b N \qquad \text{(Product Rule)}$$

$$\log_b\!\left(\frac{M}{N}\right) = \log_b M - \log_b N \qquad \text{(Quotient Rule)}$$

$$\log_b(M^p) = p \cdot \log_b M \qquad \text{(Power Rule)}$$

**Change-of-base formula** (converts any log to natural log or common log):

$$\log_b(x) = \frac{\ln x}{\ln b}$$

## Worked Examples

**Example 1: Expand $\log_3(4 \cdot 5)$**

The argument is a product of two factors. The product rule says a log of a product equals a sum of logs — this works because multiplying the inputs of a log corresponds to adding in the exponent world.

Apply the product rule:

$$\log_3(4 \cdot 5) = \log_3(4) + \log_3(5)$$

The expression is now fully expanded. Each factor inside the original log becomes its own separate log term. Notice the base 3 stays the same throughout — you are splitting the argument, not the base.

---

**Example 2: Condense $\log_5(x^2) - \log_5(y)$**

This is the product rule in reverse: a difference of logs with the same base condenses into a log of a quotient. The first term, $\log_5(x^2)$, has a power in the argument — the power rule tells you that is equivalent to bringing the exponent in front, but here it is already inside, so leave it as $x^2$ in the argument.

Apply the quotient rule in the condensing direction:

$$\log_5(x^2) - \log_5(y) = \log_5\!\left(\frac{x^2}{y}\right)$$

The subtracted log becomes the denominator of the argument. The result is a single log expression.

---

**Example 3: Rewrite $\log_7(10)$ using the change-of-base formula**

Your calculator has buttons for $\ln$ and $\log_{10}$, but not for $\log_7$. The change-of-base formula lets you rewrite any log as a ratio of natural logs (or common logs), which you can then compute.

Apply the formula with $b = 7$ and $x = 10$:

$$\log_7(10) = \frac{\ln(10)}{\ln(7)}$$

Leave the answer in this form. The two $\ln$ values can be looked up, but the expression $\frac{\ln(10)}{\ln(7)}$ is the complete, exact rewritten form. This is what change-of-base produces.

## Common Mistakes

- **Treating $\log(M + N)$ as $\log M + \log N$.** There is no rule for the log of a sum. The product rule applies only to a log of a product: $\log(MN) = \log M + \log N$.
- **Moving a coefficient to the base instead of the exponent.** The power rule says $p \cdot \log_b M = \log_b(M^p)$ — the $p$ becomes an exponent on the argument, not a multiplier on the base. $2\log_3 x = \log_3(x^2)$, not $\log_6 x$.
- **Mixing bases when combining logs.** The product and quotient rules only apply when both logs share the exact same base. $\log_2(x) + \log_3(y)$ cannot be condensed.

## Quick Check

1. Expand $\ln(x^2 y)$
2. Condense $\log(4) + \log(3)$
3. Rewrite $\log_4(8)$ using the change-of-base formula (leave in $\frac{\ln(\cdot)}{\ln(\cdot)}$ form)

*(Answers: $2\ln x + \ln y$; $\log(12)$; $\dfrac{\ln(8)}{\ln(4)}$)*
