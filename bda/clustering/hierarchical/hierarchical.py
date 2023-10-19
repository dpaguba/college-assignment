"""Hierarchical clustering: the whole tree instead of one clustering.

Merge the closest pair of clusters, repeat, and the record of merges is a
dendrogram that can be cut at any height. Nothing has to be decided in
advance, which is the advantage, and the distance between clusters has to be
defined, which is where the choice moved.

Single linkage takes the closest pair of members and chains: a line of points
one step apart becomes one cluster however long it is. Complete linkage takes
the furthest pair and refuses to chain, at the price of splitting elongated
clusters.
"""


def _distance(first, second):
    """The Euclidean distance between two points."""
    return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


def _linkage(first, second, kind):
    """The distance between two groups under the given linkage."""
    pairs = [_distance(a, b) for a in first for b in second]
    if kind == "single":
        return min(pairs)
    if kind == "complete":
        return max(pairs)
    if kind == "average":
        return sum(pairs) / len(pairs)
    raise ValueError("unknown linkage: %s" % kind)


def merge_trace(points, linkage="single"):
    """The sequence of merges, with the distance at which each happened."""
    groups = [[point] for point in points]
    indices = [[index] for index in range(len(points))]
    merges = []
    while len(groups) > 1:
        best = None
        for first in range(len(groups)):
            for second in range(first + 1, len(groups)):
                distance = _linkage(groups[first], groups[second], linkage)
                if best is None or distance < best[0]:
                    best = (distance, first, second)
        distance, first, second = best
        merges.append({"distance": distance,
                       "members": sorted(indices[first] + indices[second])})
        groups[first] = groups[first] + groups[second]
        indices[first] = indices[first] + indices[second]
        del groups[second]
        del indices[second]
    return merges


def cut(points, clusters, linkage="single"):
    """The clustering obtained by stopping the merges at a given count."""
    groups = [[index] for index in range(len(points))]
    while len(groups) > clusters:
        best = None
        for first in range(len(groups)):
            for second in range(first + 1, len(groups)):
                distance = _linkage([points[index] for index in groups[first]],
                                    [points[index] for index in groups[second]],
                                    linkage)
                if best is None or distance < best[0]:
                    best = (distance, first, second)
        _distance_value, first, second = best
        groups[first] = groups[first] + groups[second]
        del groups[second]
    labels = [0] * len(points)
    for label, group in enumerate(groups):
        for index in group:
            labels[index] = label
    return labels


def chaining_example():
    """A line of points, clustered under both linkages.

    Single linkage joins the whole line into one cluster because every
    neighbour is close; complete linkage splits it because the ends are far
    apart. The same data, two answers, and the linkage is the reason.
    """
    points = [(value,) for value in (0.0, 1.0, 2.0, 3.0, 4.0, 5.0)]
    single = cut(points, clusters=2, linkage="single")
    complete = cut(points, clusters=2, linkage="complete")
    return {"single chains": len(set(single[:5])) == 1,
            "complete chains": len(set(complete[:5])) == 1,
            "single": single, "complete": complete}
