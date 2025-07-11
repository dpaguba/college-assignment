"""Using the data itself as the distribution, and what that costs.

The empirical distribution function puts equal weight on every observation,
so sampling from it means drawing observations at random. Nothing is assumed
about the shape, and nothing beyond the observed range can ever be produced,
which is the whole trade: a fitted distribution can extrapolate and might be
wrong, an empirical one cannot extrapolate and cannot be wrong about what it
never saw.

For a queue that is the wrong side of the trade, because the tail of the
service time distribution is what fills the buffer.
"""

import random


def from_sample(values):
    """The empirical distribution function of a sample."""
    ordered = sorted(values)

    def cdf(point):
        """The share of observations at most the point."""
        return sum(1 for value in ordered if value <= point) / len(ordered)

    return {"values": ordered, "cdf": cdf}


def sample(values, count, seed=0):
    """Draws from the empirical distribution, which is drawing observations."""
    generator = random.Random(seed)
    return [generator.choice(values) for _ in range(count)]


def tail_is_lost(values):
    """Whether the empirical distribution can produce anything beyond the data.

    It cannot, by construction, and that is the limitation worth stating: a
    simulation fed with an empirical distribution never sees a value larger
    than the largest one measured, however long it runs.
    """
    drawn = sample(values, 5000, seed=3)
    return max(drawn) <= max(values)


def smoothed(values, point):
    """A linearly interpolated version, which fills the gaps between points."""
    ordered = sorted(values)
    size = len(ordered)
    if point <= ordered[0]:
        return 0.0
    if point >= ordered[-1]:
        return 1.0
    for index in range(size - 1):
        if ordered[index] <= point <= ordered[index + 1]:
            span = ordered[index + 1] - ordered[index]
            share = 0.0 if span == 0 else (point - ordered[index]) / span
            return (index + share) / (size - 1)
    return 1.0
