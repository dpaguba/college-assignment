"""Turning uniform numbers into any distribution.

Three methods and the same starting point. The inverse transform applies the
inverse distribution function, which is exact and needs that inverse to
exist. Rejection sampling draws from a box and throws away what falls outside
the density, which needs no inverse and wastes a share of the draws equal to
the empty part of the box. Convolution adds simpler variables, which is how
an Erlang variable is built from exponentials.

The acceptance rate is the measurable part of the second method: for a
triangular density under a box of height two it is exactly one half, and half
the uniform numbers are thrown away.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))
import generators


def exponential(rate, count, seed=0):
    """An exponential sample by the inverse transform."""
    uniforms = generators.uniform_sample(count, seed=seed)
    return [-math.log(1 - value) / rate for value in uniforms if value < 1]


def rejection(density, low, high, ceiling, count, seed=0):
    """A sample from a density by drawing in a box and rejecting."""
    return rejection_report(density, low, high, ceiling, count, seed)["values"]


def rejection_report(density, low, high, ceiling, count, seed=0):
    """The sample together with how many draws were needed."""
    generator = random.Random(seed)
    values = []
    attempts = 0
    while len(values) < count:
        attempts += 1
        candidate = generator.uniform(low, high)
        height = generator.uniform(0, ceiling)
        if height <= density(candidate):
            values.append(candidate)
    return {"values": values, "attempts": attempts,
            "acceptance rate": count / attempts}


def discrete_counts(weights, count, seed=0):
    """How often each outcome is drawn, by the inverse method."""
    generator = random.Random(seed)
    names = list(weights)
    counts = {name: 0 for name in names}
    for _ in range(count):
        point = generator.random()
        running = 0.0
        for name in names:
            running += weights[name]
            if point <= running:
                counts[name] += 1
                break
    return counts


def erlang(shape, rate, count, seed=0):
    """An Erlang sample, built by adding exponential variables."""
    generator = random.Random(seed)
    return [sum(generator.expovariate(rate) for _ in range(shape))
            for _ in range(count)]


def normal_box_muller(count, seed=0):
    """A normal sample from pairs of uniforms.

    The transform that turns two uniform numbers into two normal ones. It is
    the standard example of a method that is exact and has no inverse
    distribution function anywhere in it.
    """
    generator = random.Random(seed)
    values = []
    while len(values) < count:
        first, second = generator.random(), generator.random()
        radius = math.sqrt(-2 * math.log(first))
        values.append(radius * math.cos(2 * math.pi * second))
        values.append(radius * math.sin(2 * math.pi * second))
    return values[:count]
