# Pooled Variance

## Overview

**Pooled variance** $S_p^2$ combines the sample variances from two groups into a single estimate of the common population variance, assuming both groups have the same $\sigma^2$.

## Key Idea

$$S_p^2 = \frac{(n_1-1)S_1^2 + (n_2-1)S_2^2}{n_1+n_2-2}$$

This is a weighted average of $S_1^2$ and $S_2^2$, with larger samples getting more weight. Used in the pooled two-sample $t$-test.

## Worked Examples

**Example 1: $S_1^2 = 9$, $n_1 = 5$; $S_2^2 = 16$, $n_2 = 9$.**

$S_p^2 = (4(9) + 8(16))/12 = (36 + 128)/12 = 164/12 \approx 13.67$.

---

**Example 2: Equal sample sizes simplify things**

If $n_1 = n_2$: $S_p^2 = (S_1^2 + S_2^2)/2$.

---

**Example 3: SE for two-sample $t$-test**

$\text{SE} = S_p\sqrt{1/n_1 + 1/n_2}$.

## Common Mistakes

- **Using $S_p^2 = (S_1^2 + S_2^2)/2$ when $n_1 \ne n_2$.** Always use the weighted formula.
- **Pooling when variances are clearly unequal** (use Levene's test first).

## Quick Check

1. $S_p^2$ for $S_1^2=4$, $n_1=3$, $S_2^2=8$, $n_2=3$?
2. When is $S_p^2$ closer to $S_1^2$ vs. $S_2^2$?
3. df for $S_p^2$?

*(Answers: 6; when $n_1 > n_2$ (or closer to whichever has larger $n$); $n_1+n_2-2$)*
