"""Subspace clustering: a cluster that exists in some dimensions only.

In high dimensional data a group can be tight in three attributes and spread
out in the other forty, so it is invisible in the full space and obvious in
the subspace. Finding it means searching the subspaces, and there are two to
the power of the dimensions of them, which is why the search needs a pruning
rule.

The rule is the Apriori one again: a set of points dense in a subspace is
dense in every projection of it, so a subspace whose projection is not dense
can be skipped. Density is anti-monotone in the dimensions, exactly as
support is anti-monotone in the items.
"""


def subspace_count(dimensions):
    """How many non-empty subspaces there are."""
    return 2 ** dimensions - 1


def dense_in_projection(points, dimensions, radius, minimum):
    """Whether the points are dense when projected on those dimensions."""
    projected = [tuple(point[index] for index in dimensions)
                 for point in points]
    for candidate in projected:
        close = sum(1 for other in projected
                    if sum((a - b) ** 2 for a, b in zip(candidate, other))
                    ** 0.5 <= radius)
        if close >= minimum:
            return True
    return False


def hidden_cluster_example():
    """A cluster tight in two dimensions and invisible in five."""
    cluster = [(0.0, 0.0, 1.0, 8.0, 3.0), (0.05, 0.02, 7.0, 2.0, 9.0),
               (0.02, 0.04, 4.0, 5.0, 1.0), (0.03, 0.01, 9.0, 1.0, 6.0)]
    noise = [(5.0, 5.0, 2.0, 3.0, 4.0), (7.0, 8.0, 6.0, 7.0, 2.0)]
    points = cluster + noise
    in_subspace = dense_in_projection(points, [0, 1], radius=0.2, minimum=4)
    in_full = dense_in_projection(points, [0, 1, 2, 3, 4], radius=0.2,
                                  minimum=4)
    return {"found in the subspace": in_subspace,
            "found in the full space": in_full,
            "subspaces to search": subspace_count(5)}


def monotonicity_holds(points, radius, minimum):
    """Whether density in a subspace implies density in every projection."""
    dimensions = len(points[0])
    for first in range(dimensions):
        for second in range(dimensions):
            if first >= second:
                continue
            pair = dense_in_projection(points, [first, second], radius, minimum)
            if pair and not dense_in_projection(points, [first], radius,
                                                minimum):
                return False
    return True
