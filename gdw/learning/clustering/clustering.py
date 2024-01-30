"""Clustering: grouping without labels, and what that costs.

k-means alternates two steps, assigning each point to the nearest centre and
moving each centre to the mean of its points. Both steps lower the objective,
so the algorithm terminates, and neither looks beyond the current assignment,
so it terminates at a local optimum that depends on where it started.

The number of clusters is not found by the method. The objective falls with
every additional cluster, so the elbow of that curve is a judgement rather
than a result, and the module returns the curve instead of a number.
"""

import random


def _distance(first, second):
    """The squared Euclidean distance."""
    return sum((a - b) ** 2 for a, b in zip(first, second))


def k_means(points, clusters, seed=0, steps=100):
    """The assignment and the objective after each iteration."""
    generator = random.Random(seed)
    centres = generator.sample(list(points), clusters)
    objective = []
    labels = [0] * len(points)
    for _ in range(steps):
        labels = [min(range(clusters),
                      key=lambda index: _distance(point, centres[index]))
                  for point in points]
        objective.append(sum(_distance(point, centres[label])
                             for point, label in zip(points, labels)))
        following = []
        for index in range(clusters):
            members = [point for point, label in zip(points, labels)
                       if label == index]
            if not members:
                following.append(centres[index])
                continue
            following.append(tuple(sum(values) / len(members)
                                   for values in zip(*members)))
        if following == centres:
            break
        centres = following
    return {"labels": labels, "centres": centres, "objective": objective}


def hierarchical(points):
    """Agglomerative clustering, merging the closest pair at each step."""
    groups = [[point] for point in points]
    merges = []
    while len(groups) > 1:
        best = None
        for first in range(len(groups)):
            for second in range(first + 1, len(groups)):
                distance = min(_distance(a, b) ** 0.5 for a in groups[first]
                               for b in groups[second])
                if best is None or distance < best[0]:
                    best = (distance, first, second)
        distance, first, second = best
        merges.append({"distance": distance, "size": len(groups[first])
                       + len(groups[second])})
        groups[first] = groups[first] + groups[second]
        del groups[second]
    return merges


def elbow(points, up_to, seed=0):
    """The objective for each number of clusters, which always falls."""
    return [k_means(points, clusters, seed)["objective"][-1]
            for clusters in range(1, up_to + 1)]
