"""MSD radix sort: split by the most significant digit, then recurse."""

from __future__ import annotations

BASE = 10


def radix_sort_msd(items, key=None, base=BASE):
    """Return a sorted copy of `items`, whose keys must be integers.

    Where LSD radix sort makes a fixed number of passes over everything, MSD
    splits the input into buckets by the leading digit and then sorts each
    bucket independently. Once a bucket holds one element, or every element in
    it shares the remaining digits, the work stops.

    That early exit is why MSD is the one used for strings: comparing
    dictionary words rarely needs more than the first few letters. The cost is
    recursion and many small buckets, where LSD is a flat loop.
    """
    values = list(items)
    of = key or (lambda item: item)
    if len(values) < 2:
        return values

    negatives = [value for value in values if of(value) < 0]
    positives = [value for value in values if of(value) >= 0]

    def sort(subset, magnitude, digit):
        """Sorts the subset by the current digit and recurses per bucket."""
        if len(subset) < 2 or digit == 0:
            return subset
        buckets: list[list] = [[] for _ in range(base)]
        for value in subset:
            buckets[(magnitude(value) // digit) % base].append(value)
        return [
            value
            for bucket in buckets
            for value in sort(bucket, magnitude, digit // base)
        ]

    def top_digit(subset, magnitude):
        """The place value of the most significant digit in the subset."""
        largest = max((magnitude(value) for value in subset), default=0)
        digit = 1
        while largest // (digit * base) > 0:
            digit *= base
        return digit

    sorted_negatives = (
        list(reversed(sort(negatives, lambda value: -of(value),
                           top_digit(negatives, lambda value: -of(value)))))
        if negatives else []
    )
    sorted_positives = sort(positives, of, top_digit(positives, of)) if positives else []
    return sorted_negatives + sorted_positives
