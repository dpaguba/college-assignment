"""Unbounded knapsack: the same problem, with an unlimited supply of each item."""

from __future__ import annotations


def unbounded_knapsack(items, capacity):
    """Return the best total value and how many of each item to take.

    The 0/1 version allows each item once; this one allows any number. The
    recurrence changes accordingly:

        best(c) = max over items of value[i] + best(c - weight[i])

    Note what disappeared: the item index. In the 0/1 version the state has to
    record which items are still available, so the table is two-dimensional.
    Here every item stays available for ever, so the amount alone is the state,
    and the table collapses to one dimension.

    In code the entire difference from the rolling 0/1 version is the direction
    of the inner loop. Walking capacities **upwards** lets a cell read a value
    that already includes the current item, which is exactly what taking it
    twice means. Downwards forbids it. One reversed loop separates two
    different problems, and it is the most common way to solve the wrong one.

    Coin change is this problem with value equal to weight, which is why the
    two folders look so similar.
    """
    if capacity < 0:
        raise ValueError("a capacity cannot be negative")

    best = [0] * (capacity + 1)
    used = [None] * (capacity + 1)

    for limit in range(1, capacity + 1):
        for item in items:
            weight, value = item
            if weight <= limit and value + best[limit - weight] > best[limit]:
                best[limit] = value + best[limit - weight]
                used[limit] = item

    counts: dict = {}
    remaining = capacity
    while remaining > 0 and used[remaining] is not None:
        item = used[remaining]
        counts[item] = counts.get(item, 0) + 1
        remaining -= item[0]

    return best[capacity], counts
