# Independence of Events

## Overview

Events $A$ and $B$ are **independent** when knowing that $B$ occurred gives you no information about whether $A$ occurred — the two events have no influence on each other. Independence is a precise mathematical condition, not just an intuitive sense that two things are unrelated. The formal test is the multiplication rule: $A$ and $B$ are independent if and only if $P(A \cap B) = P(A) \cdot P(B)$. This condition must be verified, not assumed.

## Key Idea

Events $A$ and $B$ are independent, written $A \perp B$, if and only if:

$$A \perp B \iff P(A \cap B) = P(A) \cdot P(B)$$

Equivalently (when $P(B) > 0$), independence means conditioning on $B$ does not change the probability of $A$:

$$P(A \mid B) = P(A)$$

For three **mutually independent** events $A$, $B$, $C$, all four conditions must hold simultaneously: the three pairwise products and the triple product:

$$P(A \cap B \cap C) = P(A) \cdot P(B) \cdot P(C)$$

## Worked Examples

**Example 1: Verify independence for two coin flips**

Flip a fair coin twice. Let $A$ = "first flip is heads" and $B$ = "second flip is heads." The sample space is $\{HH, HT, TH, TT\}$, each with probability $1/4$.

$P(A) = 2/4 = 1/2$ (outcomes $HH$ and $HT$). $P(B) = 2/4 = 1/2$ (outcomes $HH$ and $TH$). $P(A \cap B) = P(\{HH\}) = 1/4$.

Check the multiplication rule:

$$P(A) \cdot P(B) = \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4} = P(A \cap B) \checkmark$$

The product matches, so $A \perp B$. This confirms the physical intuition: what the first coin lands on cannot affect what the second coin does.

---

**Example 2: Show two events are NOT independent using the product rule**

Roll a fair six-sided die. Let $A$ = "result is even" $= \{2,4,6\}$ and $B$ = "result is 1 or 2" $= \{1,2\}$.

$P(A) = 3/6 = 1/2$. $P(B) = 2/6 = 1/3$. $P(A \cap B) = P(\{2\}) = 1/6$.

Check: $P(A) \cdot P(B) = (1/2)(1/3) = 1/6 = P(A \cap B)$.

These happen to be independent despite $B$ being a small set. Now try $B' = \{1, 2, 3\}$ (result is at most 3). $P(B') = 1/2$, $P(A \cap B') = P(\{2\}) = 1/6$. But $P(A) \cdot P(B') = (1/2)(1/2) = 1/4 \neq 1/6$. So $A$ and $B'$ are **not** independent — knowing the result is at most 3 changes the probability that it is even (only $\{2\}$ qualifies, not $\{4, 6\}$).

---

**Example 3: Extend to three mutually independent events**

Flip a fair coin three times. Let $A$ = "flip 1 is H", $B$ = "flip 2 is H", $C$ = "flip 3 is H." Each has probability $1/2$.

For mutual independence, all pairwise and triple conditions must hold. The triple intersection is the event $\{HHH\}$:

$$P(A \cap B \cap C) = \frac{1}{8} = \frac{1}{2} \cdot \frac{1}{2} \cdot \frac{1}{2} = P(A) \cdot P(B) \cdot P(C) \checkmark$$

All three pairwise products also equal $1/4$, which matches the pairwise joint probabilities. When events are mutually independent, you can compute the probability of any combination of them by multiplying individual probabilities — this is the powerful computational shortcut that independence provides.

## Common Mistakes

- **Confusing mutual exclusivity with independence.** If $P(A) > 0$ and $P(B) > 0$, then $A$ and $B$ cannot be both mutually exclusive and independent. Mutually exclusive events have $P(A \cap B) = 0$, but independence requires $P(A \cap B) = P(A) \cdot P(B) > 0$. They are opposite conditions.
- **Inferring mutual independence from pairwise independence.** Three events can be pairwise independent (every pair satisfies the product rule) without being mutually independent. Always check the triple product condition separately.
- **Assuming physical separation implies independence.** Two measurements from the same system may be statistically dependent even if they seem unrelated. Independence must be verified from the joint distribution, not assumed from context.

## Quick Check

1. $P(A) = 0.4$, $P(B) = 0.5$, $P(A \cap B) = 0.2$. Are $A$ and $B$ independent?
2. $A$ and $B$ are mutually exclusive with $P(A) = 0.3$ and $P(B) = 0.4$. Are they independent?
3. $A \perp B$ and $A \perp C$ and $B \perp C$. Does this guarantee $A \perp B \perp C$ (mutual independence)?

*(Answers: yes, $0.4 \times 0.5 = 0.20 = P(A \cap B)$; no, $P(A \cap B) = 0 \neq 0.12 = P(A)P(B)$; no, pairwise independence does not imply mutual independence)*
