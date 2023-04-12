"""A*: Dijkstra that also uses an estimate of the distance still to go."""

from __future__ import annotations

import heapq


def a_star(graph, start, goal, heuristic, count=False):
    """Return the cheapest path, its cost, and optionally how much was explored.

    Dijkstra expands the cheapest vertex so far, which means it spreads in every
    direction equally, including away from the goal. A* orders the queue by
    cost so far plus an estimate of the cost remaining, so the search leans
    towards the target.

    The estimate has to be **admissible**: it must never overestimate the true
    remaining cost. Under that condition A* returns the same answer Dijkstra
    would, having looked at fewer vertices. Overestimate, and it becomes fast
    and wrong, which is the trade greedy best-first search makes deliberately.

    With `heuristic` returning zero the formula reduces to Dijkstra exactly, and
    the test suite checks that. That is the cleanest way to see what A* is:
    not a different algorithm, but the same one with a better queue order.

    On a grid with unit steps, Manhattan distance is admissible because no route
    can be shorter than the straight line count. Choosing such a function is
    the entire craft of using A*.
    """
    if start not in graph:
        raise KeyError(f"{start!r} is not a vertex of this graph")

    costs = {start: 0}
    parents = {start: None}
    finished = set()
    expanded = 0
    queue = [(heuristic(start), 0, start)]

    while queue:
        _, cost, vertex = heapq.heappop(queue)
        if vertex in finished:
            continue
        finished.add(vertex)
        expanded += 1

        if vertex == goal:
            path = [goal]
            while parents[path[-1]] is not None:
                path.append(parents[path[-1]])
            path.reverse()
            return (path, cost, expanded) if count else (path, cost)

        for neighbour in graph.neighbours(vertex):
            candidate = cost + graph.weight(vertex, neighbour)
            if candidate < costs.get(neighbour, float("inf")):
                costs[neighbour] = candidate
                parents[neighbour] = vertex
                heapq.heappush(queue, (candidate + heuristic(neighbour), candidate, neighbour))

    return (None, float("inf"), expanded) if count else (None, float("inf"))
