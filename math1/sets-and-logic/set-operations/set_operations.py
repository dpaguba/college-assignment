"""Set operations, and the laws checked by enumeration.

A law about sets is a statement about every pair of subsets, and over a small
universe there are few enough of those to try them all. The De Morgan laws
over a universe of six elements are 4096 pairs, which is a proof for that
universe and an experiment for the general claim.
"""

import itertools


def power_set(base):
    """Every subset, as a list of frozensets."""
    items = sorted(base, key=str)
    subsets = []
    for size in range(len(items) + 1):
        for combination in itertools.combinations(items, size):
            subsets.append(frozenset(combination))
    return subsets


def cartesian_product(first, second):
    """Every ordered pair with one component from each set."""
    return {(left, right) for left in first for right in second}


def complement(subset, universe):
    """The elements of the universe outside the subset."""
    return frozenset(universe) - frozenset(subset)


def symmetric_difference(first, second):
    """The elements in exactly one of the two sets."""
    return frozenset(first) ^ frozenset(second)


def inclusion_exclusion(sets):
    """The size of the union, computed by alternating over intersections.

    The formula is the interesting part: adding the sizes counts every
    element once per set it belongs to, so the overcount is removed by
    subtracting the pairwise intersections, which then removes the triples
    too often, and so on.
    """
    total = 0
    for size in range(1, len(sets) + 1):
        for combination in itertools.combinations(sets, size):
            common = set(combination[0])
            for further in combination[1:]:
                common &= set(further)
            total += (-1) ** (size + 1) * len(common)
    return total


def chain_to(target):
    """A chain of subsets from the empty set up to the target, one step at a time."""
    chain = [frozenset()]
    current = set()
    for element in sorted(target, key=str):
        current = current | {element}
        chain.append(frozenset(current))
    return chain


def is_subset_closed(family):
    """Whether every subset of a member of the family is also a member."""
    members = {frozenset(item) for item in family}
    for member in members:
        for subset in power_set(member):
            if subset not in members:
                return False
    return True
