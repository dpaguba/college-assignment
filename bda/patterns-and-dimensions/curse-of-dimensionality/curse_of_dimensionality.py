"""The curse of dimensionality: distance stops distinguishing.

In many dimensions the distances between random points concentrate: the
nearest and the farthest neighbour of a point become almost equally far, so
any method that relies on a nearest neighbour is relying on a difference that
has nearly vanished.

The volume argument says the same thing geometrically. The ball inscribed in
a cube fills 79 percent of it in two dimensions and a quarter of a percent in
ten, so almost all of a high dimensional cube is in its corners.
"""

import math
import random


def distance_spread(dimensions, points, seed=0):
    """The spread of the pairwise distances relative to their mean."""
    generator = random.Random(seed)
    sample = [[generator.random() for _ in range(dimensions)]
              for _ in range(points)]
    distances = []
    for first in range(len(sample)):
        for second in range(first + 1, len(sample)):
            distances.append(sum((a - b) ** 2 for a, b
                                 in zip(sample[first], sample[second])) ** 0.5)
    mean = sum(distances) / len(distances)
    spread = (sum((value - mean) ** 2 for value in distances)
              / len(distances)) ** 0.5
    return {"mean": mean, "spread": spread, "relative spread": spread / mean}


def nearest_versus_farthest(dimensions, points, seed=0):
    """The ratio between the farthest and the nearest neighbour of a point."""
    generator = random.Random(seed)
    sample = [[generator.random() for _ in range(dimensions)]
              for _ in range(points)]
    query = [generator.random() for _ in range(dimensions)]
    distances = [sum((a - b) ** 2 for a, b in zip(query, point)) ** 0.5
                 for point in sample]
    return {"nearest": min(distances), "farthest": max(distances),
            "ratio": max(distances) / min(distances)}


def ball_share(dimensions):
    """The share of a cube filled by its inscribed ball."""
    radius = 0.5
    volume = math.pi ** (dimensions / 2) * radius ** dimensions \
        / math.gamma(dimensions / 2 + 1)
    return volume


def points_for_coverage(dimensions, per_axis):
    """How many points a grid needs to cover the space at a given resolution."""
    return per_axis ** dimensions
