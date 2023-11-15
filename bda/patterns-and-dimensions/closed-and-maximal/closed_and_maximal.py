"""Closed and maximal itemsets on the exercise database.

The twelfth sheet asks for both on eight transactions at a support of three,
and the published answer is ten closed itemsets and two maximal ones. The
module reproduces both.

The example shows the difference clearly. The singleton A is frequent and not
closed, because A and E occur in exactly the same transactions, so listing A
separately adds nothing. Only ACE and DEF are maximal, and every frequent
itemset is a subset of one of them.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fp-growth"))
import fp_growth


def support(transactions, itemset):
    """How many transactions contain the itemset."""
    return sum(1 for transaction in transactions
               if set(itemset) <= set(transaction))


def closed(transactions, minimum):
    """The frequent itemsets no superset of which has the same support."""
    found = fp_growth.frequent(transactions, minimum)
    universe = {item for transaction in transactions for item in transaction}
    result = set()
    for itemset in found:
        own = support(transactions, itemset)
        if all(support(transactions, frozenset(itemset | {item})) != own
               for item in universe - set(itemset)):
            result.add(itemset)
    return result


def maximal(transactions, minimum):
    """The frequent itemsets with no frequent superset."""
    found = fp_growth.frequent(transactions, minimum)
    universe = {item for transaction in transactions for item in transaction}
    return {itemset for itemset in found
            if all(frozenset(itemset | {item}) not in found
                   for item in universe - set(itemset))}


def why_not_closed(transactions, minimum, itemset):
    """The superset that has the same support, when there is one."""
    universe = {item for transaction in transactions for item in transaction}
    own = support(transactions, itemset)
    for item in universe - set(itemset):
        bigger = frozenset(set(itemset) | {item})
        if support(transactions, bigger) == own:
            return bigger
    return None
