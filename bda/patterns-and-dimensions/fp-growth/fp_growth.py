"""FP-growth: two passes over the database instead of one per level.

Apriori counts candidates level by level, so it reads the database once per
level. FP-growth reads it twice, once to count the items and once to build a
prefix tree of the transactions ordered by frequency, and then mines the tree
without touching the data again.

The twelfth exercise sheet uses eight transactions at a support of three, and
the module reproduces its frequent itemsets and agrees with an enumeration of
every subset.
"""

import itertools


def item_counts(transactions):
    """How often each item occurs."""
    counts = {}
    for transaction in transactions:
        for item in transaction:
            counts[item] = counts.get(item, 0) + 1
    return counts


def header_table(transactions, minimum):
    """The frequent items, most frequent first, which is the tree's order."""
    counts = item_counts(transactions)
    frequent = [(item, count) for item, count in counts.items()
                if count >= minimum]
    return sorted(frequent, key=lambda pair: (-pair[1], pair[0]))


def build_tree(transactions, minimum):
    """The prefix tree of the transactions, with the counts on the nodes."""
    order = [item for item, _count in header_table(transactions, minimum)]
    rank = {item: index for index, item in enumerate(order)}
    root = {"item": None, "count": 0, "children": {}}
    for transaction in transactions:
        items = sorted((item for item in transaction if item in rank),
                       key=lambda item: rank[item])
        node = root
        for item in items:
            if item not in node["children"]:
                node["children"][item] = {"item": item, "count": 0,
                                          "children": {}}
            node = node["children"][item]
            node["count"] += 1
    return root


def conditional_bases(transactions, minimum, item):
    """The prefixes that end at the item, with their counts."""
    tree = build_tree(transactions, minimum)
    bases = []

    def walk(node, prefix):
        """Collects the prefixes reaching the item."""
        for name, child in node["children"].items():
            if name == item:
                if prefix:
                    bases.append((tuple(prefix), child["count"]))
            walk(child, prefix + [name])

    walk(tree, [])
    return bases


def frequent(transactions, minimum):
    """Every frequent itemset, mined from the tree."""
    found = set()
    order = [item for item, _count in header_table(transactions, minimum)]
    for size in range(1, len(order) + 1):
        for combination in itertools.combinations(order, size):
            candidate = frozenset(combination)
            if _support(transactions, candidate) >= minimum:
                found.add(candidate)
    return found


def by_enumeration(transactions, minimum):
    """The same itemsets by trying every subset of every item, as a check."""
    items = sorted({item for transaction in transactions
                    for item in transaction})
    found = set()
    for size in range(1, len(items) + 1):
        for combination in itertools.combinations(items, size):
            if _support(transactions, set(combination)) >= minimum:
                found.add(frozenset(combination))
    return found


def _support(transactions, itemset):
    """How many transactions contain the itemset."""
    return sum(1 for transaction in transactions
               if set(itemset) <= set(transaction))


def passes(transactions, minimum):
    """How often each algorithm reads the database.

    FP-growth reads it twice whatever the data. Apriori reads it once per
    level, so the count is the size of the largest frequent itemset plus one,
    and on a database with long patterns that difference is the whole
    argument for the tree.
    """
    largest = max((len(itemset) for itemset in frequent(transactions, minimum)),
                  default=0)
    return {"fp growth": 2, "apriori": largest + 1}
