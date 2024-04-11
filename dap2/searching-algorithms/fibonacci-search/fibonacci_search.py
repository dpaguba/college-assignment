"""Fibonacci search: binary search that never divides, only adds and subtracts."""

from __future__ import annotations

def fibonacci_search(items, target, key=None):
    """Return the index of `target` in a sorted sequence, or -1.

    Split the range at a Fibonacci number instead of in half. Because
    F(k) = F(k-1) + F(k-2), moving to either sub-range is a subtraction, and
    the next split point is another table lookup. No division, no midpoint
    computation.

    That mattered when division cost tens of cycles and addition cost one, and
    it still matters on small microcontrollers without a divider. The split is
    at the golden ratio rather than the middle, so it makes marginally more
    comparisons than binary search, which is the price for the cheaper
    arithmetic.

    The other advantage is locality: the probes step through memory in smaller
    increments than binary search's halving, which is friendlier to a cache or
    a tape.
    """
    of = key or (lambda item: item)
    size = len(items)
    if size == 0:
        return -1

    two_back, one_back = 0, 1
    current = two_back + one_back
    while current < size:
        two_back, one_back = one_back, current
        current = two_back + one_back

    offset = -1
    while current > 1:
        index = min(offset + two_back, size - 1)
        value = of(items[index])
        if value < target:
            current, one_back = one_back, two_back
            two_back = current - one_back
            offset = index
        elif value > target:
            current, one_back = two_back, one_back - two_back
            two_back = current - one_back
        else:
            return index

    if one_back and offset + 1 < size and of(items[offset + 1]) == target:
        return offset + 1
    return -1
