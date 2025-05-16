"""Patience sort: deal into piles like the card game, then merge the piles."""

from __future__ import annotations

import heapq
from bisect import bisect_left

def patience_sort(items, key=None):
    """Return a sorted copy of `items`.

    Deal each element onto the leftmost pile whose top card is not smaller,
    starting a new pile when none will take it. Every pile ends up decreasing
    from bottom to top, so merging the piles gives sorted output.

    The useful part is a by-product: the number of piles is exactly the length
    of the longest increasing subsequence of the input. That is what the
    algorithm is normally used for, rather than sorting.

    The pile tops stay ascending, so the leftmost pile that can take a value is
    one bisection away rather than a scan.
    """
    of = key or (lambda item: item)
    piles: list[list] = []
    tops: list = []

    for value in items:
        position = bisect_left(tops, of(value))
        if position == len(piles):
            piles.append([value])
            tops.append(of(value))
        else:
            piles[position].append(value)
            tops[position] = of(value)

    ordered = []
    heap = [(of(pile[-1]), index) for index, pile in enumerate(piles)]
    heapq.heapify(heap)
    while heap:
        _, index = heapq.heappop(heap)
        ordered.append(piles[index].pop())
        if piles[index]:
            heapq.heappush(heap, (of(piles[index][-1]), index))

    return ordered

def longest_increasing_subsequence_length(items, key=None):
    """The pile count, which is what patience sorting is really used for."""
    of = key or (lambda item: item)
    tops: list = []
    for value in items:
        position = bisect_left(tops, of(value))
        if position == len(tops):
            tops.append(of(value))
        else:
            tops[position] = of(value)
    return len(tops)
