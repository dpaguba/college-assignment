"""Quantiles, the empirical distribution function, and the boxplot.

The course defines the quartiles as the medians of the two halves of the
sorted sample, which is one of several conventions and the one reproduced
here: for the exam data it gives 2 and 3, as the published solution says.
Statistical software often uses an interpolating definition and gets other
numbers on the same data, so the convention has to be stated.
"""


def _median(values):
    """The median of a list."""
    ordered = sorted(values)
    size = len(ordered)
    middle = size // 2
    if size % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def lower_quartile(data):
    """The median of the lower half, excluding a middle value."""
    ordered = sorted(data)
    half = len(ordered) // 2
    return _median(ordered[:half])


def upper_quartile(data):
    """The median of the upper half."""
    ordered = sorted(data)
    half = len(ordered) // 2
    upper = ordered[half + 1:] if len(ordered) % 2 else ordered[half:]
    return _median(upper)


def quantile(data, share):
    """The value below which the given share of the sample lies."""
    ordered = sorted(data)
    if share == 0.5:
        return _median(ordered)
    position = share * len(ordered)
    if position.is_integer():
        index = int(position)
        return (ordered[index - 1] + ordered[index]) / 2
    return ordered[int(position)]


def empirical_cdf(data, point):
    """The share of observations at most the given point."""
    return sum(1 for value in data if value <= point) / len(data)


def boxplot(data):
    """The five numbers a boxplot draws."""
    return {"minimum": min(data), "lower": lower_quartile(data),
            "median": _median(data), "upper": upper_quartile(data),
            "maximum": max(data)}


def outliers(data, factor=1.5):
    """The points more than the given number of boxes beyond a quartile."""
    lower = lower_quartile(data)
    upper = upper_quartile(data)
    width = upper - lower
    return [value for value in sorted(data)
            if value < lower - factor * width or value > upper + factor * width]


def whiskers(data, factor=1.5):
    """The ends of the whiskers, which stop at the last point inside the fence."""
    lower = lower_quartile(data)
    upper = upper_quartile(data)
    width = upper - lower
    inside = [value for value in data
              if lower - factor * width <= value <= upper + factor * width]
    return (min(inside), max(inside))
