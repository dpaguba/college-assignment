"""Data quality: missing values, outliers, and the cost of each repair.

Every repair loses something. Dropping incomplete rows loses observations,
dropping incomplete columns loses variables, and imputing the mean keeps both
and lowers the variance, which makes every subsequent confidence interval too
narrow.

The module measures that last effect rather than warning about it: filling
one value of four with the mean leaves the mean unchanged and reduces the
variance, which is exactly the bias the method introduces.
"""


def missing(rows):
    """How many values are missing in each column."""
    counts = {}
    for row in rows:
        for name, value in row.items():
            counts.setdefault(name, 0)
            if value is None:
                counts[name] += 1
    return counts


def drop_incomplete_rows(rows):
    """The rows with no missing value."""
    return [row for row in rows if all(value is not None
                                       for value in row.values())]


def drop_incomplete_columns(rows):
    """The rows restricted to the columns that are complete everywhere."""
    incomplete = {name for name, count in missing(rows).items() if count}
    return [{name: value for name, value in row.items()
             if name not in incomplete} for row in rows]


def impute_mean(values):
    """The values with the missing ones replaced by the mean of the rest."""
    known = [value for value in values if value is not None]
    average = sum(known) / len(known)
    return [average if value is None else value for value in values]


def variance(values):
    """The sample variance."""
    average = sum(values) / len(values)
    return sum((value - average) ** 2 for value in values) / (len(values) - 1)


def outliers(values, factor=1.5):
    """The values beyond the interquartile fence."""
    ordered = sorted(values)
    half = len(ordered) // 2
    lower = _median(ordered[:half])
    upper = _median(ordered[half + 1:] if len(ordered) % 2 else ordered[half:])
    width = upper - lower
    return [value for value in ordered
            if value < lower - factor * width or value > upper + factor * width]


def _median(values):
    """The median of a list."""
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def normalise(values):
    """The values scaled to the unit interval."""
    low, high = min(values), max(values)
    span = high - low
    if span == 0:
        return [0.0 for _ in values]
    return [(value - low) / span for value in values]


def standardise(values):
    """The values shifted and scaled to mean zero and variance one."""
    average = sum(values) / len(values)
    spread = variance(values) ** 0.5
    if spread == 0:
        return [0.0 for _ in values]
    return [(value - average) / spread for value in values]
