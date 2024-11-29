"""Bezier curves: a curve defined by points it mostly does not pass through.

The control polygon is the interface. Its first and last points are on the
curve, the rest pull it without being reached, and the whole curve stays inside
their convex hull. That combination is what makes the representation usable by
hand: every control point has a predictable local effect, and no control point
can send the curve somewhere unexpected.

Everything here follows from the Bernstein polynomials, which are a partition
of unity on `[0, 1]`: they are non-negative and sum to one, so a point on the
curve is always a weighted average of the control points.
"""

from __future__ import annotations

import math


def binomial(n, k):
    """Binomial coefficient, the combinatorial part of the Bernstein basis."""
    return math.comb(n, k)


def bernstein(n, i, t):
    """The `i`-th Bernstein polynomial of degree `n`.

    `C(n,i) t^i (1-t)^(n-i)`. Non-negative on `[0, 1]` and summing to one
    across `i`, which is the entire reason the convex hull property holds.
    """
    return binomial(n, i) * (t ** i) * ((1 - t) ** (n - i))


def evaluate(control, t):
    """Point on the curve at parameter `t`, by the Bernstein sum.

    Direct and numerically fine for low degrees. For anything else de Casteljau
    is better conditioned, because it never forms the large binomial
    coefficients that cancel against small powers.
    """
    n = len(control) - 1
    dimension = len(control[0])
    return tuple(sum(bernstein(n, i, t) * point[axis] for i, point in enumerate(control))
                 for axis in range(dimension))


def de_casteljau(control, t):
    """Point on the curve by repeated linear interpolation.

    Take the control polygon, interpolate between each adjacent pair at `t`,
    and repeat on the result until one point is left. Geometric, stable, and it
    produces the subdivision as a by-product: the intermediate points form the
    control polygons of the two halves.

    This is the algorithm the interactive demos step through.
    """
    points = [tuple(point) for point in control]

    while len(points) > 1:
        points = [tuple(a[axis] + t * (b[axis] - a[axis]) for axis in range(len(a)))
                  for a, b in zip(points, points[1:])]

    return points[0]


def de_casteljau_levels(control, t):
    """Every intermediate level of the construction, not just the final point.

    The first element of each level, read downwards, is the control polygon of
    the left half; the last element of each level, read upwards, is the right
    half. That is subdivision for free, and it is why de Casteljau is the basis
    of every rendering and intersection algorithm for these curves.
    """
    levels = [[tuple(point) for point in control]]

    while len(levels[-1]) > 1:
        points = levels[-1]
        levels.append([tuple(a[axis] + t * (b[axis] - a[axis]) for axis in range(len(a)))
                       for a, b in zip(points, points[1:])])

    return levels


def subdivide(control, t=0.5):
    """Split a curve into two curves that together trace the same shape.

    The pair of control polygons read off the de Casteljau levels. Repeated
    subdivision converges to the curve fast, which is how curves are actually
    drawn: split until each polygon is flat to within a pixel, then draw the
    polygon.
    """
    levels = de_casteljau_levels(control, t)
    return ([level[0] for level in levels], [level[-1] for level in levels][::-1])


def flatten(control, tolerance=0.1, depth=0):
    """Approximate a curve by a polyline, subdividing until it is flat enough.

    Flatness is measured as the distance from the control points to the chord.
    Because the curve lies in the convex hull of its control points, a flat
    control polygon guarantees a flat curve, so the test on the polygon is a
    valid test on the curve. That implication is what makes the recursion
    sound, and it fails for any representation without the hull property.
    """
    if depth > 20 or _flatness(control) <= tolerance:
        return [control[0], control[-1]]

    left, right = subdivide(control)
    return flatten(left, tolerance, depth + 1)[:-1] + flatten(right, tolerance, depth + 1)


def _flatness(control):
    """Largest distance from a control point to the **chord segment**.

    Measuring to the infinite line through the endpoints looks equivalent and
    is not. A control point can sit almost on that line while lying far past
    one of the endpoints, and then the curve overshoots the segment by more
    than the reported flatness: a quadratic with control points barely off the
    line was measured at 0.378 by the line test while straying 0.603 from the
    segment it was approximated by.

    Distance to a convex set is a convex function, so its maximum over the
    convex hull is attained at a vertex. Measuring to the segment therefore
    bounds the whole curve, and measuring to the line does not.
    """
    start, end = control[0], control[-1]
    return max(_point_to_segment(point, start, end) for point in control[1:-1])


