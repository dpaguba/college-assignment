"""LSD radix sort: one counting sort per digit, least significant first."""

from __future__ import annotations

BASE = 10


def counting_pass(values, of, digit, base):
    """One stable counting sort on a single digit."""
    counts = [0] * base
    digits = [(of(value) // digit) % base for value in values]
    for d in digits:
        counts[d] += 1

    total = 0
    for index, count in enumerate(counts):
        counts[index] = total
        total += count

    output = [None] * len(values)
    for value, d in zip(values, digits):
        output[counts[d]] = value
        counts[d] += 1
    return output


def radix_sort_lsd(items, key=None, base=BASE):
    """Return a sorted copy of `items`, whose keys must be integers.

    Sort by the last digit, then the second to last, and so on. The trick is
    that each pass must be stable: the order established by the previous, less
    significant digit survives, so after the final pass the whole numbers are
    in order.

    Negative keys are handled by sorting the absolute values of the negatives
    and reversing them in front, since digit extraction has no sign.
    """
    values = list(items)
    of = key or (lambda item: item)
    if len(values) < 2:
        return values

    negatives = [value for value in values if of(value) < 0]
    positives = [value for value in values if of(value) >= 0]

    def sort_by_digits(subset, magnitude):
        """Sorts the subset one digit at a time, least significant first."""
        if not subset:
            return subset
        largest = max(magnitude(value) for value in subset)
        digit = 1
        while largest // digit > 0:
            subset = counting_pass(subset, magnitude, digit, base)
            digit *= base
        return subset

    sorted_negatives = sort_by_digits(negatives, lambda value: -of(value))
    sorted_positives = sort_by_digits(positives, of)
    return list(reversed(sorted_negatives)) + sorted_positives
