"""Linear search: look at every element until the target turns up."""

from __future__ import annotations


def linear_search(items, target, key=None):
    """Return the index of `target`, or -1 if it is not there.

    The only search that needs nothing from the data: no order, no index, no
    structure. That is its whole argument. Everything faster on this list
    demands a sorted array, and sorting costs n log n, so for a single lookup
    in unsorted data this is the optimal algorithm, not the naive one.

    It is also the only one here that works on a stream, a linked list or
    anything you can walk but not index.
    """
    of = key or (lambda item: item)

    for index, item in enumerate(items):
        if of(item) == target:
            return index

    return -1
