"""Interpolation search: guess where the value should be, the way a phone book works."""

from __future__ import annotations

def interpolation_search(items, target, key=None):
    """Return the index of `target` in a sorted sequence, or -1.

    Nobody opens a phone book in the middle to find Aaronson. Binary search
    does exactly that, because it uses only the order of the keys and ignores
    their values.

    Interpolation search uses the values: assuming the data rises evenly, the
    target's position is estimated by linear interpolation between the ends of
    the range. On uniformly distributed keys that lands close enough that the
    remaining range shrinks doubly exponentially, giving O(log log n): a
    million elements take about four probes rather than twenty.

    The assumption is load bearing. On keys like 1, 2, 3, ..., 1000, 10⁹ the
    estimate lands at the wrong end every time and the search degrades to O(n),
    worse than binary search on the same data. Real implementations detect that
    and fall back.
    """
    of = key or (lambda item: item)
    low, high = 0, len(items) - 1

    while low <= high:
        low_value, high_value = of(items[low]), of(items[high])
        if target < low_value or target > high_value:
            return -1
        if low_value == high_value:
            return low if low_value == target else -1

        guess = low + (target - low_value) * (high - low) // (high_value - low_value)
        guess = max(low, min(guess, high))

        value = of(items[guess])
        if value == target:
            return guess
        if value < target:
            low = guess + 1
        else:
            high = guess - 1

    return -1
