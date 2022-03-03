"""Boolean lattices: distributive, complemented, and made of their atoms.

Every finite Boolean lattice is isomorphic to the lattice of subsets of its
atoms, so it has a power of two elements and looks like a power set. The
divisor lattice shows the condition sharply: for a squarefree number it is
Boolean, and one square factor is enough to break it, because a prime power
gives a chain rather than a complemented pair.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "partial-orders"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lattices"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "complete-lattices"))
import complete_lattices
import lattices


def complements(order, element):
    """Every element whose join with this one is the top and meet the bottom."""
    top = complete_lattices.top(order)
    bottom = complete_lattices.bottom(order)
    found = []
    for candidate in order.elements:
        if (order.supremum(element, candidate) == top
                and order.infimum(element, candidate) == bottom):
            found.append(candidate)
    return found


def is_complemented(order):
    """Whether every element has at least one complement."""
    return all(complements(order, element) for element in order.elements)


def is_boolean(order):
    """Whether the lattice is distributive and complemented."""
    if not lattices.is_lattice(order):
        return False
    return lattices.Lattice(order).is_distributive() and is_complemented(order)


def atoms(order):
    """The elements covering the bottom."""
    bottom = complete_lattices.bottom(order)
    return [item for item in order.elements
            if item != bottom and not any(
                order.less(bottom, middle) and order.less(middle, item)
                for middle in order.elements)]


def de_morgan_holds(order):
    """Whether complementation exchanges join and meet, over every pair."""
    for left in order.elements:
        for right in order.elements:
            left_complement = complements(order, left)
            right_complement = complements(order, right)
            join_complement = complements(order, order.supremum(left, right))
            if not (left_complement and right_complement and join_complement):
                return False
            expected = order.infimum(left_complement[0], right_complement[0])
            if join_complement[0] != expected:
                return False
    return True


def atom_isomorphism(order):
    """The map sending each element to the set of atoms below it.

    This is the representation theorem in the finite case: the map is a
    bijection onto the subsets of the atoms, and it preserves both
    operations, so a finite Boolean lattice is a power set in disguise.
    """
    if not is_boolean(order):
        return None
    found = atoms(order)
    mapping = {element: frozenset(atom for atom in found if order.leq(atom, element))
               for element in order.elements}
    if len(set(mapping.values())) != len(order.elements):
        return None
    if len(order.elements) != 2 ** len(found):
        return None
    return mapping
