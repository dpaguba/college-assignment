"""Applicative functors: mapping a function that is itself inside the functor.

A functor maps a plain function over a container. An applicative also has a
function inside the container, which is what makes it possible to apply a
function of several arguments to several containers. For lists that means
every combination, so applying two functions to two values gives four
results, and for Maybe it means the absence of either side wins.

The laws relate the two operations, and the one worth stating is that pure
followed by application has to agree with the functor's map, which is what
makes an applicative a functor rather than something merely similar.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "haskell-core", "algebraic-data-types"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "functor"))
import algebraic_data_types as adt
import functor


def pure(name, value):
    """The value put into the functor in the least surprising way."""
    if name == "List":
        return [value]
    if name == "Maybe":
        return adt.just(value)
    raise ValueError("no applicative instance for %s" % name)


def apply(name, functions, values):
    """Applies functions inside the functor to values inside it."""
    if name == "List":
        return [function(value) for function in functions for value in values]
    if name == "Maybe":
        if adt.is_nothing(functions) or adt.is_nothing(values):
            return adt.NOTHING
        return adt.just(adt.from_just(functions)(adt.from_just(values)))
    raise ValueError("no applicative instance for %s" % name)


def identity_law(name):
    """Whether applying the pure identity changes nothing."""
    for sample in _samples(name):
        if apply(name, pure(name, lambda value: value), sample) != sample:
            return False
    return True


def homomorphism_law(name):
    """Whether pure commutes with application on pure arguments."""
    function = lambda value: value * 2
    for value in (1, 5, -3):
        left = apply(name, pure(name, function), pure(name, value))
        if left != pure(name, function(value)):
            return False
    return True


def agrees_with_fmap(name):
    """Whether applying a pure function agrees with the functor's map."""
    function = lambda value: value + 1
    for sample in _samples(name):
        if apply(name, pure(name, function), sample) != \
                functor.fmap(name, function, sample):
            return False
    return True


def _samples(name):
    """Sample values for the instance."""
    if name == "List":
        return [[], [1], [1, 2, 3]]
    return [adt.NOTHING, adt.just(1), adt.just(7)]
