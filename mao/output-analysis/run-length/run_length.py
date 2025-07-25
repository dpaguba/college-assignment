"""How long a run has to be, and why the answer is quadratic.

The half width of a confidence interval falls with the square root of the
number of observations, so halving it needs four times the run. That is the
economics of the whole subject: precision is bought by the square.

The sequential procedure is the practical answer. Run until the interval is
small enough rather than deciding the length in advance, which is what the
lecture recommends and what the module implements.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "confidence-intervals"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "simulation-concepts", "queueing-models"))
import confidence_intervals
import queueing_models


def needed(deviation, half_width, level=0.95):
    """How many observations a given precision needs."""
    quantile = confidence_intervals.quantile(level)
    return math.ceil((quantile * deviation / half_width) ** 2)


def sequential(target, seed=0, level=0.95, limit=200000, block=100):
    """Runs until the interval is narrow enough."""
    generator = random.Random(seed)
    values = []
    while len(values) < limit:
        values.extend(generator.gauss(5.0, 2.0) for _ in range(block))
        report = confidence_intervals.interval(values, level)
        if report["half width"] <= target:
            return {"observations": len(values), "mean": report["mean"],
                    "half width": report["half width"]}
    return {"observations": len(values), "mean": None, "half width": None}


def for_queue(load, target, seed=0, level=0.95, limit=200):
    """How many replications a queue needs for the given precision.

    The heavier the load, the larger the variance of the response time and
    the more replications the same precision costs, which is why a study of a
    congested system is far more expensive than one of an idle system.
    """
    means = []
    for index in range(limit):
        report = queueing_models.simulate_mm1(load, 1.0, 2000, seed=seed + index)
        means.append(report["response time"])
        if len(means) >= 5:
            if confidence_intervals.interval(means, level)["half width"] <= target:
                return len(means)
    return limit
