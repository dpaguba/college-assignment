"""Pigeonhole sort: one hole per key, drop each element into its hole."""

from __future__ import annotations


def pigeonhole_sort(items, key=None):
    """Return a sorted copy of `items`, whose keys must be integers.

    Counting sort's simpler cousin: instead of counting first and placing
    second, it keeps a list per key and then reads the lists in order.

    It is only reasonable when the number of keys is close to the number of
    elements. Sorting ten values whose keys span a million allocates a million
    empty lists, which is the same trap counting sort has and the reason both
    are reserved for small, dense key ranges such as ages, grades or bytes.
    """
    values = list(items)
    of = key or (lambda item: item)
    if not values:
        return values

    keys = [of(value) for value in values]
    low, high = min(keys), max(keys)
    holes: list[list] = [[] for _ in range(high - low + 1)]

    for value, k in zip(values, keys):
        holes[k - low].append(value)

    return [value for hole in holes for value in hole]
