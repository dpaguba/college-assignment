"""Polygon triangulation: cutting a polygon into triangles.

Graphics hardware draws triangles and nothing else, so every polygon that
reaches the screen has been through this. A convex polygon needs no algorithm,
a fan from any vertex works. A concave one does, because a fan from the wrong
vertex produces triangles that stick out of the polygon.

Every simple polygon with `n` vertices triangulates into exactly `n - 2`
triangles, whatever the algorithm and whatever the shape. That count is a free
correctness check on any implementation.
"""

from __future__ import annotations

import math


def signed_area(polygon):
    """Twice the signed area, by the shoelace formula.

    The sign is the orientation: positive counterclockwise, negative clockwise.
    Every geometric predicate below depends on knowing which way the polygon
    winds, so this is computed first and the polygon normalised.
    """
    return sum(polygon[index][0] * polygon[(index + 1) % len(polygon)][1]
               - polygon[(index + 1) % len(polygon)][0] * polygon[index][1]
               for index in range(len(polygon)))


def is_counterclockwise(polygon):
    """Whether the vertices wind counterclockwise."""
    return signed_area(polygon) > 0


def is_convex_vertex(previous, current, following):
    """Whether the interior angle at a vertex is less than 180 degrees.

    Assumes counterclockwise winding, so a left turn is convex. This is the
    same turn predicate the convex hull uses; the difference is that here it
    classifies a vertex rather than deciding whether to discard it.
    """
    return ((current[0] - previous[0]) * (following[1] - previous[1])
            - (current[1] - previous[1]) * (following[0] - previous[0])) > 0


def point_in_triangle(point, a, b, c):
    """Whether a point lies inside a triangle, boundary included."""
    def sign(p, q, r):
        """Which side of the line `p, q` the point `r` falls on."""
        return (p[0] - r[0]) * (q[1] - r[1]) - (q[0] - r[0]) * (p[1] - r[1])

    d1, d2, d3 = sign(point, a, b), sign(point, b, c), sign(point, c, a)
    has_negative = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_positive = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_negative and has_positive)


def is_ear(polygon, indices, position):
    """Whether a vertex is an ear: convex, and its triangle is empty.

    Both conditions are needed. A convex vertex whose triangle swallows a
    distant part of the polygon is not an ear, and cutting it would produce a
    triangle sticking outside the shape. Checking emptiness is what makes ear
    clipping quadratic rather than linear.
    """
    count = len(indices)
    previous = polygon[indices[(position - 1) % count]]
    current = polygon[indices[position]]
    following = polygon[indices[(position + 1) % count]]

    if not is_convex_vertex(previous, current, following):
        return False

    for offset in range(count):
        if offset in ((position - 1) % count, position, (position + 1) % count):
            continue
        if point_in_triangle(polygon[indices[offset]], previous, current, following):
            return False

    return True


def ear_clipping(polygon):
    """Triangulate by repeatedly cutting off ears.

    Every simple polygon with more than three vertices has at least two ears,
    which is what guarantees the loop terminates. Each pass removes one vertex
    and costs a scan, so the whole thing is `O(n^2)`.

    Faster algorithms exist, monotone decomposition at `O(n log n)` and
    Chazelle's linear one, but ear clipping is the one that fits on a page and
    handles holes with a simple bridge construction, so it is what most
    libraries actually ship.
    """
    if len(polygon) < 3:
        return []

    working = list(polygon)
    if not is_counterclockwise(working):
        working = working[::-1]

    indices = list(range(len(working)))
    triangles = []
    guard = 0

    while len(indices) > 3 and guard < len(polygon) ** 2:
        guard += 1
        for position in range(len(indices)):
            if is_ear(working, indices, position):
                count = len(indices)
                triangles.append((indices[(position - 1) % count],
                                  indices[position],
                                  indices[(position + 1) % count]))
                indices.pop(position)
                break
        else:
            break

    if len(indices) == 3:
        triangles.append(tuple(indices))

    return [tuple(working[index] for index in triangle) for triangle in triangles]


def fan_triangulation(polygon):
    """Fan from the first vertex, correct only for convex polygons.

    The cheapest possible triangulation and the one a renderer applies to a
    quad without thinking. On a concave polygon it produces triangles that
    leave the shape, which is why `ear_clipping` exists.
    """
    return [(polygon[0], polygon[index], polygon[index + 1])
            for index in range(1, len(polygon) - 1)]


def triangulation_area(triangles):
    """Total area of a set of triangles."""
    return sum(abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2
               for a, b, c in triangles)


def classify_vertices(polygon):
    """Split the vertices into convex and reflex.

    A polygon is convex exactly when it has no reflex vertices, and the number
    of reflex vertices bounds how much work any decomposition has to do. It
    also bounds the number of guards needed to see the whole polygon, which is
    the art gallery problem.
    """
    working = polygon if is_counterclockwise(polygon) else polygon[::-1]
    convex, reflex = [], []

    for index in range(len(working)):
        previous = working[index - 1]
        current = working[index]
        following = working[(index + 1) % len(working)]
        (convex if is_convex_vertex(previous, current, following) else reflex).append(current)

    return convex, reflex


def is_simple(polygon):
    """Whether the polygon has no self-intersections.

    Every algorithm here assumes it. A self-intersecting polygon has no
    well-defined inside, so "triangulate its interior" is not a question with
    an answer, and an implementation that does not check will loop or produce
    nonsense rather than fail.
    """
    count = len(polygon)

    for i in range(count):
        for j in range(i + 1, count):
            if abs(i - j) <= 1 or (i == 0 and j == count - 1):
                continue
            if _segments_cross(polygon[i], polygon[(i + 1) % count],
                               polygon[j], polygon[(j + 1) % count]):
                return False

    return True


def _segments_cross(a, b, c, d):
    """Whether two segments properly cross."""
    def orientation(p, q, r):
        """Turn direction of three points, as -1, 0 or 1."""
        value = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return 0 if abs(value) < 1e-12 else (1 if value > 0 else -1)

    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    return o1 != o2 and o3 != o4 and o1 != 0 and o2 != 0 and o3 != 0 and o4 != 0
