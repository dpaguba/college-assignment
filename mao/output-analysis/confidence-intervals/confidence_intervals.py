"""The interval, and the assumption it rests on.

A confidence interval needs independent observations. A simulation produces a
correlated series, so the interval computed from the raw output is too narrow
and the coverage it claims is not the coverage it has. Two standard repairs
exist: run the model many times with different seeds, which gives one
independent observation per run, or batch a single long run, which is the
next module.

The half width falls with the square root of the number of observations, so
halving it costs four times the runs, which is the whole economics of
simulation output analysis.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "simulation-concepts", "queueing-models"))
import queueing_models


def quantile(level):
    """The normal quantile for a two-sided interval at the given level."""
    share = 1 - (1 - level) / 2
    low, high = -10.0, 10.0
    for _ in range(200):
        middle = (low + high) / 2
        if 0.5 * (1 + math.erf(middle / math.sqrt(2))) < share:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def half_width(deviation, size, level):
    """Half the width of the interval."""
    return quantile(level) * deviation / math.sqrt(size)


def interval(values, level=0.95):
    """The interval for the mean of independent observations."""
    size = len(values)
    mean = sum(values) / size
    deviation = math.sqrt(sum((value - mean) ** 2 for value in values)
                          / (size - 1))
    width = half_width(deviation, size, level)
    return {"mean": mean, "half width": width,
            "interval": (mean - width, mean + width)}


def replications(runs, length, seed=0, level=0.95):
    """One observation per independent run, which is the simplest repair."""
    means = []
    for index in range(runs):
        report = queueing_models.simulate_mm1(0.5, 1.0, length, seed=seed + index)
        means.append(report["response time"])
    result = interval(means, level)
    result["means"] = means
    return result


def coverage(repeats, size, seed=0, level=0.95):
    """How often the interval actually contains the mean it estimates."""
    generator = random.Random(seed)
    covered = 0
    for _ in range(repeats):
        values = [generator.gauss(5.0, 2.0) for _ in range(size)]
        low, high = interval(values, level)["interval"]
        if low <= 5.0 <= high:
            covered += 1
    return covered / repeats
