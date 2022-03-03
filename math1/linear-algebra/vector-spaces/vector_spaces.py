"""Span, independence, basis, dimension, and the exchange that ties them.

All four notions reduce to the rank of a matrix, which is why the module is
short. A family is independent when its rank equals its size, a vector lies
in the span when adding it does not raise the rank, and the dimension is the
rank itself. The Steinitz exchange lemma is the statement that lets a basis
be built by swapping one vector at a time, and it is what makes dimension
well defined.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "gaussian-elimination"))
import gaussian_elimination as gauss


def is_independent(vectors):
    """Whether no vector is a combination of the others."""
    if not vectors:
        return True
    return gauss.rank(vectors) == len(vectors)


def in_span(vectors, target):
    """Whether the target is a combination of the family."""
    if not vectors:
        return all(entry == 0 for entry in target)
    return gauss.rank(vectors) == gauss.rank(list(vectors) + [list(target)])


def dimension(vectors):
    """The dimension of the space the family spans."""
    return gauss.rank(vectors) if vectors else 0


def basis_of(vectors):
    """A basis of the span, taken from the family itself."""
    chosen = []
    for vector in vectors:
        if not in_span(chosen, vector):
            chosen.append(list(vector))
    return chosen


def coordinates(basis, target):
    """The coefficients writing the target in the basis.

    The system is the basis written as columns, so the coordinates are the
    solution, and uniqueness of the solution is uniqueness of the
    representation, which is what a basis is for.
    """
    columns = [[row[index] for row in basis] for index in range(len(target))]
    solution = gauss.solve(columns, list(target))
    if solution["kind"] == "none":
        return None
    return solution["particular"]


def exchange(family, incoming):
    """The family with one member replaced by the incoming vector.

    The Steinitz lemma says such a member exists whenever the incoming vector
    lies in the span and is not zero, and that the span is unchanged. Both
    halves are visible here: the member is searched for, and the caller can
    check the span afterwards.
    """
    if not in_span(family, incoming) or all(entry == 0 for entry in incoming):
        return None
    for index in range(len(family)):
        candidate = [list(vector) for position, vector in enumerate(family)
                     if position != index] + [list(incoming)]
        if dimension(candidate) == dimension(family):
            return candidate
    return None


def is_subspace(vectors, candidate):
    """Whether every candidate vector lies in the span of the family."""
    return all(in_span(vectors, vector) for vector in candidate)
