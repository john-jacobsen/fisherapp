# SLR in Matrix Form

## Overview

Writing **simple (and multiple) linear regression in matrix form** compactly represents the entire estimation problem and generalizes to any number of predictors.

## Key Idea

Model: $\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$, where $\mathbf{X}$ is the $n \times p$ design matrix (first column all 1s).

OLS estimate: $\hat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1}\mathbf{X}^T \mathbf{Y}$.

Hat matrix: $\mathbf{H} = \mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T$. Fitted values: $\hat{\mathbf{Y}} = \mathbf{H}\mathbf{Y}$.

## Worked Examples

**Example 1: Design matrix for SLR with $n=3$, $X=(1,2,3)$**

$$\mathbf{X} = \begin{pmatrix}1&1\\1&2\\1&3\end{pmatrix}$$

---

**Example 2: OLS formula derivation**

Minimize $\|\mathbf{Y} - \mathbf{X}\boldsymbol{\beta}\|^2$. Normal equations: $\mathbf{X}^T\mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{X}^T\mathbf{Y}$.

---

**Example 3: Hat matrix properties**

$\mathbf{H}$ is symmetric ($\mathbf{H}^T = \mathbf{H}$) and idempotent ($\mathbf{H}^2 = \mathbf{H}$). It's a projection matrix onto $\text{col}(\mathbf{X})$.

## Common Mistakes

- **Forgetting the intercept column of 1s** in $\mathbf{X}$.
- **Assuming $\mathbf{X}^T\mathbf{X}$ is always invertible.** Fails if predictors are perfectly collinear.

## Quick Check

1. OLS estimator formula in matrix form?
2. $\hat{\mathbf{Y}} = ?$ in matrix form?
3. What does the hat matrix project onto?

*(Answers: $(X^TX)^{-1}X^TY$; $HY$; column space of $X$)*
