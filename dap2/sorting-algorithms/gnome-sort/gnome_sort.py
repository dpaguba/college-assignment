"""Gnome sort: step forward when ordered, step back and swap when not."""

from __future__ import annotations


def gnome_sort(items, key=None):
    """Return a sorted copy of `items`.

    Insertion sort with a single index and no inner loop, named for a garden
    gnome sorting flower pots: he looks at the pot beside him, and if it is out
    of order he swaps the two and steps back, otherwise he steps forward.

    It does the same work as insertion sort and reads in five lines, which is
    the only reason to prefer it.
    """
    result = list(items)
    of = key or (lambda item: item)
    position = 0

    while position < len(result):
        if position == 0 or of(result[position - 1]) <= of(result[position]):
            position += 1
        else:
            result[position - 1], result[position] = result[position], result[position - 1]
            position -= 1

    return result
