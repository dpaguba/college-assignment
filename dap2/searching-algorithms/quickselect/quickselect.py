"""Quickselect: quicksort that recurses into one side only."""

from __future__ import annotations

import random

def quickselect(items, k, key=None, seed=None):
    """Return the k-th smallest value, counting from zero.

    Quicksort partitions and then sorts both sides. If all you want is the
    k-th element, only one side can contain it, so the other is thrown away
    unsorted. That turns the recurrence from T(n) = 2T(n/2) + n into
    T(n) = T(n/2) + n, and the sum collapses from n log n to n.

    Expected linear time, and a worst case of n² for the same reason quicksort
    has one: a pivot that keeps landing at an end. Random pivots make that a
    matter of luck rather than a property of the input; median of medians, in
    the folder next door, removes the luck entirely.

    This is how "the median" is computed without sorting, and how the k largest
    of a million records are found without ordering the rest.

    The partition is three-way, so runs of equal keys cannot drive the
    quadratic behaviour that a two-way split falls into.
    """
    if not 0 <= k < len(items):
        raise IndexError(f"k must be between 0 and {len(items) - 1}, got {k}")

    values = list(items)
    of = key or (lambda item: item)
    generator = random.Random(seed)
    low, high = 0, len(values) - 1

    while True:
        if low == high:
            return values[low]

        pivot_index = generator.randint(low, high)
        pivot = of(values[pivot_index])
        values[pivot_index], values[high] = values[high], values[pivot_index]

        less, equal, greater = low, low, high
        while equal <= greater:
            value = of(values[equal])
            if value < pivot:
                values[less], values[equal] = values[equal], values[less]
                less, equal = less + 1, equal + 1
            elif value > pivot:
                values[equal], values[greater] = values[greater], values[equal]
                greater -= 1
            else:
                equal += 1

        if k < less:
            high = less - 1
        elif k > greater:
            low = greater + 1
        else:
            return values[k]
