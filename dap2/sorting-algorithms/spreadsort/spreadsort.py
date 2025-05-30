"""Spreadsort: radix and comparison sorting, whichever is cheaper per split.

Below the size cutoff a comparison sort wins outright, so the recursion stops
there. The bin limit caps how many bins one split may create.
"""

from __future__ import annotations

SMALL = 16
MAX_BINS = 256

def spreadsort(items, key=None):
    """Return a sorted copy of `items`, whose keys must be integers.

    Steven Ross's hybrid. Pure radix sort is fast but pays for every digit,
    even when the data is nearly sorted; pure comparison sorting pays log n per
    element regardless of key width. Spreadsort measures the key range at each
    step and picks: wide range and enough elements, split into bins by the top
    bits; otherwise hand the piece to a comparison sort.

    The result is a sort that behaves like radix on the parts that suit radix
    and like introsort on the parts that do not, which is why it is the default
    integer sort in Boost.
    """
    values = list(items)
    of = key or (lambda item: item)

    def sort(subset):
        """Sorts the subset by spreading it over buckets by key range."""
        if len(subset) <= SMALL:
            return sorted(subset, key=of)

        keys = [of(value) for value in subset]
        low, high = min(keys), max(keys)
        if low == high:
            return subset

        span = high - low + 1
        bins = min(MAX_BINS, span, len(subset))
        if bins < 2:
            return sorted(subset, key=of)

        width = -(-span // bins)
        buckets: list[list] = [[] for _ in range(bins)]
        for value, k in zip(subset, keys):
            buckets[min((k - low) // width, bins - 1)].append(value)

        return [value for bucket in buckets for value in sort(bucket)]

    return sort(values)
