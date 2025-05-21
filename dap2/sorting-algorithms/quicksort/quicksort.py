"""Quicksort: partition around a pivot, then sort both sides."""

from __future__ import annotations

import random

def quicksort(items, key=None, seed=None):
    """Return a sorted copy of `items`.

    The pivot is chosen at random. With a fixed pivot an already sorted list
    produces the worst case, n² comparisons, and sorted input is exactly what
    turns up in practice. Randomising makes that case a matter of luck rather
    than a matter of the caller's data.

    Recursion happens only on the smaller side, with the larger one handled by
    a loop, which keeps the stack at O(log n) even when every partition is
    lopsided.
    """
    result = list(items)
    of = key or (lambda item: item)
    generator = random.Random(seed)

    def partition(low, high):
        """Hoare's scheme: return an index that splits the range in two."""
        pivot = of(result[generator.randint(low, high)])
        left, right = low - 1, high + 1
        while True:
            left += 1
            while of(result[left]) < pivot:
                left += 1
            right -= 1
            while of(result[right]) > pivot:
                right -= 1
            if left >= right:
                return right
            result[left], result[right] = result[right], result[left]

    def sort(low, high):
        """Sorts the range, recursing into the smaller side first."""
        while low < high:
            split = partition(low, high)
            if split - low < high - split - 1:
                sort(low, split)
                low = split + 1
            else:
                sort(split + 1, high)
                high = split

    if result:
        sort(0, len(result) - 1)
    return result
