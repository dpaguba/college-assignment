"""Expectation and variance, and the shortcut that is easy to misuse.

The expectation is the balance point of the distribution and need not be a
value the variable can take: the modified die of the fifth sheet has faces 1,
3, 3, 4, 4, 6 and expectation 3.5, which is not a face. Its variance is 2.25,
against 2.917 for a fair die, and both dice have the same expectation, which
is the point of the exercise.
"""


def expectation(weights):
    """The weighted average of the values."""
    return sum(value * weight for value, weight in weights.items())


def second_moment(weights):
    """The expectation of the square."""
    return sum(value ** 2 * weight for value, weight in weights.items())


def variance(weights):
    """The expected squared deviation from the expectation."""
    centre = expectation(weights)
    return sum((value - centre) ** 2 * weight
               for value, weight in weights.items())


def standard_deviation(weights):
    """The square root of the variance, in the units of the variable."""
    return variance(weights) ** 0.5


def moment(weights, order, central=False):
    """The moment of the given order, raw or about the expectation."""
    centre = expectation(weights) if central else 0.0
    return sum((value - centre) ** order * weight
               for value, weight in weights.items())


def skewness(weights):
    """The third standardised moment, which is zero for a symmetric variable."""
    deviation = standard_deviation(weights)
    return moment(weights, 3, central=True) / deviation ** 3


def median(weights):
    """The smallest value whose cumulative probability reaches one half."""
    running = 0.0
    for value in sorted(weights):
        running += weights[value]
        if running >= 0.5:
            return value
    raise ValueError("the weights do not sum to one")
