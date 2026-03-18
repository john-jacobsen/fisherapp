# Poisson Process

## Overview

A **Poisson process** models a sequence of events occurring randomly in time (or space), with a constant average rate $\lambda$ and independent increments. It connects the Poisson, Exponential, and Gamma distributions.

## Key Idea

$N(t)$ = number of events in $[0,t]$, $N(t) \sim \text{Poisson}(\lambda t)$.

Inter-arrival times $T_1, T_2, \ldots \overset{iid}{\sim} \text{Exp}(\lambda)$.

Time to $n$-th event: $S_n = T_1 + \cdots + T_n \sim \text{Gamma}(n, \lambda)$.

## Worked Examples

**Example 1: Customers arrive at rate 3/hour. $P(\text{exactly 5 arrive in 2 hours})$?**

$\lambda t = 6$. $P(N=5) = e^{-6}6^5/5! \approx 0.161$.

---

**Example 2: Expected inter-arrival time?**

$E[T_i] = 1/3$ hour.

---

**Example 3: $P(\text{wait more than 1 hour for 1st customer})$?**

$P(T_1 > 1) = e^{-3} \approx 0.050$.

## Common Mistakes

- **Confusing the rate and the mean.** Rate $\lambda = 3$/hr means mean inter-arrival time $= 1/3$ hr.
- **Adding rates for two independent Poisson processes.** The merged process has rate $\lambda_1 + \lambda_2$.

## Quick Check

1. $N(t) \sim ?$ for Poisson process with rate $\lambda$?
2. Inter-arrival times follow what distribution?
3. Time to $k$-th event follows what distribution?

*(Answers: Poisson($\lambda t$); Exp($\lambda$); Gamma($k,\lambda$))*
