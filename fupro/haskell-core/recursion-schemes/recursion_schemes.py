"""Folds and unfolds, which are recursion written as a value.

A fold replaces every constructor of a value by a function, so it is
determined by one function per constructor. That is why every recursive
function over a list can be written as a fold, and why the exam asks for the
fold of the binary numbers before asking for anything that uses it.

The two directions of folding differ whenever the operation is not
associative: folding a subtraction from the right over 1, 2, 3 gives 2 and
from the left gives -6.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "algebraic-data-types"))
import algebraic_data_types as adt


def foldr(step, start, values):
    """Folds from the right, replacing the list constructors."""
    result = start
    for value in reversed(values):
        result = step(value, result)
    return result


def foldl(step, start, values):
    """Folds from the left, accumulating as it goes."""
    result = start
    for value in values:
        result = step(result, value)
    return result


def fold_nat(zero, successor, value):
    """The fold of the Peano numbers: one function per constructor."""
    if adt.name_of(value) == "Z":
        return zero
    return successor(fold_nat(zero, successor, adt.arguments_of(value)[0]))


def map_as_fold(function, values):
    """The map written as a fold, which is what makes it a catamorphism."""
    return foldr(lambda value, rest: [function(value)] + rest, [], values)


def length_as_fold(values):
    """The length written as a fold."""
    return foldr(lambda value, count: count + 1, 0, values)


def unfold(step, seed):
    """Builds a list from a seed until the step returns nothing.

    The dual of a fold: a fold consumes a structure and an unfold produces
    one, and composing them is the loop that the two together replace.
    """
    result = []
    current = seed
    while True:
        produced = step(current)
        if produced is None:
            return result
        value, current = produced
        result.append(value)
