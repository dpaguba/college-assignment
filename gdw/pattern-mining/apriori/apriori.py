"""Apriori: one property, and the search it makes possible.

A subset of a frequent itemset is frequent, so an itemset can only be
frequent if all of its subsets are. That is the whole algorithm: build
candidates of size k+1 from frequent sets of size k, discard any whose
subsets are not all frequent, and count what remains.

The saving is measured rather than claimed. On the five transactions here the
lattice has sixteen subsets and the algorithm counts far fewer, and the
result agrees with the brute force enumeration.
"""

import itertools


def items(transactions):
    """Every item that occurs."""
    return sorted({item for transaction in transactions for item in transaction})


def support(transactions, itemset):
    """How many transactions contain the itemset."""
    return sum(1 for transaction in transactions
               if set(itemset) <= set(transaction))


def frequent(transactions, minimum):
    """Every itemset with at least the minimum support."""
    return with_counts(transactions, minimum)["frequent"]


def with_counts(transactions, minimum):
    """The frequent itemsets together with how many candidates were counted."""
    found = set()
    candidates = [frozenset([item]) for item in items(transactions)]
    counted = 0
    level = 1
    while candidates:
        surviving = []
        for candidate in candidates:
            counted += 1
            if support(transactions, candidate) >= minimum:
                surviving.append(candidate)
                found.add(candidate)
        candidates = _join(surviving, level + 1, found)
        level += 1
    return {"frequent": found, "candidates": counted}


def _join(surviving, size, found):
    """The candidates of the next size whose subsets are all frequent."""
    candidates = set()
    for first in surviving:
        for second in surviving:
            union = frozenset(first | second)
            if len(union) != size:
                continue
            if all(frozenset(union - {item}) in found for item in union):
                candidates.add(union)
    return sorted(candidates, key=sorted)


def brute_force(transactions, minimum):
    """Every frequent itemset by trying all subsets, as a check."""
    universe = items(transactions)
    found = set()
    for size in range(1, len(universe) + 1):
        for combination in itertools.combinations(universe, size):
            if support(transactions, set(combination)) >= minimum:
                found.add(frozenset(combination))
    return found
