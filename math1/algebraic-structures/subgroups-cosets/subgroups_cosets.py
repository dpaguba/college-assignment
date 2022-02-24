"""Subgroups, cosets, and why the order of a subgroup divides the order.

Lagrange's theorem is a counting argument: the left cosets of a subgroup
partition the group and all have the size of the subgroup, so the order of
the subgroup divides the order of the group. Both halves are checked here by
enumeration, over every subgroup of every group in the sample.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "groups"))
import groups


def subgroups(group):
    """Every subgroup, found by closing each subset under the operation."""
    unit = group.identity()
    found = []
    seen = set()
    for size in range(1, len(group.elements) + 1):
        for subset in itertools.combinations(group.elements, size):
            if unit not in subset:
                continue
            key = frozenset(map(str, subset))
            if key in seen:
                continue
            candidate = groups.Group(list(subset), group.operation)
            if candidate.is_group():
                seen.add(key)
                found.append(candidate)
    return found


def left_cosets(group, subgroup):
    """The sets obtained by multiplying the subgroup from the left."""
    cosets = []
    seen = set()
    for element in group.elements:
        coset = frozenset(map(str, (group.apply(element, member)
                                    for member in subgroup.elements)))
        if coset in seen:
            continue
        seen.add(coset)
        cosets.append([group.apply(element, member)
                       for member in subgroup.elements])
    return cosets


def right_cosets(group, subgroup):
    """The sets obtained by multiplying from the right."""
    cosets = []
    seen = set()
    for element in group.elements:
        coset = frozenset(map(str, (group.apply(member, element)
                                    for member in subgroup.elements)))
        if coset in seen:
            continue
        seen.add(coset)
        cosets.append([group.apply(member, element)
                       for member in subgroup.elements])
    return cosets


def index(group, subgroup):
    """How many cosets the subgroup has."""
    return len(left_cosets(group, subgroup))


def non_normal_subgroup(group):
    """A subgroup whose left and right cosets differ, or nothing."""
    for subgroup in subgroups(group):
        left = sorted(sorted(map(str, coset)) for coset in left_cosets(group, subgroup))
        right = sorted(sorted(map(str, coset))
                       for coset in right_cosets(group, subgroup))
        if left != right:
            return subgroup
    return None


def sample_groups():
    """A selection of small groups the theorem is checked against."""
    return [groups.cyclic(size) for size in range(1, 13)] + [
        groups.symmetric(3), groups.klein_four(), groups.dihedral(4),
        groups.quaternion(), groups.units(12),
        groups.direct_product(groups.cyclic(2), groups.cyclic(3))]
