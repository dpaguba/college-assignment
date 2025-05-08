"""Insertion sort: take the next element, slide it back to where it belongs."""

from __future__ import annotations


def insertion_sort(items, key=None):
    """Return a sorted copy of `items`.

    The left part of the list is always sorted. Each step takes the first
    unsorted element and moves it left past everything larger than it.

    The comparison is strict, `>` rather than `>=`, so an element never moves
    past an equal one. That single character is what makes the sort stable, and
    it is also why nearly sorted input costs almost nothing: the inner loop
    stops on the first comparison.
    """
    result = list(items)
    of = key or (lambda item: item)

    for position in range(1, len(result)):
        value = result[position]
        index = position - 1
        while index >= 0 and of(result[index]) > of(value):
            result[index + 1] = result[index]
            index -= 1
        result[index + 1] = value

    return result
