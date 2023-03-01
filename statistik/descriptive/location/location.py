"""Measures of location, and which of them an outlier can move.

Three answers to "where is the middle": the value that occurs most often, the
value in the middle of the sorted sample, and the balance point. They differ
on the exam data of the first sheet, where the mode is 2, the median is 2 and
the mean is 2.5, and they differ far more once a single extreme value is
added.
"""

from collections import Counter


def sample_size(data):
    """How many observations there are."""
    return len(data)


def mode(data):
    """Every most frequent value, since the mode need not be unique."""
    counts = Counter(data)
    largest = max(counts.values())
    return sorted(value for value, count in counts.items() if count == largest)


def median(data):
    """The middle value, averaging the two middle ones for an even sample."""
    ordered = sorted(data)
    size = len(ordered)
    if size == 0:
        raise ValueError("the median of an empty sample is not defined")
    middle = size // 2
    if size % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def mean(data):
    """The arithmetic mean."""
    return sum(data) / len(data)


def geometric_mean(data):
    """The mean for rates of growth, which multiply rather than add.

    Averaging growth factors arithmetically overstates the result: doubling
    and then quartering is a factor of one half overall, and the geometric
    mean of 2 and 0.25 is 0.707 while the arithmetic mean is 1.125.
    """
    product = 1.0
    for value in data:
        if value <= 0:
            raise ValueError("the geometric mean needs positive values")
        product *= value
    return product ** (1 / len(data))


def harmonic_mean(data):
    """The mean for rates per unit, such as speeds over equal distances."""
    return len(data) / sum(1 / value for value in data)


def trimmed_mean(data, share):
    """The mean after dropping the given share at each end."""
    ordered = sorted(data)
    drop = int(len(ordered) * share)
    kept = ordered[drop:len(ordered) - drop] or ordered
    return sum(kept) / len(kept)
