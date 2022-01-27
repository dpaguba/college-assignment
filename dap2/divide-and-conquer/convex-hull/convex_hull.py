"""Convex hull: the smallest convex polygon containing every point."""

from __future__ import annotations

from math import atan2

def cross(origin, first, second):
    """Twice the signed area of the triangle, which is really a turn direction.

    Positive means the three points turn left, negative means right, zero means
    they are collinear. Every convex hull algorithm is this one test in a loop,
    and it uses only multiplication and subtraction: no square roots, no
    trigonometry, no floating point error if the inputs are integers.
    """
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (
        first[1] - origin[1]
    ) * (second[0] - origin[0])

def monotone_chain(points):
    """Andrew's monotone chain: sort by coordinate, build two halves.

    Sort the points left to right. Sweep once building the lower boundary and
    once the upper, and in each sweep pop any point that would make the chain
    turn the wrong way. Joining the two chains gives the hull.

    O(n log n), dominated entirely by the sort, and the sweep is linear because
    each point is pushed once and popped at most once. Simpler than Graham's
    scan, which sorts by angle and needs a chosen pivot, and numerically better
    behaved because it never computes an angle at all.
    """
    unique = sorted(set(points))
    if len(unique) < 3:
        return unique

    def build(sequence):
        """One chain of the hull, dropping points that turn the wrong way."""
        chain: list = []
        for point in sequence:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], point) <= 0:
                chain.pop()
            chain.append(point)
        return chain

    lower = build(unique)
    upper = build(reversed(unique))
    return lower[:-1] + upper[:-1]

def graham_scan(points):
    """Graham's scan: sort by angle around the lowest point, then walk.

    The 1972 original, and the first hull algorithm to reach O(n log n). Pick
    the lowest point, sort the rest by the angle they make with it, and walk
    the sorted list keeping only left turns.

    Sorting by angle is what makes it more delicate than the monotone chain:
    points at the same angle have to be ordered by distance, and the arctangent
    introduces floating point comparisons where the chain uses only integer
    arithmetic. Both are here so the difference is visible rather than asserted.
    """
    unique = list(set(points))
    if len(unique) < 3:
        return sorted(unique)

    pivot = min(unique, key=lambda point: (point[1], point[0]))

    def angle_then_distance(point):
        """The sort key: angle from the pivot, then distance."""
        return (
            atan2(point[1] - pivot[1], point[0] - pivot[0]),
            (point[0] - pivot[0]) ** 2 + (point[1] - pivot[1]) ** 2,
        )

    ordered = sorted((p for p in unique if p != pivot), key=angle_then_distance)

    hull = [pivot]
    for point in ordered:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)

    return hull
