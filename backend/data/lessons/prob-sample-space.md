# Sample Spaces and Events

## Overview

A **sample space** $\Omega$ is the set of every possible outcome of a random experiment. An **event** is any subset $A \subseteq \Omega$ — a collection of outcomes you care about. Before you can assign any probabilities, you must define $\Omega$ precisely, because every probability statement is really a statement about which outcomes fall inside a particular subset of $\Omega$. Getting $\Omega$ right is not a formality; if you omit outcomes or conflate distinct ones, every probability you compute afterward will be wrong.

## Key Idea

For a finite sample space with equally likely outcomes, the size $|\Omega|$ counts the total number of outcomes and the probability of an event is:

$$P(A) = \frac{|A|}{|\Omega|}$$

The empty set $\emptyset \subseteq \Omega$ is the **impossible event** — no outcome satisfies it. The full set $\Omega$ is the **certain event** — every outcome satisfies it. Every event you write down is just a set, which is why set notation and probability notation are interchangeable throughout this subject.

## Worked Examples

**Example 1: Rolling a six-sided die — list $\Omega$ and identify the event "even"**

You roll a fair six-sided die once. Every face is a distinct outcome, so:

$$\Omega = \{1,\, 2,\, 3,\, 4,\, 5,\, 6\}, \qquad |\Omega| = 6$$

Define $E$ = "the result is even." You scan $\Omega$ and collect the outcomes that satisfy the condition:

$$E = \{2, 4, 6\}, \qquad |E| = 3$$

$$P(E) = \frac{3}{6} = \frac{1}{2}$$

The key move was listing $\Omega$ first. You cannot define $E$ without knowing all possibilities to sift through. The formula works here because every face is equally likely — a fair die assigns probability $1/6$ to each outcome.

---

**Example 2: Flipping two coins — write $\Omega$ and the event "at least one head"**

You flip a fair coin twice. The flips are ordered (first flip, then second flip), so each outcome is an ordered pair. Listing systematically: first flip $H$ pairs with $H$ or $T$, first flip $T$ pairs with $H$ or $T$:

$$\Omega = \{HH,\, HT,\, TH,\, TT\}, \qquad |\Omega| = 4$$

Define $A$ = "at least one head." You include every outcome containing at least one $H$:

$$A = \{HH,\, HT,\, TH\}, \qquad |A| = 3, \qquad P(A) = \frac{3}{4}$$

Notice that $A^c$ = "no heads" = $\{TT\}$ contains only one outcome. Recognizing the complement is often easier than listing the event directly, because $P(A) = 1 - P(A^c) = 1 - 1/4 = 3/4$.

---

**Example 3: Drawing a card — describe $\Omega$ and the event "face card"**

A standard deck has 52 cards: 4 suits (clubs, diamonds, hearts, spades) each with 13 ranks (2–10, J, Q, K, A). Rather than listing all 52 cards, you describe $\Omega$ structurally:

$$\Omega = \{\text{suit} \times \text{rank}\}, \qquad |\Omega| = 4 \times 13 = 52$$

Define $F$ = "the card is a face card." Face cards are Jacks, Queens, and Kings — 3 ranks across all 4 suits:

$$|F| = 3 \times 4 = 12, \qquad P(F) = \frac{12}{52} = \frac{3}{13}$$

You did not need to enumerate all 52 cards explicitly. Describing $\Omega$ in structured terms (suits $\times$ ranks) made counting $|F|$ straightforward without listing.

## Common Mistakes

- **Applying $|A|/|\Omega|$ when outcomes are not equally likely.** The counting formula only works when every outcome has the same probability. If a biased coin lands heads with probability $0.7$, you cannot use $|A|/|\Omega|$ — you must weight each outcome by its individual probability.
- **Treating unordered and ordered outcomes as identical.** For two coin flips, writing $\Omega = \{HH, HT, TT\}$ misses the fact that $HT$ and $TH$ are distinct outcomes. Using this shrunken $\Omega$ makes $P(\text{exactly one head}) = 1/3$, which is wrong — the correct answer is $1/2$.
- **Confusing a single outcome with an event.** The outcome $HT$ is one element of $\Omega$. The event $\{HT\}$ is a set containing that element. The distinction matters as soon as you apply set operations like union or complement.

## Quick Check

1. List $\Omega$ for rolling two four-sided dice (faces 1–4) and state $|\Omega|$.
2. For the two-coin flip space $\Omega = \{HH, HT, TH, TT\}$, write the event $B$ = "exactly one tail."
3. A bag contains balls labeled 1 through 5. You draw one ball. Write the event $C$ = "the number is prime."

*(Answers: $\Omega = \{(i,j) : i,j \in \{1,2,3,4\}\}$, $|\Omega| = 16$; $B = \{HT, TH\}$; $C = \{2, 3, 5\}$)*
