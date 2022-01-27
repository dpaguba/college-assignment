"""Counting inversions: how far a sequence is from being sorted."""

from __future__ import annotations

def count_inversions(values, collect=True):
    """Return how many pairs are out of order, and optionally which ones.

    An inversion is a pair i < j with values[i] > values[j]. The count measures
    disorder: zero for sorted input, n(n-1)/2 for reversed. It is also exactly
    the number of swaps insertion sort performs, which is why insertion sort is
    linear on nearly sorted data and why this quantity appears in the DAP2
    exercise sheet next to it.

    Counting them one by one is O(n²). The trick is that **merge sort already
    knows**. During a merge, when an element is taken from the right half while
    k elements remain unconsumed on the left, that element is smaller than all
    k of them, so k inversions are counted in one step rather than k steps.

    Counting them costs nothing on top of the sort, so the whole thing is
    O(n log n). This is the standard example of a divide and conquer algorithm
    that computes something other than what it appears to: sorting is the
    by-product, and the count is the answer.

    Listing the pairs is optional because there can be n²/2 of them, and asking
    for the list throws away the reason the algorithm is fast.

    The count comes from the merge: when an element of the right half is taken,
    everything still unconsumed in the left half is greater than it, so that
    many inversions are recorded at once.
    """
    indexed = list(enumerate(values))
    pairs: list = []

    def sort(items):
        """Sorts the items and counts the inversions it removes."""
        if len(items) < 2:
            return items, 0

        middle = len(items) // 2
        left, left_count = sort(items[:middle])
        right, right_count = sort(items[middle:])

        merged = []
        total = left_count + right_count
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i][1] <= right[j][1]:
                merged.append(left[i])
                i += 1
            else:
                remaining = len(left) - i
                total += remaining
                if collect:
                    pairs.extend((left[k][0], right[j][0]) for k in range(i, len(left)))
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, total

    _, count = sort(indexed)
    return count, sorted(pairs) if collect else []
