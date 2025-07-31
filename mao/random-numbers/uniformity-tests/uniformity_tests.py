"""Testing a generator: uniformity is necessary and nowhere near sufficient.

The chi-square test compares the counts in buckets against what uniformity
predicts. A stream that alternates between two values passes it easily, and
that is the point of the module: uniformity is a property of the marginal
distribution and says nothing about the order.

The serial correlation and the gap test look at the order, and the
alternating stream fails both immediately.
"""

import math


def chi_square(values, buckets):
    """The chi-square test of uniformity over the unit interval."""
    counts = [0] * buckets
    for value in values:
        index = min(buckets - 1, int(value * buckets))
        counts[index] += 1
    expected = len(values) / buckets
    statistic = sum((count - expected) ** 2 / expected for count in counts)
    return {"statistic": statistic, "degrees": buckets - 1,
            "p value": _chi_square_tail(buckets - 1, statistic)}


def _chi_square_tail(degrees, point):
    """The probability of exceeding the statistic, by the incomplete gamma."""
    if point <= 0:
        return 1.0
    return 1.0 - _regularised_gamma(degrees / 2, point / 2)


def _regularised_gamma(shape, point):
    """The lower regularised incomplete gamma function."""
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
    return 1 - math.exp(-point + shape * math.log(point)
                        - math.lgamma(shape)) * fraction


def serial_correlation(values):
    """The correlation between each value and the next.

    Zero for an independent stream and close to minus one for an alternating
    one, which is the pattern the bucket test cannot see.
    """
    size = len(values) - 1
    mean = sum(values) / len(values)
    numerator = sum((values[index] - mean) * (values[index + 1] - mean)
                    for index in range(size))
    denominator = sum((value - mean) ** 2 for value in values)
    return numerator / denominator if denominator else 0.0


def gap_test(values, low, high):
    """The distances between consecutive values inside an interval.

    For an independent stream the gaps are geometric with the probability of
    the interval, so their mean is one over that probability: an interval of
    width one half gives a mean gap of two.
    """
    gaps = []
    last = None
    for index, value in enumerate(values):
        if low <= value < high:
            if last is not None:
                gaps.append(index - last)
            last = index
    return {"gaps": len(gaps),
            "mean gap": sum(gaps) / len(gaps) if gaps else 0.0}
