"""Testing whether the fitted distribution matches the data.

The Kolmogorov-Smirnov statistic is the largest vertical distance between the
empirical distribution function and the fitted one. It uses every observation
and needs no buckets, which is why the lecture prefers it for continuous data;
the chi-square test needs buckets and enough observations in each of them,
and the module refuses rather than producing a number from three points.

A test that does not reject is not a test that confirms. With enough data
every fitted distribution is eventually rejected, because no family is
exactly right, and that is the reason the lecture treats fitting as a
modelling decision rather than a statistical one.
"""

import math


def kolmogorov_smirnov(values, cdf):
    """The largest distance between the empirical and the fitted function."""
    ordered = sorted(values)
    size = len(ordered)
    largest = 0.0
    for index, value in enumerate(ordered):
        theoretical = cdf(value)
        largest = max(largest, abs((index + 1) / size - theoretical),
                      abs(theoretical - index / size))
    scaled = largest * math.sqrt(size)
    return {"statistic": largest, "scaled": scaled,
            "p value": _kolmogorov_tail(scaled)}


def _kolmogorov_tail(scaled):
    """The asymptotic probability of exceeding the scaled statistic."""
    if scaled <= 0:
        return 1.0
    total = 0.0
    for index in range(1, 100):
        total += (-1) ** (index - 1) * math.exp(-2 * index ** 2 * scaled ** 2)
    return max(0.0, min(1.0, 2 * total))


def chi_square(values, cdf, buckets):
    """The bucketed test, which needs enough observations in every bucket."""
    if len(values) < 5 * buckets:
        raise ValueError("the chi-square test needs at least five per bucket")
    edges = [index / buckets for index in range(buckets + 1)]
    counts = [0] * buckets
    for value in values:
        position = cdf(value)
        index = min(buckets - 1, int(position * buckets))
        counts[index] += 1
    expected = len(values) / buckets
    statistic = sum((count - expected) ** 2 / expected for count in counts)
    return {"statistic": statistic, "degrees": buckets - 1, "edges": edges}
