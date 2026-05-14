"""Natural transformations: maps between functors that ignore the values.

A transformation from one functor to another is natural when it commutes with
mapping: transforming and then mapping gives the same result as mapping and
then transforming. That square is the definition, and it says the
transformation may rearrange the structure and may not look at what is inside
it.

Taking the head of a list, reversing a list and taking the length are all
natural. A transformation that inspects the values is not, and the test finds
the failure by trying a function that changes them.
"""


def maybe_to_list(value, _function=None):
    """Turns an optional value into a list of nothing or one element."""
    return [] if value is None else [value]


maybe_to_list.samples = [None, 1, 5, -3]


def head_to_maybe(values, _function=None):
    """Takes the first element of a list, or nothing."""
    return values[0] if values else None


def reverse_list(values, _function=None):
    """Reverses a list."""
    return list(reversed(values))


def not_natural(values, _function=None):
    """A transformation that looks at the values, so the square fails."""
    return [value for value in values if isinstance(value, int) and value > 2]


def is_natural(transformation, samples=None, functions=None):
    """Whether the naturality square commutes on the samples.

    The check is the definition read as a computation: map then transform
    against transform then map, over several containers and several
    functions.
    """
    samples = samples or getattr(transformation, "samples",
                                 [[], [1], [1, 2, 3], [3, 4]])
    functions = functions or [lambda value: value + 10,
                              lambda value: value * 2,
                              lambda value: -value]
    for sample in samples:
        for function in functions:
            left = _fmap(function, transformation(sample))
            right = transformation(_fmap(function, sample))
            if left != right:
                return False
    return True


def _fmap(function, container):
    """Maps a function over a list, an optional value or a plain value."""
    if container is None:
        return None
    if isinstance(container, list):
        return [function(value) for value in container]
    return function(container)


def length_is_natural():
    """Whether the length of a list is a natural transformation.

    Its target is the constant functor, whose map does nothing, so the square
    says that the length is unchanged by mapping, which is exactly what makes
    it natural.
    """
    for sample in ([], [1], [1, 2, 3], [5, 5, 5, 5]):
        for function in (lambda value: value + 1, lambda value: value * 3):
            if len([function(value) for value in sample]) != len(sample):
                return False
    return True
