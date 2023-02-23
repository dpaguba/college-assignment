# Association measures

The chi-square statistic adds the squared deviations from independence,
weighted by what independence predicted. For the pizza data:

| | |
|---|---|
| chi-square, exact | 33.1924 |
| chi-square, as published | 33.191 |
| corrected Pearson coefficient | 0.3653 exact, 0.366 as published |

The statistic grows with the sample size, so it cannot be compared across
studies: doubling every count doubles it while the association is unchanged.
The coefficients derived from it are attempts to remove that dependence.
Pearson's C is bounded but its maximum depends on the shape of the table, the
corrected version divides that maximum out, and Cramer's V does the same job
by a different route.

## Two formulas, one statistic

The third sheet asks for a proof that the definition equals a shortcut form
that sums squared counts over expected counts and subtracts the sample size.
Both are implemented and agree to twelve decimals on every table tested,
which is the computational half of the proof: the algebra is checked, not
merely asserted.

## Interpretation

0.366 on a scale from 0 to 1 is a weak association, which is what the
solution concludes. The number alone does not say whether it is meaningful,
and the test in [hypothesis-tests](../../inference/hypothesis-tests/) is what
turns it into a decision.
