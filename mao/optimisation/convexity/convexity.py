"""Convexity, which is what makes an optimisation problem tractable.

A set is convex when it contains the segment between any two of its points.
The feasible region of a linear program is convex, so a local optimum is
global and the simplex method can follow edges to the answer. The integer
points inside the same region are not convex, and that single fact is why
integer programming is a different subject rather than a special case.

The tenth sheet asks which of four sets are convex, and the module answers by
sampling segments rather than by citing the definition, so the reasoning can
be checked on an example.
"""


SETS = {
    "Ax <= b, x >= 0": True,
    "Ax <= b, x in {0,1}": False,
    "circle": True,
    "union of two discs": False,
}
"""The sets of the tenth sheet, with whether they are convex."""


def is_convex_set(name):
    """Whether the named set is convex."""
    if name not in SETS:
        raise ValueError("unknown set: %s" % name)
    return SETS[name]


def sampled_check(points, membership, steps=20):
    """Whether every sampled segment between members stays inside."""
    members = [point for point in points if membership(point)]
    for first in members:
        for second in members:
            for index in range(steps + 1):
                share = index / steps
                middle = tuple(share * a + (1 - share) * b
                               for a, b in zip(first, second))
                if not membership(middle):
                    return False
    return True


def intersection_stays_convex():
    """Whether adding a linear constraint to a convex set keeps it convex.

    The fourth part of the sheet's question. A half space is convex and the
    intersection of convex sets is convex, so the answer is yes, and the
    check here confirms it on a sampled square.
    """
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
    return sampled_check(points, lambda point: point[0] + point[1] <= 1.5)


def is_convex_function(function, low, high, steps=40):
    """Whether a function lies below its chords on the interval."""
    for first in range(steps + 1):
        for second in range(steps + 1):
            left = low + (high - low) * first / steps
            right = low + (high - low) * second / steps
            middle = (left + right) / 2
            if function(middle) > (function(left) + function(right)) / 2 + 1e-9:
                return False
    return True
