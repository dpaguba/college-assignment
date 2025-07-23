"""Batch means: one long run turned into a few independent observations.

Consecutive observations of a simulation are correlated, so the usual
confidence interval computed from them is too narrow. Averaging blocks of
consecutive observations removes most of the correlation, because the
correlation decays with the distance and a batch mean averages over many
distances at once.

The trade is between the number of batches and their length. Few long batches
are nearly independent and give a wide interval because there are few of
them; many short batches are still correlated and give an interval that is
too narrow. The module measures the correlation of the batch means so the
choice can be made on evidence.
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "confidence-intervals"))
import confidence_intervals


def correlation(values):
    """The correlation between consecutive observations."""
    mean = sum(values) / len(values)
    numerator = sum((values[index] - mean) * (values[index + 1] - mean)
                    for index in range(len(values) - 1))
    denominator = sum((value - mean) ** 2 for value in values)
    return numerator / denominator if denominator else 0.0


def deviation(values):
    """The sample standard deviation."""
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values)
                     / (len(values) - 1))


def split(values, count):
    """The trace split into that many batches of equal length."""
    size = len(values) // count
    return [values[index * size:(index + 1) * size] for index in range(count)]


def analyse(values, batches, level=0.95):
    """The estimate and interval from batch means, with both correlations."""
    blocks = split(values, batches)
    means = [sum(block) / len(block) for block in blocks]
    result = confidence_intervals.interval(means, level)
    return {"estimate": result["mean"], "half width": result["half width"],
            "raw correlation": correlation(values),
            "batch correlation": correlation(means),
            "batch size": len(blocks[0])}
