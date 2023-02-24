"""Covariance, Pearson's correlation, and the rank version.

Covariance measures whether two variables deviate from their means in the
same direction, and its size depends on the units. Dividing by the two
standard deviations removes them, which is why the correlation is comparable
and the covariance is not.

For the children's data of the third sheet: covariance 14, standard
deviations 2 and 7.746, correlation 0.904.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "descriptive", "dispersion"))
import dispersion


def covariance(first, second, corrected=True):
    """The average product of the two deviations from the means."""
    size = len(first)
    mean_first = sum(first) / size
    mean_second = sum(second) / size
    total = sum((left - mean_first) * (right - mean_second)
                for left, right in zip(first, second))
    return total / (size - 1) if corrected else total / size


def pearson(first, second):
    """The correlation coefficient of Bravais and Pearson."""
    return covariance(first, second) / (dispersion.standard_deviation(first)
                                        * dispersion.standard_deviation(second))


def ranks(values):
    """The ranks of the values, averaging the ranks of ties."""
    order = sorted(range(len(values)), key=lambda index: values[index])
    result = [0.0] * len(values)
    position = 0
    while position < len(order):
        end = position
        while end + 1 < len(order) and values[order[end + 1]] == values[order[position]]:
            end += 1
        average = (position + end) / 2 + 1
        for index in range(position, end + 1):
            result[order[index]] = average
        position = end + 1
    return result


def spearman(first, second):
    """Pearson's coefficient applied to the ranks.

    Invariant under any monotone transformation of either variable, because
    a monotone map does not change ranks. That is what it measures: whether
    the two variables rise together, without assuming they do so linearly.
    """
    return pearson(ranks(first), ranks(second))


def is_uncorrelated_but_dependent():
    """A dependent pair with zero correlation, as the lecture warns.

    The points of a symmetric parabola: the correlation is exactly zero and
    the dependence is complete, since one variable determines the other.
    """
    x = [-2, -1, 0, 1, 2]
    y = [value ** 2 for value in x]
    return abs(pearson(x, y)) < 1e-12
