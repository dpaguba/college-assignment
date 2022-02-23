"""Quotient groups, and the condition that makes the operation well defined.

Multiplying cosets by multiplying representatives only works when the answer
does not depend on which representatives are chosen. That independence is
exactly normality, and the failure is visible: in the symmetric group on
three points, a subgroup of order two gives two different products from two
choices of representative for the same pair of cosets.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "groups"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "subgroups-cosets"))
import groups
import subgroups_cosets


def is_normal(group, subgroup):
    """Whether conjugation by any element keeps the subgroup where it was."""
    members = {str(item) for item in subgroup.elements}
    for element in group.elements:
        inverse = group.inverse(element)
        for member in subgroup.elements:
            conjugate = group.apply(group.apply(element, member), inverse)
            if str(conjugate) not in members:
                return False
    return True


def coset_of(group, subgroup, element):
    """The coset containing the element, as a frozen set of names."""
    return frozenset(str(group.apply(element, member))
                     for member in subgroup.elements)


def well_defined(group, subgroup):
    """Whether multiplying representatives gives the same coset every time."""
    for first in group.elements:
        for second in group.elements:
            for other_first in group.elements:
                if coset_of(group, subgroup, other_first) != \
                        coset_of(group, subgroup, first):
                    continue
                for other_second in group.elements:
                    if coset_of(group, subgroup, other_second) != \
                            coset_of(group, subgroup, second):
                        continue
                    if coset_of(group, subgroup, group.apply(first, second)) != \
                            coset_of(group, subgroup,
                                     group.apply(other_first, other_second)):
                        return False
    return True


def quotient(group, subgroup):
    """The group of cosets, which needs the subgroup to be normal."""
    if not is_normal(group, subgroup):
        raise ValueError("the subgroup is not normal")
    representatives = []
    seen = set()
    for element in group.elements:
        coset = coset_of(group, subgroup, element)
        if coset in seen:
            continue
        seen.add(coset)
        representatives.append(element)
    lookup = {}
    for representative in representatives:
        for name in coset_of(group, subgroup, representative):
            lookup[name] = representative

    def operation(left, right):
        """The product of two cosets, taken through their representatives."""
        return lookup[str(group.apply(left, right))]

    return groups.Group(representatives, operation,
                        "%s/N" % (group.name or "G"))
