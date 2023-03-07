"""Tests, their two errors, and the power that connects them.

A test is a rule for deciding, so its result is a random variable and it can
be wrong in two ways. The level fixes how often it rejects a true hypothesis;
the power is how often it rejects a false one, and it depends on how false
the hypothesis is. Lowering the level lowers the power, which is the trade
the chapter is about and which the simulations here measure.
"""

import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "distributions", "normal-distribution"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "bivariate", "association-measures"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "random-variables", "expectation-variance"))
import association_measures
import expectation_variance
import normal_distribution


def one_sample(data, null_mean, level):
    """The test of a mean against a fixed value.

    The statistic is the standardised distance between the sample mean and
    the hypothesised one. It is compared with a normal quantile, which is the
    large-sample version; for small samples the exact distribution is a t
    distribution and the critical value is slightly larger.
    """
    size = len(data)
    centre = sum(data) / size
    spread = math.sqrt(sum((value - centre) ** 2 for value in data) / (size - 1))
    statistic = (centre - null_mean) / (spread / math.sqrt(size))
    critical = normal_distribution.quantile(1 - level / 2)
    probability = 2 * (1 - normal_distribution.cdf(abs(statistic)))
    return {"statistic": statistic, "critical": critical,
            "p value": probability, "reject": abs(statistic) > critical}


def first_kind_rate(weights, size, level, repeats, seed=0):
    """How often the test rejects a hypothesis that is true."""
    generator = random.Random(seed)
    truth = expectation_variance.expectation(weights)
    rejected = 0
    for _ in range(repeats):
        sample = _sample(weights, size, generator)
        if one_sample(sample, truth, level)["reject"]:
            rejected += 1
    return rejected / repeats


def power(distance, size, level, repeats, seed=0):
    """How often the test rejects a hypothesis that is wrong by this much."""
    generator = random.Random(seed)
    rejected = 0
    for _ in range(repeats):
        sample = [generator.gauss(distance, 1.0) for _ in range(size)]
        if one_sample(sample, 0.0, level)["reject"]:
            rejected += 1
    return rejected / repeats


def independence_test(table, level):
    """The chi-square test of independence in a contingency table."""
    statistic = association_measures.chi_square(table)
    rows = len(table)
    columns = len(next(iter(table.values())))
    degrees = (rows - 1) * (columns - 1)
    critical = _chi_square_quantile(degrees, 1 - level)
    return {"statistic": statistic, "degrees": degrees, "critical": critical,
            "reject": statistic > critical}


def sign_test(data, null_median, level):
    """A test of the median that assumes no distribution at all.

    It counts how many observations lie above the hypothesised median and
    compares that count with a binomial distribution. Nothing about the shape
    of the data enters, which is why it survives the outlier that would move
    a mean-based test.
    """
    above = sum(1 for value in data if value > null_median)
    size = sum(1 for value in data if value != null_median)
    probability = 0.0
    for count in range(size + 1):
        term = math.comb(size, count) * 0.5 ** size
        if abs(count - size / 2) >= abs(above - size / 2):
            probability += term
    return {"above": above, "size": size, "p value": probability,
            "reject": probability <= level}


def _sample(weights, size, generator):
    """A sample from a discrete distribution."""
    values = []
    for _ in range(size):
        point = generator.random()
        running = 0.0
        for value, weight in weights.items():
            running += weight
            if point <= running:
                values.append(value)
                break
        else:
            values.append(list(weights)[-1])
    return values


def _chi_square_quantile(degrees, share):
    """The quantile of the chi-square distribution, by bisection."""
    low, high = 0.0, 1000.0
    for _ in range(200):
        middle = (low + high) / 2
        if _chi_square_cdf(degrees, middle) < share:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def _chi_square_cdf(degrees, point):
    """The distribution function, through the regularised incomplete gamma.

    Numerical integration fails here for one degree of freedom, where the
    density has a pole at zero: a midpoint rule misses the mass near the
    origin and reports 0.9425 at the point where the true value is 0.95, so
    the critical value comes out unbounded. The series below has no such
    problem.
    """
    if point <= 0:
        return 0.0
    return _regularised_gamma(degrees / 2, point / 2)


def _regularised_gamma(shape, point):
    """The lower regularised incomplete gamma function.

    A series for small arguments and a continued fraction for large ones,
    which is the standard split: each converges quickly exactly where the
    other does not.
    """
    if point < shape + 1:
        term = 1.0 / shape
        total = term
        index = shape
        for _ in range(500):
            index += 1
            term *= point / index
            total += term
            if abs(term) < abs(total) * 1e-15:
                break
        return total * math.exp(-point + shape * math.log(point)
                                - math.lgamma(shape))
    tiny = 1e-300
    first = point + 1 - shape
    coefficient = 1 / tiny
    second = 1 / first
    fraction = second
    for index in range(1, 500):
        step = -index * (index - shape)
        first += 2
        second = first + step * second
        if abs(second) < tiny:
            second = tiny
        coefficient = first + step / coefficient
        if abs(coefficient) < tiny:
            coefficient = tiny
        second = 1 / second
        change = second * coefficient
        fraction *= change
        if abs(change - 1) < 1e-15:
            break
    upper = math.exp(-point + shape * math.log(point)
                     - math.lgamma(shape)) * fraction
    return 1 - upper
