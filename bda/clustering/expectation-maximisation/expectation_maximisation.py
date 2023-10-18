"""Expectation maximisation: clustering with soft membership.

k-means assigns each point to one cluster. A mixture model gives each point a
probability of belonging to each component, and the algorithm alternates
between computing those probabilities and refitting the components to them.

The likelihood never falls, which is the guarantee the method offers, and it
converges to a local optimum, which is the guarantee it does not. A point
between two components keeps a share of both, and that is the difference from
the hard assignment worth seeing.
"""

import math
import random


def fit(values, components, seed=0, steps=200):
    """A one-dimensional Gaussian mixture, with the trace of the likelihood."""
    generator = random.Random(seed)
    means = generator.sample(list(values), components)
    variances = [1.0] * components
    weights = [1 / components] * components
    trace = []
    responsibilities = []
    for _ in range(steps):
        responsibilities = []
        for value in values:
            densities = [weights[index] * _density(value, means[index],
                                                   variances[index])
                         for index in range(components)]
            total = sum(densities) or 1e-300
            responsibilities.append([density / total for density in densities])
        trace.append(sum(math.log(sum(weights[index]
                                      * _density(value, means[index],
                                                 variances[index])
                                      for index in range(components)) + 1e-300)
                         for value in values))
        for index in range(components):
            mass = sum(row[index] for row in responsibilities) or 1e-300
            means[index] = sum(row[index] * value
                               for row, value in zip(responsibilities,
                                                     values)) / mass
            variances[index] = max(1e-6, sum(
                row[index] * (value - means[index]) ** 2
                for row, value in zip(responsibilities, values)) / mass)
            weights[index] = mass / len(values)
        if len(trace) > 2 and abs(trace[-1] - trace[-2]) < 1e-12:
            break
    return {"means": means, "variances": variances, "weights": weights,
            "responsibilities": responsibilities, "log likelihood": trace}


def _density(value, mean, variance):
    """The Gaussian density."""
    return math.exp(-(value - mean) ** 2 / (2 * variance)) \
        / math.sqrt(2 * math.pi * variance)


def hard_assignment(report):
    """The component with the largest responsibility for each point."""
    return [max(range(len(row)), key=lambda index: row[index])
            for row in report["responsibilities"]]
