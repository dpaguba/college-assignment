"""The k-means family: same loop, different notion of a centre.

k-means moves each centre to the mean, k-medoid to the most central actual
point, k-median to the coordinatewise median and k-mode to the most frequent
value. The loop is identical and the choice of centre decides what the method
is robust to and what kind of data it accepts.

The outlier is the case that separates them. One point at a hundred drags a
mean centre most of the way there, and leaves a medoid where it was.
"""

import random


def _distance(first, second):
    """The squared Euclidean distance."""
    return sum((a - b) ** 2 for a, b in zip(first, second))


def _assign(points, centres):
    """Each point to the nearest centre."""
    return [min(range(len(centres)),
                key=lambda index: _distance(point, centres[index]))
            for point in points]


def _loop(points, clusters, seed, centre_of, steps=100):
    """The shared loop, with the centre computed by the given function."""
    generator = random.Random(seed)
    centres = list(generator.sample(list(points), clusters))
    labels = []
    for _ in range(steps):
        labels = _assign(points, centres)
        following = []
        for index in range(clusters):
            members = [point for point, label in zip(points, labels)
                       if label == index]
            following.append(centre_of(members) if members else centres[index])
        if following == centres:
            break
        centres = following
    return {"labels": labels, "centres": centres}


def k_means(points, clusters, seed=0):
    """Centres at the mean of their members."""
    return _loop(points, clusters, seed,
                 lambda members: tuple(sum(values) / len(members)
                                       for values in zip(*members)))


def k_medoid(points, clusters, seed=0):
    """Centres at an actual point, the one closest to all the others."""
    def centre(members):
        """The member minimising the distance to the rest."""
        return min(members, key=lambda candidate:
                   sum(_distance(candidate, other) for other in members))
    return _loop(points, clusters, seed, centre)


def k_median(points, clusters, seed=0):
    """Centres at the coordinatewise median, which minimises absolute distance."""
    def centre(members):
        """The coordinatewise median of the members."""
        return tuple(_median(sorted(values)) for values in zip(*members))
    return _loop(points, clusters, seed, centre)


def _median(values):
    """The median of a sorted list."""
    middle = len(values) // 2
    if len(values) % 2:
        return values[middle]
    return (values[middle - 1] + values[middle]) / 2


def k_mode(rows, clusters, seed=0):
    """Centres at the most frequent value per attribute, for categorical data.

    The distance is the number of attributes that differ, so the method needs
    no numbers at all, which is what makes it the variant for survey data.
    """
    def distance(first, second):
        """How many attributes differ."""
        return sum(1 for a, b in zip(first, second) if a != b)

    def centre(members):
        """The most frequent value in each position."""
        return tuple(max(set(values), key=list(values).count)
                     for values in zip(*members))

    generator = random.Random(seed)
    centres = list(generator.sample(list(rows), clusters))
    for _ in range(50):
        labels = [min(range(len(centres)),
                      key=lambda index: distance(row, centres[index]))
                  for row in rows]
        following = []
        for index in range(clusters):
            members = [row for row, label in zip(rows, labels) if label == index]
            following.append(centre(members) if members else centres[index])
        if following == centres:
            break
        centres = following
    return {"labels": labels, "centres": centres}
