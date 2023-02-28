"""Measures of spread, for metric data and for categories.

Variance and range need numbers. Simpson's index and Leti's index answer the
same question for nominal and ordinal data, and the third sheet computes both
for the beer example: Simpson 0.611, normalised 0.9165, Leti 0.361,
normalised 0.722.

The two indices differ in what they use. Simpson only counts how the mass is
split among categories; Leti reads the cumulative distribution and therefore
notices the order, which is why an ordinal variable gets a different number
from the two.
"""

import math


def variance(data, corrected=True):
    """The variance, by default with the correction for a sample."""
    size = len(data)
    average = sum(data) / size
    total = sum((value - average) ** 2 for value in data)
    return total / (size - 1) if corrected else total / size


def standard_deviation(data, corrected=True):
    """The square root of the variance."""
    return math.sqrt(variance(data, corrected))


def value_range(data):
    """The distance between the largest and the smallest value."""
    return max(data) - min(data)


def interquartile_range(data):
    """The width of the middle half."""
    ordered = sorted(data)
    half = len(ordered) // 2
    lower = ordered[:half]
    upper = ordered[half + 1:] if len(ordered) % 2 else ordered[half:]
    return _median(upper) - _median(lower)


def _median(values):
    """The median of a list, used by the quartiles."""
    ordered = sorted(values)
    size = len(ordered)
    middle = size // 2
    if size % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def mean_absolute_deviation(data, centre):
    """The average distance from a chosen centre.

    Minimal at the median rather than at the mean, which is the counterpart
    of the variance being minimal at the mean, and the reason the median is
    the right centre when deviations are measured in absolute terms.
    """
    return sum(abs(value - centre) for value in data) / len(data)


def relative_frequencies(counts):
    """The shares of the categories."""
    total = sum(counts.values())
    return {name: count / total for name, count in counts.items()}


def simpson(counts):
    """Simpson's index: the chance that two draws differ."""
    shares = relative_frequencies(counts)
    return 1 - sum(share ** 2 for share in shares.values())


def simpson_normalised(counts, digits=None):
    """The index scaled so that an even split gives one.

    With ``digits`` the index is rounded before scaling, as the published
    solution does: 1.5 times the rounded 0.611 gives 0.9165, while the exact
    computation gives 0.9167.
    """
    categories = len(counts)
    if categories < 2:
        return 0.0
    index = simpson(counts)
    if digits is not None:
        index = round(index, digits)
    return index * categories / (categories - 1)


def leti(counts, order):
    """Leti's index, which reads the cumulative shares and so sees the order."""
    shares = relative_frequencies(counts)
    cumulative = 0.0
    total = 0.0
    for name in order[:-1]:
        cumulative += shares[name]
        total += cumulative * (1 - cumulative)
    return total


def leti_normalised(counts, order):
    """Leti's index scaled to the unit interval."""
    categories = len(order)
    if categories < 2:
        return 0.0
    return leti(counts, order) * 4 / (categories - 1)


def coefficient_of_variation(data):
    """The standard deviation relative to the mean, for comparing scales."""
    return standard_deviation(data) / (sum(data) / len(data))
