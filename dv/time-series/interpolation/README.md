# Interpolation

Lagrange and Newton produce the same polynomial by different arithmetic, and
the module checks that they agree at every test point and that both agree
with `numpy.polyfit` on 50 random node sets. Newton's form is preferred in
practice because adding a node costs one more term instead of a recomputation.

## Runge

The function 1/(1 + 25x²) on [−1, 1] with 15 nodes:

| nodes | largest error |
|---|---|
| equidistant | 7.19 |
| Chebyshev | 0.047 |

A factor of 154. The equidistant polynomial does not merely fail to improve
with the degree, it gets worse, and it does so at the ends of the interval.
The Chebyshev nodes cluster there, which is exactly where the error wants to
grow, and the module checks that clustering directly by comparing the spacing
at the edge with the spacing in the middle.

## Approximation is a different question

Least squares does not pass through the points and does not try to: on noisy
data its residual is 0.35 while the interpolating polynomial's is exactly
zero. The interpolation reproduces the measurement errors faithfully, which
is the wrong thing to do when the measurements have errors.
