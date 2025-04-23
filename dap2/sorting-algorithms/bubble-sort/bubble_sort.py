"""Bubble sort: walk the list, swap neighbours that are out of order, repeat."""

from __future__ import annotations


def bubble_sort(items, key=None):
    """Return a sorted copy of `items`.

    Each pass carries the largest remaining element to the end, which is why
    the unsorted part shrinks by one every time. The `swapped` flag turns an
    already sorted list into a single pass, and that is the whole reason the
    best case is linear.
    """
    result = list(items)
    of = key or (lambda item: item)

    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if of(result[index]) > of(result[index + 1]):
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break

    return result
