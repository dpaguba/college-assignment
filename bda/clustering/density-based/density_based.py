"""DBSCAN: clusters as dense regions, whatever their shape.

A point is a core point when enough neighbours lie within a radius; core
points that reach each other are one cluster, and a point that reaches no
core point is noise. The number of clusters is not a parameter, which is the
main difference from k-means, and the radius is, which is where the
difficulty moves.

Two concentric rings are the standard example: k-means cuts them in half
because it can only draw straight boundaries, and DBSCAN separates them
because it follows the density.
"""

import math


def parameters():
    """The parameters the method takes, which do not include a cluster count."""
    return ["radius", "minimum points"]


def dbscan(points, radius, minimum):
    """The cluster label of each point, with noise as minus one."""
    labels = [None] * len(points)
    cluster = 0
    for index in range(len(points)):
        if labels[index] is not None:
            continue
        neighbours = _neighbours(points, index, radius)
        if len(neighbours) < minimum:
            labels[index] = -1
            continue
        labels[index] = cluster
        frontier = list(neighbours)
        while frontier:
            other = frontier.pop()
            if labels[other] == -1:
                labels[other] = cluster
            if labels[other] is not None:
                continue
            labels[other] = cluster
            further = _neighbours(points, other, radius)
            if len(further) >= minimum:
                frontier.extend(further)
        cluster += 1
    return labels


def _neighbours(points, index, radius):
    """The points within the radius, excluding the point itself."""
    return [other for other in range(len(points))
            if other != index and _distance(points[index], points[other])
            <= radius]


def _distance(first, second):
    """The Euclidean distance."""
    return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


def rings_example():
    """Two concentric rings, clustered by density and by k-means."""
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                    "k-means-variants"))
    import k_means_variants
    inner = [(math.cos(angle / 12 * 2 * math.pi),
              math.sin(angle / 12 * 2 * math.pi)) for angle in range(12)]
    outer = [(4 * math.cos(angle / 24 * 2 * math.pi),
              4 * math.sin(angle / 24 * 2 * math.pi)) for angle in range(24)]
    points = inner + outer
    labels = dbscan(points, radius=1.2, minimum=2)
    density_clusters = len({label for label in labels if label >= 0})
    means = k_means_variants.k_means(points, clusters=2, seed=1)["labels"]
    mistakes = sum(1 for index, label in enumerate(means)
                   if (index < len(inner)) != (label == means[0]))
    return {"density clusters": density_clusters,
            "k means error": mistakes, "points": len(points)}
