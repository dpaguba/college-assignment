# Linear regression

The published line for the children's data:

```
height = 103.5 + 3.5 · age
```

The slope is the covariance over the variance of the explanatory variable,
and the intercept places the line through the centre of the data, which is
why the line always passes through the point of the two means and why the
residuals always sum to zero.

## The line is not symmetric

Regressing height on age and age on height give different lines. The product
of their slopes is the squared correlation, which is 0.817 here, and it is 1
exactly when the points lie on a straight line. That identity is the reason
the two regressions coincide only in the degenerate case, and the reason
"correlation" and "regression" are different questions.

Least squares minimises the vertical distances, so it treats one variable as
explained and the other as given. The tests check that the fitted line beats
every other line through the same centre, which is the property that defines
it.

## Coefficient of determination

The share of the variance the line explains is exactly the squared
correlation, verified numerically. That equality holds only for a simple
linear regression with an intercept, which is the case the course covers, and
it is the reason the same number is quoted under two names.
