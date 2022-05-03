"""Rod cutting: where to cut a rod so the pieces sell for the most."""

from __future__ import annotations


def rod_cutting(length, prices):
    """Return the best revenue for a rod of `length`, and the cuts that give it.

    A rod of length n can be cut in 2^(n-1) ways, so enumerating them is
    hopeless by twenty. The recurrence is one line: the best revenue for length
    n is the best over every first cut i of `price[i] + best(n - i)`.

    What makes it work is that the remainder after the first cut is an
    independent smaller instance of the same problem, and there are only n
    distinct remainders. Exponentially many arrangements, linearly many
    subproblems: that is optimal substructure and overlapping subproblems
    together, which is exactly the pair dynamic programming needs.

    This is the simplest problem where the state is a single number and the
    transition is a loop over choices, which is the shape that knapsack, coin
    change and longest increasing subsequence all share.
    """
    if length < 0:
        raise ValueError("a rod cannot have negative length")

    best = [0] * (length + 1)
    first_cut = [0] * (length + 1)

    for total in range(1, length + 1):
        for piece in range(1, total + 1):
            if piece not in prices:
                continue
            candidate = prices[piece] + best[total - piece]
            if candidate > best[total]:
                best[total] = candidate
                first_cut[total] = piece

    cuts = []
    remaining = length
    while remaining > 0 and first_cut[remaining]:
        cuts.append(first_cut[remaining])
        remaining -= first_cut[remaining]

    return best[length], cuts
