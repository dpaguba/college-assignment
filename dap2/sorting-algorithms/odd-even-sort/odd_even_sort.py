"""Odd-even sort, also called brick sort: compare fixed pairs in two phases."""

from __future__ import annotations


def odd_even_sort(items, key=None):
    """Return a sorted copy of `items`.

    One phase compares every pair starting at an even index, the next starts
    at an odd one. No pair in a phase shares an element, so on real parallel
    hardware every comparison in a phase happens at once. On one processor it
    is bubble sort with extra steps, which is the point: the algorithm is
    shaped for the machine, not for the count.
    """
    result = list(items)
    of = key or (lambda item: item)
    sorted_through = False

    while not sorted_through:
        sorted_through = True
        for start in (1, 0):
            for index in range(start, len(result) - 1, 2):
                if of(result[index]) > of(result[index + 1]):
                    result[index], result[index + 1] = result[index + 1], result[index]
                    sorted_through = False

    return result
