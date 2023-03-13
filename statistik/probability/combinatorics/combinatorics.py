"""Counting draws, in the four ways the lecture distinguishes.

Ordered or not, with replacement or not: four formulas that are easy to
confuse and easy to check by enumeration for small cases, which is what the
tests do.

| | with replacement | without |
|---|---|---|
| ordered | n^k | n!/(n-k)! |
| unordered | (n+k-1 choose k) | (n choose k) |
"""

import itertools
from math import comb, factorial


def count(n, k, ordered, replace):
    """How many draws of k from n there are, under the given rules."""
    if ordered and replace:
        return n ** k
    if ordered and not replace:
        return factorial(n) // factorial(n - k)
    if not ordered and not replace:
        return comb(n, k)
    return comb(n + k - 1, k)


def enumerate_draws(n, k, ordered, replace):
    """Every such draw, for checking the formula on small cases."""
    items = range(n)
    if ordered and replace:
        return list(itertools.product(items, repeat=k))
    if ordered and not replace:
        return list(itertools.permutations(items, k))
    if not ordered and not replace:
        return list(itertools.combinations(items, k))
    return list(itertools.combinations_with_replacement(items, k))


def multinomial(counts):
    """How many distinct arrangements a multiset has."""
    total = factorial(sum(counts))
    for value in counts:
        total //= factorial(value)
    return total


def birthday(people, days=365):
    """The probability that two of the people share a birthday.

    The answer passes one half at 23 people, which surprises most readers
    because the question sounds like it is about one person against the rest
    and is actually about all the pairs.
    """
    if people > days:
        return 1.0
    distinct = 1.0
    for index in range(people):
        distinct *= (days - index) / days
    return 1 - distinct
