"""Convex hulls: the smallest convex set containing a point set.

Used everywhere as a cheap conservative stand-in for a complicated shape:
collision tests, view frustum culling, the bound on a Bezier curve in
[bezier-curves](../bezier-curves/). Being convex is what makes it cheap, since
a point is inside exactly when it is on the inner side of every edge, with no
special cases.

Three algorithms with three different costs, and the difference between them is
what they sort.
"""

from __future__ import annotations

import math


def cross(o, a, b):
    """Sign of the turn from `o->a` to `o->b`, as the z of the cross product.

    Positive means counterclockwise, negative clockwise, zero collinear. Every
    algorithm here is built out of this one predicate, which is why the whole
    field is careful about it: computed in floating point it can report a turn
    that contradicts another turn it just reported, and the algorithms then
    produce hulls that are not convex.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def monotone_chain(points):
    """Andrew's monotone chain: sort by x, then build the lower and upper hull.

    Sorting costs `O(n log n)` and the two sweeps cost `O(n)`, so the sort is
    the whole cost. Each sweep pops points that would make a clockwise turn,
    and each point is pushed and popped at most once.

    Simpler than Graham's scan and numerically better behaved, because it sorts
    by coordinate rather than by angle around a pivot, and angles need a
    division and an arctangent that the turn predicate does not.
    """
    ordered = sorted(set(tuple(point) for point in points))
    if len(ordered) < 3:
        return ordered

    def build(sequence):
        """One half of the hull, popping points that turn the wrong way."""
        chain = []
        for point in sequence:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], point) <= 0:
                chain.pop()
            chain.append(point)
        return chain

    return build(ordered)[:-1] + build(ordered[::-1])[:-1]


def graham_scan(points):
    """Sort by angle around the lowest point, then walk once removing turns.

    The historical algorithm and the same cost. The pivot is the lowest point,
    which is guaranteed on the hull, and ties in angle are broken by distance
    so that collinear points nearer the pivot are discarded first.
    """
    unique = list(set(tuple(point) for point in points))
    if len(unique) < 3:
        return sorted(unique)

    pivot = min(unique, key=lambda point: (point[1], point[0]))

    def key(point):
        """Sort key: angle around the pivot, then distance to break ties."""
        angle = math.atan2(point[1] - pivot[1], point[0] - pivot[0])
        return (angle, (point[0] - pivot[0]) ** 2 + (point[1] - pivot[1]) ** 2)

    ordered = sorted((point for point in unique if point != pivot), key=key)
    hull = [pivot]

    for point in ordered:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)

    return hull


def gift_wrapping(points):
    """Jarvis march: from a known hull point, repeatedly find the next one.

    Costs `O(n h)` for `h` hull points, so it beats the sorting algorithms when
    the hull is tiny compared to the input, and degrades to `O(n^2)` when every
    point is on the hull. It is the only one of the three whose cost depends on
    the answer rather than on the input size, which is called output sensitive.
    """
    unique = list(set(tuple(point) for point in points))
    if len(unique) < 3:
        return sorted(unique)

    start = min(unique, key=lambda point: (point[0], point[1]))
    hull = [start]
    current = start

    while True:
        candidate = unique[0] if unique[0] != current else unique[1]
        for point in unique:
            if point == current:
                continue
            turn = cross(current, candidate, point)
            if turn < 0 or (turn == 0
                            and math.dist(current, point) > math.dist(current, candidate)):
                candidate = point

        if candidate == start:
            return hull
        hull.append(candidate)
        current = candidate


def hull_area(hull):
    """Area enclosed by a hull, by the shoelace formula."""
    return abs(sum(hull[index][0] * hull[(index + 1) % len(hull)][1]
                   - hull[(index + 1) % len(hull)][0] * hull[index][1]
                   for index in range(len(hull)))) / 2


def hull_perimeter(hull):
    """Perimeter of a hull."""
    return sum(math.dist(hull[index], hull[(index + 1) % len(hull)])
               for index in range(len(hull)))


def contains(hull, point, tolerance=1e-12):
    """Whether a point lies inside a counterclockwise hull.

    One sign test per edge, no special cases, which is the property that makes
    convex shapes worth extracting in the first place. A general polygon needs
    the parity rule instead.
    """
    return all(cross(hull[index], hull[(index + 1) % len(hull)], point) >= -tolerance
               for index in range(len(hull)))


def is_convex(polygon, tolerance=1e-9):
    """Whether every turn of a polygon goes the same way."""
    signs = set()
    for index in range(len(polygon)):
        turn = cross(polygon[index - 1], polygon[index],
                     polygon[(index + 1) % len(polygon)])
        if abs(turn) > tolerance:
            signs.add(turn > 0)
    return len(signs) <= 1


def diameter(hull):
    """The farthest pair of points, by rotating callipers.

    Every diametral pair is a pair of hull vertices, and walking one index
    forward while the other chases it visits all the candidate pairs in linear
    time. Brute force over all pairs of the original points is quadratic; over
    hull points it is quadratic in `h`, and this is linear in `h`.
    """
    if len(hull) < 2:
        return 0.0
    if len(hull) == 2:
        return math.dist(hull[0], hull[1])

    best = 0.0
    count = len(hull)
    opposite = 1

    for index in range(count):
        following = (index + 1) % count
        while True:
            following_area = abs(cross(hull[index], hull[following],
                                       hull[(opposite + 1) % count]))
            current_area = abs(cross(hull[index], hull[following], hull[opposite]))
            if following_area <= current_area:
                break
            opposite = (opposite + 1) % count

        best = max(best, math.dist(hull[index], hull[opposite]),
                   math.dist(hull[following], hull[opposite]))

    return best
