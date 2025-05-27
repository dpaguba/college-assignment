"""Selection sort: find the smallest remaining element, put it in place."""

from __future__ import annotations


def selection_sort(items, key=None):
    """Return a sorted copy of `items`.

    The number of comparisons is fixed at n(n-1)/2 no matter what the input
    looks like, so unlike bubble or insertion sort this one has no best case.
    What it does have is a minimum of writes, exactly n-1 swaps, which used to
    matter when writing to storage cost far more than reading.

    Swapping distant elements is what makes it unstable: moving the smallest
    element into position jumps over equal keys and reverses them.
    """
    result = list(items)
    of = key or (lambda item: item)

    for start in range(len(result) - 1):
        smallest = start
        for index in range(start + 1, len(result)):
            if of(result[index]) < of(result[smallest]):
                smallest = index
        if smallest != start:
            result[start], result[smallest] = result[smallest], result[start]

    return result
