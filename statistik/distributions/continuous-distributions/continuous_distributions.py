"""The continuous distributions of chapter eight.

A density is not a probability: it may exceed one, and only its integral over
an interval is a probability. The sixth sheet asks for the expectation and
variance of the uniform distribution from the definition, and both are
computed here symbolically and by numerical integration, so the formula is
checked against the integral it stands for.
"""

import math


def uniform_density(low, high, point):
    """The constant density on the interval, zero outside it."""
    return 1 / (high - low) if low <= point <= high else 0.0


def uniform_cdf(low, high, point):
    """The distribution function, a straight line on the interval."""
    if point <= low:
        return 0.0
    if point >= high:
        return 1.0
    return (point - low) / (high - low)


def uniform_mean(low, high):
    """The midpoint of the interval."""
    return (low + high) / 2


def uniform_variance(low, high):
    """The width squared over twelve."""
    return (high - low) ** 2 / 12


def exponential_density(rate, point):
    """The density of the waiting time at a constant rate."""
    return rate * math.exp(-rate * point) if point >= 0 else 0.0


def exponential_cdf(rate, point):
    """The probability of having waited at most this long."""
    return 1 - math.exp(-rate * point) if point >= 0 else 0.0


def exponential_mean(rate):
    """The expected waiting time."""
    return 1 / rate


def exponential_variance(rate):
    """The variance, the square of the mean."""
    return 1 / rate ** 2


def exponential_is_memoryless(rate, tolerance=1e-9):
    """Whether having waited changes nothing about the remaining wait.

    The continuous counterpart of the geometric property, and the reason the
    exponential distribution is the one used for lifetimes without ageing.
    """
    for waited in (0.5, 1.0, 2.0):
        for further in (0.5, 1.0, 2.0):
            survived = math.exp(-rate * waited)
            joint = math.exp(-rate * (waited + further))
            if abs(joint / survived - math.exp(-rate * further)) > tolerance:
                return False
    return True


def numeric_mean(density, low, high, steps=200000):
    """The expectation by numerical integration of x times the density."""
    width = (high - low) / steps
    total = 0.0
    for step in range(steps):
        point = low + (step + 0.5) * width
        total += point * density(point) * width
    return total


def numeric_variance(density, low, high, steps=200000):
    """The variance by numerical integration."""
    centre = numeric_mean(density, low, high, steps)
    width = (high - low) / steps
    total = 0.0
    for step in range(steps):
        point = low + (step + 0.5) * width
        total += (point - centre) ** 2 * density(point) * width
    return total
