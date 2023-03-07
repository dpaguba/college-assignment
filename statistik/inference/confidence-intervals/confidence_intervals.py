"""Confidence intervals, and what the level actually promises.

A 95 percent interval does not say the parameter lies in this interval with
probability 0.95. The parameter is fixed; the interval is random. What the
level promises is that intervals built this way cover the parameter in 95
percent of samples, which is a statement about the procedure and can
therefore be measured by repeating it, which is what the coverage function
does.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "distributions", "normal-distribution"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "random-variables", "expectation-variance"))
import expectation_variance
import normal_distribution


def width(sigma, size, level):
    """The full width of the interval for a known standard deviation."""
    quantile = normal_distribution.quantile(1 - (1 - level) / 2)
    return 2 * quantile * sigma / math.sqrt(size)


def for_mean(data, level):
    """The interval for the mean, using the sample standard deviation."""
    size = len(data)
    centre = sum(data) / size
    spread = math.sqrt(sum((value - centre) ** 2 for value in data) / (size - 1))
    half = normal_distribution.quantile(1 - (1 - level) / 2) * spread \
        / math.sqrt(size)
    return (centre - half, centre + half)


def for_share(successes, size, level):
    """The interval for a probability, by the normal approximation."""
    share = successes / size
    half = normal_distribution.quantile(1 - (1 - level) / 2) \
        * math.sqrt(share * (1 - share) / size)
    return (share - half, share + half)


def coverage(weights, size, level, repeats, seed=0):
    """How often the interval actually contains the expectation.

    The measurement that gives the level its meaning. It comes out close to
    the nominal level, and the small shortfall for small samples is the
    price of using a normal quantile where the exact distribution would call
    for a t quantile.
    """
    generator = random.Random(seed)
    truth = expectation_variance.expectation(weights)
    covered = 0
    for _ in range(repeats):
        sample = []
        for _ in range(size):
            point = generator.random()
            running = 0.0
            for value, weight in weights.items():
                running += weight
                if point <= running:
                    sample.append(value)
                    break
            else:
                sample.append(list(weights)[-1])
        low, high = for_mean(sample, level)
        if low <= truth <= high:
            covered += 1
    return covered / repeats
