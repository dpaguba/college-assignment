# Gaussian process regression

The covariance function says how strongly two points bind each other: nearby
points almost completely, distant ones not at all. The length scale is the
measure of "nearby" and therefore the real assumption about the unknown
function.

## Two checks that catch an algebra error

With no noise, the posterior mean passes through every observation exactly and
the variance there is zero. Measured: the largest deviation of the mean is
1.2 × 10⁻¹⁰ and the largest variance at an observation is 1.0 × 10⁻¹⁰.

And an extra observation can never raise the variance anywhere. The largest
rise measured over 300 test points is −2.8 × 10⁻¹⁰, that is, a fall. A sign
error in the formula violates this immediately.

## The length scale is where the answer comes from

Seven observations, two length scales, the same points:

| length scale | total variation of the posterior mean |
|---:|---:|
| 0.15 | 6.85 |
| 3.0 | 3.73 |

Both curves pass through the same seven points. What stands between them does
not come from the data.

## What it costs

Solving the system grows with the cube of the number of observations, so a few
thousand points is the limit. For hyperparameter search that is no obstacle,
because every observation there is expensive and there are therefore never
many. That ratio is what makes the method the obvious choice in this one
place.
