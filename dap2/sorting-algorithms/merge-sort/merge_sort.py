"""Merge sort: split in half, sort each half, merge the two sorted halves."""

from __future__ import annotations

def merge(left, right, of):
    """Combine two sorted lists into one, taking from the left on a tie."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if of(left[i]) <= of(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def merge_sort(items, key=None):
    """Return a sorted copy of `items`.

    The recursion tree is log n levels deep and each level touches every
    element once, which is where n log n comes from, and it holds for every
    input: there is no bad case.

    The price is the n extra space the merge needs. That is why quicksort,
    despite a worse worst case, usually wins in memory-bound settings, and why
    merge sort wins when the data does not fit in memory at all.

    The merge compares with <= and not <: on equal keys the element from the
    left half, which came first in the input, goes first. That is the whole of
    stability.
    """
    of = key or (lambda item: item)

    def sort(values):
        """Sorts the values by splitting, sorting the halves and merging."""
        if len(values) < 2:
            return values
        middle = len(values) // 2
        return merge(sort(values[:middle]), sort(values[middle:]), of)

    return sort(list(items))
