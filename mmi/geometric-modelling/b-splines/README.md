# B-splines

A Bezier curve of degree `n` needs `n+1` control points, so a long curve means
a high degree, and at high degree every control point affects the whole curve.
B-splines keep the degree fixed and add knots instead.

## Local support, measured

With 8 control points, degree 3 and a clamped knot vector, moving control point
3 changed the curve exactly on `[0.003, 0.797]`, and the theoretical support of
its basis function is `[0.0, 0.8]`. Nothing outside moved at all.

That is the entire reason the representation exists. A designer editing one
part of a shape does not disturb the rest, and a renderer only has to
re-evaluate four spans.

## The knot vector does the work

Repeating a knot lowers the continuity there by one, so the same curve type
covers everything from perfectly smooth to a deliberate corner:

| interior knot at 0.5 | multiplicity | continuity | tangent turn at the knot |
|---|---|---|---|
| simple | 1 | C2 | 0.23° |
| double | 2 | C1 | 0.00° |
| triple | 3 | C0 | **126.78°** |

Clamping the ends (repeating the first and last knot `degree + 1` times) is
what makes the curve interpolate its first and last control point, exactly, for
degrees 2, 3 and 4 alike.

## Verified

- basis functions sum to 1 to 2.22e-16
- de Boor agrees with the direct basis sum to 3.55e-15 over 200 curves
- knot insertion leaves the curve unchanged to 3.55e-15 over 200 insertions,
  adding exactly one control point each time
- conversion to Bezier segments reproduces the B-spline to 3.55e-15: 6 control
  points with 2 interior knots become 3 cubic Bezier segments

## Why CAD uses NURBS and not this

No polynomial traces a circle. The rational form divides by the weighted basis
sum, and with weight `cos(45°) = 0.707107` on the middle control point a
quadratic NURBS is an **exact** quarter circle: maximum radius deviation
2.22e-16. The same three control points with unit weights, an ordinary
B-spline, deviate by up to 0.0607.

That gap is why every CAD kernel is built on the rational form: a design
language that cannot represent a hole is not usable.
