"""Exponential search: double the bound until it overshoots, then binary search."""

from __future__ import annotations


def exponential_search(items, target, key=None):
    """Return the index of `target` in a sorted sequence, or -1.

    Also called doubling or galloping search. Check position 1, then 2, 4, 8,
    16, until the value there passes the target, and binary search the range
    between the last two bounds.

    Finding the bound costs log(i) steps where i is the answer's position, and
    the binary search costs another log(i). So a target near the front is found
    in a handful of comparisons regardless of how long the array is, which is
    exactly what binary search cannot promise: it always starts in the middle.

    Two consequences follow. It works on unbounded or streamed sorted input,
    where the length is not known in advance. And it is the merge strategy
    inside timsort, which galloping is named after: when one run keeps winning,
    doubling finds how far it wins by, far faster than stepping.
    """
    of = key or (lambda item: item)
    size = len(items)
    if size == 0:
        return -1
    if of(items[0]) == target:
        return 0

    bound = 1
    while bound < size and of(items[bound]) <= target:
        bound *= 2

    low, high = bound // 2, min(bound, size - 1)
    while low <= high:
        middle = (low + high) // 2
        value = of(items[middle])
        if value == target:
            return middle
        if value < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1
