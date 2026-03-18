# Paired t-Test

## Overview

The **paired $t$-test** compares means when each observation in group 1 is naturally matched to one in group 2 (e.g., before/after, twin pairs). It reduces variability by analyzing differences $D_i = X_{i1} - X_{i2}$.

## Key Idea

Compute $D_i = X_{i1} - X_{i2}$. Then apply a one-sample $t$-test to $\{D_i\}$:

$$T = \frac{\bar{D} - 0}{S_D/\sqrt{n}} \sim t_{n-1}$$

## Worked Examples

**Example 1: Blood pressure before (B) and after (A) treatment.**

| Person | B | A | D |
|--------|---|---|---|
| 1 | 130 | 120 | 10 |
| 2 | 140 | 128 | 12 |
| 3 | 125 | 120 | 5 |

$\bar{D} = 9$, $S_D \approx 3.6$. $T = 9/(3.6/\sqrt{3}) = 4.33$. Reject $H_0$.

---

**Example 2: Why paired > two-sample?**

Pairing removes person-to-person variation, leaving only the treatment effect in $D_i$.

---

**Example 3: CI for mean difference**

$\bar{D} \pm t_{n-1,\alpha/2} \cdot S_D/\sqrt{n}$.

## Common Mistakes

- **Using two-sample $t$-test when data is paired.** This inflates variance and reduces power.
- **Wrong sample size.** $n$ is the number of pairs, not total observations.

## Quick Check

1. What are the "observations" in a paired $t$-test?
2. df for $n = 12$ pairs?
3. Why is paired usually more powerful than two-sample?

*(Answers: the differences $D_i$; 11; pairing removes nuisance variation)*
