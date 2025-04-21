"""Bitonic sort: a sorting network, the comparisons fixed before the data."""

from __future__ import annotations

class _Sentinel:
    """Padding that compares greater than every real key."""

    def __lt__(self, other):
        """The sentinel compares below every real value."""
        return False

    def __gt__(self, other):
        """The sentinel compares below every real value."""
        return not isinstance(other, _Sentinel)

    def __le__(self, other):
        """The sentinel compares below every real value."""
        return isinstance(other, _Sentinel)

    def __ge__(self, other):
        """The sentinel compares below every real value."""
        return True

    def __eq__(self, other):
        """Two sentinels are the same value."""
        return isinstance(other, _Sentinel)

    def __hash__(self):
        """A constant, since all sentinels are equal."""
        return 0

PAD = _Sentinel()

def bitonic_sort(items, key=None):
    """Return a sorted copy of `items`.

    Ken Batcher's network. A bitonic sequence rises then falls; the network
    builds one out of the input and then splits it in halves that can each be
    made bitonic again, until everything is ordered.

    What makes it a network rather than an algorithm: which elements get
    compared is decided by the position alone, never by a value. Every
    comparison in a stage is independent, so hardware or a GPU runs the whole
    stage at once. On one processor it does O(n log² n) comparisons, worse than
    merge sort, and it is still the standard GPU sort because the depth is only
    log² n.

    The network needs a power of two, so the list is padded with sentinels that
    sort to the end and are dropped afterwards.

    One half is built ascending and the other descending, which is what makes
    the whole range bitonic. The merge below handles nothing else.
    """
    values = list(items)
    of = key or (lambda item: item)
    size = len(values)
    if size < 2:
        return values

    padded = 1
    while padded < size:
        padded *= 2
    work = values + [PAD] * (padded - size)

    def sort_key(value):
        """The key of a value, or the sentinel itself for padding."""
        return value if isinstance(value, _Sentinel) else of(value)

    def compare_and_swap(i, j, ascending):
        """The comparator: exchanges the pair if it is out of the wanted order."""
        left, right = sort_key(work[i]), sort_key(work[j])
        if (left > right) == ascending:
            work[i], work[j] = work[j], work[i]

    def bitonic_merge(low, length, ascending):
        """Merges a bitonic sequence into a sorted one."""
        if length < 2:
            return
        half = length // 2
        for index in range(low, low + half):
            compare_and_swap(index, index + half, ascending)
        bitonic_merge(low, half, ascending)
        bitonic_merge(low + half, half, ascending)

    def build(low, length, ascending):
        """Builds a bitonic sequence from the two halves."""
        if length < 2:
            return
        half = length // 2
        build(low, half, True)
        build(low + half, half, False)
        bitonic_merge(low, length, ascending)

    build(0, padded, True)
    return [value for value in work if not isinstance(value, _Sentinel)]
