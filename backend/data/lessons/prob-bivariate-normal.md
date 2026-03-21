# Bivariate Normal Distribution

## Overview

The **bivariate normal distribution** extends the normal distribution to two variables jointly. It is fully characterized by five parameters: the means $\mu_X$ and $\mu_Y$, the variances $\sigma_X^2$ and $\sigma_Y^2$, and the correlation $\rho \in (-1, 1)$. Its most important property is closure under conditioning and marginalization — every marginal and every conditional distribution derived from a bivariate normal is again normal.

## Key Idea

If $(X, Y)$ is bivariate normal, written $(X, Y) \sim N(\mu_X, \mu_Y, \sigma_X^2, \sigma_Y^2, \rho)$, then:

**Marginals:** $X \sim N(\mu_X, \sigma_X^2)$ and $Y \sim N(\mu_Y, \sigma_Y^2)$ independently of $\rho$.

**Conditional distribution of $Y$ given $X = x$:**

$$Y \mid X = x \;\sim\; N\!\left(\mu_Y + \rho\frac{\sigma_Y}{\sigma_X}(x - \mu_X),\;\; \sigma_Y^2(1 - \rho^2)\right)$$

The conditional mean is a linear function of $x$, and the conditional variance $\sigma_Y^2(1 - \rho^2)$ is smaller than the marginal variance whenever $\rho \neq 0$ — knowing $X$ reduces uncertainty about $Y$.

## Worked Examples

**Example 1: Identify the marginal distributions**

Suppose $(X, Y) \sim N(3, 7, 4, 9, 0.6)$ — that is, $\mu_X = 3$, $\mu_Y = 7$, $\sigma_X^2 = 4$, $\sigma_Y^2 = 9$, $\rho = 0.6$.

The marginal distributions follow directly from the parameters without any integration. Because the bivariate normal's joint PDF factors correctly to give normal marginals regardless of $\rho$:

$$X \sim N(3, 4), \qquad Y \sim N(7, 9)$$

The correlation $\rho = 0.6$ affects the joint structure and the conditionals, but it does not change the marginal means or variances. Each variable, viewed on its own, behaves as a univariate normal with its own mean and variance.

---

**Example 2: Find the conditional mean $E[Y \mid X = x]$**

Using the same parameters: $\mu_Y = 7$, $\rho = 0.6$, $\sigma_Y = 3$, $\sigma_X = 2$.

Substitute into the conditional mean formula. The term $\rho(\sigma_Y / \sigma_X)$ is the slope of the conditional mean as a function of $x$ — it quantifies how much the expected value of $Y$ shifts per unit increase in $X$:

$$E[Y \mid X = x] = 7 + 0.6 \cdot \frac{3}{2}(x - 3) = 7 + 0.9(x - 3)$$

At $x = 3$ (the mean of $X$), the conditional mean equals 7, the marginal mean of $Y$. At $x = 5$, $E[Y \mid X = 5] = 7 + 0.9(2) = 8.8$. Higher $X$ shifts the conditional distribution of $Y$ upward, as expected from a positive $\rho$.

The conditional variance is $\sigma_Y^2(1 - \rho^2) = 9(1 - 0.36) = 5.76$. Knowing $X$ reduces the variance of $Y$ from 9 to 5.76.

---

**Example 3: Zero correlation implies independence for bivariate normal**

In general, $\rho = 0$ (zero correlation) does not imply independence — two variables can be uncorrelated yet dependent. However, the bivariate normal is a special case: if $(X, Y)$ is bivariate normal and $\rho = 0$, then $X$ and $Y$ are independent.

When $\rho = 0$, the conditional distribution of $Y$ given $X = x$ becomes:

$$Y \mid X = x \sim N(\mu_Y + 0, \;\sigma_Y^2 \cdot 1) = N(\mu_Y,\, \sigma_Y^2)$$

The conditional distribution does not depend on $x$ at all — knowing $X$ tells you nothing about $Y$. This is exactly the definition of independence. The bivariate normal joint PDF also factors into the product of two independent normal PDFs when $\rho = 0$, confirming this result.

## Common Mistakes

- **Applying the bivariate normal's independence result to other distributions.** The equivalence of $\rho = 0$ and independence is specific to the bivariate normal. For any other joint distribution, you must verify independence separately — uncorrelatedness is not enough.
- **Confusing the marginal variance with the conditional variance.** The marginal variance of $Y$ is $\sigma_Y^2$. The conditional variance of $Y$ given $X = x$ is $\sigma_Y^2(1 - \rho^2)$, which is strictly smaller when $\rho \neq 0$.
- **Forgetting that $\rho$ must satisfy $|\rho| < 1$ for a valid bivariate normal.** At $|\rho| = 1$, the distribution degenerates to a line, and the joint PDF no longer exists.

## Quick Check

1. If $(X,Y) \sim N(0, 2, 1, 4, -0.5)$, what is the marginal distribution of $Y$?
2. For the same distribution, what is $E[Y \mid X = 1]$?
3. If $\rho = 0$ in a bivariate normal, are $X$ and $Y$ independent?

*(Answers: $N(2, 4)$; $E[Y \mid X=1] = 2 + (-0.5)(2/1)(1-0) = 2 - 1 = 1$; yes, for bivariate normal only)*
