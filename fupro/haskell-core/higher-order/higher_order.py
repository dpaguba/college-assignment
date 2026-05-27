"""Functions as values: currying, composition, partial application.

In a curried language every function takes one argument and returns a
function, so applying it to fewer arguments than it seems to need is
ordinary rather than special. That is what makes sections and point-free
definitions possible, and it is why the type of a two-argument function is
written with two arrows.
"""


def curry(function):
    """Turns a function on pairs into one taking its arguments one at a time."""
    return lambda first: lambda second: function((first, second))


def uncurry(function):
    """The inverse: turns a curried function into one on pairs."""
    return lambda pair: function(pair[0])(pair[1])


def compose(second, first):
    """The function applying the right one and then the left one."""
    return lambda value: second(first(value))


def flip(function):
    """The curried function with its two arguments exchanged."""
    return lambda first: lambda second: function(second)(first)


def apply_all(functions, value):
    """Applies each function in turn, left to right."""
    result = value
    for function in functions:
        result = function(result)
    return result


def constant(value):
    """The function that ignores its argument."""
    return lambda _ignored: value


def identity(value):
    """The function that returns its argument."""
    return value
