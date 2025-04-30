"""Counting sort: count how many of each key there are, then lay them out."""

from __future__ import annotations

def counting_sort(items, key=None):
    """Return a sorted copy of `items`, whose keys must be integers.

    No two elements are ever compared. The count of each key says exactly how
    many slots it occupies, and the running total of the counts says where its
    block starts. That is why the n log n lower bound does not apply: the bound
    is about comparisons, and there are none.

    The cost is a table the size of the key range, so sorting three numbers
    that happen to be a million apart allocates a million counters. Walking the
    input backwards when placing is what keeps equal keys in their original
    order.
    """
    values = list(items)
    of = key or (lambda item: item)
    if not values:
        return values

    keys = [of(value) for value in values]
    low, high = min(keys), max(keys)
    counts = [0] * (high - low + 1)
    for k in keys:
        counts[k - low] += 1

    total = 0
    for index, count in enumerate(counts):
        counts[index] = total
        total += count

    result = [None] * len(values)
    for value, k in zip(values, keys):
        result[counts[k - low]] = value
        counts[k - low] += 1

    return result
