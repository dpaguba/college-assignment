"""The summary of a column, and which parts of it an outlier moves.

Mean, median, deviation, quartiles, skewness, correlation. Everything here
also appears in the statistics subject; what this module adds is the habit of
computing the whole summary at once, because any single number is easy to
choose to suit a conclusion.
"""

import math


def summary(values):
    """The usual summary of a numeric column."""
    ordered = sorted(values)
    size = len(ordered)
    mean = sum(ordered) / size
    variance = sum((value - mean) ** 2 for value in ordered) / (size - 1) \
        if size > 1 else 0.0
    return {"count": size, "mean": mean, "median": _median(ordered),
            "deviation": math.sqrt(variance), "minimum": ordered[0],
            "maximum": ordered[-1],
            "lower quartile": _median(ordered[:size // 2]),
            "upper quartile": _median(ordered[size // 2 + size % 2:])}


def _median(values):
    """The median of a sorted list."""
    if not values:
        return None
    middle = len(values) // 2
    if len(values) % 2:
        return values[middle]
    return (values[middle - 1] + values[middle]) / 2


def correlation(first, second):
    """Pearson's correlation between two columns."""
    size = len(first)
    mean_first = sum(first) / size
    mean_second = sum(second) / size
    numerator = sum((a - mean_first) * (b - mean_second)
                    for a, b in zip(first, second))
    left = sum((a - mean_first) ** 2 for a in first) ** 0.5
    right = sum((b - mean_second) ** 2 for b in second) ** 0.5
    if left == 0 or right == 0:
        return 0.0
    return numerator / (left * right)


def skewness(values):
    """The third standardised moment, positive for a long right tail."""
    size = len(values)
    mean = sum(values) / size
    deviation = (sum((value - mean) ** 2 for value in values) / size) ** 0.5
    if deviation == 0:
        return 0.0
    return sum((value - mean) ** 3 for value in values) / (size * deviation ** 3)
