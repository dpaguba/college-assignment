# Data quality

Every repair loses something.

| repair | loses |
|---|---|
| drop incomplete rows | observations |
| drop incomplete columns | variables |
| impute the mean | variance |

The third is the one that looks free. Filling a missing value with the mean
leaves the mean unchanged and lowers the variance, so every confidence
interval computed afterwards is too narrow, and nothing in the data says that
happened.

The outlier rule is worth reading carefully as well. On `1, 2, 3, 4, 100` the
interquartile fence does **not** flag the 100, because with only two points
per half the quartiles are 1.5 and 52 and the fence reaches 128. The rule
needs enough data to describe the middle before it can say what is outside
it.
