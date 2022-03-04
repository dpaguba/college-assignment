"""Lattices as orders and as algebras, and the two smallest counterexamples.

A lattice is an order in which every pair has a supremum and an infimum, and
it is equally a set with two operations obeying four laws. The absorption law
is what makes the two descriptions the same: it is the law that ties the join
to the meet, and without it the two operations would be unrelated.

The pentagon and the diamond are the standard counterexamples. A lattice is
distributive exactly when it contains neither, and modular exactly when it
does not contain the pentagon, so the two five-element lattices settle both
questions.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "partial-orders"))
import partial_orders


def is_lattice(order):
    """Whether every pair of elements has a supremum and an infimum."""
    for left in order.elements:
        for right in order.elements:
            if order.supremum(left, right) is None:
                return False
            if order.infimum(left, right) is None:
                return False
    return True


class Lattice:
    """A partial order in which every pair has both bounds."""

    def __init__(self, order):
        """Wraps an order, rejecting one that is not a lattice."""
        if not is_lattice(order):
            raise ValueError("this order is not a lattice")
        self.order = order
        self.elements = order.elements

    def join(self, left, right):
        """The supremum of two elements."""
        return self.order.supremum(left, right)

    def meet(self, left, right):
        """The infimum."""
        return self.order.infimum(left, right)

    def laws(self):
        """Which of the four lattice laws hold, checked over every triple."""
        report = {"idempotence": True, "commutativity": True,
                  "associativity": True, "absorption": True}
        for left in self.elements:
            if self.join(left, left) != left or self.meet(left, left) != left:
                report["idempotence"] = False
            for right in self.elements:
                if (self.join(left, right) != self.join(right, left)
                        or self.meet(left, right) != self.meet(right, left)):
                    report["commutativity"] = False
                if (self.meet(left, self.join(left, right)) != left
                        or self.join(left, self.meet(left, right)) != left):
                    report["absorption"] = False
                for third in self.elements:
                    if (self.join(self.join(left, right), third)
                            != self.join(left, self.join(right, third))):
                        report["associativity"] = False
                    if (self.meet(self.meet(left, right), third)
                            != self.meet(left, self.meet(right, third))):
                        report["associativity"] = False
        return report

    def is_distributive(self):
        """Whether the meet distributes over the join and the other way round."""
        for left in self.elements:
            for right in self.elements:
                for third in self.elements:
                    if (self.meet(left, self.join(right, third))
                            != self.join(self.meet(left, right),
                                         self.meet(left, third))):
                        return False
        return True

    def is_modular(self):
        """The weaker law, required only when the first element is below the third."""
        for left in self.elements:
            for right in self.elements:
                for third in self.elements:
                    if not self.order.leq(left, third):
                        continue
                    if (self.join(left, self.meet(right, third))
                            != self.meet(self.join(left, right), third)):
                        return False
        return True

    def top(self):
        """The greatest element."""
        for candidate in self.elements:
            if all(self.order.leq(other, candidate) for other in self.elements):
                return candidate
        return None

    def bottom(self):
        """The least element."""
        for candidate in self.elements:
            if all(self.order.leq(candidate, other) for other in self.elements):
                return candidate
        return None


def m3():
    """The diamond: three incomparable elements between a bottom and a top."""
    return partial_orders.Poset(["0", "a", "b", "c", "1"],
                                [("0", "a"), ("0", "b"), ("0", "c"),
                                 ("a", "1"), ("b", "1"), ("c", "1")])


def n5():
    """The pentagon: a two-element chain beside a single element."""
    return partial_orders.Poset(["0", "a", "b", "c", "1"],
                                [("0", "a"), ("a", "b"), ("b", "1"),
                                 ("0", "c"), ("c", "1")])
