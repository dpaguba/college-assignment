"""The five properties a relation may have, and how many relations have them.

A relation on a set of three elements is one of 512 sets of pairs, so every
question about which properties can hold together is settled by counting
rather than by argument. The counts are the exercise: 171 of the 512 are
transitive, 19 are partial orders, and 5 are equivalences.
"""

import itertools


def is_reflexive(relation, base):
    """Whether every element is related to itself."""
    return all((element, element) in relation for element in base)


def is_irreflexive(relation, base):
    """Whether no element is related to itself."""
    return all((element, element) not in relation for element in base)


def is_symmetric(relation):
    """Whether every pair occurs in both directions."""
    return all((right, left) in relation for left, right in relation)


def is_antisymmetric(relation):
    """Whether no two distinct elements are related both ways."""
    return all(left == right or (right, left) not in relation
               for left, right in relation)


def is_transitive(relation):
    """Whether a path of two steps is always a single step as well."""
    for left, middle in relation:
        for other, right in relation:
            if middle == other and (left, right) not in relation:
                return False
    return True


def is_total(relation, base):
    """Whether any two elements are comparable in one direction or the other."""
    return all((left, right) in relation or (right, left) in relation
               for left in base for right in base)


def is_equivalence(relation, base):
    """Reflexive, symmetric and transitive at once."""
    return (is_reflexive(relation, base) and is_symmetric(relation)
            and is_transitive(relation))


def is_partial_order(relation, base):
    """Reflexive, antisymmetric and transitive at once."""
    return (is_reflexive(relation, base) and is_antisymmetric(relation)
            and is_transitive(relation))


def count_properties(size):
    """How many relations on a set of the given size have each property."""
    base = list(range(size))
    pairs = [(left, right) for left in base for right in base]
    counts = {"all": 0, "reflexive": 0, "symmetric": 0, "antisymmetric": 0,
              "transitive": 0, "equivalence": 0, "partial order": 0}
    for mask in range(2 ** len(pairs)):
        relation = {pair for index, pair in enumerate(pairs) if mask >> index & 1}
        counts["all"] += 1
        counts["reflexive"] += is_reflexive(relation, base)
        counts["symmetric"] += is_symmetric(relation)
        counts["antisymmetric"] += is_antisymmetric(relation)
        counts["transitive"] += is_transitive(relation)
        counts["equivalence"] += is_equivalence(relation, base)
        counts["partial order"] += is_partial_order(relation, base)
    return counts


def compose(first, second):
    """The relation reached by taking a step of each, in that order."""
    return {(left, right) for left, middle in first
            for other, right in second if middle == other}
