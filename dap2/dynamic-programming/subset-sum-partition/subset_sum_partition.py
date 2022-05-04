"""Subset sum and partition: can a target be hit exactly with these numbers."""

from __future__ import annotations

def subset_sum(values, target):
    """Return whether some subset sums to `target`, and one such subset.

    The knapsack recurrence with the value dropped: only reachability matters.
    A boolean per achievable sum, and each number either extends a reachable
    sum or does not.

    Same warning as knapsack. The table is `target` wide, and the target needs
    only log(target) bits to write down, so this is pseudo-polynomial rather
    than polynomial. Subset sum is one of Karp's original 21 NP-complete
    problems, and this algorithm does not contradict that: it is fast when the
    numbers are small and hopeless when they are large.

    Recording which number first reached each sum is what allows the subset to
    be reconstructed rather than merely confirmed to exist.

    The inner loop walks the sums downwards. Upwards would let one number be
    used twice, because the cell it reads would already include itself, and the
    answer would silently become the unbounded version of the problem.
    """
    if target < 0:
        return False, []

    reachable = [False] * (target + 1)
    reachable[0] = True
    reached_by = [None] * (target + 1)

    for index, value in enumerate(values):
        for total in range(target, value - 1, -1):
            if reachable[total - value] and not reachable[total]:
                reachable[total] = True
                reached_by[total] = index

    if not reachable[target]:
        return False, []

    subset = []
    remaining = target
    while remaining > 0:
        index = reached_by[remaining]
        subset.append(values[index])
        remaining -= values[index]
    return True, subset

def can_partition(values):
    """Whether the numbers split into two groups of equal sum.

    Two observations turn this into subset sum. An odd total can never split,
    which is checked first and costs nothing. And if a subset sums to half the
    total, the rest sums to the other half automatically, so only one side has
    to be found.

    Recognising that a new problem is an old one in different words is the
    skill this pair is here to demonstrate. The partition problem, subset sum
    and knapsack are the same algorithm three times.
    """
    total = sum(values)
    if total % 2:
        return False
    return subset_sum(values, total // 2)[0]

def partition_halves(values):
    """The two halves themselves, or (None, None) when no split exists."""
    total = sum(values)
    if total % 2:
        return None, None

    found, left = subset_sum(values, total // 2)
    if not found:
        return None, None

    right = list(values)
    for value in left:
        right.remove(value)
    return left, right
