# Nested Expressions

## Overview

A **nested expression** contains parentheses within parentheses (or brackets within brackets). You evaluate from the **innermost** grouping outward.

## Key Idea

Work from the inside out:

$$\bigl[\,(a + b) \cdot c\,\bigr] + d$$

Evaluate $(a + b)$ first, multiply by $c$, then add $d$.

## Worked Examples

**Example 1: $2 \times [3 + (4 - 1)]$**

Innermost: $4 - 1 = 3$. Brackets: $3 + 3 = 6$. Multiply: $2 \times 6 = 12$.

---

**Example 2: $\{[(2 + 3) \times 2] - 4\} \div 2$**

Step 1 (innermost): $2 + 3 = 5$. Step 2: $5 \times 2 = 10$. Step 3: $10 - 4 = 6$. Step 4: $6 \div 2 = 3$.

---

**Example 3: $4 + 2 \times [5 - (1 + 2)]$**

Innermost: $1 + 2 = 3$. Brackets: $5 - 3 = 2$. Multiply: $2 \times 2 = 4$. Add: $4 + 4 = 8$.

## Common Mistakes

- **Starting with the outer grouping.** Always work from the innermost group.
- **Losing track of which closing bracket matches which opening bracket.** Count carefully — every opener has exactly one closer.

## Quick Check

1. $3 \times [2 + (5 - 3)]$
2. $[(4 + 2) \times 3] - 8$
3. $10 - [2 \times (3 + 1)]$

*(Answers: 12, 10, 2)*
