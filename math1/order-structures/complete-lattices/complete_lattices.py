"""Complete lattices, where every subset has both bounds.

On a finite lattice completeness is free: a supremum of a subset is the join
of its elements taken one at a time, and the empty subset gets the bottom.
The definition earns its keep on infinite lattices, and the finite case is
where it can be checked exhaustively, including the two cases that look like
exceptions and are not.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "partial-orders"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lattices"))
import lattices
import partial_orders


def all_subsets(elements):
    """Every subset of the element list."""
    found = []
    for size in range(len(elements) + 1):
        for combination in itertools.combinations(elements, size):
            found.append(list(combination))
    return found


def upper_bounds_of(order, subset):
    """The elements above every member of the subset."""
    return [item for item in order.elements
            if all(order.leq(member, item) for member in subset)]


def lower_bounds_of(order, subset):
    """The elements below every member."""
    return [item for item in order.elements
            if all(order.leq(item, member) for member in subset)]


def supremum_of(order, subset):
    """The least upper bound of a subset, or nothing.

    The empty subset is the case worth noticing: every element is vacuously
    an upper bound of it, so its supremum is the bottom of the lattice.
    """
    bounds = upper_bounds_of(order, subset)
    for candidate in bounds:
        if all(order.leq(candidate, other) for other in bounds):
            return candidate
    return None


def infimum_of(order, subset):
    """The greatest lower bound, with the empty subset giving the top."""
    bounds = lower_bounds_of(order, subset)
    for candidate in bounds:
        if all(order.leq(other, candidate) for other in bounds):
            return candidate
    return None


def is_complete(order):
    """Whether every subset has both bounds."""
    for subset in all_subsets(order.elements):
        if supremum_of(order, subset) is None or infimum_of(order, subset) is None:
            return False
    return True


def top(order):
    """The greatest element, which is the supremum of everything."""
    return supremum_of(order, order.elements)


def bottom(order):
    """The least element."""
    return infimum_of(order, order.elements)


def height(order):
    """The length of the longest chain, which bounds any iteration."""
    return order.longest_chain()
