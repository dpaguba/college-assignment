"""Pareto fronts: what is left when no single criterion decides.

A design dominates another when it is at least as good in every criterion and
better in at least one. The undominated designs form the front, and no
argument about weights is needed to draw it, which is the point: the front is
a fact about the designs and the weighting is a decision about preferences.

The exam draws it for energy against miss rate, both to be minimised.
"""


def dominates(first, second):
    """Whether the first point is better in every criterion and strictly in one."""
    if first == second:
        return False
    return (all(a <= b for a, b in zip(first, second))
            and any(a < b for a, b in zip(first, second)))


def front(points):
    """The undominated points, in the order they were given."""
    return [point for point in points
            if not any(dominates(other, point) for other in points)]


def regions(point):
    """Which part of the plane dominates a point and which it dominates.

    With both criteria minimised, everything below and to the left is better
    and everything above and to the right is worse. The two remaining
    quadrants are incomparable, and they are the reason the front exists at
    all.
    """
    return {"dominated by it": "upper right", "dominating it": "lower left",
            "incomparable": ["upper left", "lower right"]}


def knee(points):
    """The front point closest to the ideal corner, by Euclidean distance.

    A common way to pick one design when a choice has to be made. It is a
    preference and not a theorem, which is why it is a separate function
    rather than part of the front.
    """
    current = front(points)
    best_x = min(point[0] for point in current)
    best_y = min(point[1] for point in current)
    return min(current, key=lambda point: ((point[0] - best_x) ** 2
                                           + (point[1] - best_y) ** 2))
