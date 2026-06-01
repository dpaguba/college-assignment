"""The list functions of the lecture, including the transitive closure.

Lists are the data type the course uses for everything, and the functions
here are the ones the lecture builds by hand before they are used: map,
filter, zip, take while, and the closure example of the fourth lecture, which
is a fixed point computation written with list operations.
"""


def map_(function, values):
    """Applies a function to every element."""
    return [function(value) for value in values]


def filter_(predicate, values):
    """Keeps the elements the predicate accepts."""
    return [value for value in values if predicate(value)]


def zip_(first, second):
    """Pairs the elements, stopping at the shorter list."""
    return [(left, right) for left, right in zip(first, second)]


def take_while(predicate, values):
    """The longest prefix whose elements the predicate accepts."""
    result = []
    for value in values:
        if not predicate(value):
            return result
        result.append(value)
    return result


def drop_while(predicate, values):
    """The rest after that prefix."""
    for index, value in enumerate(values):
        if not predicate(value):
            return list(values[index:])
    return []


def append(first, second):
    """The concatenation of two lists."""
    return list(first) + list(second)


def reverse(values):
    """The list in the opposite order."""
    return list(reversed(values))


def comprehension(function, predicate, values):
    """A list comprehension, which is a map after a filter."""
    return [function(value) for value in values if predicate(value)]


def quicksort(values):
    """Quicksort written as the lecture writes it, with comprehensions.

    Two comprehensions and a recursive call, which is the standard example of
    how much a functional definition can leave out: no indices, no swaps, no
    loop.
    """
    if not values:
        return []
    pivot, rest = values[0], values[1:]
    smaller = [value for value in rest if value < pivot]
    larger = [value for value in rest if value >= pivot]
    return quicksort(smaller) + [pivot] + quicksort(larger)


def transitive_closure(relation):
    """The transitive closure, computed as a least fixed point.

    The example of the fourth lecture. New pairs are added until nothing
    changes, which terminates because the relation is finite and only grows.
    """
    closed = list(relation)
    while True:
        additions = [(left, right)
                     for left, middle in closed
                     for other, right in closed
                     if middle == other and (left, right) not in closed]
        if not additions:
            return closed
        for pair in additions:
            if pair not in closed:
                closed.append(pair)
