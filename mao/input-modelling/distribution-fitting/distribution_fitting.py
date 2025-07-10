"""Choosing a distribution for the input, and reading the data for a hint.

The coefficient of variation is the quantity that points at the family. An
exponential distribution has it equal to one, an Erlang below one, and a
hyperexponential above, so computing it from the sample narrows the choice
before any fitting happens.

The parameters then come from matching moments, which is the method the
lecture uses because it is exact for these families and needs no search.
"""

import math


def mean(values):
    """The sample mean."""
    return sum(values) / len(values)


def deviation(values):
    """The sample standard deviation, with the correction."""
    average = mean(values)
    return math.sqrt(sum((value - average) ** 2 for value in values)
                     / (len(values) - 1))


def coefficient_of_variation(values):
    """The deviation relative to the mean, which points at the family."""
    average = mean(values)
    return deviation(values) / average if average else 0.0


def suggest(coefficient, tolerance=0.1):
    """The family the coefficient of variation suggests."""
    if abs(coefficient - 1) <= tolerance:
        return "exponential"
    if coefficient < 1:
        return "Erlang"
    return "hyperexponential"


def exponential_rate(values):
    """The rate of an exponential distribution, from the mean."""
    return 1 / mean(values)


def normal(values):
    """The mean and deviation of a normal distribution."""
    return {"mean": mean(values), "deviation": deviation(values)}


def erlang(values):
    """The shape and rate of an Erlang distribution, by matching two moments."""
    coefficient = coefficient_of_variation(values)
    if coefficient >= 1:
        return None
    shape = max(1, round(1 / coefficient ** 2))
    return {"shape": shape, "rate": shape / mean(values)}


def uniform(values):
    """The endpoints of a uniform distribution, by matching two moments."""
    average = mean(values)
    spread = deviation(values) * math.sqrt(3)
    return {"low": average - spread, "high": average + spread}
