# Geometric Probability

## Overview

**Geometric probability** assigns probabilities proportional to length, area, or volume. It is used when outcomes form a continuous set (like a point chosen uniformly at random in a region).

## Key Idea

$$P(\text{event}) = \frac{\text{measure of favorable region}}{\text{measure of total region}}$$

The "measure" is length (1D), area (2D), or volume (3D).

## Worked Examples

**Example 1: A point is chosen uniformly in $[0, 10]$. Probability it falls in $[3, 7]$?**

$$P = \frac{7-3}{10-0} = \frac{4}{10} = 0.4$$

---

**Example 2: A point is chosen uniformly in the unit square. Probability it is inside the quarter-circle $x^2+y^2 \le 1$?**

Area of quarter-circle: $\pi/4$. Area of square: 1. $P = \pi/4 \approx 0.785$.

---

**Example 3: Two buses arrive uniformly at random in an hour. Probability they arrive within 15 minutes of each other?**

Total area: $60^2$. Favorable: region $|x-y| \le 15$. $P = 1 - (45/60)^2 = 1 - 9/16 = 7/16$.

## Common Mistakes

- **Treating continuous outcomes as discrete.** A single point has probability 0 in a continuous distribution.
- **Computing ratio of lengths when areas are needed (2D problems).**

## Quick Check

1. Uniform on $[0,5]$. $P(X < 2)$?
2. Point in unit circle. $P(\text{in unit square around origin})$?
3. If $P = \pi/4$ approximates $\pi$, what experiment estimates $\pi$?

*(Answers: 2/5; $1/\pi$ (sq. area 4, circle area $\pi$); Monte Carlo dart throwing)*
