"""Grouped data, where the class width decides what the picture says.

The second sheet gives heights in six classes of unequal width. Plotting the
counts as bars would put the tallest bar on the class 175 to 185, which has
14 observations spread over 10 centimetres. The histogram plots density,
count divided by width, and the tallest bar becomes 165 to 170 with 12
observations in 5 centimetres.

That is the whole point of the exercise: with unequal classes, the height of
a bar has to be a density, or the picture answers a question nobody asked.
"""


def total(classes):
    """The number of observations across all classes."""
    return sum(count for _, _, count in classes)


def histogram_heights(classes):
    """The density of each class: relative frequency over class width."""
    size = total(classes)
    return [(count / size) / (upper - lower) for lower, upper, count in classes]


def median_class(classes):
    """The class in which the median falls."""
    size = total(classes)
    seen = 0
    for lower, upper, count in classes:
        seen += count
        if seen >= size / 2:
            return (lower, upper)
    raise ValueError("no class holds the median")


def mean(classes):
    """The mean estimated from the class midpoints.

    An approximation, since the raw data is gone. It assumes the
    observations sit at the middle of their class, which is exactly the
    information that was lost by grouping.
    """
    size = total(classes)
    return sum((lower + upper) / 2 * count for lower, upper, count in classes) / size


def variance(classes):
    """The variance estimated the same way."""
    size = total(classes)
    centre = mean(classes)
    return sum(count * ((lower + upper) / 2 - centre) ** 2
               for lower, upper, count in classes) / (size - 1)


def cumulative(classes):
    """The cumulative relative frequency at the upper end of each class."""
    size = total(classes)
    running = 0
    result = []
    for _, upper, count in classes:
        running += count
        result.append((upper, running / size))
    return result


def interpolated_median(classes):
    """The median interpolated linearly inside its class."""
    size = total(classes)
    seen = 0
    for lower, upper, count in classes:
        if seen + count >= size / 2:
            return lower + (size / 2 - seen) / count * (upper - lower)
        seen += count
    raise ValueError("no class holds the median")
