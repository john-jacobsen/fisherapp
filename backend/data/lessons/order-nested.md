# Nested Expressions

## Overview

A **nested expression** contains parentheses inside parentheses — or brackets containing parentheses. The rule is always the same: work from the **innermost grouping outward**. Each inner group must produce a single value before the outer group can use it.

## Key Idea

$$\bigl[\,(a + b) \cdot c\,\bigr] + d$$

Resolve the inner group $(a + b)$ first, producing a single number. Then use that number inside the brackets, and finally handle what is outside them. Each layer peels away from the inside out.

Different bracket styles — $(\,)$, $[\,]$, $\{\,\}$ — are used to make nesting visually clear. Mathematically they all mean the same thing: evaluate the contents before using the result elsewhere.

## Worked Examples

**Example 1: $2 \times [3 + (4 - 1)]$**

The innermost group is $(4 - 1)$. It must become a single value before the bracket $[3 + \ldots]$ can be evaluated.

- **Innermost:** $4 - 1 = 3$. The expression is now $2 \times [3 + 3]$.
- **Brackets:** $3 + 3 = 6$. The expression is now $2 \times 6$.
- **Multiply:** $2 \times 6 = 12$.

If you had tried to evaluate left to right without respecting nesting, you would get the wrong answer. The brackets force you to settle the inner sum first.

---

**Example 2: $\{[(2 + 3) \times 2] - 4\} \div 2$**

Three layers of grouping. Identify the innermost — $(2 + 3)$ — and work outward one layer at a time.

- **Layer 1 (innermost parentheses):** $2 + 3 = 5$. Now: $\{[5 \times 2] - 4\} \div 2$.
- **Layer 2 (square brackets):** $5 \times 2 = 10$. Now: $\{10 - 4\} \div 2$.
- **Layer 3 (curly braces):** $10 - 4 = 6$. Now: $6 \div 2$.
- **Final:** $6 \div 2 = 3$.

Each layer collapses to a single number before the next layer is touched. That is the entire strategy.

---

**Example 3: $4 + 2 \times [5 - (1 + 2)]$**

Here both order-of-operations rules and nesting apply. After resolving all groupings, you still must respect PEMDAS for the remaining expression.

- **Innermost:** $1 + 2 = 3$. Now: $4 + 2 \times [5 - 3]$.
- **Brackets:** $5 - 3 = 2$. Now: $4 + 2 \times 2$.
- **Multiplication before addition (PEMDAS):** $2 \times 2 = 4$. Now: $4 + 4$.
- **Final:** $4 + 4 = 8$.

Note that once all brackets are gone, you are back to standard PEMDAS — multiplication happens before addition.

## Common Mistakes

- **Starting with the outermost grouping.** The outer group depends on the inner group's result, so you cannot evaluate it first. Always find the deepest nesting level and start there.
- **Losing track of which closing bracket matches which opening bracket.** Every opener has exactly one closer. When expressions get long, mark matched pairs or work through one layer at a time, rewriting after each step.
- **Forgetting PEMDAS after all brackets are gone.** Resolving nesting does not mean the rest of the expression is evaluated left to right — normal order-of-operations rules still apply to whatever remains.

## Quick Check

Try these before using hints:

1. $3 \times [2 + (5 - 3)]$
2. $[(4 + 2) \times 3] - 8$
3. $10 - [2 \times (3 + 1)]$

*(Answers: $12$, $10$, $2$)*
