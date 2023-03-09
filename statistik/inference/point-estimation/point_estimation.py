"""Point estimation, and the correction that makes the variance unbiased.

An estimator is a random variable, so it has a distribution, an expectation
and a variance of its own. It is unbiased when its expectation is the
parameter, and the sample variance is the standard example of what goes
wrong: dividing by n understates the variance by exactly a factor (n-1)/n,
because the deviations are measured from the sample mean rather than from the
true mean, and the sample mean is closer to the data than the truth is.

The bias is measured here by simulation rather than derived, so the size of
the correction is a number: for samples of four from the modified die, the
uncorrected estimator is low by a quarter of the variance.
"""

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "random-variables", "expectation-variance"))
import expectation_variance


def _draw(weights, generator):
    """One draw from a discrete distribution."""
    point = generator.random()
    running = 0.0
    for value, weight in weights.items():
        running += weight
        if point <= running:
            return value
    return list(weights)[-1]


def sample(weights, size, generator):
    """A sample of the given size."""
    return [_draw(weights, generator) for _ in range(size)]


def bias_of_mean(weights, size, repeats, seed=0):
    """The average error of the sample mean over many samples."""
    generator = random.Random(seed)
    truth = expectation_variance.expectation(weights)
    total = 0.0
    for _ in range(repeats):
        values = sample(weights, size, generator)
        total += sum(values) / size
    return {"estimate": total / repeats, "truth": truth,
            "bias": total / repeats - truth}


def bias_of_variance(weights, size, repeats, seed=0):
    """The bias of both variance estimators, measured the same way."""
    generator = random.Random(seed)
    truth = expectation_variance.variance(weights)
    corrected_total = 0.0
    uncorrected_total = 0.0
    for _ in range(repeats):
        values = sample(weights, size, generator)
        centre = sum(values) / size
        squares = sum((value - centre) ** 2 for value in values)
        corrected_total += squares / (size - 1)
        uncorrected_total += squares / size
    return {"truth": truth,
            "corrected bias": corrected_total / repeats - truth,
            "uncorrected bias": uncorrected_total / repeats - truth}


def mean_squared_error(weights, size, repeats, seed=0):
    """The error of the sample mean, split into bias and variance."""
    generator = random.Random(seed)
    truth = expectation_variance.expectation(weights)
    estimates = []
    for _ in range(repeats):
        values = sample(weights, size, generator)
        estimates.append(sum(values) / size)
    average = sum(estimates) / repeats
    variance = sum((value - average) ** 2 for value in estimates) / repeats
    mse = sum((value - truth) ** 2 for value in estimates) / repeats
    return {"bias": average - truth, "variance": variance, "mse": mse}


def moment_estimate_poisson(data):
    """The rate estimated by matching the first moment."""
    return sum(data) / len(data)


def moment_estimate_uniform(data):
    """The endpoints estimated by matching the first two moments."""
    size = len(data)
    centre = sum(data) / size
    spread = sum((value - centre) ** 2 for value in data) / size
    half_width = (3 * spread) ** 0.5
    return (centre - half_width, centre + half_width)
