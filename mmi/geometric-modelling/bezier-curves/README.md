# Bezier curves

A curve steered by points it mostly does not pass through. The first and last
control points are on the curve, the rest pull it, and the whole curve stays
inside their convex hull. That last property is what makes every algorithm here
possible.

## The Bernstein basis is a partition of unity

Non-negative and summing to one for every parameter value, verified to 5.6e-16
over degrees 2 to 8. Every point on the curve is therefore a weighted average
of the control points, which gives the convex hull property directly: **0**
points outside the hull over 200 random curves sampled at 51 parameters each.

The same fact gives affine invariance: transforming the curve equals
transforming the control points, agreeing to 3.55e-15 over 200 random rotations,
scalings and translations. A modeller can move a control cage and know that the
curve follows exactly.

## De Casteljau

Repeated linear interpolation instead of the polynomial sum. It matches the
Bernstein evaluation to 5.33e-15, and it produces the subdivision for free: the
first and last elements of each level are the control polygons of the two
halves, reproducing the original to 9.77e-15.

Subdivision is why curves can be drawn at all. Split until the control polygon
is flat, then draw the polygon; the hull property is what makes flatness of the
polygon imply flatness of the curve.

## Flatness has to be measured to the chord segment

Measuring the control points' distance to the infinite line through the
endpoints looks equivalent and is not. A quadratic whose middle control point
sits almost on that line but well past one endpoint measured 0.378 by the line
test while the curve strayed **0.603** from the segment it was approximated by.

Distance to a convex set is convex, so its maximum over the hull is at a
vertex; measuring to the segment therefore bounds the whole curve and measuring
to the line does not. After the change: **0** tolerance violations over 2000
random curves of degrees 2 to 7, with the worst case using 87% of its budget.

| tolerance | points | actual error |
|---|---|---|
| 1.0 | 5 | 0.2238 |
| 0.01 | 33 | 0.0037 |
| 0.0001 | 257 | 0.000057 |

## Degree elevation

Adds a control point without moving the curve, verified to 5.33e-15. The
control polygon gets closer to the curve each time, and slowly: for a
quadratic with arc length 7.509, the polygon goes 10.129, 8.753, 8.350, 8.145,
8.020 over five elevations. Convergent, but not a way to draw anything.

## Joining segments

The derivative of a Bezier curve is `n` times the differences of consecutive
control points, so the tangent at each end runs along the corresponding edge of
the control polygon. Joining is then a condition on points rather than a
calculation:

| second segment's first edge | C0 | C1 | G1 |
|---|---|---|---|
| equal to the first's last edge | yes | yes | yes |
| same direction, shorter | yes | no | yes |
| different direction | yes | no | no |

G1 is what makes a shape look smooth. C1 additionally constrains the
parameterisation, which matters when something travels along the curve at a
speed rather than merely being drawn.

The interactive demos in [demos/](../../demos/) step through de Casteljau,
subdivision and the Bernstein basis for these curves.
