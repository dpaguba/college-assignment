"""Comb sort: bubble sort that starts with a wide gap and closes it.

The shrink factor is the one from Lacey and Box. Much smaller degrades to
bubble sort, much larger leaves inversions behind.
"""

from __future__ import annotations

SHRINK = 1.3

def comb_sort(items, key=None):
    """Return a sorted copy of `items`.

    Bubble sort is slow because a small value at the far end moves one step per
    pass. Comparing elements a wide gap apart kills those long-range inversions
    early, and by the time the gap reaches one the list is nearly ordered.
    """
    result = list(items)
    of = key or (lambda item: item)
    gap = len(result)
    swapped = True

    while gap > 1 or swapped:
        gap = max(1, int(gap / SHRINK))
        swapped = False
        for index in range(len(result) - gap):
            if of(result[index]) > of(result[index + gap]):
                result[index], result[index + gap] = result[index + gap], result[index]
                swapped = True

    return result
