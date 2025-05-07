"""In-place merge sort: the same recursion, merging by rotation instead of copy."""

from __future__ import annotations

def in_place_merge_sort(items, key=None):
    """Return a sorted copy of `items`, sorted without a second array.

    Ordinary merge sort needs n spare slots. This version merges two adjacent
    sorted runs by rotating blocks inside the array, so the extra memory is
    only the recursion stack.

    Nothing is free: rotations turn the merge from linear into n log n, and the
    whole sort into n log² n. It is the trade you make when memory is the
    scarce thing rather than time.
    """
    result = list(items)
    of = key or (lambda item: item)

    def rotate(low, middle, high):
        """Swap the block [low, middle) with [middle, high) in place."""
        result[low:high] = result[middle:high] + result[low:middle]

    def lower_bound(low, high, value):
        """The first position at or after which the value belongs."""
        while low < high:
            mid = (low + high) // 2
            if of(result[mid]) < value:
                low = mid + 1
            else:
                high = mid
        return low

    def upper_bound(low, high, value):
        """The first position after every occurrence of the value."""
        while low < high:
            mid = (low + high) // 2
            if of(result[mid]) <= value:
                low = mid + 1
            else:
                high = mid
        return low

    def merge(low, middle, high):
        """Merge two sorted runs by splitting the larger one and recursing."""
        if low >= middle or middle >= high:
            return
        if high - low == 2:
            if of(result[low]) > of(result[low + 1]):
                result[low], result[low + 1] = result[low + 1], result[low]
            return

        if middle - low >= high - middle:
            left_cut = (low + middle) // 2
            right_cut = lower_bound(middle, high, of(result[left_cut]))
        else:
            right_cut = (middle + high) // 2
            left_cut = upper_bound(low, middle, of(result[right_cut]))

        rotate(left_cut, middle, right_cut)
        new_middle = left_cut + (right_cut - middle)
        merge(low, left_cut, new_middle)
        merge(new_middle, right_cut, high)

    def sort(low, high):
        """Sorts the range and merges the halves without extra storage."""
        if high - low < 2:
            return
        middle = (low + high) // 2
        sort(low, middle)
        sort(middle, high)
        merge(low, middle, high)

    sort(0, len(result))
    return result
