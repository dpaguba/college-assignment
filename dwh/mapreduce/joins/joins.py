"""Joins in map and reduce, and the one that moves no data.

A reduce-side join emits both sides keyed by the join attribute and pairs
them in the reducer, so both tables cross the network. A map-side join
broadcasts the small side to every mapper and joins there, so only the small
side moves and the large one is read where it already is.

The condition is whether the small side fits in memory, which is why a star
schema suits this model: the dimensions are small and the fact table is not.
"""


def reduce_side(left, right):
    """The join computed in the reducer, after shuffling both sides."""
    grouped = {}
    for key, value in left:
        grouped.setdefault(key, ([], []))[0].append(value)
    for key, value in right:
        grouped.setdefault(key, ([], []))[1].append(value)
    result = []
    for key, (lefts, rights) in grouped.items():
        for first in lefts:
            for second in rights:
                result.append((key, first, second))
    return result


def map_side(left, right):
    """The join computed in the mapper, with the small side broadcast."""
    table = {}
    for key, value in left:
        table.setdefault(key, []).append(value)
    result = []
    for key, value in right:
        for other in table.get(key, []):
            result.append((key, other, value))
    return result


def map_side_possible(left_rows, memory_rows):
    """Whether the small side fits in the memory of a mapper."""
    return left_rows <= memory_rows


def network_cost(left_rows, right_rows, memory_rows):
    """How many rows cross the network under each plan."""
    return {"map side": 0 if map_side_possible(left_rows, memory_rows)
            else None,
            "reduce side": left_rows + right_rows}
