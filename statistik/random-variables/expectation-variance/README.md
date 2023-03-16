# Expectation and variance

For the die of the fifth sheet, with faces 1, 3, 3, 4, 4, 6:

| | modified die | fair die |
|---|---:|---:|
| expectation | 3.5 | 3.5 |
| variance | 2.25 | 2.917 |

Both published values are reproduced. The pair is the exercise: two dice with
the same expectation and different spread, and the expectation 3.5 is not a
face either die can show, which is the standard reminder that the expectation
is a balance point rather than a typical value.

## What the operations do

Expectation is linear, so `E(aX + b) = aE(X) + b` exactly. Variance is not:
`Var(aX + b) = a²Var(X)`, with the shift dropping out entirely because
variance measures spread and a shift moves everything together. Both are
checked by transforming the distribution and recomputing rather than by
applying the rule.

The shortcut `Var(X) = E(X²) - E(X)²` is checked against the definition. It
is the form used in every derivation and the form that loses precision in
floating point when the two terms are close, which is why the module keeps
the definition as the primary computation.
