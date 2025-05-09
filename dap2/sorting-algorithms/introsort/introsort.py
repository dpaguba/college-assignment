"""Introsort: quicksort that gives up on itself before the worst case lands.

Ranges below the cutoff go to insertion sort, which beats quicksort on them.
"""

from __future__ import annotations

from math import log2

SMALL = 16

def introsort(items, key=None):
    """Return a sorted copy of `items`.

    David Musser's fix for the one real objection to quicksort: its n² worst
    case, which an adversary or an unlucky input can trigger. Introsort counts
    how deep the recursion has gone, and once it passes 2·log₂(n) it stops
    trusting quicksort and finishes that range with heapsort, which is n log n
    no matter what.

    So the average case is quicksort's, the worst case is heapsort's, and short
    ranges are left to a single insertion sort pass at the end. That is what
    `std::sort` does in C++.
    """
    result = list(items)
    of = key or (lambda item: item)
    size = len(result)
    if size < 2:
        return result

    def median_of_three(low, middle, high):
        """The index of the median of the three positions."""
        a, b, c = of(result[low]), of(result[middle]), of(result[high])
        if a < b:
            return middle if b < c else (high if a < c else low)
        return low if a < c else (high if b < c else middle)

    def partition(low, high):
        """Splits the range around a pivot and returns its final position."""
        pivot_index = median_of_three(low, (low + high) // 2, high)
        result[pivot_index], result[high] = result[high], result[pivot_index]
        pivot = of(result[high])
        boundary = low
        for index in range(low, high):
            if of(result[index]) < pivot:
                result[boundary], result[index] = result[index], result[boundary]
                boundary += 1
        result[boundary], result[high] = result[high], result[boundary]
        return boundary

    def heap_range(low, high):
        """Heapsort applied to one range, the escape hatch."""
        length = high - low + 1

        def sift(root, end):
            """Restores the heap condition below the root of the range."""
            while True:
                largest = root
                for child in (2 * root + 1, 2 * root + 2):
                    if child < end and of(result[low + child]) > of(result[low + largest]):
                        largest = child
                if largest == root:
                    return
                result[low + root], result[low + largest] = (
                    result[low + largest],
                    result[low + root],
                )
                root = largest

        for root in range(length // 2 - 1, -1, -1):
            sift(root, length)
        for end in range(length - 1, 0, -1):
            result[low], result[low + end] = result[low + end], result[low]
            sift(0, end)

    def sort(low, high, depth):
        """Sorts the range, switching to heapsort when the depth runs out."""
        while high - low + 1 > SMALL:
            if depth == 0:
                heap_range(low, high)
                return
            depth -= 1
            split = partition(low, high)
            sort(split + 1, high, depth)
            high = split - 1

    sort(0, size - 1, 2 * int(log2(size)) if size > 1 else 0)

    for position in range(1, size):
        value = result[position]
        index = position - 1
        while index >= 0 and of(result[index]) > of(value):
            result[index + 1] = result[index]
            index -= 1
        result[index + 1] = value

    return result
