"""Precomputed aggregates, and the lattice that says which answers which.

An aggregate over a set of dimensions answers any query over a subset of
them, because summing further is always possible and splitting is not. The
aggregates therefore form a lattice ordered by inclusion, and materialising a
node makes every node below it cheap.

The base cube answers everything and costs the most to store and to keep up
to date, which is the trade the next module optimises.
"""

import itertools


def lattice(dimensions):
    """Every subset of the dimensions, as the nodes of the lattice."""
    nodes = []
    for size in range(len(dimensions) + 1):
        for combination in itertools.combinations(sorted(dimensions), size):
            nodes.append(frozenset(combination))
    return nodes


def answers(view, query):
    """Whether a materialised view can answer a query."""
    return set(query) <= set(view)


def query_cost(sizes, query):
    """The size of the smallest materialised view that answers the query."""
    usable = [size for view, size in sizes.items()
              if answers(view, query)]
    return min(usable) if usable else None


def maintenance(views, loads):
    """How many view updates a number of loads costs."""
    return {"updates": views * loads, "views": views, "loads": loads}
