"""Homomorphisms: maps that respect the structure they are given.

A monoid is a set with an associative operation and a unit, and a
homomorphism between two of them turns the operation into the operation and
the unit into the unit. The length of a list is the standard example, since
the length of a concatenation is the sum of the lengths and the empty list
has length zero.

The lecture's point is that a fold is exactly a homomorphism out of the term
algebra, which is why folds compose so well and why a definition written as
a fold inherits the laws of the algebra it maps into.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "term-algebras"))
import term_algebras

LIST_MONOID = {"unit": [], "operation": lambda left, right: list(left) + list(right),
               "samples": [[], [1], [1, 2], [3, 4, 5]]}
"""Lists under concatenation."""

SUM_MONOID = {"unit": 0, "operation": lambda left, right: left + right,
              "samples": [0, 1, 2, 5, -3]}
"""Numbers under addition."""

PRODUCT_MONOID = {"unit": 1, "operation": lambda left, right: left * right,
                  "samples": [1, 2, 3, 0]}
"""Numbers under multiplication."""


def is_homomorphism(source, target, function):
    """Whether the map respects the unit and the operation."""
    if function(source["unit"]) != target["unit"]:
        return False
    for left in source["samples"]:
        for right in source["samples"]:
            combined = function(source["operation"](left, right))
            separately = target["operation"](function(left), function(right))
            if combined != separately:
                return False
    return True


def fold_is_unique():
    """Whether two folds agreeing on the constructors agree everywhere.

    The uniqueness half of initiality. Two homomorphisms out of the term
    algebra that agree on every constructor are the same map, so a fold is
    determined by its algebra and nothing else.
    """
    samples = [term_algebras.term("Add", term_algebras.term("Lit", 2),
                                  term_algebras.term("Lit", 3)),
               term_algebras.term("Mul", term_algebras.term("Lit", 4),
                                  term_algebras.term("Lit", 5))]
    other = dict(term_algebras.VALUE)
    for sample in samples:
        if term_algebras.interpret(sample, term_algebras.VALUE) != \
                term_algebras.interpret(sample, other):
            return False
    return True


def monoid_laws(monoid):
    """Whether the operation is associative and the unit does nothing."""
    for left in monoid["samples"]:
        if monoid["operation"](monoid["unit"], left) != left:
            return False
        if monoid["operation"](left, monoid["unit"]) != left:
            return False
        for middle in monoid["samples"]:
            for right in monoid["samples"]:
                first = monoid["operation"](monoid["operation"](left, middle),
                                            right)
                second = monoid["operation"](left,
                                             monoid["operation"](middle, right))
                if first != second:
                    return False
    return True
