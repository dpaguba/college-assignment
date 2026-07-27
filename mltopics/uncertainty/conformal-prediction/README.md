# Prediction sets with a guarantee

Fit on one part, measure the errors on a second, and use their quantile as the
half-width. The quantile is not the one at 1 − α but the one at
`⌈(n+1)(1−α)⌉ / n`, and that correction is the whole difference between a rule
of thumb and a guarantee that holds for a finite sample.

Measured over 200 runs at α = 0.1: coverage **0.9016** against a promise of
0.9.

## The guarantee does not depend on the model

A model that ignores the slope entirely and always predicts the mean:

| | good model | bad model |
|---|---:|---:|
| coverage | 0.902 | **0.904** |
| mean width | 3.32 | **11.41** |

The coverage is identical; the width is three and a half times larger. Model
quality shows up in the width and never in the coverage, so a paper reporting
only coverage has said nothing about its model.

## The one condition

Calibration and test data have to be exchangeable. Shifting the target by 4
while leaving the model alone:

| | coverage |
|---|---:|
| without a shift | 0.902 |
| after the shift | **0.009** |

The intervals look exactly the same and the guarantee is gone. Note that the
shift has to change the distribution of the **residuals**: moving the inputs
along the fitted line changes nothing, because the errors stay the same.

## What is not promised

Coverage on average over all cases, not for each one. A method may
systematically miss the hard cases and overshoot the easy ones and still keep
the promise. Coverage for a subgroup has to be arranged separately.
