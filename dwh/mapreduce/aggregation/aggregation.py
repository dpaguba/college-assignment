"""Aggregating in the model, and the three kinds of measure.

A distributive measure such as a sum can be computed on parts and combined.
An algebraic one such as the mean can be, once the parts carry enough state:
the sum and the count rather than the mean. A holistic one such as an exact
distinct count cannot be combined at all, which is why approximate versions
of it exist.

That classification decides whether a combiner is possible, and the combiner
is what keeps the shuffle small.
"""

COMBINABLE = {"sum": True, "count": True, "maximum": True, "minimum": True,
              "mean": False, "median": False, "distinct count": False,
              "approximate distinct count": True, "variance": False}
"""Which measures can be combined without extra state."""


def combinable(measure):
    """Whether a combiner can be used for the measure as it stands."""
    if measure not in COMBINABLE:
        raise ValueError("unknown measure: %s" % measure)
    return COMBINABLE[measure]


def partial_mean(values):
    """The state that makes a mean combinable: the sum and the count."""
    return {"sum": sum(values), "count": len(values)}


def merge_means(partials):
    """The mean assembled from the partial states."""
    total = sum(part["sum"] for part in partials)
    count = sum(part["count"] for part in partials)
    return total / count if count else 0.0


def combiner_effect(records):
    """How many pairs cross the network with and without a combiner."""
    without = len(records)
    counts = {}
    for record in records:
        counts[record] = counts.get(record, 0) + 1
    return {"without combiner": without, "with combiner": len(counts)}
