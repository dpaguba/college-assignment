"""Median of medians: quickselect with a pivot good enough to guarantee linear time.

Groups of five are what make the recurrence close: three is too small to
guarantee the split, and seven works but costs more per level.
"""

from __future__ import annotations

GROUP = 5

def median_of_medians(items, k, key=None):
    """Return the k-th smallest value, counting from zero, in guaranteed O(n).

    Quickselect is linear on average and quadratic when the pivots are bad.
    Blum, Floyd, Pratt, Rivest and Tarjan removed the luck in 1973: choose the
    pivot by splitting the input into groups of five, taking each group's
    median, and recursively selecting the median of those medians.

    That pivot is guaranteed to be greater than at least 30 percent of the
    elements and smaller than at least 30 percent, so each level discards a
    constant fraction. The recurrence T(n) = T(n/5) + T(7n/10) + O(n) sums to
    O(n) because 1/5 + 7/10 is less than one.

    The constant is large enough that quickselect wins in practice, so this is
    the algorithm you cite rather than the one you run. Introselect, like
    introsort, uses quickselect and falls back to this when the pivots go bad.
    """
    if not 0 <= k < len(items):
        raise IndexError(f"k must be between 0 and {len(items) - 1}, got {k}")

    of = key or (lambda item: item)

    def select(values, rank):
        """The value of the given rank, chosen with a guaranteed good pivot."""
        if len(values) <= GROUP:
            return sorted(values, key=of)[rank]

        medians = [
            sorted(values[start : start + GROUP], key=of)[
                min(GROUP, len(values) - start) // 2
            ]
            for start in range(0, len(values), GROUP)
        ]
        pivot = of(select(medians, len(medians) // 2))

        smaller = [value for value in values if of(value) < pivot]
        equal = [value for value in values if of(value) == pivot]
        larger = [value for value in values if of(value) > pivot]

        if rank < len(smaller):
            return select(smaller, rank)
        if rank < len(smaller) + len(equal):
            return equal[0]
        return select(larger, rank - len(smaller) - len(equal))

    return select(list(items), k)
