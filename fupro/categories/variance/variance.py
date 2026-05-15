"""Variance: which way a function type lets a map travel.

A type constructor is covariant in a position when a function from a to b
gives a function from F a to F b, and contravariant when it gives one the
other way round. The function type is the case that matters: it is covariant
in its result and contravariant in its argument, because a function that
accepts more can be used wherever one that accepts less was expected.

Nesting multiplies the signs, which is why a position inside two arguments is
covariant again. That rule is the whole content of the topic, and it is the
reason a callback taking a callback behaves like an ordinary value.
"""

POSITIONS = {"result": "covariant", "argument": "contravariant"}
"""The variance of the two positions of a function type."""


def of_position(position):
    """The variance of one position of a function type."""
    if position not in POSITIONS:
        raise ValueError("unknown position: %s" % position)
    return POSITIONS[position]


def of_path(path):
    """The variance of a nested position, by multiplying the signs."""
    sign = 1
    for position in path:
        sign *= 1 if of_position(position) == "covariant" else -1
    return "covariant" if sign > 0 else "contravariant"


def map_direction(kind):
    """Which way a map has to point for a functor of the given variance."""
    if kind == "covariant":
        return "a -> b"
    if kind == "contravariant":
        return "b -> a"
    raise ValueError("unknown variance: %s" % kind)


def reader_is_covariant():
    """Whether the reader functor maps forwards in its result.

    The reader is a function from a fixed environment, so its parameter is in
    the result position and composing after it is the map. Checked by
    building the map and applying it, rather than by consulting the rule.
    """
    def fmap(function, reader):
        """The map of the reader functor: compose after."""
        return lambda environment: function(reader(environment))

    reader = lambda environment: environment * 2
    mapped = fmap(lambda value: value + 1, reader)
    return mapped(3) == 7


def predicate_is_contravariant():
    """Whether a predicate maps backwards in its argument.

    A predicate on b becomes a predicate on a by composing before, so the map
    needs a function from a to b, which is the definition of contravariance.
    """
    def contramap(function, predicate):
        """The map of a contravariant functor: compose before."""
        return lambda value: predicate(function(value))

    is_even = lambda value: value % 2 == 0
    on_strings = contramap(len, is_even)
    return on_strings("abcd") and not on_strings("abc")
