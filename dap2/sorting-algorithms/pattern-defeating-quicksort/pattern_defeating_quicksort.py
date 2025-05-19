"""Pattern-defeating quicksort: quicksort that notices the shape of its input."""

from __future__ import annotations

from math import log2

SMALL = 24

def pattern_defeating_quicksort(items, key=None):
    """Return a sorted copy of `items`.

    Orson Peters's sort, the one behind Rust's `sort_unstable`. Introsort fixes
    the worst case but still does full work on inputs that need almost none.
    This one looks at what the partition told it:

    - a partition that moved nothing means the range may already be sorted, so
      it checks, and returns early if it is;
    - a badly unbalanced partition means the pivot choice is being defeated, so
      it shuffles a few elements to break whatever pattern is doing it;
    - too many bad partitions in a row and it falls back to heapsort.

    Sorted, reverse sorted, all-equal and organ-pipe inputs all become linear
    or near linear, while random input costs the same as quicksort.
    """
    result = list(items)
    of = key or (lambda item: item)
    size = len(result)
    if size < 2:
        return result

    def insertion(low, high):
        """Sorts the range by insertion, used for short ranges."""
        for position in range(low + 1, high + 1):
            value = result[position]
            index = position - 1
            while index >= low and of(result[index]) > of(value):
                result[index + 1] = result[index]
                index -= 1
            result[index + 1] = value

    def already_sorted(low, high):
        """Whether the range is already in order, which ends the work early."""
        return all(of(result[i]) <= of(result[i + 1]) for i in range(low, high))

    def median_of_three(a, b, c):
        """The index of the median of the three positions."""
        ka, kb, kc = of(result[a]), of(result[b]), of(result[c])
        if ka < kb:
            return b if kb < kc else (c if ka < kc else a)
        return a if ka < kc else (c if kb < kc else b)

    def choose_pivot(low, high):
        """The pivot: a median of three, or of nine for a long range."""
        middle = (low + high) // 2
        if high - low > 128:
            step = (high - low) // 8
            return median_of_three(
                median_of_three(low, low + step, low + 2 * step),
                median_of_three(middle - step, middle, middle + step),
                median_of_three(high - 2 * step, high - step, high),
            )
        return median_of_three(low, middle, high)

    def partition(low, high):
        """Splits the range around a pivot and returns its final position."""
        pivot_index = choose_pivot(low, high)
        result[low], result[pivot_index] = result[pivot_index], result[low]
        pivot = of(result[low])

        left, right = low + 1, high
        while True:
            while left <= right and of(result[left]) < pivot:
                left += 1
            while left <= right and of(result[right]) >= pivot:
                right -= 1
            if left > right:
                break
            result[left], result[right] = result[right], result[left]
        result[low], result[right] = result[right], result[low]
        return right, left == low + 1

    def sort(low, high, depth):
        """Sorts the range, falling back to insertion when the depth runs out."""
        while high - low + 1 > SMALL:
            if depth == 0:
                insertion(low, high)
                return
            split, untouched = partition(low, high)

            if untouched and already_sorted(low, high):
                return

            left_size, right_size = split - low, high - split
            if min(left_size, right_size) < (high - low) // 8:
                depth -= 1
                for a, b in ((low, low + left_size // 2), (high, high - right_size // 2)):
                    result[a], result[b] = result[b], result[a]

            sort(low, split - 1, depth)
            low = split + 1
        insertion(low, high)

    sort(0, size - 1, 2 * int(log2(size)) if size > 1 else 0)
    return result
