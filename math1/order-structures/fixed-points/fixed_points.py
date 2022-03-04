"""Fixed points of monotone maps, by Knaster and Tarski and by iteration.

Tarski's theorem says a monotone map on a complete lattice has a least and a
greatest fixed point, and gives them as an infimum and a supremum of sets
that are defined without any iteration. On a finite lattice the same points
are reached by iterating from the bottom, and the number of steps is bounded
by the height of the lattice, which is the connection between the theorem and
the way a data flow analysis is actually computed.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "partial-orders"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "complete-lattices"))
import complete_lattices


def is_monotone(order, function):
    """Whether the map preserves the order."""
    for left in order.elements:
        for right in order.elements:
            if order.leq(left, right) and not order.leq(function(left),
                                                        function(right)):
                return False
    return True


def fixed_points(order, function):
    """Every element the map leaves unchanged."""
    return [element for element in order.elements if function(element) == element]


def least_fixed_point(order, function):
    """The infimum of the elements the map sends downwards.

    Tarski's construction: the set of pre-fixed points is closed under
    infima, and its infimum is itself a fixed point, so no iteration is
    needed to know that one exists.
    """
    pre_fixed = [element for element in order.elements
                 if order.leq(function(element), element)]
    return complete_lattices.infimum_of(order, pre_fixed)


def greatest_fixed_point(order, function):
    """The supremum of the elements the map sends upwards."""
    post_fixed = [element for element in order.elements
                  if order.leq(element, function(element))]
    return complete_lattices.supremum_of(order, post_fixed)


def kleene(order, function):
    """The limit of iterating the map from the bottom."""
    current = complete_lattices.bottom(order)
    for _ in range(len(order.elements) + 1):
        following = function(current)
        if following == current:
            return current
        current = following
    raise ValueError("the iteration did not settle")


def kleene_steps(order, function):
    """How many iterations the ascent needs."""
    current = complete_lattices.bottom(order)
    for step in range(len(order.elements) + 1):
        following = function(current)
        if following == current:
            return step
        current = following
    raise ValueError("the iteration did not settle")
