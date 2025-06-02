"""Strand sort: pull out already sorted runs, merge them one at a time."""

from __future__ import annotations

def strand_sort(items, key=None):
    """Return a sorted copy of `items`.

    Walk the remaining input and take every element that is not smaller than
    the last one taken. That is a "strand", a subsequence that was already in
    order. Merge it into the output and repeat with what is left.

    On sorted input the first strand swallows everything and the sort is
    linear. On reversed input every strand is one element long and it costs n².
    So this is the sort whose running time is a direct measure of how ordered
    the input already was.

    A strand is taken later than anything already merged, so on a tie the
    existing element keeps its place and the sort stays stable.
    """
    of = key or (lambda item: item)
    remaining = list(items)
    ordered: list = []

    while remaining:
        strand = [remaining.pop(0)]
        leftover = []
        for value in remaining:
            if of(value) >= of(strand[-1]):
                strand.append(value)
            else:
                leftover.append(value)
        remaining = leftover

        merged = []
        i = j = 0
        while i < len(ordered) and j < len(strand):
            if of(ordered[i]) <= of(strand[j]):
                merged.append(ordered[i])
                i += 1
            else:
                merged.append(strand[j])
                j += 1
        merged.extend(ordered[i:])
        merged.extend(strand[j:])
        ordered = merged

    return ordered
