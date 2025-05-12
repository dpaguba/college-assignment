"""Library sort: insertion sort with deliberate gaps left between elements.

The gap factor is how much room is left between elements. A factor of two means
half the array is gaps, which is the trade the algorithm makes: memory for the
shifting it avoids.
"""

from __future__ import annotations

SLACK = 2

def library_sort(items, key=None):
    """Return a sorted copy of `items`.

    Insertion sort is slow because inserting into the middle shifts everything
    after it. A librarian shelving a new book does not slide the whole shelf:
    the shelves already have gaps.

    Here the array is kept at twice the needed length with gaps between
    elements, so an insertion usually shifts a handful of items rather than
    thousands. When a region fills up, the whole array is rebalanced and the
    gaps are spread out again. That gives n log n on average, though a run of
    unlucky insertions into one spot still costs n².
    """
    of = key or (lambda item: item)
    values = list(items)
    if len(values) < 2:
        return values

    shelf: list = [None] * (SLACK * len(values))
    shelf[0] = values[0]
    filled = 1

    def occupied():
        """The shelf without its gaps."""
        return [slot for slot in shelf if slot is not None]

    def rebalance():
        """Spread what is on the shelf evenly, restoring the gaps."""
        present = occupied()
        spread: list = [None] * max(SLACK * len(present), SLACK)
        for position, value in enumerate(present):
            spread[position * SLACK] = value
        return spread

    for value in values[1:]:
        if filled * SLACK > len(shelf):
            shelf = rebalance()

        present = [index for index, slot in enumerate(shelf) if slot is not None]
        low, high = 0, len(present)
        while low < high:
            middle = (low + high) // 2
            if of(shelf[present[middle]]) <= of(value):
                low = middle + 1
            else:
                high = middle
        target = present[low] if low < len(present) else len(shelf)

        gap = target
        while gap < len(shelf) and shelf[gap] is not None:
            gap += 1
        if gap == len(shelf):
            shelf = rebalance()
            shelf.append(None)
            gap = len(shelf) - 1
            while gap > 0 and shelf[gap - 1] is None:
                gap -= 1
            target = min(target, gap)
        for index in range(gap, target, -1):
            shelf[index] = shelf[index - 1]
        shelf[target] = value
        filled += 1

    return occupied()
