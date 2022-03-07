"""Closures: the smallest extension with a wanted property.

A closure exists because the property is preserved under intersection, so
there is a least relation containing the original and having the property.
The three closures do not commute, and that is the result worth measuring:
closing symmetrically and then transitively is an equivalence, while doing it
the other way round need not even be transitive.
"""


def reflexive_closure(relation, base):
    """The relation with the diagonal added."""
    return set(relation) | {(element, element) for element in base}


def symmetric_closure(relation):
    """The relation with every pair reversed as well."""
    return set(relation) | {(right, left) for left, right in relation}


def transitive_closure(relation):
    """The relation with every path contracted to a single step.

    Computed as a least fixed point: keep composing until nothing new
    appears, which terminates because the relation is finite and only grows.
    """
    closed = set(relation)
    while True:
        additions = {(left, right) for left, middle in closed
                     for other, right in closed
                     if middle == other and (left, right) not in closed}
        if not additions:
            return closed
        closed |= additions


def equivalence_closure(relation, base):
    """The smallest equivalence relation containing the given one."""
    return reflexive_closure(transitive_closure(symmetric_closure(relation)), base)


def closure_steps(relation):
    """How many rounds the transitive closure needs before it settles."""
    closed = set(relation)
    rounds = 0
    while True:
        additions = {(left, right) for left, middle in closed
                     for other, right in closed
                     if middle == other and (left, right) not in closed}
        if not additions:
            return rounds
        closed |= additions
        rounds += 1
