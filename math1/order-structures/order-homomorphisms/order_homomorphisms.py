"""Maps between orders, and the gap between monotone and structure preserving.

A lattice homomorphism preserves join and meet, and every such map is
monotone, because the order can be recovered from either operation. The
converse fails, and the counterexample is easy to produce by enumeration: a
map can respect every comparison and still send a join somewhere other than
the join of the images.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "partial-orders"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lattices"))
import lattices


def all_maps(source, target):
    """Every map from the elements of one order into those of the other."""
    return [dict(zip(source.elements, values))
            for values in itertools.product(target.elements,
                                            repeat=len(source.elements))]


def is_monotone(source, target, mapping):
    """Whether the map respects every comparison."""
    for left in source.elements:
        for right in source.elements:
            if source.leq(left, right) and not target.leq(mapping[left],
                                                          mapping[right]):
                return False
    return True


def is_lattice_homomorphism(source, target, mapping):
    """Whether the map preserves both operations."""
    for left in source.elements:
        for right in source.elements:
            join = source.supremum(left, right)
            meet = source.infimum(left, right)
            if join is None or meet is None:
                return False
            if mapping[join] != target.supremum(mapping[left], mapping[right]):
                return False
            if mapping[meet] != target.infimum(mapping[left], mapping[right]):
                return False
    return True


def monotone_but_not_a_homomorphism(source, target):
    """A map that respects the order without preserving the operations."""
    for mapping in all_maps(source, target):
        if is_monotone(source, target, mapping) and not is_lattice_homomorphism(
                source, target, mapping):
            return mapping
    return None


def is_order_isomorphism(source, target, mapping):
    """Whether the map is a bijection whose inverse is monotone as well."""
    if sorted(map(str, mapping.values())) != sorted(map(str, target.elements)):
        return False
    if len(set(map(str, mapping.values()))) != len(target.elements):
        return False
    inverse = {value: key for key, value in mapping.items()}
    return (is_monotone(source, target, mapping)
            and is_monotone(target, source, inverse))


def isomorphism(source, target):
    """An order isomorphism between the two orders, or nothing."""
    if len(source.elements) != len(target.elements):
        return None
    for values in itertools.permutations(target.elements):
        mapping = dict(zip(source.elements, values))
        if is_order_isomorphism(source, target, mapping):
            return mapping
    return None
