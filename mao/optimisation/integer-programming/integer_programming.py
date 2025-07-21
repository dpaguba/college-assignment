"""Integer programming: the relaxation, the bound, and the branching.

Dropping the integrality gives a linear program whose optimum is at least as
good as the integer one, so it is a bound. Branch and bound uses it twice: to
prune a branch whose bound is worse than the best solution found, and to
decide where to branch, which is the fractional variable.

The knapsack is the standard example and it is also the standard warning
about greedy methods: taking the best ratio first gives 160 where the optimum
is 220, because the item with the best ratio blocks the two that fit
together.
"""

import itertools
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "linear-programming"))
import linear_programming


def branch_and_bound(objective, constraints, limit=1000):
    """The integer optimum, with the nodes explored counted."""
    best = {"solution": None, "value": None}
    nodes = 0
    stack = [list(constraints)]
    while stack and nodes < limit:
        current = stack.pop()
        nodes += 1
        relaxed = linear_programming.solve(objective, current)
        if relaxed["value"] is None:
            continue
        if best["value"] is not None and relaxed["value"] <= best["value"]:
            continue
        solution = relaxed["solution"]
        fractional = next((index for index, value in enumerate(solution)
                           if abs(value - round(value)) > 1e-9), None)
        if fractional is None:
            if best["value"] is None or relaxed["value"] > best["value"]:
                best = {"solution": [int(round(value)) for value in solution],
                        "value": relaxed["value"]}
            continue
        value = solution[fractional]
        lower = [0] * len(objective)
        lower[fractional] = 1
        stack.append(current + [(lower, math.floor(value))])
        upper = [0] * len(objective)
        upper[fractional] = -1
        stack.append(current + [(upper, -math.ceil(value))])
    best["nodes"] = nodes
    return best


def enumerate_integer(objective, constraints, bound=30):
    """The optimum found by trying every integer point, as a check."""
    best, best_value, nodes = None, None, 0
    for point in itertools.product(range(bound + 1), repeat=len(objective)):
        nodes += 1
        if any(sum(coefficient * value
                   for coefficient, value in zip(row, point)) > limit
               for row, limit in constraints):
            continue
        value = sum(coefficient * component
                    for coefficient, component in zip(objective, point))
        if best_value is None or value > best_value:
            best, best_value = list(point), value
    return {"solution": best, "value": best_value, "nodes": nodes}


def knapsack(values, weights, capacity):
    """The best selection by dynamic programming over the capacity."""
    count = len(values)
    table = [[0] * (capacity + 1) for _ in range(count + 1)]
    for index in range(1, count + 1):
        for room in range(capacity + 1):
            table[index][room] = table[index - 1][room]
            if weights[index - 1] <= room:
                table[index][room] = max(
                    table[index][room],
                    table[index - 1][room - weights[index - 1]]
                    + values[index - 1])
    chosen = []
    room = capacity
    for index in range(count, 0, -1):
        if table[index][room] != table[index - 1][room]:
            chosen.append(index - 1)
            room -= weights[index - 1]
    return {"value": table[count][capacity], "chosen": sorted(chosen)}


def greedy_knapsack(values, weights, capacity):
    """The best ratio first, which is fast and not optimal."""
    order = sorted(range(len(values)),
                   key=lambda index: -values[index] / weights[index])
    total, room, chosen = 0, capacity, []
    for index in order:
        if weights[index] <= room:
            chosen.append(index)
            room -= weights[index]
            total += values[index]
    return {"value": total, "chosen": sorted(chosen)}
