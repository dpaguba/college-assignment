"""Functors: a container that can be mapped over, and the two laws.

The class has one method and two laws that are not checked by the compiler:
mapping the identity changes nothing, and mapping twice is mapping once with
the composition. Any instance that satisfies them is forced to leave the
shape alone, which is why "a functor is a container" is a useful slogan and
why the instance for a type is usually unique.

The function type is the case that makes the slogan strained. Mapping over a
function is composing after it, and there is no container anywhere.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "haskell-core", "algebraic-data-types"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "data-structures", "trees"))
import algebraic_data_types as adt
import trees


def fmap(name, function, value):
    """Maps a function over the given functor."""
    if name == "List":
        return [function(item) for item in value]
    if name == "Maybe":
        return adt.NOTHING if adt.is_nothing(value) \
            else adt.just(function(adt.from_just(value)))
    if name == "Baum":
        return trees.fmap(function, value)
    if name == "Function":
        return lambda argument: function(value(argument))
    if name == "Broken":
        return list(reversed([function(item) for item in value]))
    raise ValueError("no functor instance for %s" % name)


SAMPLES = {
    "List": [1, 2, 3],
    "Maybe": adt.just(2),
    "Baum": trees.node(1, trees.node(2, trees.LEER, trees.LEER), trees.LEER),
}
"""One sample value per instance, used by the law checks."""


def identity_law(name, sample):
    """Whether mapping the identity leaves the value alone."""
    return _equal(name, fmap(name, lambda value: value, sample), sample)


def composition_law(name, sample):
    """Whether mapping twice equals mapping the composition once."""
    first = lambda value: value + 1
    second = lambda value: value * 3
    left = fmap(name, second, fmap(name, first, sample))
    right = fmap(name, lambda value: second(first(value)), sample)
    return _equal(name, left, right)


def _equal(name, left, right):
    """Compares two functor values, applying functions before comparing."""
    if name == "Function":
        return all(left(point) == right(point) for point in range(5))
    return left == right
