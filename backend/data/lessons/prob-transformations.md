# Transformations of Random Variables

## Overview

For a **monotone** function $g$, the change-of-variables formula gives the PDF of $Y = g(X)$ in one step — it is a shortcut that avoids the full CDF-then-differentiate procedure. The key ingredient is the Jacobian: the absolute value of the derivative of the inverse transformation, which accounts for how the transformation stretches or compresses the density. If $g$ is not monotone, split the domain into pieces where it is monotone and sum the contributions.

## Key Idea

If $Y = g(X)$ and $g$ is monotone and differentiable with inverse $x = g^{-1}(y)$:

$$f_Y(y) = f_X\!\left(g^{-1}(y)\right) \cdot \left|\frac{d}{dy} g^{-1}(y)\right|$$

The factor $\left|\frac{d}{dy} g^{-1}(y)\right|$ is the Jacobian. It corrects for the fact that a transformation that compresses the $x$-axis must proportionally inflate the density, and vice versa — otherwise the total probability would not remain 1.

## Worked Examples

**Example 1: $Y = 2X + 3$ where $X \sim N(0,1)$. Show $Y \sim N(3, 4)$.**

The inverse transformation is $g^{-1}(y) = (y - 3)/2$, and its derivative is $1/2$. Substitute into the formula — $f_X$ is the standard normal PDF $\phi$.

$$f_Y(y) = f_X\!\left(\frac{y-3}{2}\right) \cdot \left|\frac{1}{2}\right| = \frac{1}{\sqrt{2\pi}} e^{-\frac{(y-3)^2}{8}} \cdot \frac{1}{2}$$

This is exactly the $N(3, 4)$ PDF (variance $\sigma^2 = 4$, so $\sigma = 2$). The shift by 3 moves the center; the scale factor 2 stretches the distribution, which the Jacobian $1/2$ corrects for so that the density still integrates to 1.

---

**Example 2: $Y = -\ln U$ where $U \sim \text{Uniform}(0,1)$. Show $Y \sim \text{Exp}(1)$.**

Since $U \in (0,1)$, we have $-\ln U \in (0, \infty)$, so $Y > 0$. The inverse transformation is $g^{-1}(y) = e^{-y}$, and its derivative is $-e^{-y}$. Take the absolute value for the Jacobian.

$$f_Y(y) = f_U(e^{-y}) \cdot \left|-e^{-y}\right| = 1 \cdot e^{-y} = e^{-y}, \quad y > 0$$

This is exactly the $\text{Exp}(1)$ PDF. The $f_U(e^{-y}) = 1$ because the uniform density is 1 on $(0,1)$, and $e^{-y} \in (0,1)$ for all $y > 0$. This result is the foundation of the inverse CDF sampling method.

---

**Example 3: $Y = X^2$ where $X \sim \text{Uniform}(0, 2)$. Apply the formula.**

On $(0, 2)$, the function $g(x) = x^2$ is strictly increasing, so the formula applies directly. The inverse is $g^{-1}(y) = \sqrt{y}$ and its derivative is $\frac{1}{2\sqrt{y}}$. The range of $Y$ is $(0, 4)$.

$$f_Y(y) = f_X(\sqrt{y}) \cdot \frac{1}{2\sqrt{y}} = \frac{1}{2} \cdot \frac{1}{2\sqrt{y}} = \frac{1}{4\sqrt{y}}, \quad 0 < y < 4$$

The factor $f_X(\sqrt{y}) = 1/2$ is the uniform density on $(0, 2)$ evaluated at $\sqrt{y}$. The Jacobian $\frac{1}{2\sqrt{y}}$ compresses near $y = 0$ (where the squaring function is steep) and expands near $y = 4$, explaining why the transformed density blows up near zero.

## Common Mistakes

- **Forgetting the absolute value on the Jacobian.** When $g$ is decreasing, $dg^{-1}/dy$ is negative. Dropping the absolute value gives a negative density, which is impossible. Always take $\left|\frac{d}{dy} g^{-1}(y)\right|$.
- **Applying the formula to a non-monotone function.** If $g$ is not monotone on the support of $X$ — for example, $g(x) = x^2$ when $X \in (-1, 1)$ — you must split into regions where $g$ is monotone, apply the formula on each piece, and add the results.

## Quick Check

1. $X \sim \text{Exp}(1)$. Find the PDF of $Y = 3X$ using the change-of-variables formula.
2. $U \sim \text{Uniform}(0,1)$. Use the formula to show $Y = -\ln(1-U) \sim \text{Exp}(1)$.
3. Why must you take the absolute value of the Jacobian?

*(Answers: $f_Y(y) = \frac{1}{3}e^{-y/3}$, so $Y \sim \text{Exp}(1/3)$; $g^{-1}(y) = 1 - e^{-y}$, Jacobian $e^{-y}$, $f_U(1-e^{-y}) = 1$, so $f_Y(y) = e^{-y}$; PDFs must be non-negative — the absolute value ensures the density is positive regardless of whether $g$ is increasing or decreasing)*