def _point_to_segment(point, start, end):
    """Distance from a point to a line segment, clamped at both ends."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    if dx == 0.0 and dy == 0.0:
        return math.dist(point, start)

    ratio = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / (dx * dx + dy * dy)
    ratio = max(0.0, min(1.0, ratio))
    return math.dist(point, (start[0] + ratio * dx, start[1] + ratio * dy))


def derivative(control):
    """Control points of the derivative curve, itself a Bezier of degree `n-1`.

    `n` times the differences of consecutive control points. So the tangent at
    the start is along the first edge of the control polygon and at the end
    along the last, which is what makes joining two segments smoothly a
    condition on three collinear points rather than a calculation.
    """
    n = len(control) - 1
    return [tuple(n * (b[axis] - a[axis]) for axis in range(len(a)))
            for a, b in zip(control, control[1:])]


def tangent(control, t):
    """Unit tangent at a parameter value."""
    velocity = evaluate(derivative(control), t)
    length = math.sqrt(sum(component ** 2 for component in velocity))
    if length < 1e-12:
        return velocity
    return tuple(component / length for component in velocity)


def elevate_degree(control):
    """Add a control point without changing the curve at all.

    Degree elevation makes two curves of different degrees comparable, which is
    what a modeller needs before joining or lofting them. The new polygon is
    closer to the curve than the old one, and repeated elevation converges to
    the curve, slowly.
    """
    n = len(control) - 1
    dimension = len(control[0])
    result = [tuple(control[0])]

    for i in range(1, n + 1):
        ratio = i / (n + 1)
        result.append(tuple(ratio * control[i - 1][axis] + (1 - ratio) * control[i][axis]
                            for axis in range(dimension)))

    result.append(tuple(control[-1]))
    return result


def in_convex_hull(control, point, tolerance=1e-9):
    """Whether a point lies in the convex hull of the control points.

    The curve never leaves this hull, because every point on it is a weighted
    average with non-negative weights summing to one. Clipping and intersection
    tests use the hull as a cheap conservative bound before touching the curve.
    """
    hull = _convex_hull(control)
    if len(hull) < 3:
        return all(abs(point[axis] - hull[0][axis]) < tolerance for axis in range(2))

    for index in range(len(hull)):
        a, b = hull[index], hull[(index + 1) % len(hull)]
        cross = ((b[0] - a[0]) * (point[1] - a[1]) - (b[1] - a[1]) * (point[0] - a[0]))
        if cross < -tolerance:
            return False
    return True


def _convex_hull(points):
    """Convex hull of a point set, by Andrew's monotone chain."""
    ordered = sorted(set(tuple(point[:2]) for point in points))
    if len(ordered) < 3:
        return ordered

    def build(sequence):
        """One half of the hull, popping points that turn the wrong way."""
        chain = []
        for point in sequence:
            while len(chain) >= 2:
                a, b = chain[-2], chain[-1]
                if ((b[0] - a[0]) * (point[1] - a[1])
                        - (b[1] - a[1]) * (point[0] - a[0])) <= 0:
                    chain.pop()
                else:
                    break
            chain.append(point)
        return chain

    return build(ordered)[:-1] + build(ordered[::-1])[:-1]


def joins_c0(first, second):
    """Whether two segments meet at all."""
    return all(abs(a - b) < 1e-9 for a, b in zip(first[-1], second[0]))


def joins_c1(first, second):
    """Whether two segments meet with matching first derivatives.

    The condition is that the last edge of the first polygon and the first edge
    of the second are equal as vectors: same direction **and** same length.
    Only then is the curve continuously differentiable in its parameter.
    """
    if not joins_c0(first, second):
        return False
    left = derivative(first)[-1]
    right = derivative(second)[0]
    return all(abs(a - b) < 1e-9 for a, b in zip(left, right))


def joins_g1(first, second):
    """Whether two segments meet with a continuous tangent direction.

    Weaker than C1 and usually what is actually wanted: the lengths may differ,
    only the directions must match, which means the three points around the
    joint are collinear. A shape looks smooth under G1; it is the
    parameterisation, not the shape, that C1 additionally constrains.
    """
    if not joins_c0(first, second):
        return False
    left = derivative(first)[-1]
    right = derivative(second)[0]
    cross = left[0] * right[1] - left[1] * right[0]
    return abs(cross) < 1e-9 and sum(a * b for a, b in zip(left, right)) > 0
