"""Binary search: halve the range until the target is cornered."""

from __future__ import annotations


def binary_search(items, target, key=None):
    """Return the index of `target` in a sorted sequence, or -1.

    Each comparison eliminates half of what is left, so the range shrinks from
    n to 1 in log₂(n) steps: a million elements take twenty comparisons.

    The classic bug is the loop condition. `low <= high` with `high = middle - 1`
    terminates; `low < high` with `high = middle` needs a different post-check,
    and mixing the two silently loses the last element. The other classic bug,
    `(low + high) // 2` overflowing, is real in C and Java and not in Python,
    where integers do not wrap.

    Order is the whole precondition. On unsorted data it returns nonsense
    rather than failing, which is worse than being slow.
    """
    of = key or (lambda item: item)
    low, high = 0, len(items) - 1

    while low <= high:
        middle = (low + high) // 2
        value = of(items[middle])
        if value == target:
            return middle
        if value < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1
