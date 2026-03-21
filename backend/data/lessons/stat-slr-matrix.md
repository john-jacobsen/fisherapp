# Simple Linear Regression: Matrix Form

## Overview

The **matrix form** of regression writes the entire model in compact notation: $\mathbf{Y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$. Here $\mathbf{X}$ is the **design matrix** — an $n \times 2$ matrix whose first column is all 1s (for the intercept) and whose second column contains the predictor values $x_1, \ldots, x_n$. Matrix form is not just a notational convenience: it generalizes immediately to any number of predictors and reveals the geometry of least squares.

## Key Idea

The OLS estimator in matrix form is the solution to the **normal equations** $\mathbf{X}^\top \mathbf{X} \hat{\boldsymbol{\beta}} = \mathbf{X}^\top \mathbf{Y}$, which gives:

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1} \mathbf{X}^\top \mathbf{Y}$$

This formula is valid whenever $\mathbf{X}^\top \mathbf{X}$ is invertible — equivalently, whenever no predictor is a perfect linear combination of the others.

## Worked Examples

**Example 1: Write out the design matrix and response vector**

Suppose you have $n = 3$ observations: $(x_1, y_1) = (1, 3)$, $(x_2, y_2) = (2, 5)$, $(x_3, y_3) = (3, 4)$. The first column of $\mathbf{X}$ is always all 1s (these multiply the intercept $\beta_0$); the second column holds the $x$ values:

$$\mathbf{X} = \begin{pmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{pmatrix}, \qquad \mathbf{Y} = \begin{pmatrix} 3 \\ 5 \\ 4 \end{pmatrix}$$

This setup encodes all three equations $y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$ simultaneously.

---

**Example 2: Compute $\mathbf{X}^\top \mathbf{X}$ and $\mathbf{X}^\top \mathbf{Y}$**

Using the matrices from Example 1:

$$\mathbf{X}^\top \mathbf{X} = \begin{pmatrix} 3 & 6 \\ 6 & 14 \end{pmatrix}, \qquad \mathbf{X}^\top \mathbf{Y} = \begin{pmatrix} 12 \\ 26 \end{pmatrix}$$

Why these values? $(\mathbf{X}^\top \mathbf{X})_{11} = \sum 1^2 = 3$ (sample size), $(\mathbf{X}^\top \mathbf{X})_{12} = \sum x_i = 6$, $(\mathbf{X}^\top \mathbf{X})_{22} = \sum x_i^2 = 1+4+9 = 14$. The vector $\mathbf{X}^\top \mathbf{Y}$ stacks $\sum y_i = 12$ and $\sum x_i y_i = 3+10+12 = 25$... wait: $1\cdot3+2\cdot5+3\cdot4=3+10+12=25$. So $\mathbf{X}^\top \mathbf{Y} = (12, 25)^\top$.

---

**Example 3: Show the matrix formula recovers the scalar estimates**

Inverting a $2 \times 2$ matrix $\begin{pmatrix} a & b \\ b & d \end{pmatrix}^{-1} = \frac{1}{ad-b^2}\begin{pmatrix} d & -b \\ -b & a \end{pmatrix}$. Here $ad - b^2 = 3 \cdot 14 - 36 = 6$, so:

$$(\mathbf{X}^\top \mathbf{X})^{-1} = \frac{1}{6}\begin{pmatrix} 14 & -6 \\ -6 & 3 \end{pmatrix}$$

Then $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{Y} = \frac{1}{6}\begin{pmatrix}14 \cdot 12 - 6 \cdot 25 \\ -6 \cdot 12 + 3 \cdot 25\end{pmatrix} = \frac{1}{6}\begin{pmatrix}18 \\ 3\end{pmatrix} = \begin{pmatrix}3 \\ 0.5\end{pmatrix}$.

So $\hat{\beta}_0 = 3$ and $\hat{\beta}_1 = 0.5$ — the same values you would get from the scalar formulas. The matrix approach is simply a systematic way to solve the same system of equations.

## Common Mistakes

- **Omitting the intercept column of 1s.** If you forget the column of 1s, the model is forced through the origin and $\hat{\boldsymbol{\beta}}$ estimates only the slope, not the intercept.

- **Assuming $\mathbf{X}^\top \mathbf{X}$ is always invertible.** If two predictors are perfectly correlated (e.g., $X_2 = 2X_1$), the columns of $\mathbf{X}$ are linearly dependent and $\mathbf{X}^\top \mathbf{X}$ is singular. OLS has no unique solution in this case.

## Quick Check

Try these before using hints:

1. For $n = 4$ observations with $x$ values $2, 4, 6, 8$, what is $\mathbf{X}^\top \mathbf{X}$?
2. What does the hat matrix $\mathbf{H} = \mathbf{X}(\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top$ do to $\mathbf{Y}$?
3. If the columns of $\mathbf{X}$ are linearly dependent, what goes wrong?

*(Answers: 1. $\begin{pmatrix}4 & 20 \\ 20 & 120\end{pmatrix}$; 2. $\mathbf{H}\mathbf{Y} = \hat{\mathbf{Y}}$ — it projects $\mathbf{Y}$ onto the column space of $\mathbf{X}$; 3. $\mathbf{X}^\top\mathbf{X}$ is singular and the OLS estimator does not exist)*
