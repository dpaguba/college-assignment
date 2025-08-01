# Variance reduction

The same number of runs, a tighter answer, by removing variance the question
does not care about.

| | variance |
|---|---:|
| plain estimate | 0.0889 |
| antithetic pairs | 0.0056 |

A factor of sixteen on this integral, from pairing each draw with its mirror
image so that a high draw is balanced by a low one. The estimate is unchanged
at 0.333, which the module checks, because a technique that lowered the
variance and moved the answer would be worthless.

Common random numbers do the same for a comparison: running two variants on
the same draws removes the difference between the draws and leaves the
difference between the variants. A control variate subtracts a quantity whose
mean is known.

All three are exact rather than approximate. They change the estimator and
not the quantity, which is what separates them from simply running less.
