"""From itemsets to rules, and why confidence is not enough.

A rule is a split of a frequent itemset, and its confidence is the share of
the transactions containing the left side that also contain the right. A high
confidence looks like a discovery and can be an artefact of a common right
side: if nearly every transaction contains milk, every rule concluding milk
has high confidence and says nothing.

Lift is the repair. It divides the confidence by the base rate, so a value
below one means the left side makes the right side **less** likely, and the
module includes such a rule to show it happening.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apriori"))
import apriori


def confidence(transactions, left, right):
    """The share of the transactions with the left side that have the right."""
    base = apriori.support(transactions, left)
    if base == 0:
        return 0.0
    return apriori.support(transactions, set(left) | set(right)) / base


def lift(transactions, left, right):
    """The confidence divided by the base rate of the right side."""
    rate = apriori.support(transactions, right) / len(transactions)
    if rate == 0:
        return 0.0
    return confidence(transactions, left, right) / rate


def generate(transactions, minimum_support, minimum_confidence):
    """Every rule above both thresholds."""
    rules = []
    for itemset in apriori.frequent(transactions, minimum_support):
        if len(itemset) < 2:
            continue
        for size in range(1, len(itemset)):
            for left in itertools.combinations(sorted(itemset), size):
                right = set(itemset) - set(left)
                value = confidence(transactions, set(left), right)
                if value >= minimum_confidence:
                    rules.append({"left": set(left), "right": right,
                                  "confidence": value,
                                  "lift": lift(transactions, set(left), right)})
    return rules


def lift_example():
    """A rule with high confidence and a lift below one.

    Almost every transaction contains the right side, so the rule looks
    strong and the left side actually makes the right side less likely. That
    is the case confidence alone cannot distinguish from a discovery.
    """
    transactions = [{"x", "y"}] * 7 + [{"y"}] * 2 + [{"x"}] * 1
    value = confidence(transactions, {"x"}, {"y"})
    return {"confidence": value, "lift": lift(transactions, {"x"}, {"y"}),
            "base rate": apriori.support(transactions, {"y"}) / len(transactions)}
