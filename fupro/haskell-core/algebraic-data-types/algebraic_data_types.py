"""Algebraic data types: a value is a constructor with arguments.

A data declaration lists the ways a value can be built, and nothing else is
possible, which is what makes exhaustive pattern matching a decidable
question. A value is represented here as a tuple whose first entry is the
constructor name, so equality is structural and two values are equal exactly
when they were built the same way.
"""

DECLARATIONS = {
    "Maybe": ["Nothing", "Just"],
    "Either": ["Left", "Right"],
    "Nat": ["Z", "S"],
    "Bin": ["LSB", "Zero", "One"],
    "Baum": ["Leer", "Knoten"],
    "List": ["Nil", "Cons"],
}
"""The data types of the lecture and the exam, with their constructors."""


def construct(name, *arguments):
    """A value built by the named constructor."""
    return (name,) + arguments


def name_of(value):
    """The constructor a value was built with."""
    return value[0]


def arguments_of(value):
    """The arguments the constructor was given."""
    return value[1:]


def constructors(type_name):
    """The constructors of a declared type."""
    if type_name not in DECLARATIONS:
        raise ValueError("no such type: %s" % type_name)
    return DECLARATIONS[type_name]


NOTHING = construct("Nothing")
"""The absent value."""

LEER = construct("Leer")
"""The empty tree."""


def just(value):
    """A present value."""
    return construct("Just", value)


def is_nothing(value):
    """Whether the value is absent."""
    return name_of(value) == "Nothing"


def from_just(value):
    """The value inside, or a raised error."""
    if is_nothing(value):
        raise ValueError("Nothing has no value")
    return arguments_of(value)[0]


def left(value):
    """The left alternative, by convention the failure."""
    return construct("Left", value)


def right(value):
    """The right alternative."""
    return construct("Right", value)


def from_integer(number):
    """The Peano representation of a natural number."""
    result = construct("Z")
    for _ in range(number):
        result = construct("S", result)
    return result


def to_integer(value):
    """The number a Peano value stands for."""
    count = 0
    while name_of(value) == "S":
        count += 1
        value = arguments_of(value)[0]
    return count
