"""Ternary search: two cuts per step, for finding a peak rather than a value."""

from __future__ import annotations

def ternary_search(items, key=None):
    """Return the index of the maximum of a unimodal sequence, or -1 if empty.

    This one answers a different question from every other search here. Binary
    search asks "where is this value"; ternary search asks "where is the
    largest value", and it needs the sequence to rise and then fall, with no
    plateau at the top.

    Cut the range at two points a third apart. If the left probe is smaller
    than the right one, the peak cannot be left of the left probe, so that part
    is discarded, and the other way round. Each step throws away a third, which
    gives log₃(n) steps at two comparisons each. Binary search on a sorted
    array is cheaper per step, which is why ternary search is used for
    optimisation and not for lookup.

    It generalises straight to continuous functions, and that is its real home:
    finding the minimum of a convex cost function without a derivative.
    """
    of = key or (lambda item: item)
    if not items:
        return -1

    low, high = 0, len(items) - 1
    while high - low > 2:
        third = (high - low) // 3
        left, right = low + third, high - third
        if of(items[left]) < of(items[right]):
            low = left + 1
        else:
            high = right - 1

    best = low
    for index in range(low + 1, high + 1):
        if of(items[index]) > of(items[best]):
            best = index
    return best
