"""Cocktail shaker sort: bubble sort that alternates direction each pass."""

from __future__ import annotations


def cocktail_shaker_sort(items, key=None):
    """Return a sorted copy of `items`.

    Bubble sort only pushes large values right quickly; a small value near the
    end crawls left one position per pass. Sweeping back as well moves it the
    whole way in one go, which is the only thing this variant buys.
    """
    result = list(items)
    of = key or (lambda item: item)
    low, high = 0, len(result) - 1

    while low < high:
        swapped = False

        for index in range(low, high):
            if of(result[index]) > of(result[index + 1]):
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        high -= 1

        for index in range(high, low, -1):
            if of(result[index - 1]) > of(result[index]):
                result[index - 1], result[index] = result[index], result[index - 1]
                swapped = True
        low += 1

        if not swapped:
            break

    return result
