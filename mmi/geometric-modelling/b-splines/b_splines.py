"""B-splines: piecewise polynomial curves with local control.

A Bezier curve of degree `n` needs `n+1` control points, so a long curve means
a high degree, and a high degree means every control point affects every point
of the curve. Moving one control point of a degree-20 curve changes all of it.

B-splines fix that by fixing the degree and adding knots instead. A cubic
B-spline with fifty control points is still cubic: each point on the curve
depends on four control points, and moving one changes only four spans. The
knot vector is what says where one polynomial piece ends and the next begins.
"""

from __future__ import annotations

import math


def uniform_knots(count, degree):
    """A uniform knot vector, evenly spaced with no repetitions.

    The curve then only covers the interval where the full set of basis
    functions is defined, so it starts and ends short of the first and last
    control points. Correct, and rarely what anyone wants.
    """
    return list(range(count + degree + 1))


def clamped_knots(count, degree):
    """A knot vector with the ends repeated `degree + 1` times.

    Repeating a knot reduces the continuity there by one. Repeating it
    `degree + 1` times reduces it to nothing, and the curve is pulled to
    interpolate its first and last control point exactly, the way a Bezier
    curve does. Almost every practical B-spline is clamped for this reason.
    """
    interior = count - degree - 1
    return ([0.0] * (degree + 1)
            + [(index + 1) / (interior + 1) for index in range(interior)]
            + [1.0] * (degree + 1))


def basis(index, degree, knots, t):
    """The Cox-de Boor recursion for one basis function.

    Degree zero is an indicator function of one knot span. Each higher degree
    blends two neighbouring functions of the degree below with linear weights.
    The support of the result spans `degree + 1` intervals and no more, and
    that bounded support is the local control property, stated as a formula.
    """
    if degree == 0:
        if knots[index] <= t < knots[index + 1]:
            return 1.0
        if t == knots[-1] and knots[index] <= t <= knots[index + 1] \
                and knots[index] < knots[index + 1]:
            return 1.0
        return 0.0

    left = right = 0.0
    denominator = knots[index + degree] - knots[index]
    if denominator > 0:
        left = (t - knots[index]) / denominator * basis(index, degree - 1, knots, t)

    denominator = knots[index + degree + 1] - knots[index + 1]
    if denominator > 0:
        right = ((knots[index + degree + 1] - t) / denominator
                 * basis(index + 1, degree - 1, knots, t))

    return left + right


def evaluate(control, degree, knots, t):
    """Point on the curve as the basis-weighted sum of the control points."""
    dimension = len(control[0])
    weights = [basis(index, degree, knots, t) for index in range(len(control))]
    return tuple(sum(weight * point[axis] for weight, point in zip(weights, control))
                 for axis in range(dimension))


def find_span(degree, knots, t, count):
    """The knot span containing `t`, by binary search.

    Only `degree + 1` basis functions are non-zero on any span, and finding
    which span it is turns the evaluation from a sum over every control point
    into a sum over four of them. This is where the linear cost of a long
    B-spline comes from.
    """
    if t >= knots[count]:
        return count - 1
    if t <= knots[degree]:
        return degree

    low, high = degree, count
    middle = (low + high) // 2
    while t < knots[middle] or t >= knots[middle + 1]:
        if t < knots[middle]:
            high = middle
        else:
            low = middle
        middle = (low + high) // 2
    return middle


def de_boor(control, degree, knots, t):
    """Evaluate by repeated interpolation, the B-spline form of de Casteljau.

    Take the `degree + 1` control points affecting this span and interpolate
    them pairwise with knot-dependent weights, `degree` times. Same shape of
    algorithm as de Casteljau, same numerical stability, and it touches only
    the control points that matter.
    """
    span = find_span(degree, knots, t, len(control))
    points = [list(control[span - degree + index]) for index in range(degree + 1)]

    for level in range(1, degree + 1):
        for index in range(degree, level - 1, -1):
            position = span - degree + index
            denominator = knots[position + degree - level + 1] - knots[position]
            alpha = 0.0 if denominator == 0 else (t - knots[position]) / denominator
            points[index] = [(1 - alpha) * before + alpha * after
                             for before, after in zip(points[index - 1], points[index])]

    return tuple(points[degree])


def support(index, degree, knots):
    """The parameter interval where one basis function is non-zero.

    `degree + 1` knot spans, always. Moving control point `i` changes the curve
    only here, which is the whole point of the representation and what a Bezier
    curve cannot offer at any degree.
    """
    return (knots[index], knots[index + degree + 1])


def multiplicity(knots, value, tolerance=1e-12):
    """How many times a knot value appears.

    Continuity at a knot is `C^(degree - multiplicity)`. A simple knot in a
    cubic gives C2, a double knot C1, a triple knot C0 (a visible corner) and a
    quadruple knot splits the curve in two. That single rule is how a modeller
    puts a crease into an otherwise smooth surface.
    """
    return sum(1 for knot in knots if abs(knot - value) < tolerance)


def continuity_at(knots, value, degree):
    """The order of continuity at a knot, from its multiplicity."""
    return degree - multiplicity(knots, value)


def insert_knot(control, degree, knots, t):
    """Boehm's algorithm: add a knot without changing the curve.

    The curve is untouched and the control polygon gains a point, moving closer
    to the curve. Inserting the same knot `degree` times makes the curve
    interpolate a control point, and inserting until every interior knot has
    multiplicity `degree` turns the B-spline into a sequence of Bezier
    segments, which is how one representation is converted to the other.
    """
    span = find_span(degree, knots, t, len(control))
    dimension = len(control[0])
    result = list(control[:span - degree + 1])

    for index in range(span - degree + 1, span + 1):
        denominator = knots[index + degree] - knots[index]
        alpha = 0.0 if denominator == 0 else (t - knots[index]) / denominator
        result.append(tuple((1 - alpha) * control[index - 1][axis] + alpha * control[index][axis]
                            for axis in range(dimension)))

    result.extend(control[span:])
    new_knots = sorted(knots + [t])
    return result, new_knots


def to_bezier_segments(control, degree, knots):
    """Split a clamped B-spline into Bezier segments by knot insertion.

    Every interior knot is raised to multiplicity `degree`, after which each
    span is an independent Bezier curve of the same degree. Renderers and file
    formats that only speak Bezier go through this conversion.
    """
    working_control, working_knots = list(control), list(knots)

    for value in sorted(set(knots[degree + 1:-degree - 1])):
        while multiplicity(working_knots, value) < degree:
            working_control, working_knots = insert_knot(
                working_control, degree, working_knots, value)

    segments = []
    for start in range(0, len(working_control) - degree, degree):
        segments.append(working_control[start:start + degree + 1])
    return segments


def nurbs_evaluate(control, weights, degree, knots, t):
    """A rational B-spline: the same sum, divided by the weighted basis sum.

    Weights let the curve represent conic sections exactly, which polynomials
    cannot: no polynomial traces a circle. A quadratic NURBS with weight
    `cos(half angle)` on the middle control point is an exact circular arc,
    which is why every CAD kernel is built on NURBS rather than on B-splines.
    """
    values = [basis(index, degree, knots, t) for index in range(len(control))]
    denominator = sum(weight * value for weight, value in zip(weights, values))
    if abs(denominator) < 1e-12:
        return tuple(control[0])

    dimension = len(control[0])
    return tuple(sum(weight * value * point[axis]
                     for weight, value, point in zip(weights, values, control)) / denominator
                 for axis in range(dimension))
