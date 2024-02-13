"""Closed and maximal itemsets: two ways to keep less and lose nothing.

An itemset is closed when no superset has the same support, and maximal when
no superset is frequent at all. Every maximal itemset is closed, so the three
families shrink in that order, and the fourth sheet asks for both.

The difference is what is preserved. The closed itemsets determine the
support of every frequent itemset, because the support of any set equals the
support of its smallest closed superset. The maximal ones determine only
which sets are frequent, so they compress more and lose the counts.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apriori"))
import apriori


def closed(transactions, minimum):
    """The frequent itemsets no superset of which has the same support."""
    found = apriori.frequent(transactions, minimum)
    universe = set(apriori.items(transactions))
    result = set()
    for itemset in found:
        own = apriori.support(transactions, itemset)
        if all(apriori.support(transactions, frozenset(itemset | {item})) != own
               for item in universe - set(itemset)):
            result.add(itemset)
    return result


def maximal(transactions, minimum):
    """The frequent itemsets with no frequent superset."""
    found = apriori.frequent(transactions, minimum)
    universe = set(apriori.items(transactions))
    return {itemset for itemset in found
            if all(frozenset(itemset | {item}) not in found
                   for item in universe - set(itemset))}


def counts(transactions, minimum):
    """How many itemsets there are of each kind."""
    return {"frequent": len(apriori.frequent(transactions, minimum)),
            "closed": len(closed(transactions, minimum)),
            "maximal": len(maximal(transactions, minimum))}


def supports_are_recoverable(transactions, minimum):
    """Whether the closed itemsets determine every frequent support.

    The support of an itemset is the largest support among the closed sets
    that contain it, which the module checks for every frequent itemset. That
    property is what makes the closed family a lossless compression.
    """
    found = apriori.frequent(transactions, minimum)
    family = closed(transactions, minimum)
    for itemset in found:
        supersets = [apriori.support(transactions, other) for other in family
                     if set(itemset) <= set(other)]
        if not supersets:
            return False
        if max(supersets) != apriori.support(transactions, itemset):
            return False
    return True
