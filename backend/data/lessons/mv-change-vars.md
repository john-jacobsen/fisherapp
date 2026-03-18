# Change of Variables (Jacobian)

## Overview

**Changing variables** in a double (or triple) integral can simplify the region of integration or the integrand. The **Jacobian** is a scaling factor that accounts for how the transformation stretches or shrinks area.

## Key Idea

For a transformation $(x,y) = T(u,v)$, the Jacobian is:

$$J = \frac{\partial(x,y)}{\partial(u,v)} = \begin{vmatrix} \partial x/\partial u & \partial x/\partial v \\ \partial y/\partial u & \partial y/\partial v \end{vmatrix}$$

Then $\iint f(x,y)\,dx\,dy = \iint f(T(u,v))\,|J|\,du\,dv$.

## Worked Examples

**Example 1: Polar coordinates $x = r\cos\theta$, $y = r\sin\theta$**

$$J = \begin{vmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix} = r$$

So $dx\,dy = r\,dr\,d\theta$.

---

**Example 2: Area of disk $x^2+y^2 \le 4$**

In polar: $\int_0^{2\pi}\int_0^2 r\,dr\,d\theta = 2\pi \cdot 2 = 4\pi$.

---

**Example 3: $\iint_R (x^2+y^2)\,dA$ over $x^2+y^2 \le 9$**

$\int_0^{2\pi}\int_0^3 r^2 \cdot r\,dr\,d\theta = 2\pi \cdot \frac{81}{4} = \frac{81\pi}{2}$.

## Common Mistakes

- **Forgetting $|J|$ in the integral.** The Jacobian is not optional.
- **Not changing the region of integration.** Transform both the integrand and the limits.

## Quick Check

1. What is the Jacobian for polar coordinates?
2. Write $\iint e^{x^2+y^2}\,dA$ over $x^2+y^2 \le 1$ in polar form.
3. Evaluate that integral.

*(Answers: $r$; $\int_0^{2\pi}\int_0^1 e^{r^2} r\,dr\,d\theta$; $\pi(e-1)$)*
