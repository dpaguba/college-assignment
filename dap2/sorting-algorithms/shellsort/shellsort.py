"""Shellsort: insertion sort on interleaved subsequences, gaps closing to 1."""

from __future__ import annotations


def ciura_gaps(size):
    """The gap sequence Ciura found by experiment, extended by a factor of 2.25.

    No gap sequence is known to be optimal. This one measures best on small and
    medium inputs, which is where Shellsort is actually used.
    """
    gaps = [1, 4, 10, 23, 57, 132, 301, 701]
    while gaps[-1] < size:
        gaps.append(int(gaps[-1] * 2.25))
    return [gap for gap in reversed(gaps) if gap < size]


def shellsort(items, key=None, gaps=None):
    """Return a sorted copy of `items`.

    Insertion sort is fast on nearly sorted data and slow otherwise, because an
    element only ever moves one position at a time. Shellsort sorts elements
    that are `gap` apart first, so values cross the list in long jumps, and
    every pass leaves the array closer to sorted for the next, smaller gap.

    The final pass with gap 1 is plain insertion sort, by then on data that is
    almost in order. Long moves are also what breaks stability.
    """
    result = list(items)
    of = key or (lambda item: item)

    for gap in (gaps if gaps is not None else ciura_gaps(len(result))):
        for position in range(gap, len(result)):
            value = result[position]
            index = position
            while index >= gap and of(result[index - gap]) > of(value):
                result[index] = result[index - gap]
                index -= gap
            result[index] = value

    return result
