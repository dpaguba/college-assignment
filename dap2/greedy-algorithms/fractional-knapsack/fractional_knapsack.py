"""Fractional knapsack: the version where greedy is correct."""

from __future__ import annotations


def fractional_knapsack(items, capacity):
    """Return the best value and what fraction of each item to take.

    Identical to the 0/1 knapsack except that items may be cut. That single
    change moves the problem from NP-complete to O(n log n), and the algorithm
    from a dynamic programming table to one sort.

    The rule: take items in order of value per unit weight, whole while they
    fit, and fill the remaining space with a fraction of the next one.

    **Why it works here and not there.** The greedy choice can always be
    completed to an optimal solution, because any leftover space can be filled
    with part of the next item. In the 0/1 version that argument fails: an item
    either fits or it does not, so a locally best density can leave a gap that
    a different choice would have filled. Weights 10, 20, 30 with values 60,
    100, 120 and capacity 50 is the standard demonstration, and both versions
    are in this repository so the difference can be run rather than read.

    This pair is the clearest statement of what greedy algorithms need: not
    optimal substructure, which both versions have, but the ability to commit
    to a choice without closing off the best completion.
    """
    if capacity <= 0:
        return 0, []

    by_density = sorted(items, key=lambda item: item[1] / item[0], reverse=True)

    total = 0.0
    taken: list = []
    remaining = capacity

    for weight, value in by_density:
        if remaining <= 0:
            break
        if weight <= remaining:
            taken.append(((weight, value), 1))
            total += value
            remaining -= weight
        else:
            fraction = remaining / weight
            taken.append(((weight, value), fraction))
            total += value * fraction
            remaining = 0

    return total, taken
