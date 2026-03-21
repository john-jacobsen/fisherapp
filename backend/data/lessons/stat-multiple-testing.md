# Multiple Testing and Error Control

## Overview

When you perform $m$ hypothesis tests simultaneously, each with Type I error rate $\alpha$, the probability of at least one false positive across all tests — the **family-wise error rate (FWER)** — inflates above $\alpha$. The **Bonferroni correction** controls FWER by requiring each individual test to use a stricter threshold. For large $m$, a less conservative approach controls the **false discovery rate (FDR)** — the expected proportion of rejected tests that are actually false positives.

## Key Idea

The **Bonferroni correction** adjusts the per-test significance threshold by dividing $\alpha$ by the number of tests:

$$\alpha_{\text{adjusted}} = \frac{\alpha}{m}$$

Reject $H_{0,j}$ only if $p_j < \alpha/m$. This guarantees that $\text{FWER} \leq \alpha$ regardless of how many tests are true nulls. The **Benjamini-Hochberg (BH) procedure** controls the FDR instead: order the $m$ p-values as $p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(m)}$, find the largest $k$ such that $p_{(k)} \leq k\alpha/m$, and reject all $H_{0,(j)}$ for $j = 1, \ldots, k$.

## Worked Examples

**Example 1: FWER inflation and Bonferroni correction**

You run $m = 20$ independent tests at $\alpha = 0.05$. If all 20 null hypotheses are true, the probability of at least one false positive is:

$$\text{FWER} = 1 - P(\text{no false positives}) = 1 - (1 - 0.05)^{20} = 1 - (0.95)^{20} \approx 1 - 0.358 = 0.642$$

Without correction, you have a 64% chance of making at least one Type I error across your 20 tests — far higher than the intended 5%.

The Bonferroni correction sets the per-test threshold to $\alpha/m = 0.05/20 = 0.0025$. Now you only reject test $j$ if $p_j < 0.0025$. This is much more demanding: where before a p-value of 0.03 would lead to rejection, now it would not. The trade-off is reduced power — you require stronger evidence in each individual test to compensate for examining many tests simultaneously.

---

**Example 2: Benjamini-Hochberg procedure**

You run $m = 5$ tests and observe p-values: $\{0.008, 0.031, 0.042, 0.180, 0.620\}$. Sort them:

| $j$ | $p_{(j)}$ | BH threshold $j\alpha/m = j \cdot 0.05/5$ | $p_{(j)} \leq$ threshold? |
|-----|-----------|------------------------------------------|--------------------------|
| 1   | 0.008     | 0.010                                    | Yes                      |
| 2   | 0.031     | 0.020                                    | No                       |
| 3   | 0.042     | 0.030                                    | No                       |
| 4   | 0.180     | 0.040                                    | No                       |
| 5   | 0.620     | 0.050                                    | No                       |

The largest $j$ where $p_{(j)} \leq j\alpha/m$ is $j = 1$. So you reject only $H_{0,(1)}$ (the test with $p = 0.008$). If instead $p_{(2)} = 0.018$ (below threshold 0.020), you would reject both $H_{0,(1)}$ and $H_{0,(2)}$, and all lower-indexed tests, because BH rejects all tests up to the largest $k$ satisfying the condition.

---

**Example 3: FDR control vs FWER control in genomics**

In a genomics study, you might test $m = 10{,}000$ genes for association with a disease. The Bonferroni threshold would be $0.05/10{,}000 = 0.000005$. This is so stringent that true associations might fail to reach it — you miss real signals (high false negative rate).

The BH procedure controls the FDR at $\alpha = 0.05$: among all tests you declare significant, at most 5% are expected to be false positives on average. If 200 genes pass the BH threshold, you expect roughly 10 of them to be false discoveries — an acceptable rate for exploratory research where follow-up validation will weed out false positives. FDR control is less conservative than FWER control, which is appropriate here because the cost of missing a true signal (a gene worth studying) outweighs the cost of occasionally investigating a false positive.

## Common Mistakes

- **Applying Bonferroni to dependent tests.** The formula $1 - (1-\alpha)^m$ for FWER assumes independence. With positively correlated tests (common in genomics), the actual FWER is lower, making Bonferroni overly conservative. Methods like Holm's stepdown procedure are less conservative while still controlling FWER.
- **Confusing FWER and FDR.** FWER is the probability of any false positive. FDR is the expected proportion of rejections that are false positives. FWER control is stricter — FWER $\leq \alpha$ implies FDR $\leq \alpha$, but not vice versa.
- **Applying BH when tests are negatively correlated.** BH controls FDR under independence or positive dependence. Under arbitrary dependence, the BY (Benjamini-Yekutieli) procedure is needed, though it is more conservative.

## Quick Check

Try these before using hints:

1. You run $m = 10$ tests at $\alpha = 0.05$. What is the Bonferroni-adjusted threshold?
2. With $m = 4$ and $\alpha = 0.05$, what is the BH threshold for the 3rd-largest p-value?
3. With $m = 5$ independent tests all under $H_0$, what is the probability of at least one false positive at $\alpha = 0.05$ without correction?

*(Answers: 1. $0.05/10 = 0.005$; 2. $3 \times 0.05/4 = 0.0375$; 3. $1 - (0.95)^5 \approx 0.226$)*
