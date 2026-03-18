# Indicator Random Variables

## Overview

An **indicator random variable** $I_A$ equals 1 if event $A$ occurs and 0 otherwise. Despite their simplicity, indicator variables are a powerful tool for computing expectations of complex quantities.

## Key Idea

$$I_A = \begin{cases}1 & \text{if } A \text{ occurs} \\ 0 & \text{otherwise}\end{cases}, \quad E[I_A] = P(A)$$

The key trick: many complicated random variables can be written as sums of indicator variables, and linearity of expectation applies term-by-term.

## Worked Examples

**Example 1: Number of heads in $n$ flips**

$X = I_1 + \cdots + I_n$. $E[X] = nP(H) = n/2$.

---

**Example 2: Expected number of matches when shuffling**

$X = \sum_{i=1}^n I_i$ where $I_i = 1$ if card $i$ is in position $i$. $E[I_i] = 1/n$. $E[X] = n \cdot (1/n) = 1$.

---

**Example 3: Expected number of pairs in a group of $n$ people with birthdays**

For each pair $(i,j)$, let $I_{ij} = 1$ if they share a birthday. $E[I_{ij}] = 1/365$.

Number of pairs = $\binom{n}{2}$. Expected matches = $\binom{n}{2}/365$.

## Common Mistakes

- **Using $E[I_A] = P(A)$ only when $I_A^2 = I_A$** (always true for indicators).
- **Assuming $I_A$ and $I_B$ are independent when $A$ and $B$ may not be.**

## Quick Check

1. $E[I_A]$ if $P(A) = 0.3$?
2. Roll three dice. Expected number showing a 6?
3. Is $I_A^2 = I_A$?

*(Answers: 0.3; 1/2; yes)*
