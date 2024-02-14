"""The Jaccard similarity: the shared share of two sets.

The intersection over the union, which is one for identical sets and zero for
disjoint ones. One minus it is a metric, so the triangle inequality holds and
the notion of a neighbourhood makes sense, which is what the indexing methods
in the next modules rely on.

Two empty sets are defined as identical here, which is a convention and not a
consequence, since the formula gives zero over zero.
"""

import itertools


def similarity(first, second):
    """The size of the intersection over the size of the union."""
    left, right = set(first), set(second)
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def distance(first, second):
    """One minus the similarity, which is a metric."""
    return 1 - similarity(first, second)


def triangle_holds(samples=None):
    """Whether the distance satisfies the triangle inequality on samples."""
    samples = samples or [set(), {1}, {2}, {1, 2}, {1, 2, 3}, {2, 3},
                          {3, 4}, {1, 4}]
    for first, second, third in itertools.product(samples, repeat=3):
        if distance(first, third) > distance(first, second) \
                + distance(second, third) + 1e-12:
            return False
    return True


def nearest(query, candidates):
    """The most similar candidate, by brute force."""
    return max(candidates, key=lambda candidate: similarity(query, candidate))
