# Geometric Probability

## Overview

**Geometric probability** handles situations where outcomes are distributed continuously and uniformly over a region — a line segment, a square, a disk — rather than being a finite list of equally likely items. When outcomes are uniform over a region, no single point has positive probability, but a sub-region does. The probability of landing in a favorable region is simply the ratio of its measure (length, area, or volume) to the total measure. The geometry does the counting.

## Key Idea

When a point is chosen uniformly at random from a region $R$ with total area (or length, or volume) $|R|$, the probability of landing in a favorable sub-region $F \subseteq R$ is:

$$P(\text{event}) = \frac{\text{area of favorable region}}{\text{total area}} = \frac{|F|}{|R|}$$

This formula is the continuous analogue of the discrete formula $P(A) = |A|/|\Omega|$. In both cases, probability is proportional to the "size" of the favorable set relative to the whole.

## Worked Examples

**Example 1: Dart thrown uniformly at a square — probability it lands in an inner circle**

A dart is thrown uniformly at random at a $2 \times 2$ square (side length 2, so area 4). The square has an inscribed circle of radius 1 centered at the square's center. Find the probability the dart lands inside the circle.

The favorable region is the disk of radius 1, which has area $\pi r^2 = \pi(1)^2 = \pi$. The total region is the square with area 4. Because the dart is thrown uniformly, every unit of area is equally likely, so probability is the ratio:

$$P(\text{inside circle}) = \frac{\pi}{4} \approx 0.785$$

This is the geometry behind Monte Carlo estimation of $\pi$: if you throw many darts uniformly and record the fraction that land in the circle, that fraction estimates $\pi/4$, so multiplying by 4 gives an approximation of $\pi$.

---

**Example 2: Point chosen uniformly on $[0,1] \times [0,1]$ — probability that $x + y < 1$**

A point $(x, y)$ is chosen uniformly at random in the unit square $[0,1] \times [0,1]$, which has area 1. The event is $x + y < 1$, meaning the point falls below the line $y = 1 - x$.

The favorable region is the triangle with vertices $(0,0)$, $(1,0)$, and $(0,1)$. A triangle with base 1 and height 1 has area $\frac{1}{2}(1)(1) = \frac{1}{2}$. Since the total area is 1:

$$P(x + y < 1) = \frac{1/2}{1} = \frac{1}{2}$$

The key insight is that you converted a probability question into an area question. The condition $x + y < 1$ defines a geometric region; finding that region's area is all you need.

---

**Example 3: Bus arrives uniformly in $[0, 60]$ — probability you wait more than 20 minutes**

A bus arrives at a uniformly random time within a 60-minute window. You arrive at time 0. The bus arrival time $T$ is uniform on $[0, 60]$. You want $P(T > 20)$.

The total length of the interval is 60. The favorable region is $T \in (20, 60]$, which has length $60 - 20 = 40$. Since outcomes are uniform over length:

$$P(T > 20) = \frac{40}{60} = \frac{2}{3}$$

For a one-dimensional uniform distribution, area collapses to length. The ratio of lengths gives the probability directly — no integration required.

## Common Mistakes

- **Using a length ratio when an area ratio is needed.** If the problem is two-dimensional, you must compute areas. Measuring only one coordinate's range while ignoring the other gives the wrong answer.
- **Assigning positive probability to a single point.** In a continuous uniform distribution, the probability of any exact value is 0. $P(T = 20) = 0$ — what you can compute is the probability of an interval or region.
- **Forgetting to identify the total region correctly.** The denominator must be the total area of the sample space, not just the area of the favorable region. Always state both regions clearly before dividing.

## Quick Check

1. A point is chosen uniformly in the interval $[0, 10]$. Find $P(3 \leq X \leq 7)$.
2. A point $(x, y)$ is chosen uniformly in the unit square $[0,1] \times [0,1]$. Find $P(x < 0.5 \text{ and } y < 0.5)$.
3. A bus arrives uniformly in $[0, 30]$ minutes. You need to leave by minute 10. Find $P(\text{bus arrives before you leave})$.

*(Answers: $4/10 = 2/5$; $0.25$ (quarter of the unit square); $10/30 = 1/3$)*
