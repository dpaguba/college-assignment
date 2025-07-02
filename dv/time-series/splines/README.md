# Splines

A natural cubic spline: a cubic on each interval, matching value, slope and
curvature at the inner nodes, zero curvature at the ends. The coefficients
come from a tridiagonal system, solved here by Gaussian elimination.

Checked on 40 random node sets: the spline passes through every node exactly,
the second derivative vanishes at both ends, and value, first and second
derivative agree from the left and from the right at every inner node.

## Bézier

De Casteljau's repeated interpolation and the Bernstein form give the same
curve, checked at eleven parameter values. The curve starts at the first
control point, ends at the last, and stays inside the convex hull of the
control points, which is what makes the control polygon a usable handle.

## Locality

Moving one control point of a Bézier curve moves the whole curve. Moving one
control point of a cubic B-spline changes the curve near it by 2.97 and, at a
parameter three knots away, by exactly zero. That is the property the basis
functions are built for: each one is non-zero on only a few intervals, so an
edit is local.
