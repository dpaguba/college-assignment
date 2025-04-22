"""Block sort: a stable merge sort that borrows its own array as scratch space.

Runs shorter than the minimum are sorted with insertion sort first, as in
Timsort.
"""

from __future__ import annotations

MIN_RUN = 16

def block_sort(items, key=None):
    """Return a sorted copy of `items`.

    Also called WikiSort. Merge sort is stable and n log n but wants n spare
    slots; the in-place merges that avoid that are usually unstable or slower.
    Block sort gets all three by taking a section of the array itself as an
    internal buffer, merging blocks by rotation, and putting the buffer back at
    the end.

    This implementation keeps the shape, bottom-up merging of fixed runs with
    rotation-based merges, and leaves out the buffer extraction: the merge here
    is the recursive rotation merge, so the memory is the recursion stack
    rather than a true O(1). The distinction is worth naming rather than
    hiding, since the O(1) claim is the entire point of the real algorithm.
    """
    result = list(items)
    of = key or (lambda item: item)
    size = len(result)
    if size < 2:
        return result

    def insertion(low, high):
        """Sorts a short range by insertion."""
        for position in range(low + 1, high):
            value = result[position]
            index = position - 1
            while index >= low and of(result[index]) > of(value):
                result[index + 1] = result[index]
                index -= 1
            result[index + 1] = value

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
        """Merges two sorted neighbouring ranges in place."""
        if low >= middle or middle >= high:
            return
        if high - low == 2:
            if of(result[low]) > of(result[low + 1]):
                result[low], result[low + 1] = result[low + 1], result[low]
            return
        if middle - low >= high - middle:
            cut = (low + middle) // 2
            other = lower_bound(middle, high, of(result[cut]))
        else:
            other = (middle + high) // 2
            cut = upper_bound(low, middle, of(result[other]))

        result[cut:other] = result[middle:other] + result[cut:middle]
        new_middle = cut + (other - middle)
        merge(low, cut, new_middle)
        merge(new_middle, other, high)

    for low in range(0, size, MIN_RUN):
        insertion(low, min(low + MIN_RUN, size))

    width = MIN_RUN
    while width < size:
        for low in range(0, size, 2 * width):
            middle = min(low + width, size)
            high = min(low + 2 * width, size)
            merge(low, middle, high)
        width *= 2

    return result
