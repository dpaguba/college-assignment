"""The two limit theorems, measured by simulation.

The law of large numbers says the sample mean approaches the expectation. The
central limit theorem says more: the error, scaled by the square root of the
sample size, approaches a normal distribution whatever the original
distribution was. The first is about where the average goes, the second about
how it is spread on the way, and only the second explains why the normal
distribution appears everywhere.

Chebyshev's inequality is the third statement, and it is the weakest and the
most general: it bounds the tail using only the variance, without assuming
anything about the shape.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "random-variables", "expectation-variance"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "normal-distribution"))
import expectation_variance
import normal_distribution


def _draw(weights, generator):
    """One draw from a discrete distribution."""
    point = generator.random()
    running = 0.0
    for value, weight in weights.items():
        running += weight
        if point <= running:
            return value
    return list(weights)[-1]


def running_averages(weights, size, seed=0):
    """The sample mean after each of the draws."""
    generator = random.Random(seed)
    total = 0.0
    averages = []
    for index in range(1, size + 1):
        total += _draw(weights, generator)
        averages.append(total / index)
    return averages


def error_by_size(weights, sizes, repeats, seed=0):
    """The average absolute error of the sample mean, per sample size."""
    generator = random.Random(seed)
    centre = expectation_variance.expectation(weights)
    report = {}
    for size in sizes:
        total = 0.0
        for _ in range(repeats):
            sample = [_draw(weights, generator) for _ in range(size)]
            total += abs(sum(sample) / size - centre)
        report[size] = total / repeats
    return report


def clt_distance(weights, size, samples, seed=0):
    """The largest gap between the standardised sums and the normal law.

    A Kolmogorov distance: the sums are standardised and their empirical
    distribution function is compared with the normal one at every sample
    point. It shrinks as the number of summands grows, which is the theorem
    stated as a measurement.
    """
    generator = random.Random(seed)
    centre = expectation_variance.expectation(weights)
    spread = expectation_variance.standard_deviation(weights)
    standardised = []
    for _ in range(samples):
        total = sum(_draw(weights, generator) for _ in range(size))
        standardised.append((total - size * centre) / (spread * math.sqrt(size)))
    standardised.sort()
    largest = 0.0
    for index, point in enumerate(standardised):
        empirical = (index + 1) / samples
        largest = max(largest, abs(empirical - normal_distribution.cdf(point)))
    return largest


def chebyshev_bound(deviations):
    """The bound on the probability of being that many deviations away."""
    if deviations <= 0:
        raise ValueError("the number of deviations has to be positive")
    return 1 / deviations ** 2
