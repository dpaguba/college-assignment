"""The normal distribution, its tables, and the rule of thumb.

Everything about a normal variable reduces to the standard one by
subtracting the mean and dividing by the standard deviation, which is why a
single table suffices and why the quantiles 1.96 and 1.645 appear in every
confidence interval in the course.

The distribution function has no elementary closed form, so it is computed
from the error function, and the quantile by inverting that numerically.
"""

import math


def pdf(point, mean=0.0, sigma=1.0):
    """The density."""
    z = (point - mean) / sigma
    return math.exp(-z * z / 2) / (sigma * math.sqrt(2 * math.pi))


def cdf(point):
    """The standard distribution function, through the error function."""
    return 0.5 * (1 + math.erf(point / math.sqrt(2)))


def cdf_general(point, mean, sigma):
    """The distribution function of any normal variable, by standardising."""
    return cdf((point - mean) / sigma)


def between(low, high):
    """The probability of falling between two standard deviations."""
    return cdf(high) - cdf(low)


def quantile(share):
    """The point below which the given share lies, by bisection."""
    if not 0 < share < 1:
        raise ValueError("the share has to lie strictly between zero and one")
    low, high = -40.0, 40.0
    for _ in range(200):
        middle = (low + high) / 2
        if cdf(middle) < share:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def sigma_rule():
    """The shares within one, two and three standard deviations."""
    return {1: between(-1, 1), 2: between(-2, 2), 3: between(-3, 3)}
