"""Longest increasing subsequence, twice: the obvious way and the fast way."""

from __future__ import annotations

from bisect import bisect_left


def lis_length_quadratic(values):
    """The length, by asking each position about every earlier one.

    The state is "the longest increasing subsequence **ending at** position i",
    the same reframing Kadane uses. Each position looks back at every smaller
    earlier value and takes the best, which is O(n²).

    This is the version worth understanding, because the recurrence is visible
    in it. The fast one below computes the same number by a route that hides
    what it is doing.
    """
    if not values:
        return 0

    best = [1] * len(values)
    for index in range(1, len(values)):
        for earlier in range(index):
            if values[earlier] < values[index]:
                best[index] = max(best[index], best[earlier] + 1)
    return max(best)


def lis_length_fast(values):
    """The same length in O(n log n), by keeping the smallest possible tails.

    Keep a list where entry k is the smallest value that can end an increasing
    subsequence of length k+1. That list is always sorted, so binary search
    finds where a new value belongs, and it either extends the list or lowers
    an existing tail.

    Lowering a tail is the part worth pausing on. It does not change the answer
    now, and it makes future extensions easier, because a smaller tail accepts
    more successors. **The list is not itself a valid subsequence**: it is a
    record of the best endings, which is why the reconstruction below needs
    separate bookkeeping.

    This is patience sorting, dealt as in the card game, and the number of
    piles is the answer.
    """
    tails: list = []
    for value in values:
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    return len(tails)


def lis(values):
    """One longest increasing subsequence itself.

    The fast method knows the length but not the sequence, because the tails
    list is not a subsequence. Recording, for each value, which value preceded
    it in the chain that made it a tail, is what allows the walk back.
    """
    if not values:
        return []

    tails: list = []
    tail_indices: list = []
    previous = [-1] * len(values)

    for index, value in enumerate(values):
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
            tail_indices.append(index)
        else:
            tails[position] = value
            tail_indices[position] = index
        previous[index] = tail_indices[position - 1] if position else -1

    result = []
    index = tail_indices[-1]
    while index != -1:
        result.append(values[index])
        index = previous[index]
    return list(reversed(result))
