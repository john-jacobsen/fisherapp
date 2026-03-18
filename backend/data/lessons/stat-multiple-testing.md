# Multiple Testing Correction

## Overview

When conducting many hypothesis tests simultaneously, the probability of at least one false positive grows rapidly. **Multiple testing correction** controls either the family-wise error rate (FWER) or the false discovery rate (FDR).

## Key Idea

With $m$ tests, each at level $\alpha$, the probability of at least one false positive is up to $1 - (1-\alpha)^m$.

- **Bonferroni correction:** Use $\alpha^* = \alpha/m$ for each test. Controls FWER.
- **Benjamini-Hochberg (BH):** Controls FDR — less conservative, higher power.

## Worked Examples

**Example 1: 20 tests at $\alpha = 0.05$**

$P(\ge 1 \text{ false positive}) \le 1 - (0.95)^{20} \approx 0.64$.

Bonferroni: use $0.05/20 = 0.0025$ per test.

---

**Example 2: BH procedure**

Sort p-values: $p_{(1)} \le \cdots \le p_{(m)}$. Reject all $H_{(i)}$ where $p_{(i)} \le (i/m)\alpha$.

---

**Example 3: FWER vs. FDR**

FWER: control probability of any false positive. FDR: control expected proportion of false discoveries among rejections.

## Common Mistakes

- **Not correcting at all in genome-wide studies** — where $m = 10^6$, FWER correction is essential.
- **Over-correcting with Bonferroni when tests are correlated** — it's too conservative.

## Quick Check

1. Bonferroni-corrected $\alpha$ for 50 tests at overall level 0.05?
2. Which is less conservative: Bonferroni or BH?
3. FDR controls what?

*(Answers: 0.001; BH; expected proportion of false rejections among all rejections)*
