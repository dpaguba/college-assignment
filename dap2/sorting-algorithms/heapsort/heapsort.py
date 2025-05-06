"""Heapsort: build a max-heap, then pull the root off one at a time."""

from __future__ import annotations

def heapsort(items, key=None):
    """Return a sorted copy of `items`.

    Selection sort spends n steps looking for the next largest element.
    A heap answers the same question in log n, and that single change is the
    whole difference between n² and n log n.

    The heap lives in the same list: the sorted part grows from the right as
    the heap shrinks from the left, so no second array is ever allocated.

    Building the heap bottom up costs O(n), not O(n log n): most nodes are
    leaves and sift down no distance at all.
    """
    result = list(items)
    of = key or (lambda item: item)
    size = len(result)

    def sift_down(root, end):
        """Push a too-small root down until the heap property holds again."""
        while True:
            largest = root
            for child in (2 * root + 1, 2 * root + 2):
                if child < end and of(result[child]) > of(result[largest]):
                    largest = child
            if largest == root:
                return
            result[root], result[largest] = result[largest], result[root]
            root = largest

    for root in range(size // 2 - 1, -1, -1):
        sift_down(root, size)

    for end in range(size - 1, 0, -1):
        result[0], result[end] = result[end], result[0]
        sift_down(0, end)

    return result
