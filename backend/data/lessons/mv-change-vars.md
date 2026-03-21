# Change of Variables (Jacobian)

## Overview

**Changing variables** in a double integral transforms a complicated region or integrand into a simpler one. Just as u-substitution in single-variable integration requires multiplying by $du/dx$, changing variables in a double integral requires multiplying by the **Jacobian** — a determinant that measures how much area is stretched or compressed by the transformation. Without it, the integral counts the wrong amount of area.

## Key Idea

For a transformation $x = x(u,v)$, $y = y(u,v)$, the **Jacobian** is:

$$J = \frac{\partial(x,y)}{\partial(u,v)} = \begin{vmatrix} \partial x/\partial u & \partial x/\partial v \\ \partial y/\partial u & \partial y/\partial v \end{vmatrix} = \frac{\partial x}{\partial u}\frac{\partial y}{\partial v} - \frac{\partial x}{\partial v}\frac{\partial y}{\partial u}$$

The change-of-variables formula is:

$$\iint_R f(x,y)\,dx\,dy = \iint_{R'} f(x(u,v),\, y(u,v))\,|J|\,du\,dv$$

The absolute value $|J|$ ensures you're multiplying by a positive area factor.

## Worked Examples

**Example 1: Polar coordinates $x = r\cos\theta$, $y = r\sin\theta$**

Compute the Jacobian. Differentiate $x$ and $y$ with respect to $r$ and $\theta$:

$$\frac{\partial x}{\partial r} = \cos\theta, \quad \frac{\partial x}{\partial \theta} = -r\sin\theta, \quad \frac{\partial y}{\partial r} = \sin\theta, \quad \frac{\partial y}{\partial \theta} = r\cos\theta$$

$$J = \begin{vmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix} = \cos\theta \cdot r\cos\theta - (-r\sin\theta)\cdot\sin\theta = r\cos^2\theta + r\sin^2\theta = r$$

So $dx\,dy = r\,dr\,d\theta$. The factor $r$ is the Jacobian — it accounts for the fact that polar "area elements" grow with radius.

---

**Example 2: Area of the disk $x^2 + y^2 \le 4$**

In Cartesian coordinates, computing this integral directly requires a square-root upper limit. In polar, the region becomes $0 \le r \le 2$, $0 \le \theta \le 2\pi$ — a rectangle in $(r,\theta)$ space.

$$\iint_{x^2+y^2\le 4} 1\,dx\,dy = \int_0^{2\pi}\int_0^2 r\,dr\,d\theta = \int_0^{2\pi}d\theta \cdot \int_0^2 r\,dr = 2\pi \cdot 2 = 4\pi$$

The Jacobian $r$ converts the flat polar measure into the correct area measure in Cartesian space.

---

**Example 3: $\iint_R (x^2 + y^2)\,dA$ over $x^2 + y^2 \le 9$**

In polar, $x^2 + y^2 = r^2$, so the integrand simplifies beautifully. The region is $0 \le r \le 3$, $0 \le \theta \le 2\pi$. Don't forget the Jacobian $r$.

$$\int_0^{2\pi}\int_0^3 r^2 \cdot r\,dr\,d\theta = \int_0^{2\pi}d\theta \cdot \int_0^3 r^3\,dr = 2\pi \cdot \left[\frac{r^4}{4}\right]_0^3 = 2\pi \cdot \frac{81}{4} = \frac{81\pi}{2}$$

## Common Mistakes

- **Forgetting the Jacobian $|J|$.** Omitting it is equivalent to computing the integral in the new coordinates as if area were preserved by the transformation — which it is not in general.
- **Not transforming the region.** Both the integrand and the limits of integration must be expressed in the new variables. Partial transformation produces integrals that mix coordinate systems.
- **Using the wrong sign for the Jacobian.** The formula uses $|J|$, the absolute value. The determinant can come out negative depending on orientation, but area is always positive.

## Quick Check

1. What is the Jacobian for polar coordinates?
2. Write $\iint_{x^2+y^2\le 1} e^{x^2+y^2}\,dA$ in polar form.
3. Evaluate that integral.

*(Answers: $r$; $\int_0^{2\pi}\int_0^1 e^{r^2}\,r\,dr\,d\theta$; $\pi(e - 1)$)*
