"""The silhouette coefficient: how well each point sits in its cluster.

For a point, compare the average distance to its own cluster with the average
distance to the nearest other cluster. The result runs from minus one to one:
near one the point is well placed, near zero it is on a boundary, and below
zero it is closer to another cluster than to its own.

Averaging over the points gives a number that can be compared across
different numbers of clusters, which is what makes it a way to choose k. The
objective of k-means cannot do that, because it falls with every added
cluster.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "k-means-variants"))
import k_means_variants


def _distance(first, second):
    """The Euclidean distance."""
    return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


def point_score(points, labels, index):
    """The silhouette of one point."""
    own = [other for position, other in enumerate(points)
           if labels[position] == labels[index] and position != index]
    if not own:
        return 0.0
    inside = sum(_distance(points[index], other) for other in own) / len(own)
    outside = None
    for label in set(labels):
        if label == labels[index]:
            continue
        members = [other for position, other in enumerate(points)
                   if labels[position] == label]
        if not members:
            continue
        average = sum(_distance(points[index], other)
                      for other in members) / len(members)
        outside = average if outside is None else min(outside, average)
    if outside is None:
        return 0.0
    return (outside - inside) / max(inside, outside)


def score(points, labels):
    """The average silhouette, or nothing when there is only one cluster."""
    if len(set(labels)) < 2:
        return None
    return sum(point_score(points, labels, index)
               for index in range(len(points))) / len(points)


def for_k(points, clusters, seed=0):
    """The silhouette of a k-means clustering with that many clusters."""
    labels = k_means_variants.k_means(points, clusters, seed)["labels"]
    return score(points, labels)
