"""Batcher's odd-even merge sort: the other classic sorting network."""

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

def odd_even_merge_sort(items, key=None):
    """Return a sorted copy of `items`.

    The same depth as bitonic sort, O(log² n), with fewer comparators. Batcher's
    merge works on two already sorted halves: sort the odd-indexed elements
    together, the even-indexed ones together, and then a single pass of
    neighbour comparisons finishes the job. Proving that last pass is enough is
    the zero-one principle, and it is the reason the network is correct for any
    input at all.

    Like every network, the comparison schedule is fixed in advance, so the
    padding to a power of two is part of the construction rather than a
    shortcut.
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

    def compare_and_swap(i, j):
        """The comparator: exchanges the pair when it is out of order."""
        if sort_key(work[i]) > sort_key(work[j]):
            work[i], work[j] = work[j], work[i]

    length = 2
    while length <= padded:
        stride = length // 2
        while stride >= 1:
            for index in range(padded):
                partner = index ^ stride if stride == length // 2 else index + stride
                if stride == length // 2:
                    if partner > index:
                        compare_and_swap(index, partner)
                elif (index // length) == (partner // length) and index % length >= stride:
                    if partner < padded and (index % length) % (2 * stride) >= stride:
                        compare_and_swap(index, partner)
            stride //= 2
        length *= 2

    return [value for value in work if not isinstance(value, _Sentinel)]
