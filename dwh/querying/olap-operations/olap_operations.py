"""The cube operations, and the count that explains the storage problem.

Roll up removes a dimension by summing over it, drill down is the inverse,
slice fixes one dimension to a value and dice restricts several to ranges.
All four are aggregations over the same cells, which is why an OLAP system is
a storage question rather than an algorithm question.

The number of possible aggregates is two to the number of dimensions, so ten
dimensions give 1024 cubes and materialising them all is out of the question.
That count is the reason the next two modules exist.
"""

import itertools


def example_cube():
    """A small cube over time, product and store."""
    cells = {}
    for time in ("2023", "2024"):
        for product in ("book", "pen"):
            for store in ("A", "B"):
                cells[(time, product, store)] = (len(time) + len(product)
                                                 + len(store)) * 1.0
    return {"dimensions": ["time", "product", "store"], "cells": cells}


def roll_up(cube, dimension):
    """The cube with one dimension summed away."""
    index = cube["dimensions"].index(dimension)
    remaining = [name for name in cube["dimensions"] if name != dimension]
    cells = {}
    for key, value in cube["cells"].items():
        reduced = tuple(part for position, part in enumerate(key)
                        if position != index)
        cells[reduced] = cells.get(reduced, 0.0) + value
    return {"dimensions": remaining, "cells": cells}


def slice_(cube, dimension, value):
    """The cube restricted to one value of a dimension, which then drops out."""
    index = cube["dimensions"].index(dimension)
    remaining = [name for name in cube["dimensions"] if name != dimension]
    cells = {}
    for key, cell in cube["cells"].items():
        if key[index] != value:
            continue
        reduced = tuple(part for position, part in enumerate(key)
                        if position != index)
        cells[reduced] = cells.get(reduced, 0.0) + cell
    return {"dimensions": remaining, "cells": cells}


def dice(cube, ranges):
    """The cube restricted to the given values in several dimensions."""
    cells = {}
    for key, value in cube["cells"].items():
        keep = True
        for dimension, allowed in ranges.items():
            index = cube["dimensions"].index(dimension)
            if key[index] not in allowed:
                keep = False
                break
        if keep:
            cells[key] = value
    return {"dimensions": list(cube["dimensions"]), "cells": cells}


def full_size(cardinalities):
    """How many cells a full cube has."""
    total = 1
    for value in cardinalities.values():
        total *= value
    return total


def aggregate_count(dimensions):
    """How many aggregates a cube of that many dimensions has."""
    return 2 ** dimensions


def all_aggregates(dimensions):
    """Every subset of the dimensions, which is the lattice of aggregates."""
    result = []
    for size in range(len(dimensions) + 1):
        for combination in itertools.combinations(dimensions, size):
            result.append(frozenset(combination))
    return result
