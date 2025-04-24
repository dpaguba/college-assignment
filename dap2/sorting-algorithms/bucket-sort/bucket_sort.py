"""Bucket sort: scatter into ranges, sort each range, concatenate."""

from __future__ import annotations


def insertion_sort(values, of):
    """The sort used inside a bucket: small, stable, fast on short lists."""
    for position in range(1, len(values)):
        value = values[position]
        index = position - 1
        while index >= 0 and of(values[index]) > of(value):
            values[index + 1] = values[index]
            index -= 1
        values[index + 1] = value
    return values


def bucket_sort(items, key=None, bucket_count=None):
    """Return a sorted copy of `items`, whose keys must be numbers.

    Split the key range into equal intervals, drop each element into the
    interval it belongs to, sort the intervals separately and join them.

    Everything depends on the keys being spread evenly. If they are, every
    bucket holds a handful of elements and the sort is linear. If they all land
    in one bucket, it is whatever the inner sort costs, n² here. So this is the
    sort that is fast because of an assumption about the data, not because of
    its structure.
    """
    values = list(items)
    of = key or (lambda item: item)
    if len(values) < 2:
        return values

    keys = [of(value) for value in values]
    low, high = min(keys), max(keys)
    if low == high:
        return values

    count = bucket_count or len(values)
    span = (high - low) / count
    buckets: list[list] = [[] for _ in range(count)]

    for value, k in zip(values, keys):
        index = min(int((k - low) / span), count - 1)
        buckets[index].append(value)

    return [value for bucket in buckets for value in insertion_sort(bucket, of)]
