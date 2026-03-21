# Variance and Standard Deviation

## Overview

**Variance** $\text{Var}(X)$ measures how spread out a distribution is around its mean. A small variance means most outcomes cluster tightly near $E[X]$; a large variance means outcomes are scattered widely. The **standard deviation** $\text{SD}(X) = \sqrt{\text{Var}(X)}$ puts the spread back in the original units of $X$, making it easier to interpret. Variance and standard deviation are the two most fundamental measures of spread in probability.

## Key Idea

The variance is defined as the expected squared deviation from the mean:

$$\text{Var}(X) = E\!\left[(X - \mu)^2\right]$$

The computational shortcut — almost always easier to use — is:

$$\text{Var}(X) = E[X^2] - (E[X])^2$$

Under linear transformations, constants shift but do not stretch; scaling multiplies variance by the square of the scale factor:

$$\text{Var}(aX + b) = a^2 \,\text{Var}(X)$$

Note that adding a constant $b$ has no effect on variance — it shifts the distribution without changing its spread.

## Worked Examples

**Example 1: Variance of a two-value random variable**

Let $X$ take value 1 with probability 0.6 and value 4 with probability 0.4. First find the mean:

$$E[X] = 1(0.6) + 4(0.4) = 0.6 + 1.6 = 2.2$$

Now apply the definition directly — compute the squared deviation at each value, weighted by its probability:

$$\text{Var}(X) = (1 - 2.2)^2 (0.6) + (4 - 2.2)^2 (0.4) = (-1.2)^2(0.6) + (1.8)^2(0.4) = 1.44(0.6) + 3.24(0.4)$$

$$= 0.864 + 1.296 = 2.16$$

Each term measures how far that outcome is from the mean, squares it to make it positive, and weights it by how often it occurs.

---

**Example 2: Using the shortcut formula $E[X^2] - \mu^2$**

Use the same $X$ from Example 1 with $\mu = 2.2$. Instead of computing deviations, compute $E[X^2]$ first:

$$E[X^2] = 1^2(0.6) + 4^2(0.4) = 0.6 + 6.4 = 7.0$$

Now subtract the square of the mean:

$$\text{Var}(X) = E[X^2] - \mu^2 = 7.0 - (2.2)^2 = 7.0 - 4.84 = 2.16$$

The result matches. The shortcut works because $E[(X-\mu)^2] = E[X^2 - 2\mu X + \mu^2] = E[X^2] - 2\mu^2 + \mu^2 = E[X^2] - \mu^2$. Use this form whenever $E[X^2]$ is easy to compute.

---

**Example 3: Applying the scaling rule for $\text{Var}(3X + 1)$**

Given $\text{Var}(X) = 2.16$ from above, find $\text{Var}(3X + 1)$.

The additive constant $+1$ does not affect spread — shifting every outcome by the same amount does not change how far apart they are. The factor of 3, however, stretches all deviations by 3, which stretches squared deviations by $3^2 = 9$:

$$\text{Var}(3X + 1) = 3^2 \cdot \text{Var}(X) = 9 \cdot 2.16 = 19.44$$

The standard deviation of $3X + 1$ is $\sqrt{19.44} \approx 4.41$, which is exactly $3 \times \sqrt{2.16} \approx 3 \times 1.47$.

## Common Mistakes

- **Applying the scaling rule to standard deviation incorrectly.** $\text{SD}(aX) = |a|\,\text{SD}(X)$, not $a^2 \,\text{SD}(X)$. The $a^2$ rule applies to variance; take the square root for standard deviation.
- **Forgetting that $\text{Var}(X + Y) \neq \text{Var}(X) + \text{Var}(Y)$ in general.** This identity holds only when $X$ and $Y$ are independent. For dependent variables, a covariance term appears.
- **Confusing $E[X^2]$ with $(E[X])^2$.** These are almost never equal. $E[X^2]$ requires squaring each value first, then averaging; $(E[X])^2$ squares the average. The difference between them is exactly the variance.

## Quick Check

1. $X$ takes value 0 with probability 0.5 and value 6 with probability 0.5. Find $\text{Var}(X)$.
2. For the same $X$, verify using the shortcut $E[X^2] - (E[X])^2$.
3. If $\text{Var}(X) = 4$, find $\text{Var}(2X - 5)$.

*(Answers: $\mu = 3$; $(0-3)^2(0.5)+(6-3)^2(0.5) = 9$; $E[X^2]=18$, $18-9=9$ ✓; $4 \cdot 4 = 16$)*
